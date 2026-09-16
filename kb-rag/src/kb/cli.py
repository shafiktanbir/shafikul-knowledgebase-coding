"""KB-RAG CLI — main entry point.

Commands:
    kb index --model <alias>      Incrementally index markdown files
    kb indexes                    Show all index statuses
    kb rebuild --model <alias>    Delete + fully rebuild one model's index
    kb ask --model <alias> <q>    RAG query: embed → search → LLM → answer
    kb search --model <alias> <q> Vector search only (no LLM)
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print as rprint

from .config import load_config
from .embeddings import build_provider
from .ingestion.indexer import run_index
from .llm import build_llm_provider
from .retrieval.search import format_context_for_llm, search
from .storage.metadata import read_metadata, write_metadata
from .vector.sqlite_vec_impl import SQLiteVecIndex

console = Console()

# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #

def _get_index(config, model_alias: str) -> tuple[SQLiteVecIndex, Path]:
    """Return (index, index_dir) for the given model alias."""
    index_dir = config.get_index_dir(model_alias)
    db_path = index_dir / "index.db"
    return SQLiteVecIndex(db_path), index_dir


# --------------------------------------------------------------------------- #
# CLI root
# --------------------------------------------------------------------------- #

@click.group()
@click.version_option("0.1.0", prog_name="kb")
def cli() -> None:
    """KB-RAG: Local RAG indexing layer for your Markdown knowledge base.

    Markdown files are ALWAYS the source of truth.
    Vector indexes are disposable, rebuildable derived artifacts.
    """


# --------------------------------------------------------------------------- #
# kb index
# --------------------------------------------------------------------------- #

@cli.command("index")
@click.option("--model", "-m", required=True, help="Embedding model alias from kb-config.yaml")
@click.option("--json-output", is_flag=True, hidden=True, help="Output result as JSON (for agent use)")
def cmd_index(model: str, json_output: bool) -> None:
    """Incrementally index Markdown files using the specified embedding model.

    Only new or changed files are re-embedded. Unchanged files are skipped.

    Examples:\n
        kb index --model gemini\n
        kb index --model openai-small
    """
    try:
        config = load_config()
    except FileNotFoundError as exc:
        console.print(f"[red]Config error:[/] {exc}")
        sys.exit(1)

    try:
        model_cfg = config.get_model_config(model)
        provider = build_provider(model_cfg, for_query=False)
    except (KeyError, EnvironmentError) as exc:
        console.print(f"[red]Error:[/] {exc}")
        sys.exit(1)

    index, index_dir = _get_index(config, model)

    # Write metadata.json before indexing
    write_metadata(
        index_dir=index_dir,
        provider=provider.get_provider_name(),
        model=provider.get_model_name(),
        dimensions=provider.get_dimensions(),
        chunking_version=config.chunking_version,
    )

    status_lines: list[tuple[str, str]] = []

    def on_progress(source: str, status: str) -> None:
        status_lines.append((source, status))
        if not json_output:
            color = {
                "indexed": "green",
                "skip": "dim",
                "error": "red",
                "empty": "yellow",
            }.get(status, "white")
            icon = {"indexed": "✓", "skip": "·", "error": "✗", "empty": "○"}.get(status, " ")
            console.print(f"  [{color}]{icon}[/] {source}  [{color}]{status}[/]")

    if not json_output:
        console.print(f"\n[bold cyan]KB Index[/] — model: [bold]{provider.get_model_name()}[/]")
        console.print(f"  KB root:    {config.knowledge_base_path}")
        console.print(f"  Index dir:  {index_dir}")
        console.print()

    result = run_index(
        config=config,
        index=index,
        provider=provider,
        model_alias=model,
        progress_callback=on_progress,
    )

    if json_output:
        output = {
            "model": provider.get_model_name(),
            "total_files": result.total_files,
            "indexed": result.indexed,
            "skipped": result.skipped,
            "total_chunks": result.total_chunks,
            "errors": result.errors,
        }
        print(json.dumps(output))
        return

    console.print()
    console.print(f"[bold green]Done.[/] {result.indexed} indexed, {result.skipped} skipped, {result.total_chunks} chunks total")

    if result.errors:
        console.print(f"\n[bold red]Errors ({len(result.errors)}):[/]")
        for err in result.errors:
            console.print(f"  [red]• {err}[/]")


# --------------------------------------------------------------------------- #
# kb indexes
# --------------------------------------------------------------------------- #

@cli.command("indexes")
@click.option("--json-output", is_flag=True, hidden=True, help="Output as JSON")
def cmd_indexes(json_output: bool) -> None:
    """Show status of all configured model indexes.

    Displays document count, chunk count, dimensions, and last indexed time.
    """
    try:
        config = load_config()
    except FileNotFoundError as exc:
        console.print(f"[red]Config error:[/] {exc}")
        sys.exit(1)

    rows = []
    for alias, model_cfg in config.embedding_models.items():
        model_name = model_cfg["model"]
        index_dir = config.get_index_dir(alias)
        db_path = index_dir / "index.db"

        meta = read_metadata(index_dir)
        dimensions = meta["dimensions"] if meta else model_cfg.get("dimensions", "?")

        if db_path.exists():
            idx = SQLiteVecIndex(db_path)
            idx.initialize(int(dimensions) if isinstance(dimensions, (int, str)) else 0)
            stats = idx.get_stats()
            status = "ready" if stats.document_count > 0 else "empty"
            doc_count = stats.document_count
            chunk_count = stats.chunk_count
            last_indexed = (stats.last_indexed_at or "—")[:19].replace("T", " ")
        else:
            status = "not built"
            doc_count = 0
            chunk_count = 0
            last_indexed = "—"

        rows.append({
            "alias": alias,
            "model": model_name,
            "docs": doc_count,
            "chunks": chunk_count,
            "dimensions": dimensions,
            "status": status,
            "last_indexed": last_indexed,
        })

    if json_output:
        print(json.dumps(rows))
        return

    table = Table(title="KB Indexes", show_header=True, header_style="bold cyan")
    table.add_column("ALIAS", style="bold")
    table.add_column("MODEL")
    table.add_column("DOCS", justify="right")
    table.add_column("CHUNKS", justify="right")
    table.add_column("DIM", justify="right")
    table.add_column("STATUS")
    table.add_column("LAST INDEXED")

    for r in rows:
        status_color = {"ready": "green", "empty": "yellow", "not built": "red"}.get(r["status"], "white")
        table.add_row(
            r["alias"],
            r["model"],
            f"{r['docs']:,}",
            f"{r['chunks']:,}",
            str(r["dimensions"]),
            f"[{status_color}]{r['status']}[/{status_color}]",
            r["last_indexed"],
        )

    console.print()
    console.print(table)
    console.print()


# --------------------------------------------------------------------------- #
# kb rebuild
# --------------------------------------------------------------------------- #

@cli.command("rebuild")
@click.option("--model", "-m", required=True, help="Embedding model alias to rebuild")
@click.option("--yes", "-y", is_flag=True, help="Skip confirmation prompt")
def cmd_rebuild(model: str, yes: bool) -> None:
    """Delete and fully rebuild ONE model's index from Markdown source.

    IMPORTANT: Only the specified model's index is touched.
    Other model indexes are completely unaffected.

    Examples:\n
        kb rebuild --model gemini\n
        kb rebuild --model openai-small --yes
    """
    try:
        config = load_config()
        model_cfg = config.get_model_config(model)
    except (FileNotFoundError, KeyError) as exc:
        console.print(f"[red]Error:[/] {exc}")
        sys.exit(1)

    index_dir = config.get_index_dir(model)

    if not yes:
        console.print(f"\n[bold yellow]⚠  Rebuild will delete all data in:[/]")
        console.print(f"   {index_dir}")
        console.print(f"\n   Other model indexes are [bold green]NOT affected[/].")
        if not click.confirm("\nProceed?"):
            console.print("[dim]Cancelled.[/]")
            return

    try:
        provider = build_provider(model_cfg, for_query=False)
    except (KeyError, EnvironmentError) as exc:
        console.print(f"[red]Error:[/] {exc}")
        sys.exit(1)

    index, _ = _get_index(config, model)

    console.print(f"\n[bold red]Clearing index[/] for [bold]{model}[/]...")
    index.initialize(provider.get_dimensions())
    index.clear()

    write_metadata(
        index_dir=index_dir,
        provider=provider.get_provider_name(),
        model=provider.get_model_name(),
        dimensions=provider.get_dimensions(),
        chunking_version=config.chunking_version,
    )

    console.print("[bold cyan]Rebuilding from Markdown source...[/]\n")

    def on_progress(source: str, status: str) -> None:
        color = {"indexed": "green", "skip": "dim", "error": "red"}.get(status, "white")
        icon = {"indexed": "✓", "skip": "·", "error": "✗"}.get(status, " ")
        console.print(f"  [{color}]{icon}[/] {source}  [{color}]{status}[/]")

    result = run_index(
        config=config,
        index=index,
        provider=provider,
        model_alias=model,
        progress_callback=on_progress,
    )

    console.print(f"\n[bold green]Rebuild complete.[/] {result.indexed} files, {result.total_chunks} chunks.")
    if result.errors:
        for err in result.errors:
            console.print(f"  [red]• {err}[/]")


# --------------------------------------------------------------------------- #
# kb search (vector only, no LLM)
# --------------------------------------------------------------------------- #

@cli.command("search")
@click.option("--model", "-m", required=True, help="Embedding model alias")
@click.option("--top-k", "-k", default=5, show_default=True)
@click.option("--json-output", is_flag=True, hidden=True)
@click.argument("query")
def cmd_search(model: str, top_k: int, json_output: bool, query: str) -> None:
    """Vector similarity search without LLM generation.

    Returns the top-K most relevant chunks for the query.
    Useful for debugging retrieval quality.

    Examples:\n
        kb search --model gemini "PostgreSQL transaction isolation"\n
        kb search --model gemini --top-k 10 "kubernetes RBAC"
    """
    try:
        config = load_config()
        model_cfg = config.get_model_config(model)
    except (FileNotFoundError, KeyError) as exc:
        console.print(f"[red]Error:[/] {exc}")
        sys.exit(1)

    index, index_dir = _get_index(config, model)
    db_path = index_dir / "index.db"

    if not db_path.exists():
        console.print(f"[red]Index not built yet.[/] Run: kb index --model {model}")
        sys.exit(1)

    try:
        provider = build_provider(model_cfg, for_query=True)
    except (KeyError, EnvironmentError) as exc:
        console.print(f"[red]Error:[/] {exc}")
        sys.exit(1)

    index.initialize(provider.get_dimensions())

    results = search(query=query, provider=provider, index=index, top_k=top_k)

    if json_output:
        output = [
            {
                "chunk_id": r.chunk_id,
                "source": r.source,
                "chunk_index": r.chunk_index,
                "score": r.score,
                "content": r.content,
                "metadata": r.metadata,
            }
            for r in results
        ]
        print(json.dumps(output, indent=2))
        return

    if not results:
        console.print("[yellow]No results found.[/]")
        return

    console.print(f"\n[bold cyan]Search Results[/] for: [italic]{query}[/]")
    console.print(f"  Model: {model} | Top-K: {top_k}\n")

    for i, r in enumerate(results, 1):
        console.print(f"[bold cyan][{i}][/] [dim]{r.source}[/]  score=[bold]{r.score:.3f}[/]")
        console.print(f"    {r.content[:300].replace(chr(10), ' ')}{'...' if len(r.content) > 300 else ''}")
        console.print()


# --------------------------------------------------------------------------- #
# kb ask (full RAG: embed → search → LLM → answer)
# --------------------------------------------------------------------------- #

@cli.command("ask")
@click.option("--model", "-m", required=True, help="Embedding model alias")
@click.option("--top-k", "-k", default=8, show_default=True)
@click.option("--show-sources", is_flag=True, default=True, show_default=True)
@click.option("--json-output", is_flag=True, hidden=True, help="Output as JSON (for Antigravity skill)")
@click.argument("question")
def cmd_ask(model: str, top_k: int, show_sources: bool, json_output: bool, question: str) -> None:
    """Ask a question — retrieves relevant KB chunks and generates an answer.

    Flow:
        Question → embed (same model as index) → vector search → top-K chunks → LLM → answer

    The LLM is separate from the embedding model. Change it in kb-config.yaml
    without rebuilding the index.

    Examples:\n
        kb ask --model gemini "What ADRs exist for the clinic app?"\n
        kb ask --model gemini "Explain PostgreSQL transaction isolation"
    """
    try:
        config = load_config()
        model_cfg = config.get_model_config(model)
    except (FileNotFoundError, KeyError) as exc:
        if json_output:
            print(json.dumps({"error": str(exc)}))
        else:
            console.print(f"[red]Error:[/] {exc}")
        sys.exit(1)

    index, index_dir = _get_index(config, model)
    db_path = index_dir / "index.db"

    if not db_path.exists():
        msg = f"Index not built yet. Run: kb index --model {model}"
        if json_output:
            print(json.dumps({"error": msg}))
        else:
            console.print(f"[red]{msg}[/]")
        sys.exit(1)

    # Build query-time embedding provider (RETRIEVAL_QUERY task type for Gemini)
    try:
        query_provider = build_provider(model_cfg, for_query=True)
    except (KeyError, EnvironmentError) as exc:
        if json_output:
            print(json.dumps({"error": str(exc)}))
        else:
            console.print(f"[red]Error:[/] {exc}")
        sys.exit(1)

    index.initialize(query_provider.get_dimensions())

    # Retrieve relevant chunks
    if not json_output:
        console.print(f"\n[bold cyan]Searching KB[/] with {model}...")

    results = search(query=question, provider=query_provider, index=index, top_k=top_k)

    if not results:
        msg = "No relevant context found in the knowledge base for this question."
        if json_output:
            print(json.dumps({"answer": msg, "sources": [], "context": ""}))
        else:
            console.print(f"[yellow]{msg}[/]")
        return

    # Format context for LLM
    context = format_context_for_llm(results)

    # Build LLM prompt
    system_prompt = config.llm.get(
        "system_prompt",
        "You are a precise technical assistant. Answer only from the provided context."
    )
    user_prompt = f"""Context from knowledge base:

{context}

---

Question: {question}

Answer based strictly on the context above. Cite the source files when relevant."""

    # Generate answer
    if not json_output:
        console.print(f"[bold cyan]Generating answer[/] with {config.llm.get('model', 'gemini')}...\n")

    try:
        llm = build_llm_provider(config.llm)
        answer = llm.generate(system_prompt=system_prompt, user_prompt=user_prompt)
    except (KeyError, EnvironmentError) as exc:
        if json_output:
            print(json.dumps({"error": str(exc), "context": context}))
        else:
            console.print(f"[red]Error:[/] {exc}")
        sys.exit(1)
    except Exception as exc:  # noqa: BLE001
        if json_output:
            print(json.dumps({"error": str(exc), "context": context}))
        else:
            console.print(f"[red]LLM error:[/] {exc}")
        sys.exit(1)

    if json_output:
        sources = [{"source": r.source, "score": r.score, "content": r.content} for r in results]
        print(json.dumps({"answer": answer, "sources": sources, "context": context}))
        return

    # Human-readable output
    console.print(f"[bold white]Answer:[/]\n")
    console.print(answer)

    if show_sources:
        console.print(f"\n[dim]── Sources ({len(results)}) ──────────────────────────────[/]")
        for r in results:
            console.print(f"  [dim]• {r.source}  (score: {r.score:.3f})[/]")
    console.print()
