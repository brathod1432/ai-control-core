"""Model runtime client factory for Local Jarvis."""

from __future__ import annotations

from jarvis.config import JarvisConfig

from .base import ModelClient, ModelRuntimeError
from .ollama import OllamaModelClient


def create_model_client(config: JarvisConfig) -> ModelClient:
    """Create a model client from validated Jarvis configuration."""

    if config.runtime.provider != "ollama":
        raise ValueError("Only the 'ollama' runtime provider is supported.")
    return OllamaModelClient(
        base_url=config.runtime.base_url,
        chat_endpoint=config.runtime.chat_endpoint,
        default_model=config.runtime.default_model,
        temperature=config.runtime.temperature,
        max_tokens=config.runtime.max_tokens,
    )


__all__ = [
    "ModelClient",
    "ModelRuntimeError",
    "OllamaModelClient",
    "create_model_client",
]

