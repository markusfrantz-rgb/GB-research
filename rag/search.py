"""Semantic search against the ChromaDB knowledge base."""

from dataclasses import dataclass

import chromadb
from google import genai

from .config import config


@dataclass
class SearchResult:
    text: str
    score: float
    metadata: dict


def _get_client() -> genai.Client:
    return genai.Client(api_key=config.google_api_key)


def _embed_query(client: genai.Client, query: str) -> list[float]:
    """Embed a single query string."""
    result = client.models.embed_content(
        model=config.embedding_model,
        contents=query,
    )
    return result.embeddings[0].values


def search(
    query: str,
    top_k: int | None = None,
    filter_where: dict | None = None,
) -> list[SearchResult]:
    """Search the knowledge base for relevant chunks."""
    if not config.google_api_key:
        raise ValueError("GOOGLE_API_KEY not set.")

    k = top_k or config.top_k
    gemini_client = _get_client()
    chroma = chromadb.PersistentClient(path=str(config.chroma_dir))

    try:
        collection = chroma.get_collection(config.collection_name)
    except ValueError:
        raise RuntimeError("No indexed data found. Run 'python -m rag.cli ingest' first.")

    query_embedding = _embed_query(gemini_client, query)

    query_params = {
        "query_embeddings": [query_embedding],
        "n_results": k,
        "include": ["documents", "metadatas", "distances"],
    }
    if filter_where:
        query_params["where"] = filter_where

    results = collection.query(**query_params)

    search_results = []
    for i in range(len(results["ids"][0])):
        search_results.append(SearchResult(
            text=results["documents"][0][i],
            score=1 - results["distances"][0][i],  # cosine distance -> similarity
            metadata=results["metadatas"][0][i],
        ))

    return search_results
