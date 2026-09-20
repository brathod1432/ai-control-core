from __future__ import annotations

import unittest
from pathlib import Path


class StartScriptTests(unittest.TestCase):
    def test_start_script_checks_local_ollama_and_qwen(self) -> None:
        root = Path(__file__).resolve().parents[2]
        script = (root / "start_jarvis.ps1").read_text(encoding="utf-8")

        self.assertIn("http://127.0.0.1:11434", script)
        self.assertIn("qwen2.5:3b", script)
        self.assertIn("/api/tags", script)
        self.assertIn("PYTHONPATH", script)
        self.assertIn("$ScriptRoot", script)
        self.assertIn("Push-Location $ScriptRoot", script)
        self.assertIn("python -m jarvis", script)
        self.assertIn("-StartOllama", script)


if __name__ == "__main__":
    unittest.main()
