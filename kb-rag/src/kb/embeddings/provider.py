"""Abstract EmbeddingProvider base class.

All embedding providers must implement this interface.
The indexing pipeline ONLY depends on this interface — never on a concrete provider.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class EmbeddingProvider(ABC):
    """Abstract base for all embedding providers.

    Design contract:
    - embed() and embed_batch() are the only two methods the indexer calls.
    - Implementations handle auth, retry, batching limits internally.
    - The provider is stateless regarding the index — it only produces vectors.
    """

    @abstractmethod
    def embed(self, text: str) -> list[float]:
        """Embed a single text string. Returns a vector of floats."""
        ...

    @abstractmethod
    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Embed a list of text strings. Returns a list of vectors.

        Implementations should handle batching/rate-limits internally.
        """
        ...

    @abstractmethod
    def get_model_name(self) -> str:
        """Return the canonical model identifier (e.g. 'text-embedding-004')."""
        ...

    @abstractmethod
    def get_dimensions(self) -> int:
        """Return the embedding vector dimension count."""
        ...

    @abstractmethod
    def get_provider_name(self) -> str:
        """Return the provider name (e.g. 'gemini', 'openai')."""
        ...
