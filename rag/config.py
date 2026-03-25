"""Configuration for the GBS-IgA Research RAG system."""

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

# Load .env from project root
_project_root = Path(__file__).resolve().parent.parent
load_dotenv(_project_root / ".env")


@dataclass(frozen=True)
class Config:
    google_api_key: str = os.getenv("GOOGLE_API_KEY", "")
    docs_dir: Path = _project_root
    chroma_dir: Path = _project_root / "chroma_db"
    embedding_model: str = "gemini-embedding-001"
    llm_model: str = "gemini-2.5-flash"
    chunk_max_tokens: int = 1200
    top_k: int = 5
    collection_name: str = "gb_research"

    # Directories to index (relative to docs_dir)
    index_dirs: tuple = (
        "01-GBS",
        "02-IgA-deficiency",
        "03-GBS-and-IgA-deficiency",
        "04-related-autoimmune",
        "05-treatment-resistance",
        "06-monitoring-prognosis",
        "07-acute-icu-protocols",
    )

    # Directories to exclude
    exclude_dirs: tuple = ("metadata", "rag", "chroma_db")


config = Config()
