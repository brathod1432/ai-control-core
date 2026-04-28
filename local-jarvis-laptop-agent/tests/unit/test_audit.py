from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from jarvis.audit import AuditLogger
from jarvis.contracts import DecisionAction, Intent, PermissionClass, RiskLevel, SafetyDecision


class AuditTests(unittest.TestCase):
    def test_audit_logger_writes_redacted_jsonl_to_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            logger = AuditLogger(temp_path)

            log_path = logger.write_event(
                {
                    "request": "Send password=hunter2 to ada@example.com",
                    "decision": SafetyDecision(
                        intent=Intent.EXTERNAL,
                        risk=RiskLevel.HIGH,
                        action=DecisionAction.ASK_APPROVAL,
                        permission=PermissionClass.NETWORK,
                        approval_required=True,
                        reason="Network action requires approval.",
                    ),
                    "tokens": ["abcdefghijklmnopqrstuvwxyz123456"],
                }
            )

            self.assertEqual(log_path, temp_path / "audit.jsonl")
            line = log_path.read_text(encoding="utf-8").strip()
            record = json.loads(line)

            self.assertTrue(record["timestamp"])
            self.assertEqual(record["request"], "Send password=[REDACTED_SECRET] to [REDACTED_EMAIL]")
            self.assertEqual(record["decision"]["intent"], "external")
            self.assertEqual(record["decision"]["risk"], "high")
            self.assertEqual(record["tokens"], ["[REDACTED_TOKEN]"])

    def test_audit_logger_accepts_explicit_jsonl_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "events.jsonl"
            logger = AuditLogger(target)

            written = logger.write_event({"message": "hello"})

            self.assertEqual(written, target)
            self.assertTrue(target.exists())
            self.assertEqual(json.loads(target.read_text(encoding="utf-8"))["message"], "hello")


if __name__ == "__main__":
    unittest.main()

