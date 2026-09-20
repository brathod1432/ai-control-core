"""Core orchestration loop for Local Jarvis."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone

from .agents import AgentRegistry
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
from .filesystem import (
    FileInspectionError,
    ReadOnlyFilesystemInspector,
    extract_explicit_path,
)
from .history import ConversationHistory
from .model_runtime.base import ModelClient
from .persona import build_system_prompt
from .safety import evaluate_safety


SYSTEM_PROMPT = build_system_prompt()


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
    history: ConversationHistory | None = None
    filesystem_inspector: ReadOnlyFilesystemInspector | None = None
    agent_registry: AgentRegistry = field(init=False)

    def __post_init__(self) -> None:
        system_prompt = build_system_prompt(
            model_name=self.config.runtime.default_model,
            base_url=self.config.runtime.base_url,
        )
        self.agent_registry = AgentRegistry(model_name=self.config.runtime.default_model)
        if self.history is None:
            self.history = ConversationHistory(
                max_messages=self.config.conversation.max_messages,
                transcript_dir=self.config.storage.transcript_dir,
                system_prompt=system_prompt,
            )
        if self.filesystem_inspector is None:
            self.filesystem_inspector = ReadOnlyFilesystemInspector()

    @property
    def messages(self) -> list[ChatMessage]:
        assert self.history is not None
        return self.history.context_messages()

    def handle_input(self, user_input: str) -> JarvisTurn:
        assert self.history is not None
        self.history.add_user(user_input)
        decision = evaluate_safety(user_input)
        if decision.action == DecisionAction.REFUSE:
            response = self._refusal(decision)
            self.history.add_assistant(response)
            self._audit(user_input, decision, response, model_used=False)
            return JarvisTurn(user_input, response, decision, model_used=False)

        if decision.action == DecisionAction.ASK_APPROVAL:
            response = self._approval_needed(decision)
            self.history.add_assistant(response)
            self._audit(user_input, decision, response, model_used=False)
            return JarvisTurn(user_input, response, decision, model_used=False)

        if decision.action == DecisionAction.ASK_CLARIFICATION:
            response = "I can help, but I need a more specific local target or desired outcome before acting."
            self.history.add_assistant(response)
            self._audit(user_input, decision, response, model_used=False)
            return JarvisTurn(user_input, response, decision, model_used=False)

        if decision.intent is Intent.INSPECT:
            inspected = self._handle_read_only_inspection(user_input, decision)
            if inspected is not None:
                return inspected

        request = ModelRequest(
            messages=self.history.model_messages(),
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
            self.history.add_assistant(response)
            self._audit(user_input, decision, response, model_used=True, error=str(exc))
            return JarvisTurn(user_input, response, decision, model_used=True, error=str(exc))

        response = self._postprocess_model_response(model_response, decision)
        self.history.add_assistant(response)
        self._audit(user_input, decision, response, model_used=True)
        return JarvisTurn(user_input, response, decision, model_used=True)

    def _handle_read_only_inspection(
        self,
        user_input: str,
        decision: SafetyDecision,
    ) -> JarvisTurn | None:
        assert self.history is not None
        assert self.filesystem_inspector is not None
        path = extract_explicit_path(user_input)
        if path is None:
            response = (
                "I can inspect local files read-only, but I need an explicit absolute path "
                "such as C:\\Users\\kbrat\\PycharmProjects\\PremiumPros."
            )
            self.history.add_assistant(response)
            self._audit(user_input, decision, response, model_used=False)
            return JarvisTurn(user_input, response, decision, model_used=False)

        try:
            result = self.filesystem_inspector.inspect(path)
        except FileInspectionError as exc:
            response = f"I could not inspect that path read-only. {exc}"
            self.history.add_assistant(response)
            self._audit(user_input, decision, response, model_used=False, error=str(exc))
            return JarvisTurn(user_input, response, decision, model_used=False, error=str(exc))

        evidence = result.evidence_summary()
        self.history.add_agent(evidence)
        request = ModelRequest(
            messages=[
                ChatMessage(
                    role="system",
                    content=(
                        "You are Jarvis. Summarize only the provided read-only local filesystem evidence. "
                        "Do not invent capabilities, do not claim web access, and do not say files were modified."
                    ),
                ),
                ChatMessage(
                    role="user",
                    content=(
                        f"User request: {user_input}\n\n"
                        f"Evidence:\n{evidence}\n\n"
                        "Give a concise project overview, note the main file types, and mention inspection bounds."
                    ),
                ),
            ],
            model=self.config.runtime.default_model,
            temperature=self.config.runtime.temperature,
            max_tokens=self.config.runtime.max_tokens,
        )
        try:
            model_response = self.model_client.chat(request)
        except Exception as exc:
            response = (
                self._deterministic_inspection_summary(evidence)
                + f"\n\nThe local model could not summarize this evidence. Details: {exc}"
            )
            self.history.add_assistant(response)
            self._audit(user_input, decision, response, model_used=True, error=str(exc))
            return JarvisTurn(user_input, response, decision, model_used=True, error=str(exc))

        content = model_response.content.strip()
        response = content or self._deterministic_inspection_summary(evidence)
        response += "\n\nNote: I only inspected files read-only. I did not create, edit, delete, or upload anything."
        self.history.add_assistant(response)
        self._audit(user_input, decision, response, model_used=True)
        return JarvisTurn(user_input, response, decision, model_used=True)

    def _deterministic_inspection_summary(self, evidence: str) -> str:
        lines = evidence.splitlines()
        head = "\n".join(lines[:20])
        return f"Read-only project inspection summary:\n{head}"

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
