"""RAG Q&A pipeline: retrieve context + generate answer with Gemini."""

from collections import defaultdict

from google import genai

from .config import config
from .search import search, SearchResult

SYSTEM_PROMPT = """# ROLL
Klinisk Forskningsanalytiker för specialister (neurologi/IVA).
Fall: GBS + selektiv IgA-brist + Hashimotos.

# STRIKT POLICY (ZERO-EXEGESIS)
- Förklara ALDRIG termer (t.ex. vad NfL, IVIG eller plasmautbyte är).
- Inga artighetsfraser eller inledningar.
- Gå direkt på den kliniska slutsatsen.
- Evidensstyrka inline: (fas 3, n=242, OR 2.4, p=0.006) eller (fallserie, n=6).
- Citera källa: [Källa: heading_path].

# SVARSSTRUKTUR
1. **KLINISK SYNTES** — en tät mening med kärnan i fyndet
2. **ANALYTISKA KOPPLINGAR** — bulletpoints om korsningar mellan domäner
3. **SIGNAL** — vad som bör bevakas eller undersökas vidare

# BEGRÄNSNINGAR
- Max 300 ord.
- Använd BARA bifogad kontext. Otillräcklig kontext = säg det.
- Svara på samma språk som frågan."""

# Map folder prefixes to clinical domains for LLM context
_DOMAIN_MAP = {
    "01-GBS": "GBS-patofysiologi",
    "02-IgA": "IgA-brist",
    "03-GBS": "GBS+IgA kombination",
    "04-related": "Autoimmuna kluster",
    "05-treatment": "Behandlingsresistens",
    "06-monitoring": "Prognostik",
    "07-acute": "IVA-protokoll",
    "08-immunoglobulin": "Immunoglobulin-säkerhet",
    "sources/": "Originalartikel",
    "research-ivig": "Originalartikel",
}


def _get_domain(source_file: str) -> str:
    """Map a source file path to its clinical domain."""
    for prefix, domain in _DOMAIN_MAP.items():
        if source_file.startswith(prefix):
            return domain
    return "Övrigt"


def _diversify(results: list[SearchResult], target_k: int) -> list[SearchResult]:
    """Re-rank results to ensure cross-domain coverage.

    Takes a larger set of results and selects target_k items,
    ensuring representation from different domains while still
    preferring higher-scoring results.
    """
    if len(results) <= target_k:
        return results

    # Group by domain, preserving score order within each group
    by_domain: dict[str, list[SearchResult]] = defaultdict(list)
    for r in results:
        domain = _get_domain(r.metadata.get("source_file", ""))
        by_domain[domain].append(r)

    selected: list[SearchResult] = []
    seen_ids = set()

    # Round 1: Take the best result from each domain
    for domain in sorted(by_domain, key=lambda d: by_domain[d][0].score, reverse=True):
        if len(selected) >= target_k:
            break
        r = by_domain[domain][0]
        selected.append(r)
        seen_ids.add(id(r))

    # Round 2: Fill remaining slots with highest-scoring unused results
    if len(selected) < target_k:
        remaining = [r for r in results if id(r) not in seen_ids]
        remaining.sort(key=lambda r: r.score, reverse=True)
        for r in remaining:
            if len(selected) >= target_k:
                break
            selected.append(r)

    return selected


def _build_context(results: list[SearchResult]) -> str:
    """Format retrieved chunks with domain labels for the LLM."""
    context_parts = []
    for i, r in enumerate(results, 1):
        heading = r.metadata.get("heading_path", "Unknown")
        source = r.metadata.get("source_file", "Unknown")
        domain = _get_domain(source)
        doc_type = r.metadata.get("doc_type", "research")
        type_label = "Originalartikel" if doc_type == "fulltext_source" else "Forskningssammanfattning"
        context_parts.append(
            f"[Chunk {i} | Domän: {domain} | Typ: {type_label}]\n"
            f"[Källa: {heading}] [Fil: {source}]\n"
            f"{r.text}"
        )
    return "\n\n---\n\n".join(context_parts)


def ask(
    question: str,
    top_k: int | None = None,
    model: str | None = None,
    filter_where: dict | None = None,
    verbose: bool = False,
) -> tuple[str, list[SearchResult]]:
    """Ask a question against the knowledge base. Returns (answer, sources)."""
    if not config.google_api_key:
        raise ValueError("GOOGLE_API_KEY not set.")

    target_k = top_k or config.top_k

    # Retrieve more candidates than needed, then diversify across domains
    candidates = search(question, top_k=target_k * 2, filter_where=filter_where)

    if not candidates:
        return "No relevant information found in the knowledge base.", []

    results = _diversify(candidates, target_k)

    # Build prompt
    context = _build_context(results)
    user_prompt = f"""FRÅGA: {question}

KONTEXT FRÅN KUNSKAPSBAS ({len(results)} chunks från {len(set(_get_domain(r.metadata.get('source_file', '')) for r in results))} domäner):

{context}"""

    # Generate with Gemini (use dedicated medical key if available)
    api_key = config.medical_api_key or config.google_api_key
    client = genai.Client(api_key=api_key)
    llm_model = model or config.llm_model

    response = client.models.generate_content(
        model=llm_model,
        contents=user_prompt,
        config={
            "system_instruction": SYSTEM_PROMPT,
            "temperature": 0.0,
            "max_output_tokens": 8192,
        },
    )

    answer = response.text if response.text else "No answer generated."
    return answer, results
