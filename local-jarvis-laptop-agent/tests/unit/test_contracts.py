"""Unit coverage for the shared Local Jarvis contract types."""

from __future__ import annotations

import dataclasses
import unittest

from jarvis.contracts import (
    ChatMessage,
    DecisionAction,
    Intent,
    ModelRequest,
    ModelResponse,
    PermissionClass,
    RiskLevel,
    SafetyDecision,
    ToolResult,
    ToolSpec,
)


class ContractTests(unittest.TestCase):
    def test_contract_enums_have_expected_wire_values(self) -> None:
        self.assertEqual(
            [item.value for item in Intent],
            ["chat", "recall", "inspect", "plan", "act", "automate", "external", "high_impact"],
        )
        self.assertEqual(
            [item.value for item in PermissionClass],
            ["none", "read_local", "write_local", "execute_local", "automate_app", "network", "high_impact"],
        )
        self.assertEqual([item.value for item in RiskLevel], ["low", "medium", "high", "blocked"])
        self.assertEqual(
            [item.value for item in DecisionAction],
            ["answer", "tool_call", "ask_approval", "ask_clarification", "refuse"],
        )

    def test_enum_members_are_string_compatible_for_json_contracts(self) -> None:
        self.assertEqual(Intent.CHAT, "chat")
        self.assertEqual(PermissionClass.NETWORK, "network")
        self.assertEqual(RiskLevel.BLOCKED, "blocked")
        self.assertEqual(DecisionAction.ASK_APPROVAL, "ask_approval")

    def test_chat_message_serializes_to_model_message_shape(self) -> None:
        message = ChatMessage(role="user", content="Explain your safety rules.")

        self.assertEqual(message.to_dict(), {"role": "user", "content": "Explain your safety rules."})

    def test_contract_dataclasses_are_frozen_at_the_top_level(self) -> None:
        decision = SafetyDecision(
            intent=Intent.CHAT,
            risk=RiskLevel.LOW,
            action=DecisionAction.ANSWER,
        )

        with self.assertRaises(dataclasses.FrozenInstanceError):
            decision.reason = "mutated"  # type: ignore[misc]

    def test_safety_decision_defaults_to_no_permission_without_approval(self) -> None:
        decision = SafetyDecision(
            intent=Intent.CHAT,
            risk=RiskLevel.LOW,
            action=DecisionAction.ANSWER,
        )

        self.assertIs(decision.permission, PermissionClass.NONE)
        self.assertFalse(decision.approval_required)
        self.assertEqual(decision.reason, "")
        self.assertIsNone(decision.safer_alternative)

    def test_model_request_and_response_defaults_are_deterministic(self) -> None:
        request = ModelRequest(
            messages=[ChatMessage(role="user", content="Say local model ready.")],
            model="qwen-local",
        )
        first_response = ModelResponse(content="ready")
        second_response = ModelResponse(content="also ready")

        first_response.raw["provider"] = "local-test-double"

        self.assertEqual(request.temperature, 0.2)
        self.assertIsNone(request.max_tokens)
        self.assertEqual(first_response.raw, {"provider": "local-test-double"})
        self.assertEqual(second_response.raw, {})

    def test_tool_spec_carries_permission_and_side_effect_metadata(self) -> None:
        spec = ToolSpec(
            name="read_text_file",
            description="Read a bounded text file inside an approved root.",
            permission=PermissionClass.READ_LOCAL,
            side_effects=False,
            approval_required=False,
            dry_run_supported=True,
        )

        self.assertIs(spec.permission, PermissionClass.READ_LOCAL)
        self.assertFalse(spec.side_effects)
        self.assertFalse(spec.approval_required)
        self.assertTrue(spec.dry_run_supported)

    def test_tool_result_data_defaults_do_not_share_mutable_state(self) -> None:
        first = ToolResult(ok=True, summary="First result")
        second = ToolResult(ok=True, summary="Second result")

        first.data["lines"] = 3

        self.assertEqual(first.data, {"lines": 3})
        self.assertEqual(second.data, {})


if __name__ == "__main__":
    unittest.main()

