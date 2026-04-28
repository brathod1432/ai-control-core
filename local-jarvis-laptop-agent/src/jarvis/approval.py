"""Helpers for presenting human approval prompts."""

from __future__ import annotations

from .contracts import SafetyDecision
from .safety import redact_text


def format_approval_prompt(decision: SafetyDecision, text: str) -> str:
    """Format a security-model-compatible approval prompt."""

    safer_alternative = decision.safer_alternative or "Answer without taking side effects."
    return "\n".join(
        (
            "Jarvis wants to perform this action:",
            f"- Action: {decision.action.value}",
            f"- Intent: {decision.intent.value}",
            f"- Permission: {decision.permission.value}",
            f"- Risk: {decision.risk.value}",
            f"- Request: {redact_text(text)}",
            "- Data accessed: Only data explicitly required for the approved action.",
            f"- Side effects: {'Possible' if decision.approval_required else 'None expected'}",
            f"- Why needed: {decision.reason or 'No reason provided.'}",
            f"- Safer alternative: {safer_alternative}",
            "",
            "Approve? yes/no",
        )
    )


class ApprovalPrompter:
    """Small wrapper for callers that prefer an object-oriented interface."""

    def format(self, decision: SafetyDecision, text: str) -> str:
        return format_approval_prompt(decision, text)
