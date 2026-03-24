"""RAG Q&A pipeline: retrieve context + generate answer with Gemini."""

from google import genai

from .config import config
from .search import search, SearchResult

SYSTEM_PROMPT = """You are a medical research assistant with expertise in neurology and immunology.
You answer questions based ONLY on the provided knowledge base context.

Rules:
- Only use information from the provided context chunks
- Cite your sources using [Source: heading_path] format after each claim
- Preserve medical precision: exact dosages, statistics, evidence levels, p-values
- If the context does not contain sufficient information, say so clearly
- Structure answers with clear sections when appropriate
- Use evidence level indicators (Level 1 = RCT/Cochrane, Level 2 = Phase 2/3, etc.)
- Answer in the same language as the question"""


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
