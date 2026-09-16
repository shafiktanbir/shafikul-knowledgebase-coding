"""Metadata storage — reads/writes metadata.json for each model index.

metadata.json sits alongside index.db and records:
- embedding provider, model, dimensions, distance metric
- chunking configuration version
- index version and creation timestamp

This file is the index's "passport" — it lets you verify an index is valid
before querying it, and lets you copy the directory to another machine.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


METADATA_FILENAME = "metadata.json"


def read_metadata(index_dir: Path) -> dict[str, Any] | None:
    """Read metadata.json from index_dir. Returns None if not found."""
    path = index_dir / METADATA_FILENAME
    if not path.exists():
        return None
    with open(path) as f:
        return json.load(f)


def write_metadata(
    index_dir: Path,
    provider: str,
    model: str,
    dimensions: int,
    chunking_version: str,
    distance_metric: str = "cosine",
    index_version: int = 1,
) -> None:
    """Write metadata.json to index_dir."""
    index_dir.mkdir(parents=True, exist_ok=True)
    metadata: dict[str, Any] = {
        "embedding_provider": provider,
        "embedding_model": model,
        "dimensions": dimensions,
        "distance_metric": distance_metric,
        "chunking_version": chunking_version,
        "index_version": index_version,
        "created_at": datetime.now(UTC).isoformat(),
    }
    path = index_dir / METADATA_FILENAME
    with open(path, "w") as f:
        json.dump(metadata, f, indent=2)
