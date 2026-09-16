"""Chunker — splits ParsedDocument sections into embedding-ready chunks.

Chunking is treated as part of the index identity.
The version string is stored in metadata.json and the index directory name.

Strategy: markdown_headers
  1. Each section (split at headings) becomes the base unit.
  2. If a section exceeds chunk_size tokens, it is further split by token count
     with chunk_overlap token overlap.
  3. Context: each chunk is prefixed with the document title and heading path
     so the LLM has navigational context even without the surrounding content.
"""

from __future__ import annotations

import hashlib
import re
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import tiktoken

from .parser import ParsedDocument, Section


@dataclass
class ChunkConfig:
    version: str = "v1"
    strategy: str = "markdown_headers"
    chunk_size: int = 512           # target tokens
    chunk_overlap: int = 64         # overlap tokens
    min_chunk_size: int = 50        # discard chunks smaller than this (tokens)


@dataclass
class RawChunk:
    """A text chunk ready for embedding — no vector yet."""

    chunk_id: str
    document_id: str
    source: str
    chunk_index: int
    content: str          # text sent to the embedding model
    content_hash: str
    metadata: dict[str, Any]


_TOKENIZER = tiktoken.get_encoding("cl100k_base")  # works for both OpenAI and Gemini approx


def _count_tokens(text: str) -> int:
    return len(_TOKENIZER.encode(text))


def _split_by_tokens(
    text: str,
    chunk_size: int,
    chunk_overlap: int,
) -> list[str]:
    """Split text into token-sized chunks with overlap."""
    tokens = _TOKENIZER.encode(text)
    chunks: list[str] = []
    start = 0
    while start < len(tokens):
        end = min(start + chunk_size, len(tokens))
        chunk_tokens = tokens[start:end]
        chunks.append(_TOKENIZER.decode(chunk_tokens))
        if end == len(tokens):
            break
        start += chunk_size - chunk_overlap
    return chunks


def _make_context_prefix(source: str, section: Section) -> str:
    """Build a concise context prefix for a chunk.

    Format: "File: <source> | Section: <path> > <title>"
    This gives the LLM navigational context in RAG responses.
    """
    filename = Path(source).stem.replace("-", " ").replace("_", " ").title()
    parts = [filename]

    if section.heading_path:
        parts.append(" > ".join(section.heading_path))
    if section.title and section.title not in ("Introduction", "Document"):
        parts.append(section.title)

    return f"[{' > '.join(parts)}]\n\n"


def chunk_document(
    doc: ParsedDocument,
    document_id: str,
    config: ChunkConfig,
) -> list[RawChunk]:
    """Split a ParsedDocument into RawChunks ready for embedding.

    Each chunk includes a context prefix with the document path and section hierarchy.
    """
    raw_chunks: list[RawChunk] = []
    chunk_index = 0

    for section in doc.sections:
        prefix = _make_context_prefix(doc.source, section)
        section_text = section.content.strip()

        if not section_text:
            # Empty section — include at least the heading as a chunk
            section_text = section.title

        full_text = prefix + section_text
        token_count = _count_tokens(full_text)

        if token_count <= config.chunk_size:
            # Section fits in one chunk
            if _count_tokens(section_text) >= config.min_chunk_size:
                raw_chunks.append(
                    _make_raw_chunk(
                        full_text, doc, document_id, chunk_index, section
                    )
                )
                chunk_index += 1
        else:
            # Section is too large — split by tokens with overlap
            sub_chunks = _split_by_tokens(
                section_text, config.chunk_size, config.chunk_overlap
            )
            for sub_text in sub_chunks:
                if _count_tokens(sub_text) < config.min_chunk_size:
                    continue
                content = prefix + sub_text
                raw_chunks.append(
                    _make_raw_chunk(
                        content, doc, document_id, chunk_index, section
                    )
                )
                chunk_index += 1

    return raw_chunks


def _make_raw_chunk(
    content: str,
    doc: ParsedDocument,
    document_id: str,
    chunk_index: int,
    section: Section,
) -> RawChunk:
    content_hash = hashlib.sha256(content.encode()).hexdigest()
    chunk_id = str(uuid.uuid5(uuid.NAMESPACE_URL, f"{document_id}::{chunk_index}::{content_hash}"))

    metadata: dict[str, Any] = {
        "section_title": section.title,
        "section_level": section.level,
        "heading_path": section.heading_path,
    }
    if doc.front_matter:
        metadata["front_matter"] = doc.front_matter

    return RawChunk(
        chunk_id=chunk_id,
        document_id=document_id,
        source=doc.source,
        chunk_index=chunk_index,
        content=content,
        content_hash=content_hash,
        metadata=metadata,
    )
