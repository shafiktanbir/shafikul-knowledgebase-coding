"""Indexer — orchestrates the full ingestion pipeline.

Flow:
    scan .md files
        ↓
    for each file:
        compute SHA-256 hash
        compare with stored hash
        if unchanged → skip
        if changed/new:
            delete old chunks
            parse + chunk
            embed chunks (batch)
            insert new chunks
            update document status
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Callable

from ..config.loader import Config
from ..embeddings import EmbeddingProvider
from ..ingestion.chunker import ChunkConfig, RawChunk, chunk_document
from ..ingestion.parser import parse_document
from ..ingestion.scanner import scan_markdown_files
from ..vector.index import Chunk, DocumentStatus, VectorIndex


@dataclass
class IndexResult:
    """Summary of an indexing run."""

    total_files: int
    indexed: int      # new or updated
    skipped: int      # unchanged
    deleted: int      # removed (file no longer exists)
    total_chunks: int
    errors: list[str]


def run_index(
    config: Config,
    index: VectorIndex,
    provider: EmbeddingProvider,
    model_alias: str,
    progress_callback: Callable[[str, str], None] | None = None,
) -> IndexResult:
    """Run incremental indexing.

    Args:
        config: Resolved Config object.
        index: VectorIndex to write into.
        provider: EmbeddingProvider configured for RETRIEVAL_DOCUMENT.
        model_alias: The alias from config (e.g. 'gemini').
        progress_callback: Optional fn(source, status) for progress reporting.

    Returns:
        IndexResult summary.
    """
    def _progress(source: str, status: str) -> None:
        if progress_callback:
            progress_callback(source, status)

    chunking_cfg = config.chunking
    chunk_config = ChunkConfig(
        version=chunking_cfg.get("version", "v1"),
        strategy=chunking_cfg.get("strategy", "markdown_headers"),
        chunk_size=chunking_cfg.get("chunk_size", 512),
        chunk_overlap=chunking_cfg.get("chunk_overlap", 64),
        min_chunk_size=chunking_cfg.get("min_chunk_size", 50),
    )

    model_cfg = config.get_model_config(model_alias)
    dimensions = provider.get_dimensions()

    # Initialize the index schema (idempotent)
    index.initialize(dimensions)

    # Scan for current .md files
    md_files = scan_markdown_files(config.knowledge_base_path, config.exclude_patterns)

    result = IndexResult(
        total_files=len(md_files),
        indexed=0,
        skipped=0,
        deleted=0,
        total_chunks=0,
        errors=[],
    )

    # Track processed sources so we can detect deleted files
    processed_sources: set[str] = set()

    for abs_path in md_files:
        source = str(abs_path.relative_to(config.knowledge_base_path)).replace("\\", "/")
        processed_sources.add(source)

        try:
            doc = parse_document(abs_path, config.knowledge_base_path)
            existing = index.get_document_status(source)

            if existing and existing.file_hash == doc.file_hash:
                _progress(source, "skip")
                result.skipped += 1
                continue

            # File is new or changed — reindex
            document_id = (
                existing.document_id
                if existing
                else str(uuid.uuid5(uuid.NAMESPACE_URL, source))
            )

            # Remove stale chunks
            if existing:
                index.delete_by_document(document_id)
                index.delete_document_status(document_id)

            # Chunk the document
            raw_chunks: list[RawChunk] = chunk_document(doc, document_id, chunk_config)

            if not raw_chunks:
                _progress(source, "empty")
                continue

            # Embed all chunks in one batch call
            texts = [c.content for c in raw_chunks]
            try:
                vectors = provider.embed_batch(texts)
            except Exception as exc:  # noqa: BLE001
                error_msg = f"Embedding error for {source}: {exc}"
                result.errors.append(error_msg)
                _progress(source, "error")
                continue

            # Build Chunk objects with embeddings
            chunks = [
                Chunk(
                    chunk_id=rc.chunk_id,
                    document_id=document_id,
                    source=rc.source,
                    chunk_index=rc.chunk_index,
                    content=rc.content,
                    content_hash=rc.content_hash,
                    embedding=vectors[i],
                    metadata=rc.metadata,
                )
                for i, rc in enumerate(raw_chunks)
            ]

            # Insert into vector index
            index.add(chunks)

            # Update document status
            index.upsert_document_status(
                DocumentStatus(
                    document_id=document_id,
                    source=source,
                    file_hash=doc.file_hash,
                    chunk_count=len(chunks),
                    indexed_at=datetime.now(UTC).isoformat(),
                )
            )

            result.indexed += 1
            result.total_chunks += len(chunks)
            _progress(source, "indexed")

        except Exception as exc:  # noqa: BLE001
            error_msg = f"Error processing {source}: {exc}"
            result.errors.append(error_msg)
            _progress(source, "error")

    return result
