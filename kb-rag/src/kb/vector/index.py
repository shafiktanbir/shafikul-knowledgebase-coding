"""Abstract VectorIndex interface.

The indexer and retrieval layers ONLY depend on this interface.
Swapping sqlite-vec for LanceDB/Qdrant only requires a new implementation.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class Chunk:
    """A single chunk of text with its embedding and provenance metadata."""

    chunk_id: str
    document_id: str
    source: str          # relative path from KB root (e.g. "01-projects/adr/README.md")
    chunk_index: int
    content: str
    content_hash: str
    embedding: list[float]
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class SearchResult:
    """A retrieved chunk with its similarity score."""

    chunk_id: str
    document_id: str
    source: str
    chunk_index: int
    content: str
    metadata: dict[str, Any]
    score: float         # cosine similarity (higher = more similar)


@dataclass
class IndexStats:
    """Statistics for a single model index."""

    document_count: int
    chunk_count: int
    dimensions: int
    last_indexed_at: str | None  # ISO timestamp or None if empty


@dataclass
class DocumentStatus:
    """Tracking record for a single source document."""

    document_id: str
    source: str
    file_hash: str
    chunk_count: int
    indexed_at: str   # ISO timestamp


class VectorIndex(ABC):
    """Abstract vector index interface."""

    @abstractmethod
    def initialize(self, dimensions: int) -> None:
        """Create the index schema. Safe to call multiple times (idempotent)."""
        ...

    @abstractmethod
    def add(self, chunks: list[Chunk]) -> None:
        """Insert chunks into the index. Caller must delete old chunks first."""
        ...

    @abstractmethod
    def delete_by_document(self, document_id: str) -> int:
        """Delete all chunks for a document. Returns number of chunks deleted."""
        ...

    @abstractmethod
    def search(self, query_vector: list[float], limit: int = 8) -> list[SearchResult]:
        """Return top-K most similar chunks to the query vector."""
        ...

    @abstractmethod
    def get_document_status(self, source: str) -> DocumentStatus | None:
        """Return tracking record for a source path, or None if not indexed."""
        ...

    @abstractmethod
    def upsert_document_status(self, status: DocumentStatus) -> None:
        """Insert or update a document tracking record."""
        ...

    @abstractmethod
    def delete_document_status(self, document_id: str) -> None:
        """Remove a document tracking record."""
        ...

    @abstractmethod
    def get_stats(self) -> IndexStats:
        """Return aggregate statistics for this index."""
        ...

    @abstractmethod
    def get_index_path(self) -> Path:
        """Return the filesystem path of the index database file."""
        ...

    @abstractmethod
    def clear(self) -> None:
        """Delete all data from the index (used by rebuild)."""
        ...
