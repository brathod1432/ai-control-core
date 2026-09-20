from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from jarvis.history import ConversationHistory


class ConversationHistoryTests(unittest.TestCase):
    def test_appends_transcript_jsonl_and_markdown(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            history = ConversationHistory(
                max_messages=6,
                transcript_dir=temp_dir,
                system_prompt="system prompt",
                session_id="test-session",
            )

            history.add_user("hello password=hunter2")
            history.add_assistant("hello back")

            jsonl_path = Path(temp_dir) / "test-session.jsonl"
            markdown_path = Path(temp_dir) / "test-session.md"
            records = [
                json.loads(line)
                for line in jsonl_path.read_text(encoding="utf-8").splitlines()
            ]

            self.assertEqual(records[0]["role"], "system")
            self.assertEqual(records[-2]["role"], "user")
            self.assertNotIn("hunter2", records[-2]["content"])
            self.assertIn("assistant", markdown_path.read_text(encoding="utf-8"))

    def test_history_compresses_context_when_it_grows(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            history = ConversationHistory(
                max_messages=5,
                transcript_dir=temp_dir,
                system_prompt="system prompt",
                session_id="test-session",
            )

            for index in range(8):
                history.add_user(f"user {index}")
                history.add_assistant(f"assistant {index}")

            context = history.context_messages()
            roles = [message.role for message in context]

            self.assertLessEqual(len(context), 5)
            self.assertEqual(context[0].role, "system")
            self.assertIn("agent", roles)
            self.assertIsNotNone(history.summary)

    def test_model_messages_map_agent_role_to_assistant_note(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            history = ConversationHistory(
                max_messages=6,
                transcript_dir=temp_dir,
                system_prompt="system prompt",
                session_id="test-session",
            )

            history.add_agent("handoff summary")

            model_messages = history.model_messages()
            self.assertEqual(model_messages[-1].role, "assistant")
            self.assertIn("[agent note]", model_messages[-1].content)


if __name__ == "__main__":
    unittest.main()
