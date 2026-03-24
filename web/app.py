"""Local web interface for the GBS-IgA Research Knowledge Base."""

import os
import sys
import time
from collections import defaultdict
from pathlib import Path
from functools import wraps

# Add project root to path so we can import rag modules
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import markdown

from rag.search import search as rag_search
from rag.qa import ask as rag_ask

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "gbs-iga-research-2026")

_project_root = Path(__file__).resolve().parent.parent
_intro_path = _project_root / "KUNSKAPSBASEN.md"

# --- Access control ---
ACCESS_CODE = os.environ.get("ACCESS_CODE", "")  # Set in Railway to require a code

# --- Rate limiting ---
RATE_LIMIT_SEARCH = int(os.environ.get("RATE_LIMIT_SEARCH", "30"))   # per minute
RATE_LIMIT_ASK = int(os.environ.get("RATE_LIMIT_ASK", "10"))         # per minute
_request_log = defaultdict(list)


def _get_client_ip():
    return request.headers.get("X-Forwarded-For", request.remote_addr or "unknown").split(",")[0].strip()


def _check_rate_limit(action, limit):
    ip = _get_client_ip()
    key = f"{ip}:{action}"
    now = time.time()
    # Clean old entries
    _request_log[key] = [t for t in _request_log[key] if now - t < 60]
    if len(_request_log[key]) >= limit:
        return False
    _request_log[key].append(now)
    return True


def require_access(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if ACCESS_CODE and not session.get("authenticated"):
            if request.is_json:
                return jsonify({"error": "Åtkomstkod krävs. Ladda om sidan."}), 401
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated


# --- Routes ---

@app.route("/login", methods=["GET", "POST"])
def login():
    if not ACCESS_CODE:
        return redirect(url_for("index"))
    error = None
    if request.method == "POST":
        code = request.form.get("code", "").strip()
        if code == ACCESS_CODE:
            session["authenticated"] = True
            return redirect(url_for("index"))
        error = "Fel kod. Försök igen."
    return render_template("login.html", error=error)


@app.route("/")
@require_access
def index():
    intro_html = _render_intro()
    return render_template("index.html", intro=intro_html)


@app.route("/api/search", methods=["POST"])
@require_access
def api_search():
    if not _check_rate_limit("search", RATE_LIMIT_SEARCH):
        return jsonify({"error": f"Begränsning: max {RATE_LIMIT_SEARCH} sökningar per minut."}), 429

    data = request.get_json()
    query = data.get("query", "").strip()
    top_k = data.get("top_k", 5)

    if not query:
        return jsonify({"error": "No query provided"}), 400

    try:
        results = rag_search(query, top_k=top_k)
        return jsonify({
            "results": [
                {
                    "text": r.text,
                    "score": round(r.score, 3),
                    "heading_path": r.metadata.get("heading_path", ""),
                    "source_file": r.metadata.get("source_file", ""),
                    "section": r.metadata.get("section", ""),
                }
                for r in results
            ]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/ask", methods=["POST"])
@require_access
def api_ask():
    if not _check_rate_limit("ask", RATE_LIMIT_ASK):
        return jsonify({"error": f"Begränsning: max {RATE_LIMIT_ASK} frågor per minut. Vänta en stund."}), 429

    data = request.get_json()
    question = data.get("question", "").strip()
    top_k = data.get("top_k", 5)

    if not question:
        return jsonify({"error": "No question provided"}), 400

    try:
        answer, sources = rag_ask(question, top_k=top_k)
        answer_html = markdown.markdown(
            answer, extensions=["tables", "fenced_code"]
        )
        return jsonify({
            "answer": answer_html,
            "answer_raw": answer,
            "sources": [
                {
                    "score": round(s.score, 3),
                    "heading_path": s.metadata.get("heading_path", ""),
                    "source_file": s.metadata.get("source_file", ""),
                }
                for s in sources
            ],
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/doc/<path:filepath>")
@require_access
def view_doc(filepath):
    """Render a markdown research document as HTML."""
    doc_path = _project_root / filepath
    if not doc_path.exists() or not str(doc_path).endswith(".md"):
        return "Document not found", 404
    # Security: ensure path stays within project
    try:
        doc_path.resolve().relative_to(_project_root.resolve())
    except ValueError:
        return "Access denied", 403

    text = doc_path.read_text(encoding="utf-8")
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            text = parts[2].strip()

    doc_html = markdown.markdown(text, extensions=["tables", "fenced_code"])
    title = filepath.split("/")[-1].replace(".md", "").replace("_", " ")
    return render_template("document.html", title=title, content=doc_html, filepath=filepath)


def _render_intro() -> str:
    text = _intro_path.read_text(encoding="utf-8")
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            text = parts[2].strip()
    return markdown.markdown(text, extensions=["tables", "fenced_code", "codehilite"])


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))
    debug = os.environ.get("FLASK_DEBUG", "1") == "1"
    app.run(host="0.0.0.0", port=port, debug=debug)
