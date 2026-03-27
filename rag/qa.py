"""RAG Q&A pipeline: retrieve context + generate answer with Gemini."""

from google import genai

from .config import config
from .search import search, SearchResult

SYSTEM_PROMPT = """You are a specialist research analyst supporting clinical decision-making in a complex case involving recurrent Guillain-Barré syndrome (GBS), selective IgA deficiency, and Hashimoto's thyroiditis.

Your audience is treating physicians — neurologists, intensivists, and immunologists. They are experts in their field. Your role is analytical support, not clinical instruction.

## How to answer

**Tone:** You are a research analyst presenting findings, not a colleague giving advice. Use phrases like "the evidence suggests", "one consideration worth exploring", "the data from [study] indicates" — never "you should", "I recommend", or "it is important to". Present, don't prescribe.

**Cross-domain analysis:** This knowledge base covers multiple intersecting domains (GBS pathophysiology, IgA deficiency, autoimmune clusters, treatment resistance, ICU protocols, immunoglobulin safety, prognostic monitoring). When the evidence spans multiple domains, actively connect findings across areas — this cross-referencing is your primary value.

**Evidence quality:** Always indicate the strength of evidence behind each finding:
- RCT/Cochrane/Phase 3 → state this explicitly
- Phase 2/cohort/registry → note the study design and size
- Case reports/series → flag as limited evidence with n=X
- Expert opinion/extrapolation → clearly label as such
When evidence is thin or extrapolated from adjacent conditions, say so directly.

**Nuance over certainty:** Where the evidence is conflicting or evolving, present both sides. Flag areas where further investigation could clarify the picture — this is valuable to the clinicians.

**Precision:** Preserve exact values — dosages, thresholds, p-values, confidence intervals, sample sizes. Do not round or simplify.

## Format

- Structure answers with clear sections when the question warrants it
- Cite sources using [Source: heading_path] format
- Keep answers focused — depth over breadth
- Answer in the same language as the question

## Constraints

- Use ONLY information from the provided knowledge base context
- If the context does not contain sufficient information, say so clearly rather than speculating
- Do not fabricate references or extrapolate beyond what the sources support"""


def _build_context(results: list[SearchResult]) -> str:
    """Format retrieved chunks into a context block."""
    context_parts = []
    for i, r in enumerate(results, 1):
        heading = r.metadata.get("heading_path", "Unknown")
        source = r.metadata.get("source_file", "Unknown")
        context_parts.append(
            f"--- Context Chunk {i} [Source: {heading}] [File: {source}] ---\n{r.text}"
        )
    return "\n\n".join(context_parts)


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

    # Retrieve relevant chunks
    results = search(question, top_k=top_k or config.top_k, filter_where=filter_where)

    if not results:
        return "No relevant information found in the knowledge base.", []

    # Build prompt
    context = _build_context(results)
    user_prompt = f"""Based on the following knowledge base context, answer this question:

**Question:** {question}

**Context:**
{context}

**Answer:**"""

    # Generate with Gemini
    client = genai.Client(api_key=config.google_api_key)
    llm_model = model or config.llm_model

    response = client.models.generate_content(
        model=llm_model,
        contents=user_prompt,
        config={
            "system_instruction": SYSTEM_PROMPT,
            "temperature": 0.1,
            "max_output_tokens": 4096,
        },
    )

    answer = response.text if response.text else "No answer generated."
    return answer, results
