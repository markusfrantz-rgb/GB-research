"""CLI entry point for the GBS-IgA Research RAG system."""

import argparse
import sys

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table

console = Console()


def cmd_ingest(args):
    from .ingest import ingest
    ingest(reindex=args.reindex, verbose=args.verbose)


def cmd_search(args):
    from .search import search

    filter_where = None
    if args.filter:
        key, value = args.filter.split("=", 1)
        filter_where = {key: value}

    results = search(args.query, top_k=args.top_k, filter_where=filter_where)

    if not results:
        console.print("[yellow]No results found.[/yellow]")
        return

    table = Table(title=f"Search: '{args.query}'", show_lines=True)
    table.add_column("#", width=3)
    table.add_column("Score", width=6)
    table.add_column("Source", width=30)
    table.add_column("Content", ratio=1)

    for i, r in enumerate(results, 1):
        heading = r.metadata.get("heading_path", "")
        preview = r.text[:300].replace("\n", " ") + "..." if len(r.text) > 300 else r.text.replace("\n", " ")
        table.add_row(str(i), f"{r.score:.3f}", heading, preview)

    console.print(table)

    if args.verbose:
        for i, r in enumerate(results, 1):
            console.print(Panel(
                Markdown(r.text),
                title=f"[bold]Chunk {i}: {r.metadata.get('heading_path', '')}[/bold]",
                subtitle=f"Score: {r.score:.3f}",
            ))


def cmd_ask(args):
    from .qa import ask

    filter_where = None
    if args.filter:
        key, value = args.filter.split("=", 1)
        filter_where = {key: value}

    with console.status("Searching and generating answer..."):
        answer, sources = ask(
            args.question,
            top_k=args.top_k,
            model=args.model,
            filter_where=filter_where,
            verbose=args.verbose,
        )

    console.print(Panel(Markdown(answer), title="[bold green]Answer[/bold green]", padding=(1, 2)))

    if sources:
        console.print("\n[bold]Sources used:[/bold]")
        for i, s in enumerate(sources, 1):
            heading = s.metadata.get("heading_path", "")
            source_file = s.metadata.get("source_file", "")
            console.print(f"  {i}. [{s.score:.3f}] {heading} ({source_file})")


def cmd_stats(args):
    import chromadb
    from .config import config

    chroma = chromadb.PersistentClient(path=str(config.chroma_dir))
    try:
        collection = chroma.get_collection(config.collection_name)
    except ValueError:
        console.print("[yellow]No indexed data. Run 'ingest' first.[/yellow]")
        return

    count = collection.count()
    all_data = collection.get(include=["metadatas"])

    # Count by source file
    sources = {}
    for meta in all_data["metadatas"]:
        src = meta.get("source_file", "unknown")
        sources[src] = sources.get(src, 0) + 1

    table = Table(title="Knowledge Base Statistics")
    table.add_column("Document", ratio=1)
    table.add_column("Chunks", width=8, justify="right")

    for src, cnt in sorted(sources.items()):
        table.add_row(src, str(cnt))

    table.add_row("[bold]Total[/bold]", f"[bold]{count}[/bold]")
    console.print(table)


def main():
    parser = argparse.ArgumentParser(
        prog="rag",
        description="GBS-IgA Research RAG Database",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # ingest
    p_ingest = sub.add_parser("ingest", help="Index all documents into ChromaDB")
    p_ingest.add_argument("--reindex", action="store_true", help="Delete existing index and rebuild")
    p_ingest.add_argument("--verbose", "-v", action="store_true")
    p_ingest.set_defaults(func=cmd_ingest)

    # search
    p_search = sub.add_parser("search", help="Semantic search the knowledge base")
    p_search.add_argument("query", help="Search query")
    p_search.add_argument("--top-k", type=int, default=5, help="Number of results")
    p_search.add_argument("--filter", help="Metadata filter (key=value)")
    p_search.add_argument("--verbose", "-v", action="store_true", help="Show full chunk content")
    p_search.set_defaults(func=cmd_search)

    # ask
    p_ask = sub.add_parser("ask", help="Ask a question (RAG Q&A)")
    p_ask.add_argument("question", help="Your question")
    p_ask.add_argument("--top-k", type=int, default=5, help="Number of context chunks")
    p_ask.add_argument("--model", help="Override LLM model (e.g., gemini-2.5-pro)")
    p_ask.add_argument("--filter", help="Metadata filter (key=value)")
    p_ask.add_argument("--verbose", "-v", action="store_true")
    p_ask.set_defaults(func=cmd_ask)

    # stats
    p_stats = sub.add_parser("stats", help="Show knowledge base statistics")
    p_stats.set_defaults(func=cmd_stats)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
