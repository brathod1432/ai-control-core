from __future__ import annotations

import unittest

from jarvis.agents import AgentRegistry


class AgentRegistryTests(unittest.TestCase):
    def test_role_prompt_uses_single_shared_model(self) -> None:
        registry = AgentRegistry(model_name="qwen2.5:3b")

        prompt = registry.build_role_prompt("browser_inspector", "Inspect localhost.")

        self.assertIn("Agent role: browser_inspector", prompt)
        self.assertIn("Shared model: qwen2.5:3b", prompt)
        self.assertIn("Read-only by default", prompt)
        self.assertIn("No external browsing", prompt)

    def test_unknown_role_is_rejected(self) -> None:
        registry = AgentRegistry(model_name="qwen2.5:3b")

        with self.assertRaisesRegex(ValueError, "Unknown Jarvis agent role"):
            registry.build_role_prompt("cloud_worker", "Do something")


if __name__ == "__main__":
    unittest.main()
