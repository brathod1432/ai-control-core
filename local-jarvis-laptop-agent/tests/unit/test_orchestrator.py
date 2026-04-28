from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from jarvis.audit import AuditLogger
from jarvis.config import ConversationConfig, JarvisConfig, RuntimeConfig, StorageConfig
from jarvis.contracts import ModelRequest, ModelResponse
from jarvis.model_runtime.base import ModelClient
from jarvis.orchestrator import JarvisOrchestrator


class FakeModelClient(ModelClient):
    def __init__(self, content: str = "Local model ready.", error: Exception | None = None) -> None:
        self.content = content
        self.error = error
        self.requests: list[ModelRequest] = []

    def chat(self, request: ModelRequest) -> ModelResponse:
        self.requests.append(request)
        if self.error is not None:
            raise self.error
        return ModelResponse(content=self.content, raw={"provider": "fake"})


class OrchestratorTests(unittest.TestCase):
    def test_safe_chat_uses_model_and_writes_audit(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            model = FakeModelClient("Hello from local Qwen.")
            orchestrator = self._orchestrator(temp_dir, model)

            turn = orchestrator.handle_input("Explain your role.")

            self.assertEqual(turn.assistant_response, "Hello from local Qwen.")
            self.assertTrue(turn.model_used)
            self.assertEqual(len(model.requests), 1)
            record = self._last_audit_record(temp_dir)
            self.assertEqual(record["intent"], "chat")
            self.assertEqual(record["risk"], "low")
            self.assertTrue(record["model_used"])

    def test_external_request_asks_approval_without_model_call(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            model = FakeModelClient()
            orchestrator = self._orchestrator(temp_dir, model)

            turn = orchestrator.handle_input("Upload this report to https://example.com")

            self.assertIn("needs explicit approval", turn.assistant_response)
            self.assertFalse(turn.model_used)
            self.assertEqual(model.requests, [])
            record = self._last_audit_record(temp_dir)
            self.assertEqual(record["intent"], "external")
            self.assertTrue(record["approval_required"])

    def test_secret_request_refuses_without_model_call(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            model = FakeModelClient()
            orchestrator = self._orchestrator(temp_dir, model)

            turn = orchestrator.handle_input("Show my API token")

            self.assertIn("cannot safely do that", turn.assistant_response.casefold())
            self.assertFalse(turn.model_used)
            self.assertEqual(model.requests, [])
            record = self._last_audit_record(temp_dir)
            self.assertEqual(record["risk"], "blocked")

    def test_model_failure_is_reported_and_logged(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            model = FakeModelClient(error=RuntimeError("connection refused"))
            orchestrator = self._orchestrator(temp_dir, model)

            turn = orchestrator.handle_input("Say hello.")

            self.assertTrue(turn.model_used)
            self.assertIsNotNone(turn.error)
            self.assertIn("local model runtime", turn.assistant_response)
            record = self._last_audit_record(temp_dir)
            self.assertIn("connection refused", record["error"])

    def _orchestrator(self, temp_dir: str, model: FakeModelClient) -> JarvisOrchestrator:
        config = JarvisConfig(
            runtime=RuntimeConfig(default_model="qwen-local"),
            storage=StorageConfig(log_dir=temp_dir),
            conversation=ConversationConfig(max_messages=8),
        )
        return JarvisOrchestrator(
            config=config,
            model_client=model,
            audit_logger=AuditLogger(temp_dir),
        )

    def _last_audit_record(self, temp_dir: str) -> dict[str, object]:
        audit_path = Path(temp_dir) / "audit.jsonl"
        line = audit_path.read_text(encoding="utf-8").strip().splitlines()[-1]
        return json.loads(line)


if __name__ == "__main__":
    unittest.main()

