"""Embeddings subpackage.

Factory function to build an EmbeddingProvider from a model config dict.
"""

from __future__ import annotations

from typing import Any

from .provider import EmbeddingProvider


def build_provider(model_config: dict[str, Any], for_query: bool = False) -> EmbeddingProvider:
    """Build the correct EmbeddingProvider from a model config dict.

    Args:
        model_config: Dict from kb-config.yaml embedding_models section.
        for_query: If True, configure the provider for query-time embedding
                   (uses RETRIEVAL_QUERY task_type for Gemini).

    Returns:
        Concrete EmbeddingProvider instance.
    """
    provider_name: str = model_config.get("provider", "gemini").lower()
    model: str = model_config["model"]
    dimensions: int = model_config.get("dimensions", 768)

    if provider_name == "gemini":
        from .gemini import GeminiEmbeddingProvider  # noqa: PLC0415

        task_type_key = "query_task_type" if for_query else "task_type"
        task_type: str = model_config.get(task_type_key, "RETRIEVAL_QUERY" if for_query else "RETRIEVAL_DOCUMENT")

        return GeminiEmbeddingProvider(
            model=model,
            dimensions=dimensions,
            task_type=task_type,
        )

    elif provider_name == "openai":
        from .openai import OpenAIEmbeddingProvider  # noqa: PLC0415

        return OpenAIEmbeddingProvider(model=model, dimensions=dimensions)

    else:
        raise ValueError(
            f"Unknown embedding provider: '{provider_name}'. "
            "Supported: gemini, openai"
        )


__all__ = ["EmbeddingProvider", "build_provider"]
