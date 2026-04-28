from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from jarvis.config import ConfigError, JarvisConfig, load_config


class LoadConfigTests(unittest.TestCase):
    def test_load_config_without_path_uses_safe_defaults(self) -> None:
        config = load_config()

        self.assertIsInstance(config, JarvisConfig)
        self.assertEqual(config.runtime.default_model, "qwen-local")
        self.assertEqual(config.runtime.base_url, "http://127.0.0.1:11434")
        self.assertEqual(config.runtime.chat_endpoint, "/api/chat")
        self.assertEqual(config.runtime.temperature, 0.2)
        self.assertIsNone(config.runtime.max_tokens)
        self.assertIn(".local-jarvis", config.storage.log_dir)
        self.assertEqual(config.conversation.max_messages, 40)

    def test_load_config_reads_runtime_values(self) -> None:
        raw_config = {
            "runtime": {
                "provider": "ollama",
                "base_url": "http://localhost:11434/",
                "chat_endpoint": "/api/chat",
                "default_model": "qwen-coder-local",
                "temperature": 0.1,
                "max_tokens": 2048,
            },
            "storage": {"log_dir": "./logs"},
            "conversation": {"max_messages": 12},
            "ignored": {"value": True},
        }

        config = self._load_from_temp_file(raw_config)

        self.assertEqual(config.runtime.default_model, "qwen-coder-local")
        self.assertEqual(config.runtime.base_url, "http://localhost:11434")
        self.assertEqual(config.runtime.chat_endpoint, "/api/chat")
        self.assertEqual(config.runtime.temperature, 0.1)
        self.assertEqual(config.runtime.max_tokens, 2048)
        self.assertTrue(config.storage.log_dir.endswith("logs"))
        self.assertEqual(config.conversation.max_messages, 12)

    def test_load_config_rejects_non_loopback_base_url(self) -> None:
        with self.assertRaisesRegex(ConfigError, "loopback"):
            self._load_from_temp_file(
                {"runtime": {"base_url": "https://models.example.test:11434"}}
            )

    def test_load_config_rejects_invalid_temperature(self) -> None:
        with self.assertRaisesRegex(ConfigError, "temperature"):
            self._load_from_temp_file({"runtime": {"temperature": 3.0}})

    def test_load_config_rejects_remote_chat_endpoint(self) -> None:
        with self.assertRaisesRegex(ConfigError, "start with"):
            self._load_from_temp_file(
                {"runtime": {"chat_endpoint": "https://example.test/api/chat"}}
            )

    def test_load_config_rejects_invalid_storage_and_conversation(self) -> None:
        with self.assertRaisesRegex(ConfigError, "storage"):
            self._load_from_temp_file({"storage": []})
        with self.assertRaisesRegex(ConfigError, "max_messages"):
            self._load_from_temp_file({"conversation": {"max_messages": 2}})

    def _load_from_temp_file(self, raw_config: dict[str, object]) -> JarvisConfig:
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "jarvis.local.json"
            config_path.write_text(json.dumps(raw_config), encoding="utf-8")
            return load_config(str(config_path))


if __name__ == "__main__":
    unittest.main()
