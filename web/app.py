"""Local web interface for the GBS-IgA Research Knowledge Base."""

import os
import sys
import time
from collections import defaultdict
from pathlib import Path
from functools import wraps

# Add project root to path so we can import rag modules
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import re

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_file
import markdown

from rag.search import search as rag_search
from rag.qa import ask as rag_ask

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "gbs-iga-research-2026")

_project_root = Path(__file__).resolve().parent.parent
_intro_path = _project_root / "KUNSKAPSBASEN.md"

# --- Access control ---
ACCESS_CODE = os.environ.get("ACCESS_CODE", "")  # Set in Railway to require a code
print(f"[AUTH] ACCESS_CODE is {'SET (' + str(len(ACCESS_CODE)) + ' chars)' if ACCESS_CODE else 'NOT SET - site is open'}")

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
                    "doc_type": r.metadata.get("doc_type", "research"),
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
            answer, extensions=["tables", "fenced_code", "toc"]
        )
        answer_html = _postprocess_html(answer_html)
        return jsonify({
            "answer": answer_html,
            "answer_raw": answer,
            "sources": [
                {
                    "score": round(s.score, 3),
                    "heading_path": s.metadata.get("heading_path", ""),
                    "source_file": s.metadata.get("source_file", ""),
                    "doc_type": s.metadata.get("doc_type", "research"),
                }
                for s in sources
            ],
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


_PUBLIC_PREFIXES = (
    "01-GBS/",
    "02-IgA-deficiency/",
    "03-GBS-and-IgA-deficiency/",
    "04-related-autoimmune/",
    "05-treatment-resistance/",
    "06-monitoring-prognosis/",
    "07-acute-icu-protocols/",
    "08-immunoglobulin-iga-safety/",
    "research-ivig-iga/",
    "Case_Madeleine_Fragor_och_Fynd.md",
    "Tillgang_till_medicinska_kallor.md",
)


@app.route("/doc/<path:filepath>")
@require_access
def view_doc(filepath):
    """Render a markdown research document as HTML."""
    if not filepath.startswith(_PUBLIC_PREFIXES):
        return "Document not found", 404
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

    doc_html = markdown.markdown(text, extensions=["tables", "fenced_code", "toc"])
    doc_html = _postprocess_html(doc_html)
    title = filepath.split("/")[-1].replace(".md", "").replace("_", " ")
    return render_template("document.html", title=title, content=doc_html, filepath=filepath)


# --- Source file serving & PMID mapping ---

_source_dirs = [
    _project_root / "sources" / "fulltext",
    _project_root / "research-ivig-iga" / "fulltexts",
]


def _build_source_map():
    """Build PMID/PMC → filename mapping from all source directories."""
    mapping = {}  # e.g. {"PMID:37814552": "Doorn_2023_...", "PMC7079539": "Altmann_2020_..."}
    for sources_dir in _source_dirs:
        if not sources_dir.exists():
            continue
        for f in sources_dir.iterdir():
            name = f.name
            # Extract PMID from filename (pattern: PMID12345678)
            pmid_match = re.search(r'PMID(\d+)', name)
            if pmid_match:
                mapping[pmid_match.group(1)] = name
            # Extract PMC ID from filename (pattern: PMC12345678)
            pmc_match = re.search(r'PMC(\d+)', name)
            if pmc_match:
                mapping[f"PMC{pmc_match.group(1)}"] = name
    return mapping


_source_map = _build_source_map()

# Known PMID → PMC mappings for files that only have PMC ID in filename
_pmid_to_pmc = {
    "25878749": "PMC4395951", "27775812": "PMC6464149", "32317366": "PMC7202739",
    "37548987": "PMC10407763", "11919115": "PMC1719164", "18354151": "PMC3152158",
    "22728497": "PMC5827325", "21292802": "PMC7965877", "21903912": "PMC7965398",
    "40536593": "PMC12345678",  # Xin 2025
}
for pmid, pmc in _pmid_to_pmc.items():
    if pmid not in _source_map and pmc in _source_map:
        _source_map[pmid] = _source_map[pmc]

print(f"[SOURCES] Mapped {len(_source_map)} PMID/PMC IDs to local files")


def _source_badge(ref_id):
    """Return an HTML badge linking to the local file, or empty string."""
    filename = _source_map.get(ref_id)
    if not filename:
        return ""
    is_pdf = filename.endswith(".pdf")
    label = "PDF" if is_pdf else "text"
    return (f' <a href="/source/{filename}" target="_blank" rel="noopener"'
            f' class="source-link" title="Visa fulltext lokalt">[{label}]</a>')


def _postprocess_html(html):
    """Add target=_blank to external links, linkify PMID/PMC, add local source badges."""
    # Linkify PMID references (skip those inside URLs or existing links)
    def _pmid_repl(m):
        if m.group(1):  # preceded by chars that mean we're inside a URL or tag
            return m.group(0)
        pmid = m.group(2)
        link = (f'PMID: <a href="https://pubmed.ncbi.nlm.nih.gov/{pmid}/"'
                f' target="_blank" rel="noopener" class="ext-link">{pmid}</a>')
        return link + _source_badge(pmid)

    html = re.sub(r'([a-zA-Z0-9_/">])?PMID:\s*(\d+)', _pmid_repl, html)

    # Linkify PMC references (skip those inside URLs, filenames or existing links)
    def _pmc_repl(m):
        if m.group(1):  # preceded by alphanumeric, _, / or " — part of URL/filename
            return m.group(0)
        pmc_id = m.group(2)
        link = (f'<a href="https://pmc.ncbi.nlm.nih.gov/articles/PMC{pmc_id}/"'
                f' target="_blank" rel="noopener" class="ext-link">PMC{pmc_id}</a>')
        return link + _source_badge(f"PMC{pmc_id}")

    html = re.sub(r'([a-zA-Z0-9_/"])?PMC(\d{5,})', _pmc_repl, html)

    # Make all <a href="http..."> open in new tab with ext-link class
    def _ext_link(m):
        tag = m.group(0)
        if 'target=' in tag:
            return tag
        return tag.replace('<a ', '<a target="_blank" rel="noopener" class="ext-link" ')

    html = re.sub(r'<a\s+href="https?://[^"]*"[^>]*>', _ext_link, html)

    # Make /source/ PDF links open in new tab (native viewer), text links stay in same tab (our HTML wrapper)
    def _source_link(m):
        tag = m.group(0)
        if 'target=' in tag:
            return tag
        if '.pdf' in tag.lower():
            return tag.replace('<a ', '<a target="_blank" rel="noopener" ')
        return tag

    html = re.sub(r'<a\s+href="/source/[^"]*"[^>]*>', _source_link, html)

    return html


@app.route("/source/<path:filename>")
@require_access
def view_source(filename):
    """Serve a source file (PDF directly, txt in HTML wrapper)."""
    # Search all source directories for the file
    file_path = None
    for sources_dir in _source_dirs:
        candidate = sources_dir / filename
        if candidate.exists():
            # Security: ensure path stays within the source dir
            try:
                candidate.resolve().relative_to(sources_dir.resolve())
                file_path = candidate
                break
            except ValueError:
                continue
    if file_path is None:
        return "Source file not found", 404

    if file_path.suffix == ".pdf":
        return send_file(file_path, mimetype="application/pdf")

    # Serve images directly
    _image_mimes = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".gif": "image/gif"}
    if file_path.suffix.lower() in _image_mimes:
        return send_file(file_path, mimetype=_image_mimes[file_path.suffix.lower()])

    # Wrap text files in readable HTML
    text = file_path.read_text(encoding="utf-8", errors="replace")
    title = filename.replace("_FULLTEXT", "").replace(".txt", "").replace("_", " ")
    return render_template("source_text.html", title=title, text=text, filename=filename)


@app.route("/api/source-map")
@require_access
def api_source_map():
    """Return PMID/PMC → local filename mapping for frontend linkification."""
    return jsonify(_source_map)


def _render_intro() -> str:
    text = _intro_path.read_text(encoding="utf-8")
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            text = parts[2].strip()
    html = markdown.markdown(text, extensions=["tables", "fenced_code", "codehilite", "toc"])
    return _postprocess_html(html)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))
    debug = os.environ.get("FLASK_DEBUG", "1") == "1"
    app.run(host="0.0.0.0", port=port, debug=debug)
