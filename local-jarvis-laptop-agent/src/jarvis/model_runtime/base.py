"""Shared model runtime contracts."""

from __future__ import annotations

from abc import ABC, abstractmethod

from jarvis.contracts import ModelRequest, ModelResponse


class ModelRuntimeError(RuntimeError):
    """Raised when a local model runtime cannot complete a request."""


class ModelClient(ABC):
    """Abstract model client used by the Jarvis orchestration layer."""

    @abstractmethod
    def chat(self, request: ModelRequest) -> ModelResponse:
        """Send a chat request to the configured local model runtime."""

