"""Bounded local conversation history and transcript persistence."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any

from .contracts import ChatMessage
from .safety import redact_text


ALLOWED_ROLES = {"system", "user", "assistant", "agent"}


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _session_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


@dataclass(frozen=True)
class ConversationEntry:
    role: str
    content: str
    timestamp: str = field(default_factory=_utc_now)

    def to_json(self) -> dict[str, str]:
        return {
            "timestamp": self.timestamp,
            "role": self.role,
            "content": redact_text(self.content),
        }


class ConversationHistory:
    """Keep a small model context while saving the full local transcript."""

    def __init__(
        self,
        *,
        max_messages: int,
        transcript_dir: str | Path,
        system_prompt: str,
        session_id: str | None = None,
    ) -> None:
        self.max_messages = max(4, max_messages)
        self.system_prompt = system_prompt
        self.session_id = session_id or _session_id()
        self.transcript_dir = Path(transcript_dir)
        self.jsonl_path = self.transcript_dir / f"{self.session_id}.jsonl"
        self.markdown_path = self.transcript_dir / f"{self.session_id}.md"
        self._context: list[ChatMessage] = []
        self._summary: str | None = None
        self._write_header()
        self.add("system", system_prompt)

    def add_user(self, content: str) -> None:
        self.add("user", content)

    def add_assistant(self, content: str) -> None:
        self.add("assistant", content)

    def add_agent(self, content: str) -> None:
        self.add("agent", content)

    def add(self, role: str, content: str) -> None:
        role = role.strip().casefold()
        if role not in ALLOWED_ROLES:
            raise ValueError(f"Unsupported conversation role: {role}")
        if not isinstance(content, str):
            raise TypeError("Conversation content must be a string.")

        entry = ConversationEntry(role=role, content=content)
        self._append_transcript(entry)
        if role != "system":
            self._context.append(ChatMessage(role=role, content=content))
            self._compress_if_needed()

    def context_messages(self) -> list[ChatMessage]:
        messages = [ChatMessage(role="system", content=self.system_prompt)]
        messages.extend(self._context)
        return messages[-self.max_messages :] if len(messages) > self.max_messages else messages

    def model_messages(self) -> list[ChatMessage]:
        """Return Ollama-compatible messages, mapping internal agent notes."""

        normalized: list[ChatMessage] = []
        for message in self.context_messages():
            if message.role == "agent":
                normalized.append(
                    ChatMessage(role="assistant", content=f"[agent note] {message.content}")
                )
            else:
                normalized.append(message)
        return normalized

    @property
    def summary(self) -> str | None:
        return self._summary

    def _compress_if_needed(self) -> None:
        limit_without_system = max(3, self.max_messages - 1)
        if len(self._context) <= limit_without_system:
            return

        keep_count = max(2, limit_without_system - 1)
        old_messages = self._context[:-keep_count]
        tail = self._context[-keep_count:]
        self._summary = _summarize_messages(self._summary, old_messages)
        summary_message = ChatMessage(
            role="agent",
            content=f"Compressed earlier session context: {self._summary}",
        )
        self._context = [summary_message] + tail
        self._append_transcript(
            ConversationEntry(role="agent", content=summary_message.content)
        )

    def _write_header(self) -> None:
        self.transcript_dir.mkdir(parents=True, exist_ok=True)
        if not self.markdown_path.exists():
            self.markdown_path.write_text(
                f"# Jarvis Session {self.session_id}\n\n", encoding="utf-8"
            )

    def _append_transcript(self, entry: ConversationEntry) -> None:
        self.transcript_dir.mkdir(parents=True, exist_ok=True)
        with self.jsonl_path.open("a", encoding="utf-8") as handle:
            json.dump(entry.to_json(), handle, ensure_ascii=True, sort_keys=True)
            handle.write("\n")
        with self.markdown_path.open("a", encoding="utf-8") as handle:
            handle.write(
                f"## {entry.role} - {entry.timestamp}\n\n"
                f"{redact_text(entry.content).strip()}\n\n"
            )


def _summarize_messages(
    previous_summary: str | None,
    messages: list[ChatMessage],
) -> str:
    counts: dict[str, int] = {}
    snippets: list[str] = []
    for message in messages:
        counts[message.role] = counts.get(message.role, 0) + 1
        snippet = " ".join(message.content.split())[:160]
        if snippet:
            snippets.append(f"{message.role}: {snippet}")

    count_text = ", ".join(f"{role}={count}" for role, count in sorted(counts.items()))
    parts: list[str] = []
    if previous_summary:
        parts.append(previous_summary)
    if count_text:
        parts.append(f"Compressed {len(messages)} messages ({count_text}).")
    if snippets:
        parts.append("Recent compressed points: " + " | ".join(snippets[-4:]))
    return " ".join(parts).strip()


def transcript_paths(history: ConversationHistory) -> dict[str, Path]:
    return {"jsonl": history.jsonl_path, "markdown": history.markdown_path}
