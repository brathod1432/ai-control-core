"""Shared contracts for the Local Jarvis core.

The core deliberately starts with small standard-library-only types so the MVP
can run before optional voice, browser, Office, or model-runtime dependencies
are added.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class Intent(str, Enum):
    CHAT = "chat"
    RECALL = "recall"
    INSPECT = "inspect"
    PLAN = "plan"
    ACT = "act"
    AUTOMATE = "automate"
    EXTERNAL = "external"
    HIGH_IMPACT = "high_impact"


class PermissionClass(str, Enum):
    NONE = "none"
    READ_LOCAL = "read_local"
    WRITE_LOCAL = "write_local"
    EXECUTE_LOCAL = "execute_local"
    AUTOMATE_APP = "automate_app"
    NETWORK = "network"
    HIGH_IMPACT = "high_impact"


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    BLOCKED = "blocked"


class DecisionAction(str, Enum):
    ANSWER = "answer"
    TOOL_CALL = "tool_call"
    ASK_APPROVAL = "ask_approval"
    ASK_CLARIFICATION = "ask_clarification"
    REFUSE = "refuse"


@dataclass(frozen=True)
class SafetyDecision:
    intent: Intent
    risk: RiskLevel
    action: DecisionAction
    permission: PermissionClass = PermissionClass.NONE
    approval_required: bool = False
    reason: str = ""
    safer_alternative: str | None = None


@dataclass(frozen=True)
class ChatMessage:
    role: str
    content: str

    def to_dict(self) -> dict[str, str]:
        return {"role": self.role, "content": self.content}


@dataclass(frozen=True)
class ModelRequest:
    messages: list[ChatMessage]
    model: str
    temperature: float = 0.2
    max_tokens: int | None = None


@dataclass(frozen=True)
class ModelResponse:
    content: str
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ToolSpec:
    name: str
    description: str
    permission: PermissionClass
    side_effects: bool = False
    approval_required: bool = False
    dry_run_supported: bool = False


@dataclass(frozen=True)
class ToolResult:
    ok: bool
    summary: str
    data: dict[str, Any] = field(default_factory=dict)
    redacted: bool = False
    error_code: str | None = None

