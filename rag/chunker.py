"""Markdown-aware hierarchical chunker for medical research documents."""

import re
import yaml
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Chunk:
    text: str
    metadata: dict = field(default_factory=dict)


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Extract YAML frontmatter and return (metadata, body)."""
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            try:
                meta = yaml.safe_load(parts[1]) or {}
                return meta, parts[2].strip()
            except yaml.YAMLError:
                pass
    return {}, text


def _estimate_tokens(text: str) -> int:
    """Rough token estimate: ~0.75 tokens per word for English medical text."""
    return int(len(text.split()) * 1.33)


def _extract_h1(body: str) -> str:
    """Extract the first H1 heading as the document title."""
    for line in body.split("\n"):
        if line.startswith("# ") and not line.startswith("## "):
            return line.lstrip("# ").strip()
    return ""


def _split_by_heading(body: str, level: int) -> list[tuple[str, str]]:
    """Split text by heading level. Returns list of (heading_text, content)."""
    prefix = "#" * level + " "
    sections = []
    current_heading = ""
    current_lines = []

    for line in body.split("\n"):
        if line.startswith(prefix) and not line.startswith("#" * (level + 1) + " "):
            if current_lines:
                sections.append((current_heading, "\n".join(current_lines)))
            current_heading = line.lstrip("#").strip()
            current_lines = [line]
        else:
            current_lines.append(line)

    if current_lines:
        sections.append((current_heading, "\n".join(current_lines)))

    return sections


def _is_protected_block(lines: list[str], start: int) -> int | None:
    """Check if position starts a protected block (table or code fence).
    Returns end index if protected, None otherwise."""
    line = lines[start]

    # Code fence
    if line.strip().startswith("```"):
        for i in range(start + 1, len(lines)):
            if lines[i].strip().startswith("```"):
                return i
        return len(lines) - 1

    # Table block (consecutive lines starting with |)
    if line.strip().startswith("|"):
        end = start
        for i in range(start, len(lines)):
            if lines[i].strip().startswith("|") or lines[i].strip().startswith(":--"):
                end = i
            else:
                break
        if end > start:
            return end

    return None


def _split_by_paragraphs(text: str, max_tokens: int) -> list[str]:
    """Split text on paragraph boundaries (double newlines), preserving protected blocks."""
    lines = text.split("\n")
    chunks = []
    current = []
    i = 0

    while i < len(lines):
        # Check for protected blocks
        protected_end = _is_protected_block(lines, i)
        if protected_end is not None:
            current.extend(lines[i:protected_end + 1])
            i = protected_end + 1
            continue

        # Paragraph boundary (empty line)
        if lines[i].strip() == "" and current:
            candidate = "\n".join(current)
            if _estimate_tokens(candidate) >= max_tokens and len(current) > 3:
                chunks.append(candidate)
                current = []
            else:
                current.append(lines[i])
        else:
            current.append(lines[i])
        i += 1

    if current:
        chunks.append("\n".join(current))

    return chunks if chunks else [text]


def chunk_markdown(
    body: str,
    source_file: str,
    max_tokens: int = 1200,
) -> list[Chunk]:
    """Chunk a markdown document using hierarchical heading splitting.

    Strategy:
    1. Split on H2 boundaries
    2. If chunk > max_tokens, split on H3
    3. If still > max_tokens, split on H4
    4. If still > max_tokens, split on paragraph boundaries
    5. Never split inside tables or code fences
    """
    doc_title = _extract_h1(body)
    chunks = []
    chunk_index = 0

    h2_sections = _split_by_heading(body, 2)

    for h2_heading, h2_content in h2_sections:
        if _estimate_tokens(h2_content) <= max_tokens:
            chunks.append(Chunk(
                text=h2_content.strip(),
                metadata={
                    "source_file": source_file,
                    "doc_title": doc_title,
                    "section": h2_heading,
                    "subsection": "",
                    "heading_path": f"{doc_title} > {h2_heading}" if h2_heading else doc_title,
                    "chunk_index": chunk_index,
                },
            ))
            chunk_index += 1
        else:
            # Split further on H3
            h3_sections = _split_by_heading(h2_content, 3)
            for h3_heading, h3_content in h3_sections:
                if _estimate_tokens(h3_content) <= max_tokens:
                    heading_path = f"{doc_title} > {h2_heading}"
                    if h3_heading:
                        heading_path += f" > {h3_heading}"
                    chunks.append(Chunk(
                        text=h3_content.strip(),
                        metadata={
                            "source_file": source_file,
                            "doc_title": doc_title,
                            "section": h2_heading,
                            "subsection": h3_heading,
                            "heading_path": heading_path,
                            "chunk_index": chunk_index,
                        },
                    ))
                    chunk_index += 1
                else:
                    # Split on H4
                    h4_sections = _split_by_heading(h3_content, 4)
                    for h4_heading, h4_content in h4_sections:
                        if _estimate_tokens(h4_content) <= max_tokens:
                            heading_path = f"{doc_title} > {h2_heading}"
                            if h3_heading:
                                heading_path += f" > {h3_heading}"
                            if h4_heading:
                                heading_path += f" > {h4_heading}"
                            chunks.append(Chunk(
                                text=h4_content.strip(),
                                metadata={
                                    "source_file": source_file,
                                    "doc_title": doc_title,
                                    "section": h2_heading,
                                    "subsection": h3_heading or h4_heading,
                                    "heading_path": heading_path,
                                    "chunk_index": chunk_index,
                                },
                            ))
                            chunk_index += 1
                        else:
                            # Last resort: paragraph splitting
                            para_chunks = _split_by_paragraphs(h4_content, max_tokens)
                            for pc in para_chunks:
                                heading_path = f"{doc_title} > {h2_heading}"
                                if h3_heading:
                                    heading_path += f" > {h3_heading}"
                                if h4_heading:
                                    heading_path += f" > {h4_heading}"
                                chunks.append(Chunk(
                                    text=pc.strip(),
                                    metadata={
                                        "source_file": source_file,
                                        "doc_title": doc_title,
                                        "section": h2_heading,
                                        "subsection": h3_heading or h4_heading,
                                        "heading_path": heading_path,
                                        "chunk_index": chunk_index,
                                    },
                                ))
                                chunk_index += 1

    # Filter out empty chunks
    return [c for c in chunks if c.text.strip()]
