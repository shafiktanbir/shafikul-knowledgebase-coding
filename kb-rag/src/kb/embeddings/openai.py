"""OpenAI embedding provider.

Secondary provider — included for portability. Not used by default.
Requires OPENAI_API_KEY environment variable.
"""

from __future__ import annotations

import os
import time
from typing import TYPE_CHECKING

from .provider import EmbeddingProvider

if TYPE_CHECKING:
    pass


class OpenAIEmbeddingProvider(EmbeddingProvider):
    """Embedding provider using OpenAI text-embedding-3-small/large."""

    _BATCH_SIZE = 100
    _RETRY_ATTEMPTS = 3
    _RETRY_DELAY_SEC = 2.0

    def __init__(
        self,
        model: str = "text-embedding-3-small",
        dimensions: int = 1536,
    ) -> None:
        self._model = model
        self._dimensions = dimensions

        try:
            from openai import OpenAI  # noqa: PLC0415
        except ImportError as exc:
            raise ImportError("openai package not installed. Run: pip install openai") from exc

        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise EnvironmentError("OPENAI_API_KEY environment variable not set.")

        self._client = OpenAI(api_key=api_key)

    def embed(self, text: str) -> list[float]:
        return self.embed_batch([text])[0]

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        all_vectors: list[list[float]] = []
        for i in range(0, len(texts), self._BATCH_SIZE):
            batch = texts[i : i + self._BATCH_SIZE]
            vectors = self._embed_with_retry(batch)
            all_vectors.extend(vectors)
        return all_vectors

    def _embed_with_retry(self, texts: list[str]) -> list[list[float]]:
        last_exc: Exception | None = None
        for attempt in range(self._RETRY_ATTEMPTS):
            try:
                response = self._client.embeddings.create(
                    model=self._model,
                    input=texts,
                    dimensions=self._dimensions,
                )
                return [item.embedding for item in response.data]
            except Exception as exc:  # noqa: BLE001
                last_exc = exc
                if attempt < self._RETRY_ATTEMPTS - 1:
                    time.sleep(self._RETRY_DELAY_SEC * (attempt + 1))
        raise RuntimeError(f"OpenAI embedding failed: {last_exc}")

    def get_model_name(self) -> str:
        return self._model

    def get_dimensions(self) -> int:
        return self._dimensions

    def get_provider_name(self) -> str:
        return "openai"
