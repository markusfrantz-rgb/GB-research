"""Local web interface for the GBS-IgA Research Knowledge Base."""

import sys
from pathlib import Path

# Add project root to path so we can import rag modules
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from flask import Flask, render_template, request, jsonify
import markdown

from rag.search import search as rag_search
from rag.qa import ask as rag_ask

app = Flask(__name__)

# Pre-render the intro page
_intro_path = Path(__file__).resolve().parent.parent / "KUNSKAPSBASEN.md"


def _render_intro() -> str:
    text = _intro_path.read_text(encoding="utf-8")
    # Strip YAML frontmatter
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            text = parts[2].strip()
    return markdown.markdown(text, extensions=["tables", "fenced_code", "codehilite"])


@app.route("/")
def index():
    intro_html = _render_intro()
    return render_template("index.html", intro=intro_html)


@app.route("/api/search", methods=["POST"])
def api_search():
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
def api_ask():
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


_project_root = Path(__file__).resolve().parent.parent


@app.route("/doc/<path:filepath>")
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
    # Strip YAML frontmatter
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            text = parts[2].strip()

    doc_html = markdown.markdown(text, extensions=["tables", "fenced_code"])
    title = filepath.split("/")[-1].replace(".md", "").replace("_", " ")
    return render_template("document.html", title=title, content=doc_html, filepath=filepath)


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))
    debug = os.environ.get("FLASK_DEBUG", "1") == "1"
    app.run(host="0.0.0.0", port=port, debug=debug)
