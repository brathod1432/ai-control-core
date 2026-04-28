from __future__ import annotations

import json
import unittest
from unittest import mock

from jarvis.config import RuntimeConfig, JarvisConfig
from jarvis.contracts import ChatMessage, ModelRequest
from jarvis.model_runtime import ModelClient, create_model_client
from jarvis.model_runtime.base import ModelRuntimeError


class ModelRuntimeTests(unittest.TestCase):
    def test_create_model_client_returns_model_client(self) -> None:
        client = create_model_client(
            JarvisConfig(
                runtime=RuntimeConfig(
                    default_model="qwen-local",
                    base_url="http://127.0.0.1:11434",
                    chat_endpoint="/api/chat",
                    temperature=0.2,
                    max_tokens=512,
                )
            )
        )

        self.assertIsInstance(client, ModelClient)

    @mock.patch("jarvis.model_runtime.ollama.urllib.request.urlopen")
    def test_chat_posts_ollama_payload_and_returns_content(
        self,
        urlopen: mock.Mock,
    ) -> None:
        response = mock.Mock()
        response.read.return_value = json.dumps(
            {"message": {"role": "assistant", "content": "Hello from local Jarvis."}}
        ).encode("utf-8")
        response.__enter__ = mock.Mock(return_value=response)
        response.__exit__ = mock.Mock(return_value=None)
        urlopen.return_value = response
        client = create_model_client(
            JarvisConfig(
                runtime=RuntimeConfig(
                    default_model="qwen-local",
                    base_url="http://127.0.0.1:11434",
                    chat_endpoint="/api/chat",
                    temperature=0.2,
                    max_tokens=1024,
                )
            )
        )

        result = client.chat(
            ModelRequest(
                messages=[ChatMessage(role="user", content="Hi")],
                model="qwen-coder-local",
                temperature=0.1,
                max_tokens=256,
            )
        )

        self.assertEqual(result.content, "Hello from local Jarvis.")
        request = urlopen.call_args.args[0]
        self.assertEqual(request.full_url, "http://127.0.0.1:11434/api/chat")
        self.assertEqual(urlopen.call_args.kwargs["timeout"], 120.0)
        payload = json.loads(request.data.decode("utf-8"))
        self.assertEqual(payload["model"], "qwen-coder-local")
        self.assertEqual(payload["messages"], [{"role": "user", "content": "Hi"}])
        self.assertFalse(payload["stream"])
        self.assertEqual(payload["options"]["temperature"], 0.1)
        self.assertEqual(payload["options"]["num_predict"], 256)

    @mock.patch("jarvis.model_runtime.ollama.urllib.request.urlopen")
    def test_chat_uses_default_model_when_request_model_empty(
        self,
        urlopen: mock.Mock,
    ) -> None:
        response = mock.Mock()
        response.read.return_value = b'{"response": "fallback content"}'
        response.__enter__ = mock.Mock(return_value=response)
        response.__exit__ = mock.Mock(return_value=None)
        urlopen.return_value = response
        client = create_model_client(JarvisConfig(runtime=RuntimeConfig()))

        result = client.chat(
            ModelRequest(
                messages=[ChatMessage(role="user", content="Hi")],
                model="",
            )
        )

        self.assertEqual(result.content, "fallback content")
        request = urlopen.call_args.args[0]
        payload = json.loads(request.data.decode("utf-8"))
        self.assertEqual(payload["model"], "qwen-local")

    def test_chat_rejects_empty_messages_without_network_call(self) -> None:
        client = create_model_client(JarvisConfig(runtime=RuntimeConfig()))

        with mock.patch("jarvis.model_runtime.ollama.urllib.request.urlopen") as urlopen:
            with self.assertRaisesRegex(ValueError, "messages"):
                client.chat(ModelRequest(messages=[], model="qwen-local"))

        urlopen.assert_not_called()

    @mock.patch("jarvis.model_runtime.ollama.urllib.request.urlopen")
    def test_chat_wraps_transport_errors(self, urlopen: mock.Mock) -> None:
        urlopen.side_effect = OSError("connection refused")
        client = create_model_client(JarvisConfig(runtime=RuntimeConfig()))

        with self.assertRaises(ModelRuntimeError):
            client.chat(
                ModelRequest(
                    messages=[ChatMessage(role="user", content="Hi")],
                    model="qwen-local",
                )
            )


if __name__ == "__main__":
    unittest.main()

