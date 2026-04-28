"""Local intent classification, redaction, and safety decisions."""

from __future__ import annotations

import re
from collections.abc import Iterable

from .contracts import DecisionAction, Intent, PermissionClass, RiskLevel, SafetyDecision


_URL_RE = re.compile(r"\b(?:https?://|www\.)\S+", re.IGNORECASE)
_EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)
_BEARER_RE = re.compile(r"\bBearer\s+[A-Za-z0-9._~+/=-]{12,}\b", re.IGNORECASE)
_ASSIGNMENT_SECRET_RE = re.compile(
    r"\b(api[_-]?key|access[_-]?token|refresh[_-]?token|secret|password|passwd|pwd)"
    r"\s*[:=]\s*([^\s,;]+)",
    re.IGNORECASE,
)
_PRIVATE_KEY_RE = re.compile(
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----",
    re.DOTALL,
)
_LONG_TOKEN_RE = re.compile(r"\b(?=[A-Za-z0-9._~+/=-]{24,}\b)(?=.*[A-Za-z])(?=.*\d)[A-Za-z0-9._~+/=-]+\b")

_CREDENTIAL_TERMS = (
    "password",
    "passwd",
    "secret",
    "token",
    "api key",
    "apikey",
    "private key",
    "credential",
    "cookie",
    ".ssh",
    "id_rsa",
    "keychain",
)
_CREDENTIAL_VERBS = (
    "show",
    "print",
    "read",
    "open",
    "display",
    "dump",
    "copy",
    "extract",
    "exfiltrate",
    "upload",
    "send",
)
_DESTRUCTIVE_TERMS = (
    "rm -rf",
    "format c:",
    "format disk",
    "wipe",
    "erase",
    "delete everything",
    "delete all",
    "remove all",
    "drop database",
    "truncate database",
    "factory reset",
)
_NETWORK_TERMS = (
    "http://",
    "https://",
    "www.",
    "download",
    "upload",
    "fetch",
    "post to",
    "publish",
    "email",
    "send email",
    "message",
    "slack",
    "discord",
    "github",
    "git push",
    "deploy",
    "release",
    "external",
    "internet",
)
_HIGH_IMPACT_TERMS = (
    "buy",
    "purchase",
    "sell",
    "trade",
    "transfer money",
    "wire",
    "bank",
    "payment",
    "pay ",
    "invoice",
    "legal advice",
    "medical advice",
    "diagnose",
    "prescribe",
    "tax filing",
    "change password",
    "delete account",
    "close account",
    "hire",
    "fire ",
)
_WRITE_TERMS = (
    "write",
    "create",
    "edit",
    "modify",
    "update",
    "save",
    "overwrite",
    "delete",
    "remove",
    "rename",
    "move",
    "replace",
)
_EXECUTE_TERMS = (
    "run",
    "execute",
    "launch",
    "start process",
    "install",
    "pip install",
    "npm install",
    "script",
    "powershell",
    "cmd",
    "bash",
    "terminal",
    "shell",
)
_AUTOMATION_TERMS = (
    "click",
    "type",
    "press",
    "fill",
    "submit",
    "browser",
    "chrome",
    "edge",
    "word",
    "excel",
    "powerpoint",
    "outlook",
    "automate",
    "ui",
)
_INSPECT_TERMS = (
    "read",
    "inspect",
    "show",
    "list",
    "find",
    "search",
    "scan",
    "summarize file",
    "look at",
)
_RECALL_TERMS = ("remember", "recall", "memory", "what did we", "what was")
_PLAN_TERMS = ("plan", "outline", "strategy", "steps", "roadmap", "schedule")


def classify_intent(text: str) -> Intent:
    """Classify user text into the shared MVP intent enum."""

    normalized = _normalize(text)
    if not normalized:
        return Intent.CHAT

    if _contains_any(normalized, _HIGH_IMPACT_TERMS):
        return Intent.HIGH_IMPACT
    if _is_external(normalized):
        return Intent.EXTERNAL
    if _contains_any(normalized, _AUTOMATION_TERMS):
        return Intent.AUTOMATE
    if _contains_any(normalized, _EXECUTE_TERMS) or _contains_any(normalized, _WRITE_TERMS):
        return Intent.ACT
    if _contains_any(normalized, _INSPECT_TERMS):
        return Intent.INSPECT
    if _contains_any(normalized, _RECALL_TERMS):
        return Intent.RECALL
    if _contains_any(normalized, _PLAN_TERMS):
        return Intent.PLAN
    return Intent.CHAT


def evaluate_safety(text: str) -> SafetyDecision:
    """Return a conservative local safety decision for a user request."""

    normalized = _normalize(text)
    intent = classify_intent(text)

    if not normalized:
        return SafetyDecision(
            intent=intent,
            risk=RiskLevel.LOW,
            action=DecisionAction.ASK_CLARIFICATION,
            reason="The request is empty or unclear.",
        )

    if _requests_credentials(normalized):
        return SafetyDecision(
            intent=intent,
            risk=RiskLevel.BLOCKED,
            action=DecisionAction.REFUSE,
            permission=PermissionClass.HIGH_IMPACT,
            reason="Requests to reveal, copy, or exfiltrate secrets are blocked.",
            safer_alternative="I can help locate safe configuration names or explain how to rotate credentials without exposing values.",
        )

    if _contains_any(normalized, _DESTRUCTIVE_TERMS):
        return SafetyDecision(
            intent=intent,
            risk=RiskLevel.BLOCKED,
            action=DecisionAction.REFUSE,
            permission=PermissionClass.HIGH_IMPACT,
            reason="Broad destructive actions are blocked by the local safety policy.",
            safer_alternative="Use a narrow dry run, backup, or explicit file list before any deletion.",
        )

    if intent is Intent.HIGH_IMPACT:
        return SafetyDecision(
            intent=intent,
            risk=RiskLevel.HIGH,
            action=DecisionAction.ASK_APPROVAL,
            permission=PermissionClass.HIGH_IMPACT,
            approval_required=True,
            reason="High-impact financial, legal, medical, identity, or account actions require explicit approval.",
            safer_alternative="I can draft a plan or checklist without taking the action.",
        )

    if intent is Intent.EXTERNAL:
        return SafetyDecision(
            intent=intent,
            risk=RiskLevel.HIGH,
            action=DecisionAction.ASK_APPROVAL,
            permission=PermissionClass.NETWORK,
            approval_required=True,
            reason="Network, publishing, messaging, deployment, or upload actions require explicit approval.",
            safer_alternative="I can prepare the local content or a dry-run summary first.",
        )

    if intent is Intent.AUTOMATE:
        return SafetyDecision(
            intent=intent,
            risk=RiskLevel.MEDIUM,
            action=DecisionAction.ASK_APPROVAL,
            permission=PermissionClass.AUTOMATE_APP,
            approval_required=True,
            reason="App and UI automation can create side effects and should be approved first.",
            safer_alternative="I can describe the manual steps or prepare inputs without controlling the app.",
        )

    if _contains_any(normalized, _EXECUTE_TERMS):
        return SafetyDecision(
            intent=intent,
            risk=RiskLevel.HIGH,
            action=DecisionAction.ASK_APPROVAL,
            permission=PermissionClass.EXECUTE_LOCAL,
            approval_required=True,
            reason="Executing local commands or scripts requires approval.",
            safer_alternative="I can explain the command or provide a dry-run where supported.",
        )

    if _contains_any(normalized, _WRITE_TERMS):
        return SafetyDecision(
            intent=intent,
            risk=RiskLevel.MEDIUM,
            action=DecisionAction.ASK_APPROVAL,
            permission=PermissionClass.WRITE_LOCAL,
            approval_required=True,
            reason="Local file modifications require approval and should stay explicitly scoped.",
            safer_alternative="I can show a proposed patch or create a separate output file first.",
        )

    if intent is Intent.INSPECT:
        return SafetyDecision(
            intent=intent,
            risk=RiskLevel.LOW,
            action=DecisionAction.TOOL_CALL,
            permission=PermissionClass.READ_LOCAL,
            reason="Read-only local inspection is allowed when scoped by the user.",
        )

    return SafetyDecision(
        intent=intent,
        risk=RiskLevel.LOW,
        action=DecisionAction.ANSWER,
        reason="The request can be handled without tool side effects.",
    )


def redact_text(text: str) -> str:
    """Redact common secrets and direct identifiers before audit logging."""

    redacted = _PRIVATE_KEY_RE.sub("[REDACTED_PRIVATE_KEY]", text)
    redacted = _BEARER_RE.sub("Bearer [REDACTED_TOKEN]", redacted)
    redacted = _ASSIGNMENT_SECRET_RE.sub(lambda match: f"{match.group(1)}=[REDACTED_SECRET]", redacted)
    redacted = _EMAIL_RE.sub("[REDACTED_EMAIL]", redacted)
    redacted = _URL_RE.sub("[REDACTED_URL]", redacted)
    return _LONG_TOKEN_RE.sub("[REDACTED_TOKEN]", redacted)


def _normalize(text: str) -> str:
    return " ".join(text.casefold().split())


def _contains_any(text: str, terms: Iterable[str]) -> bool:
    return any(term in text for term in terms)


def _is_external(text: str) -> bool:
    return bool(_URL_RE.search(text)) or _contains_any(text, _NETWORK_TERMS)


def _requests_credentials(text: str) -> bool:
    return _contains_any(text, _CREDENTIAL_TERMS) and _contains_any(text, _CREDENTIAL_VERBS)
