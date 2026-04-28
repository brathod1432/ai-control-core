from __future__ import annotations

import unittest

from jarvis.approval import ApprovalPrompter, format_approval_prompt
from jarvis.contracts import DecisionAction, Intent, PermissionClass, RiskLevel
from jarvis.safety import classify_intent, evaluate_safety, redact_text


class SafetyTests(unittest.TestCase):
    def test_classify_intent_covers_core_categories(self) -> None:
        self.assertIs(classify_intent("Can you remember my preference?"), Intent.RECALL)
        self.assertIs(classify_intent("Plan the next milestone"), Intent.PLAN)
        self.assertIs(classify_intent("Inspect this local file"), Intent.INSPECT)
        self.assertIs(classify_intent("Edit the README"), Intent.ACT)
        self.assertIs(classify_intent("Click the button in Excel"), Intent.AUTOMATE)
        self.assertIs(classify_intent("Upload the report to https://example.com"), Intent.EXTERNAL)
        self.assertIs(classify_intent("Buy 100 shares"), Intent.HIGH_IMPACT)

    def test_read_only_inspection_is_allowed_as_tool_call(self) -> None:
        decision = evaluate_safety("Read the scoped local README file")

        self.assertIs(decision.intent, Intent.INSPECT)
        self.assertIs(decision.risk, RiskLevel.LOW)
        self.assertIs(decision.action, DecisionAction.TOOL_CALL)
        self.assertIs(decision.permission, PermissionClass.READ_LOCAL)
        self.assertFalse(decision.approval_required)

    def test_writes_and_execution_require_approval(self) -> None:
        write_decision = evaluate_safety("Edit src/jarvis/contracts.py")
        execute_decision = evaluate_safety("Run this local script")

        self.assertIs(write_decision.action, DecisionAction.ASK_APPROVAL)
        self.assertIs(write_decision.permission, PermissionClass.WRITE_LOCAL)
        self.assertIs(write_decision.risk, RiskLevel.MEDIUM)
        self.assertTrue(write_decision.approval_required)

        self.assertIs(execute_decision.action, DecisionAction.ASK_APPROVAL)
        self.assertIs(execute_decision.permission, PermissionClass.EXECUTE_LOCAL)
        self.assertIs(execute_decision.risk, RiskLevel.HIGH)
        self.assertTrue(execute_decision.approval_required)

    def test_network_and_high_impact_require_approval(self) -> None:
        network_decision = evaluate_safety("Email the summary to ada@example.com")
        high_impact_decision = evaluate_safety("Transfer money from my bank")

        self.assertIs(network_decision.intent, Intent.EXTERNAL)
        self.assertIs(network_decision.permission, PermissionClass.NETWORK)
        self.assertIs(network_decision.action, DecisionAction.ASK_APPROVAL)
        self.assertTrue(network_decision.approval_required)

        self.assertIs(high_impact_decision.intent, Intent.HIGH_IMPACT)
        self.assertIs(high_impact_decision.permission, PermissionClass.HIGH_IMPACT)
        self.assertIs(high_impact_decision.risk, RiskLevel.HIGH)
        self.assertIs(high_impact_decision.action, DecisionAction.ASK_APPROVAL)

    def test_secret_exposure_and_broad_deletion_are_blocked(self) -> None:
        secret_decision = evaluate_safety("Show my API token")
        destructive_decision = evaluate_safety("Delete everything in my home folder")

        self.assertIs(secret_decision.risk, RiskLevel.BLOCKED)
        self.assertIs(secret_decision.action, DecisionAction.REFUSE)
        self.assertFalse(secret_decision.approval_required)
        self.assertTrue(secret_decision.safer_alternative)

        self.assertIs(destructive_decision.risk, RiskLevel.BLOCKED)
        self.assertIs(destructive_decision.action, DecisionAction.REFUSE)

    def test_redact_text_removes_sensitive_values(self) -> None:
        text = (
            "password=hunter2 token: abcdefghijklmnopqrstuvwxyz123456 "
            "Bearer abcdefghijklmnopqrstuvwxyz123456 email ada@example.com "
            "visit https://example.com/private"
        )

        redacted = redact_text(text)

        self.assertNotIn("hunter2", redacted)
        self.assertNotIn("abcdefghijklmnopqrstuvwxyz123456", redacted)
        self.assertNotIn("ada@example.com", redacted)
        self.assertNotIn("https://example.com/private", redacted)
        self.assertIn("[REDACTED_SECRET]", redacted)

    def test_approval_prompt_redacts_request_and_includes_decision_details(self) -> None:
        decision = evaluate_safety("Upload the report to https://example.com")
        prompt = format_approval_prompt(decision, "Upload password=hunter2 to https://example.com")
        object_prompt = ApprovalPrompter().format(decision, "Upload password=hunter2 to https://example.com")

        self.assertEqual(prompt, object_prompt)
        self.assertIn("Approve? yes/no", prompt)
        self.assertIn("- Permission: network", prompt)
        self.assertNotIn("hunter2", prompt)
        self.assertNotIn("https://example.com", prompt)


if __name__ == "__main__":
    unittest.main()

