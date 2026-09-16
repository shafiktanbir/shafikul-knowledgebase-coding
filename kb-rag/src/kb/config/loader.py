"""Configuration loader for kb-rag.

Loads kb-config.yaml and resolves all paths relative to the config file location.
Supports optional .env file for API keys.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv


# The config file is expected to sit inside kb-rag/
_DEFAULT_CONFIG_NAME = "kb-config.yaml"


def _find_config() -> Path:
    """Walk up from the current directory to find kb-config.yaml."""
    # 1. Check env override
    env_path = os.environ.get("KB_CONFIG")
    if env_path:
        p = Path(env_path)
        if p.exists():
            return p
        raise FileNotFoundError(f"KB_CONFIG env points to missing file: {env_path}")

    # 2. Walk up from CWD
    current = Path.cwd()
    for directory in [current, *current.parents]:
        candidate = directory / "kb-rag" / _DEFAULT_CONFIG_NAME
        if candidate.exists():
            return candidate
        candidate2 = directory / _DEFAULT_CONFIG_NAME
        if candidate2.exists():
            return candidate2

    raise FileNotFoundError(
        f"Could not find {_DEFAULT_CONFIG_NAME}. "
        "Run from inside the knowledgebase/ directory or set KB_CONFIG env var."
    )


class Config:
    """Parsed and resolved configuration."""

    def __init__(self, raw: dict[str, Any], config_path: Path) -> None:
        self._raw = raw
        self.config_dir = config_path.parent  # kb-rag/

        # Resolve paths relative to config file location
        kb_raw = raw.get("knowledge_base_path", "../")
        self.knowledge_base_path: Path = (self.config_dir / kb_raw).resolve()

        idx_raw = raw.get("indexes_path", "../.ai/indexes")
        self.indexes_path: Path = (self.config_dir / idx_raw).resolve()

        self.exclude_patterns: list[str] = raw.get("exclude_patterns", [])
        self.embedding_models: dict[str, Any] = raw.get("embedding_models", {})
        self.chunking: dict[str, Any] = raw.get("chunking", {})
        self.llm: dict[str, Any] = raw.get("llm", {})
        self.retrieval: dict[str, Any] = raw.get("retrieval", {})

    def get_model_config(self, alias: str) -> dict[str, Any]:
        """Return the embedding model config for the given alias.

        Raises KeyError if alias is not found.
        """
        if alias not in self.embedding_models:
            available = ", ".join(self.embedding_models.keys())
            raise KeyError(
                f"Embedding model alias '{alias}' not found in config. "
                f"Available: {available}"
            )
        return self.embedding_models[alias]

    def get_index_dir(self, model_alias: str) -> Path:
        """Return the index directory for the given model alias + chunking version."""
        model_cfg = self.get_model_config(model_alias)
        model_name: str = model_cfg["model"]
        chunking_version: str = self.chunking.get("version", "v1")
        return self.indexes_path / model_name / f"chunking-{chunking_version}"

    @property
    def chunking_version(self) -> str:
        return self.chunking.get("version", "v1")


def load_config() -> Config:
    """Find, load, and return the resolved Config object."""
    config_path = _find_config()

    # Load .env from kb-rag directory if present
    env_file = config_path.parent / ".env"
    if env_file.exists():
        load_dotenv(env_file)

    with open(config_path) as f:
        raw = yaml.safe_load(f)

    return Config(raw, config_path)
