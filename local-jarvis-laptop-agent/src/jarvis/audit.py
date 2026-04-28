"""JSONL audit logging for local Jarvis events."""

from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any

from .safety import redact_text


class AuditLogger:
    """Append redacted JSON audit events to a local JSONL file."""

    def __init__(self, log_dir_or_file: str | Path) -> None:
        path = Path(log_dir_or_file)
        if path.suffix.lower() == ".jsonl":
            self.log_file = path
        else:
            self.log_file = path / "audit.jsonl"

    def write_event(self, event: dict[str, Any]) -> Path:
        """Append an event and return the JSONL path that was written."""

        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        record = _redact_value(event)
        record["timestamp"] = datetime.now(timezone.utc).isoformat()
        with self.log_file.open("a", encoding="utf-8") as handle:
            json.dump(record, handle, ensure_ascii=True, sort_keys=True)
            handle.write("\n")
        return self.log_file


def _redact_value(value: Any) -> Any:
    if isinstance(value, str):
        return redact_text(value)
    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value) and not isinstance(value, type):
        return _redact_value(asdict(value))
    if isinstance(value, dict):
        return {str(key): _redact_value(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_redact_value(item) for item in value]
    if isinstance(value, tuple):
        return tuple(_redact_value(item) for item in value)
    return value
