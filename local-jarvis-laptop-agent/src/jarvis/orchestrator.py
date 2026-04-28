"""Core orchestration loop for the Local Jarvis MVP."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone

from .audit import AuditLogger
from .config import JarvisConfig
from .contracts import (
    ChatMessage,
    DecisionAction,
    Intent,
    ModelRequest,
    ModelResponse,
    SafetyDecision,
)
from .model_runtime.base import ModelClient
from .safety import evaluate_safety


SYSTEM_PROMPT = """You are Jarvis, a local-first laptop assistant.
You run on the user's laptop and must protect privacy and local control.
You may answer questions, reason, and propose actions.
You must not claim that you inspected, changed, ran, sent, downloaded, or opened
anything unless an approved tool result confirms it.
Ask before network access, shell commands, file writes, desktop control, browser
automation, Office automation, memory writes, or high-impact actions.
Keep responses concise, practical, and honest about limits.
"""


@dataclass
class JarvisTurn:
    user_input: str
    assistant_response: str
    decision: SafetyDecision
    model_used: bool
    error: str | None = None


@dataclass
class JarvisOrchestrator:
    config: JarvisConfig
    model_client: ModelClient
    audit_logger: AuditLogger
    messages: list[ChatMessage] = field(
        default_factory=lambda: [ChatMessage(role="system", content=SYSTEM_PROMPT)]
    )

    def handle_input(self, user_input: str) -> JarvisTurn:
        decision = evaluate_safety(user_input)
        if decision.action == DecisionAction.REFUSE:
            response = self._refusal(decision)
            self._audit(user_input, decision, response, model_used=False)
            return JarvisTurn(user_input, response, decision, model_used=False)

        if decision.action == DecisionAction.ASK_APPROVAL:
            response = self._approval_needed(decision)
            self._audit(user_input, decision, response, model_used=False)
            return JarvisTurn(user_input, response, decision, model_used=False)

        if decision.action == DecisionAction.ASK_CLARIFICATION:
            response = "I can help, but I need a more specific local target or desired outcome before acting."
            self._audit(user_input, decision, response, model_used=False)
            return JarvisTurn(user_input, response, decision, model_used=False)

        self.messages.append(ChatMessage(role="user", content=user_input))
        request = ModelRequest(
            messages=self.messages,
            model=self.config.runtime.default_model,
            temperature=self.config.runtime.temperature,
            max_tokens=self.config.runtime.max_tokens,
        )
        try:
            model_response = self.model_client.chat(request)
        except Exception as exc:  # Keep CLI alive when local runtime is down.
            response = (
                "The local model runtime is not available or returned an error. "
                f"Check the loopback endpoint and model config. Details: {exc}"
            )
            self._audit(user_input, decision, response, model_used=True, error=str(exc))
            return JarvisTurn(user_input, response, decision, model_used=True, error=str(exc))

        response = self._postprocess_model_response(model_response, decision)
        self.messages.append(ChatMessage(role="assistant", content=response))
        self._trim_history()
        self._audit(user_input, decision, response, model_used=True)
        return JarvisTurn(user_input, response, decision, model_used=True)

    def _approval_needed(self, decision: SafetyDecision) -> str:
        safer = f"\nSafer alternative: {decision.safer_alternative}" if decision.safer_alternative else ""
        return (
            "That action needs explicit approval before Jarvis can continue.\n"
            f"Risk: {decision.risk.value}\n"
            f"Permission: {decision.permission.value}\n"
            f"Reason: {decision.reason}{safer}"
        )

    def _refusal(self, decision: SafetyDecision) -> str:
        safer = f" Safer alternative: {decision.safer_alternative}" if decision.safer_alternative else ""
        return f"I cannot safely do that by default. Reason: {decision.reason}.{safer}"

    def _postprocess_model_response(
        self,
        response: ModelResponse,
        decision: SafetyDecision,
    ) -> str:
        content = response.content.strip()
        if not content:
            return "The local model returned an empty response."
        if decision.intent in {Intent.ACT, Intent.AUTOMATE, Intent.EXTERNAL, Intent.HIGH_IMPACT}:
            return (
                content
                + "\n\nNote: I have not performed any action. This is proposal-only unless you explicitly approve the next step."
            )
        return content

    def _trim_history(self) -> None:
        max_messages = max(4, self.config.conversation.max_messages)
        if len(self.messages) <= max_messages:
            return
        system = self.messages[:1]
        tail = self.messages[-(max_messages - 1) :]
        self.messages = system + tail

    def _audit(
        self,
        user_input: str,
        decision: SafetyDecision,
        response: str,
        *,
        model_used: bool,
        error: str | None = None,
    ) -> None:
        self.audit_logger.write_event(
            {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "request_summary": user_input[:500],
                "intent": decision.intent.value,
                "risk": decision.risk.value,
                "action": decision.action.value,
                "permission": decision.permission.value,
                "approval_required": decision.approval_required,
                "model_used": model_used,
                "result_summary": response[:500],
                "error": error,
            }
        )

