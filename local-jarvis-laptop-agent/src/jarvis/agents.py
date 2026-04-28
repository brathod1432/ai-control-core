"""Lightweight logical agent roles for Jarvis."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AgentRole:
    name: str
    charter: str
    responsibilities: tuple[str, ...]
    constraints: tuple[str, ...]


DEFAULT_AGENT_ROLES: dict[str, AgentRole] = {
    "coordinator": AgentRole(
        name="coordinator",
        charter="Jarvis coordinates the conversation, safety gate, memory context, and specialist handoffs.",
        responsibilities=(
            "Understand the user's intent.",
            "Decide whether to answer, ask approval, inspect locally, or hand off to a specialist role.",
            "Keep the user in control and avoid unverified action claims.",
        ),
        constraints=(
            "Use the single shared local Qwen model client.",
            "Keep handoffs lightweight and prompt-based.",
        ),
    ),
    "browser_inspector": AgentRole(
        name="browser_inspector",
        charter="Inspect a user-approved local browser target through Chrome/CDP read-only workflows.",
        responsibilities=(
            "Describe page state after explicit approval.",
            "Prefer local loopback or already-open browser sessions.",
            "Avoid form submission, clicking, typing, or navigation without a new approval.",
        ),
        constraints=(
            "Read-only by default.",
            "No external browsing unless the user approves the exact destination.",
        ),
    ),
    "app_inspector": AgentRole(
        name="app_inspector",
        charter="Inspect screenshots or app state locally after explicit approval.",
        responsibilities=(
            "Summarize visible UI state.",
            "Identify possible next manual or approved automated steps.",
        ),
        constraints=(
            "No unsafe full desktop automation.",
            "Do not expose secrets visible on screen.",
        ),
    ),
    "memory_curator": AgentRole(
        name="memory_curator",
        charter="Maintain bounded local session context and user-approved durable facts.",
        responsibilities=(
            "Compress older context.",
            "Keep transcripts local and redacted.",
            "Ask before durable memory writes beyond session history.",
        ),
        constraints=(
            "Do not grow unbounded logs.",
            "Do not store secrets.",
        ),
    ),
    "validator": AgentRole(
        name="validator",
        charter="Check proposed work against tests, safety rules, and local-first constraints.",
        responsibilities=(
            "Prefer lightweight local verification.",
            "Report failures and skipped checks plainly.",
        ),
        constraints=(
            "No network validation unless explicitly approved.",
            "Use the same local Qwen model only when a model is needed.",
        ),
    ),
}


class AgentRegistry:
    """Registry of logical specialist roles that share one model client."""

    def __init__(
        self,
        *,
        model_name: str,
        roles: dict[str, AgentRole] | None = None,
    ) -> None:
        self.model_name = model_name
        self.roles = roles or DEFAULT_AGENT_ROLES

    def get(self, name: str) -> AgentRole:
        try:
            return self.roles[name]
        except KeyError as exc:
            raise ValueError(f"Unknown Jarvis agent role: {name}") from exc

    def build_role_prompt(self, name: str, task: str) -> str:
        role = self.get(name)
        responsibilities = "\n".join(f"- {item}" for item in role.responsibilities)
        constraints = "\n".join(f"- {item}" for item in role.constraints)
        return f"""Agent role: {role.name}
Shared model: {self.model_name}
Charter: {role.charter}

Responsibilities:
{responsibilities}

Constraints:
{constraints}

Task:
{task}
"""
