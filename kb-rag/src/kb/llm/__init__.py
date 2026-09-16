"""LLM subpackage with factory function."""
from __future__ import annotations
from typing import Any

from .provider import LLMProvider


def build_llm_provider(llm_config: dict[str, Any]) -> LLMProvider:
    """Build a LLMProvider from the llm section of kb-config.yaml."""
    provider_name = llm_config.get("provider", "gemini").lower()
    model = llm_config.get("model", "gemini-1.5-flash-latest")
    temperature = float(llm_config.get("temperature", 0.2))
    max_tokens = int(llm_config.get("max_tokens", 2048))

    if provider_name == "gemini":
        from .gemini import GeminiLLMProvider  # noqa: PLC0415
        return GeminiLLMProvider(model=model, temperature=temperature, max_tokens=max_tokens)

    elif provider_name == "openai":
        from .openai_llm import OpenAILLMProvider  # noqa: PLC0415
        return OpenAILLMProvider(model=model, temperature=temperature, max_tokens=max_tokens)

    elif provider_name == "anthropic":
        from .anthropic_llm import AnthropicLLMProvider  # noqa: PLC0415
        return AnthropicLLMProvider(model=model, max_tokens=max_tokens)

    else:
        raise ValueError(f"Unknown LLM provider: '{provider_name}'. Supported: gemini, openai, anthropic")


__all__ = ["LLMProvider", "build_llm_provider"]
