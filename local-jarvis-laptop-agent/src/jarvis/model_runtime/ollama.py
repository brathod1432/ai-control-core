"""Ollama-style loopback model client."""

from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any
import urllib.error
import urllib.request

from jarvis.contracts import ModelRequest, ModelResponse

from .base import ModelClient, ModelRuntimeError


@dataclass(frozen=True)
class OllamaModelClient(ModelClient):
    base_url: str
    chat_endpoint: str
    default_model: str
    temperature: float = 0.2
    max_tokens: int | None = None
    timeout_seconds: float = 120.0

    def chat(self, request: ModelRequest) -> ModelResponse:
        self._validate_request(request)
        payload = self._payload(request)
        http_request = urllib.request.Request(
            self._chat_url(),
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urllib.request.urlopen(
                http_request,
                timeout=self.timeout_seconds,
            ) as response:
                response_body = response.read().decode("utf-8")
        except urllib.error.URLError as exc:
            raise ModelRuntimeError("Local model endpoint is not reachable.") from exc
        except OSError as exc:
            raise ModelRuntimeError("Unable to communicate with local model endpoint.") from exc

        try:
            parsed_body = json.loads(response_body)
        except json.JSONDecodeError as exc:
            raise ModelRuntimeError("Local model endpoint returned invalid JSON.") from exc
        if not isinstance(parsed_body, dict):
            raise ModelRuntimeError("Local model endpoint returned an invalid response.")

        return ModelResponse(content=_extract_content(parsed_body), raw=parsed_body)

    def _payload(self, request: ModelRequest) -> dict[str, Any]:
        options: dict[str, Any] = {"temperature": request.temperature}
        if request.max_tokens is not None:
            options["num_predict"] = request.max_tokens

        return {
            "model": request.model or self.default_model,
            "messages": [message.to_dict() for message in request.messages],
            "stream": False,
            "options": options,
        }

    def _chat_url(self) -> str:
        return f"{self.base_url.rstrip('/')}{self.chat_endpoint}"

    def _validate_request(self, request: ModelRequest) -> None:
        if not request.messages:
            raise ValueError("ModelRequest.messages must not be empty.")
        if not request.model and not self.default_model:
            raise ValueError("ModelRequest.model must not be empty.")
        if not 0.0 <= request.temperature <= 2.0:
            raise ValueError("ModelRequest.temperature must be between 0.0 and 2.0.")
        if request.max_tokens is not None and request.max_tokens <= 0:
            raise ValueError("ModelRequest.max_tokens must be positive when set.")
        for message in request.messages:
            if not message.role.strip():
                raise ValueError("ChatMessage.role must not be empty.")
            if not isinstance(message.content, str):
                raise ValueError("ChatMessage.content must be a string.")


def _extract_content(response: dict[str, Any]) -> str:
    message = response.get("message")
    if isinstance(message, dict) and isinstance(message.get("content"), str):
        return message["content"]
    if isinstance(response.get("response"), str):
        return response["response"]
    raise ModelRuntimeError("Local model endpoint response did not include content.")

