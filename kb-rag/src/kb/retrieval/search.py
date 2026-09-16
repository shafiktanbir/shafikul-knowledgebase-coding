"""RAG search — embeds a query and retrieves top-K relevant chunks.

The query embedding MUST use the same model as the index.
This module enforces that by accepting the provider as a parameter.
"""

from __future__ import annotations

from ..embeddings import EmbeddingProvider
from ..vector.index import SearchResult, VectorIndex


def search(
    query: str,
    provider: EmbeddingProvider,
    index: VectorIndex,
    top_k: int = 8,
) -> list[SearchResult]:
    """Embed the query and return top-K matching chunks from the index.

    Args:
        query: Natural language question.
        provider: EmbeddingProvider configured for RETRIEVAL_QUERY task_type.
                  MUST be the same model that created the index.
        index: VectorIndex to search in.
        top_k: Number of results to return.

    Returns:
        List of SearchResult sorted by score descending (most relevant first).
    """
    query_vector = provider.embed(query)
    results = index.search(query_vector, limit=top_k)
    return sorted(results, key=lambda r: r.score, reverse=True)


def format_context_for_llm(results: list[SearchResult]) -> str:
    """Format search results into a context block for the LLM prompt.

    Returns a numbered list of source-attributed passages.
    """
    if not results:
        return "No relevant context found in the knowledge base."

    lines: list[str] = []
    for i, r in enumerate(results, 1):
        lines.append(f"--- Context [{i}] | Source: {r.source} | Score: {r.score:.3f} ---")
        lines.append(r.content.strip())
        lines.append("")

    return "\n".join(lines)
