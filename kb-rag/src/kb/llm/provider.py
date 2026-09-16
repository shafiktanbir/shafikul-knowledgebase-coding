"""Abstract LLMProvider interface.

The LLM is COMPLETELY decoupled from the embedding model.
Changing the LLM never requires rebuilding the vector index.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class LLMProvider(ABC):
    """Abstract LLM provider for the generation step in RAG."""

    @abstractmethod
    def generate(self, system_prompt: str, user_prompt: str) -> str:
        """Generate a response given a system + user prompt."""
        ...

    @abstractmethod
    def get_model_name(self) -> str:
        """Return the model identifier."""
        ...
