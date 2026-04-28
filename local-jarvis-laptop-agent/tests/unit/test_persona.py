from __future__ import annotations

import unittest

from jarvis.persona import JarvisPersona, build_system_prompt


class PersonaTests(unittest.TestCase):
    def test_system_prompt_names_jarvis_and_local_model(self) -> None:
        prompt = build_system_prompt(
            model_name="qwen2.5:3b",
            base_url="http://127.0.0.1:11434",
        )

        self.assertIn("You are Jarvis", prompt)
        self.assertIn("qwen2.5:3b", prompt)
        self.assertIn("http://127.0.0.1:11434", prompt)
        self.assertIn("privacy", prompt)
        self.assertIn("simulated conversational stance", prompt)
        self.assertIn("must not claim sentience", prompt)
        self.assertIn("Never claim to have inspected", prompt)
        self.assertIn("Use only the configured local Ollama model", prompt)
        self.assertIn("Do not claim abilities that are not implemented", prompt)
        self.assertIn("inspect explicitly scoped local files read-only", prompt)
        self.assertIn("cannot set alarms", prompt)

    def test_custom_persona_can_keep_jarvis_identity(self) -> None:
        prompt = build_system_prompt(persona=JarvisPersona(name="Jarvis"))

        self.assertIn("Your name is Jarvis", prompt)


if __name__ == "__main__":
    unittest.main()
