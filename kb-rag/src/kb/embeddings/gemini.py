"""Google Gemini embedding provider.

Uses the google-genai SDK (v2+). Auth is resolved automatically:
1. GEMINI_API_KEY environment variable (set by user or Antigravity context)
2. GOOGLE_API_KEY environment variable
3. Application Default Credentials (ADC) via gcloud
"""

from __future__ import annotations

import os
import time

from google import genai
from google.genai import types as genai_types

from .provider import EmbeddingProvider


class GeminiEmbeddingProvider(EmbeddingProvider):
    """Embedding provider using Google Gemini text-embedding-004 (768 dims).

    The task_type distinguishes between index-time (RETRIEVAL_DOCUMENT) and
    query-time (RETRIEVAL_QUERY) embeddings, which improves retrieval quality.
    """

    _BATCH_SIZE = 100  # Gemini API batch limit
    _RETRY_ATTEMPTS = 3
    _RETRY_DELAY_SEC = 2.0

    def __init__(
        self,
        model: str = "text-embedding-004",
        dimensions: int = 768,
        task_type: str = "RETRIEVAL_DOCUMENT",
    ) -> None:
        self._model = model
        self._dimensions = dimensions
        self._task_type = task_type

        # Resolve API key: GEMINI_API_KEY > GOOGLE_API_KEY > ADC
        api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
        if api_key:
            self._client = genai.Client(api_key=api_key)
        else:
            # Use Application Default Credentials (Antigravity/gcloud)
            self._client = genai.Client()

    def embed(self, text: str) -> list[float]:
        """Embed a single text string."""
        return self.embed_batch([text])[0]

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Embed a list of texts in batches respecting the API limit."""
        all_vectors: list[list[float]] = []

        for i in range(0, len(texts), self._BATCH_SIZE):
            batch = texts[i : i + self._BATCH_SIZE]
            vectors = self._embed_batch_with_retry(batch)
            all_vectors.extend(vectors)

        return all_vectors

    def _embed_batch_with_retry(self, texts: list[str]) -> list[list[float]]:
        """Embed a batch with retry logic for transient API errors."""
        last_exc: Exception | None = None

        for attempt in range(self._RETRY_ATTEMPTS):
            try:
                response = self._client.models.embed_content(
                    model=f"models/{self._model}",
                    contents=texts,
                    config=genai_types.EmbedContentConfig(
                        task_type=self._task_type,
                        output_dimensionality=self._dimensions,
                    ),
                )
                return [list(emb.values) for emb in response.embeddings]
            except Exception as exc:  # noqa: BLE001
                last_exc = exc
                if attempt < self._RETRY_ATTEMPTS - 1:
                    time.sleep(self._RETRY_DELAY_SEC * (attempt + 1))

        raise RuntimeError(
            f"Gemini embedding failed after {self._RETRY_ATTEMPTS} attempts: {last_exc}"
        )

    def get_model_name(self) -> str:
        return self._model

    def get_dimensions(self) -> int:
        return self._dimensions

    def get_provider_name(self) -> str:
        return "gemini"

    def with_query_task_type(self, query_task_type: str = "RETRIEVAL_QUERY") -> "GeminiEmbeddingProvider":
        """Return a copy of this provider configured for query-time embedding."""
        return GeminiEmbeddingProvider(
            model=self._model,
            dimensions=self._dimensions,
            task_type=query_task_type,
        )
