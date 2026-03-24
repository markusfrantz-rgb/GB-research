"""Document ingestion: load markdown, chunk, embed, store in ChromaDB."""

from pathlib import Path

import chromadb
from google import genai

from .config import config
from .chunker import Chunk, chunk_markdown, parse_frontmatter


def _get_client() -> genai.Client:
    return genai.Client(api_key=config.google_api_key)


def _find_documents() -> list[Path]:
    """Find all markdown files in configured index directories."""
    docs = []
    for dir_name in config.index_dirs:
        dir_path = config.docs_dir / dir_name
        if dir_path.exists():
            docs.extend(sorted(dir_path.rglob("*.md")))
    return docs


def _embed_batch(client: genai.Client, texts: list[str]) -> list[list[float]]:
    """Embed a batch of texts using Gemini embedding API."""
    result = client.models.embed_content(
        model=config.embedding_model,
        contents=texts,
    )
    return [e.values for e in result.embeddings]


def ingest(reindex: bool = False, verbose: bool = False):
    """Load documents, chunk, embed, and store in ChromaDB."""
    if not config.google_api_key:
        raise ValueError("GOOGLE_API_KEY not set. Copy .env.example to .env and add your key.")

    # Initialize ChromaDB
    chroma = chromadb.PersistentClient(path=str(config.chroma_dir))

    if reindex:
        try:
            chroma.delete_collection(config.collection_name)
        except Exception:
            pass

    collection = chroma.get_or_create_collection(
        name=config.collection_name,
        metadata={"hnsw:space": "cosine"},
    )

    # Find and process documents
    doc_paths = _find_documents()
    if not doc_paths:
        print("No documents found to index.")
        return

    all_chunks: list[Chunk] = []
    gemini_client = _get_client()

    for doc_path in doc_paths:
        rel_path = str(doc_path.relative_to(config.docs_dir))
        text = doc_path.read_text(encoding="utf-8")
        frontmatter, body = parse_frontmatter(text)

        chunks = chunk_markdown(body, rel_path, max_tokens=config.chunk_max_tokens)

        # Add frontmatter metadata to each chunk
        for chunk in chunks:
            chunk.metadata["doc_type"] = frontmatter.get("doc_type", "")
            chunk.metadata["doc_status"] = frontmatter.get("status", "active")
            chunk.metadata["doc_date"] = str(frontmatter.get("date", ""))

        all_chunks.extend(chunks)

        if verbose:
            print(f"  {rel_path}: {len(chunks)} chunks")

    if not all_chunks:
        print("No chunks generated.")
        return

    print(f"Processing {len(doc_paths)} documents -> {len(all_chunks)} chunks")

    # Embed in batches
    batch_size = 50
    all_embeddings = []
    for i in range(0, len(all_chunks), batch_size):
        batch_texts = [c.text for c in all_chunks[i:i + batch_size]]
        embeddings = _embed_batch(gemini_client, batch_texts)
        all_embeddings.extend(embeddings)
        if verbose:
            print(f"  Embedded batch {i // batch_size + 1}/{(len(all_chunks) - 1) // batch_size + 1}")

    # Store in ChromaDB
    ids = [f"{c.metadata['source_file']}::{c.metadata['chunk_index']}" for c in all_chunks]
    documents = [c.text for c in all_chunks]
    metadatas = [c.metadata for c in all_chunks]

    collection.upsert(
        ids=ids,
        embeddings=all_embeddings,
        documents=documents,
        metadatas=metadatas,
    )

    print(f"Indexed {len(all_chunks)} chunks into '{config.collection_name}' collection")
    print(f"ChromaDB stored at: {config.chroma_dir}")
