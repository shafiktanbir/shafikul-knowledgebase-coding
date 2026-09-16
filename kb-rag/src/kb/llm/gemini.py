"""Google Gemini LLM provider for the RAG answer generation step.

Uses google-genai SDK v2. Auth is the same as GeminiEmbeddingProvider:
GEMINI_API_KEY env → GOOGLE_API_KEY env → Application Default Credentials.

This provider is completely independent of the embedding model.
You can switch from gemini-flash to gemini-pro without touching the index.
"""

from __future__ import annotations

import os

from google import genai
from google.genai import types as genai_types

from .provider import LLMProvider


class GeminiLLMProvider(LLMProvider):
    """LLM provider using Google Gemini Flash or Pro."""

    def __init__(
        self,
        model: str = "gemini-1.5-flash-latest",
        temperature: float = 0.2,
        max_tokens: int = 2048,
    ) -> None:
        self._model = model
        self._temperature = temperature
        self._max_tokens = max_tokens

        api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
        try:
            if api_key:
                self._client = genai.Client(api_key=api_key)
            else:
                self._client = genai.Client()
        except Exception as exc:
            raise EnvironmentError(
                "Gemini API key is required for LLM generation.\n"
                "Please add your free GEMINI_API_KEY to kb-rag/.env or export it in your shell:\n"
                "  export GEMINI_API_KEY=\"AIzaSy...\"\n"
                "You can get a free key at: https://aistudio.google.com/apikey"
            ) from exc

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        """Generate a response using Gemini."""
        full_prompt = f"{system_prompt}\n\n{user_prompt}"

        response = self._client.models.generate_content(
            model=self._model,
            contents=full_prompt,
            config=genai_types.GenerateContentConfig(
                temperature=self._temperature,
                max_output_tokens=self._max_tokens,
            ),
        )
        return response.text or ""

    def get_model_name(self) -> str:
        return self._model
