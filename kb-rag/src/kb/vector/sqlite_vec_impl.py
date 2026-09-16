"""SQLite + sqlite-vec implementation of VectorIndex.

Schema design:
  - documents table: tracks source files (hash, timestamps, chunk count)
  - chunks table: stores text content and metadata
  - vec_chunks virtual table: sqlite-vec index for cosine similarity search

The index is a single .db file — fully portable, no server required.
"""

from __future__ import annotations

import json
import sqlite3
import struct
from datetime import UTC, datetime
from pathlib import Path

import sqlite_vec

from .index import (
    Chunk,
    DocumentStatus,
    IndexStats,
    SearchResult,
    VectorIndex,
)


def _serialize_float32(vector: list[float]) -> bytes:
    """Pack a list of floats into a little-endian binary blob for sqlite-vec."""
    return struct.pack(f"{len(vector)}f", *vector)


class SQLiteVecIndex(VectorIndex):
    """SQLite + sqlite-vec vector index implementation.

    Each instance corresponds to one .db file at a specific path.
    Thread safety: sqlite connections are not thread-safe; create one
    instance per thread if needed.
    """

    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path
        self._conn: sqlite3.Connection | None = None
        self._dimensions: int | None = None

    def _get_conn(self) -> sqlite3.Connection:
        if self._conn is None:
            self._db_path.parent.mkdir(parents=True, exist_ok=True)
            conn = sqlite3.connect(str(self._db_path))
            conn.enable_load_extension(True)
            sqlite_vec.load(conn)
            conn.enable_load_extension(False)
            conn.row_factory = sqlite3.Row
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA synchronous=NORMAL")
            self._conn = conn
        return self._conn

    def initialize(self, dimensions: int) -> None:
        """Create all tables. Safe to call multiple times (idempotent via IF NOT EXISTS)."""
        self._dimensions = dimensions
        conn = self._get_conn()

        conn.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                document_id   TEXT PRIMARY KEY,
                source        TEXT NOT NULL UNIQUE,
                file_hash     TEXT NOT NULL,
                chunk_count   INTEGER NOT NULL DEFAULT 0,
                indexed_at    TEXT NOT NULL
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS chunks (
                chunk_id      TEXT PRIMARY KEY,
                document_id   TEXT NOT NULL REFERENCES documents(document_id) ON DELETE CASCADE,
                source        TEXT NOT NULL,
                chunk_index   INTEGER NOT NULL,
                content       TEXT NOT NULL,
                content_hash  TEXT NOT NULL,
                metadata_json TEXT NOT NULL DEFAULT '{}'
            )
        """)

        conn.execute(f"""
            CREATE VIRTUAL TABLE IF NOT EXISTS vec_chunks USING vec0(
                chunk_id TEXT PRIMARY KEY,
                embedding FLOAT[{dimensions}]
            )
        """)

        conn.execute("CREATE INDEX IF NOT EXISTS idx_chunks_document ON chunks(document_id)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_chunks_source ON chunks(source)")
        conn.commit()

    def add(self, chunks: list[Chunk]) -> None:
        """Insert chunks into both the metadata table and the vector index."""
        if not chunks:
            return

        conn = self._get_conn()
        now = datetime.now(UTC).isoformat()

        chunk_rows = [
            (
                c.chunk_id,
                c.document_id,
                c.source,
                c.chunk_index,
                c.content,
                c.content_hash,
                json.dumps(c.metadata),
            )
            for c in chunks
        ]
        conn.executemany(
            """INSERT OR REPLACE INTO chunks
               (chunk_id, document_id, source, chunk_index, content, content_hash, metadata_json)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            chunk_rows,
        )

        vec_rows = [
            (c.chunk_id, _serialize_float32(c.embedding))
            for c in chunks
        ]
        conn.executemany(
            "INSERT OR REPLACE INTO vec_chunks (chunk_id, embedding) VALUES (?, ?)",
            vec_rows,
        )

        conn.commit()

    def delete_by_document(self, document_id: str) -> int:
        """Delete all chunks for a document from both tables."""
        conn = self._get_conn()

        # Get chunk IDs to delete from vec table
        rows = conn.execute(
            "SELECT chunk_id FROM chunks WHERE document_id = ?", (document_id,)
        ).fetchall()
        chunk_ids = [r["chunk_id"] for r in rows]

        if chunk_ids:
            placeholders = ",".join("?" * len(chunk_ids))
            conn.execute(f"DELETE FROM vec_chunks WHERE chunk_id IN ({placeholders})", chunk_ids)
            conn.execute("DELETE FROM chunks WHERE document_id = ?", (document_id,))

        conn.commit()
        return len(chunk_ids)

    def search(self, query_vector: list[float], limit: int = 8) -> list[SearchResult]:
        """Cosine similarity search using sqlite-vec KNN query."""
        conn = self._get_conn()
        query_blob = _serialize_float32(query_vector)

        rows = conn.execute(
            """
            SELECT
                c.chunk_id,
                c.document_id,
                c.source,
                c.chunk_index,
                c.content,
                c.metadata_json,
                v.distance
            FROM vec_chunks v
            JOIN chunks c ON v.chunk_id = c.chunk_id
            WHERE v.embedding MATCH ?
              AND k = ?
            ORDER BY v.distance
            """,
            (query_blob, limit),
        ).fetchall()

        results = []
        for row in rows:
            # sqlite-vec returns L2 distance by default; convert to similarity score
            # For cosine distance: similarity = 1 - distance
            distance = row["distance"]
            score = max(0.0, 1.0 - distance)

            results.append(
                SearchResult(
                    chunk_id=row["chunk_id"],
                    document_id=row["document_id"],
                    source=row["source"],
                    chunk_index=row["chunk_index"],
                    content=row["content"],
                    metadata=json.loads(row["metadata_json"]),
                    score=score,
                )
            )
        return results

    def get_document_status(self, source: str) -> DocumentStatus | None:
        conn = self._get_conn()
        row = conn.execute(
            "SELECT * FROM documents WHERE source = ?", (source,)
        ).fetchone()
        if row is None:
            return None
        return DocumentStatus(
            document_id=row["document_id"],
            source=row["source"],
            file_hash=row["file_hash"],
            chunk_count=row["chunk_count"],
            indexed_at=row["indexed_at"],
        )

    def upsert_document_status(self, status: DocumentStatus) -> None:
        conn = self._get_conn()
        conn.execute(
            """INSERT OR REPLACE INTO documents
               (document_id, source, file_hash, chunk_count, indexed_at)
               VALUES (?, ?, ?, ?, ?)""",
            (
                status.document_id,
                status.source,
                status.file_hash,
                status.chunk_count,
                status.indexed_at,
            ),
        )
        conn.commit()

    def delete_document_status(self, document_id: str) -> None:
        conn = self._get_conn()
        conn.execute("DELETE FROM documents WHERE document_id = ?", (document_id,))
        conn.commit()

    def get_stats(self) -> IndexStats:
        conn = self._get_conn()
        doc_count = conn.execute("SELECT COUNT(*) FROM documents").fetchone()[0]
        chunk_count = conn.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]

        last_row = conn.execute(
            "SELECT indexed_at FROM documents ORDER BY indexed_at DESC LIMIT 1"
        ).fetchone()
        last_indexed = last_row[0] if last_row else None

        dims = self._dimensions or self._detect_dimensions(conn)

        return IndexStats(
            document_count=doc_count,
            chunk_count=chunk_count,
            dimensions=dims,
            last_indexed_at=last_indexed,
        )

    def _detect_dimensions(self, conn: sqlite3.Connection) -> int:
        """Try to detect dimensions from stored vectors."""
        try:
            row = conn.execute("SELECT embedding FROM vec_chunks LIMIT 1").fetchone()
            if row and row[0]:
                return len(struct.unpack(f"{len(row[0]) // 4}f", row[0]))
        except Exception:  # noqa: BLE001
            pass
        return 0

    def get_index_path(self) -> Path:
        return self._db_path

    def clear(self) -> None:
        """Delete all data — used by rebuild command."""
        conn = self._get_conn()
        conn.execute("DELETE FROM vec_chunks")
        conn.execute("DELETE FROM chunks")
        conn.execute("DELETE FROM documents")
        conn.commit()

    def close(self) -> None:
        if self._conn:
            self._conn.close()
            self._conn = None

    def __enter__(self) -> "SQLiteVecIndex":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()
