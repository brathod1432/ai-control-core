"""Configuration loading and validation for Local Jarvis.

The loader is deliberately standard-library-only and local-first. Runtime
network access is limited by validation to loopback model endpoints.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import json
import os
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


DEFAULT_BASE_URL = "http://127.0.0.1:11434"
DEFAULT_CHAT_ENDPOINT = "/api/chat"
DEFAULT_MODEL = "qwen-local"
DEFAULT_PROVIDER = "ollama"
DEFAULT_TEMPERATURE = 0.2
DEFAULT_LOG_DIR = "%USERPROFILE%/.local-jarvis/logs"
DEFAULT_MAX_MESSAGES = 40


class ConfigError(ValueError):
    """Raised when a Jarvis configuration file is invalid."""


@dataclass(frozen=True)
class RuntimeConfig:
    provider: str = DEFAULT_PROVIDER
    default_model: str = DEFAULT_MODEL
    base_url: str = DEFAULT_BASE_URL
    chat_endpoint: str = DEFAULT_CHAT_ENDPOINT
    temperature: float = DEFAULT_TEMPERATURE
    max_tokens: int | None = None


@dataclass(frozen=True)
class StorageConfig:
    log_dir: str = DEFAULT_LOG_DIR


@dataclass(frozen=True)
class ConversationConfig:
    max_messages: int = DEFAULT_MAX_MESSAGES


@dataclass(frozen=True)
class JarvisConfig:
    runtime: RuntimeConfig = field(default_factory=RuntimeConfig)
    storage: StorageConfig = field(default_factory=StorageConfig)
    conversation: ConversationConfig = field(default_factory=ConversationConfig)


def load_config(path: str | None = None) -> JarvisConfig:
    """Load and validate Jarvis configuration from JSON.

    When *path* is omitted, safe local defaults are returned. Unknown keys are
    ignored so the loader can consume the broader example config while this MVP
    owns only runtime settings.
    """

    raw_config: dict[str, Any] = {}
    if path is not None:
        config_path = Path(path)
        try:
            with config_path.open("r", encoding="utf-8") as config_file:
                parsed = json.load(config_file)
        except OSError as exc:
            raise ConfigError(f"Unable to read config file: {config_path}") from exc
        except json.JSONDecodeError as exc:
            raise ConfigError(f"Config file is not valid JSON: {config_path}") from exc
        if not isinstance(parsed, dict):
            raise ConfigError("Config root must be a JSON object.")
        raw_config = parsed

    runtime = raw_config.get("runtime", {})
    if not isinstance(runtime, dict):
        raise ConfigError("runtime must be a JSON object.")

    storage = raw_config.get("storage", {})
    if not isinstance(storage, dict):
        raise ConfigError("storage must be a JSON object.")

    conversation = raw_config.get("conversation", {})
    if not isinstance(conversation, dict):
        raise ConfigError("conversation must be a JSON object.")

    return JarvisConfig(
        runtime=_load_runtime_config(runtime),
        storage=_load_storage_config(storage),
        conversation=_load_conversation_config(conversation),
    )


def _load_runtime_config(raw: dict[str, Any]) -> RuntimeConfig:
    provider = _string_value(raw, "provider", DEFAULT_PROVIDER)
    default_model = _string_value(raw, "default_model", DEFAULT_MODEL)
    base_url = _string_value(raw, "base_url", DEFAULT_BASE_URL)
    chat_endpoint = _string_value(raw, "chat_endpoint", DEFAULT_CHAT_ENDPOINT)
    temperature = _float_value(raw, "temperature", DEFAULT_TEMPERATURE)
    max_tokens = _optional_positive_int(raw, "max_tokens")

    if provider != "ollama":
        raise ConfigError("runtime.provider must be 'ollama'.")
    if not default_model:
        raise ConfigError("runtime.default_model must not be empty.")
    if not 0.0 <= temperature <= 2.0:
        raise ConfigError("runtime.temperature must be between 0.0 and 2.0.")
    _validate_loopback_base_url(base_url)
    _validate_chat_endpoint(chat_endpoint)

    return RuntimeConfig(
        provider=provider,
        default_model=default_model,
        base_url=base_url.rstrip("/"),
        chat_endpoint=chat_endpoint,
        temperature=temperature,
        max_tokens=max_tokens,
    )


def _string_value(raw: dict[str, Any], key: str, default: str) -> str:
    value = raw.get(key, default)
    if not isinstance(value, str):
        raise ConfigError(f"runtime.{key} must be a string.")
    return value.strip()


def _float_value(raw: dict[str, Any], key: str, default: float) -> float:
    value = raw.get(key, default)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ConfigError(f"runtime.{key} must be a number.")
    return float(value)


def _optional_positive_int(raw: dict[str, Any], key: str) -> int | None:
    if key not in raw or raw[key] is None:
        return None
    value = raw[key]
    if isinstance(value, bool) or not isinstance(value, int):
        raise ConfigError(f"runtime.{key} must be a positive integer or null.")
    if value <= 0:
        raise ConfigError(f"runtime.{key} must be a positive integer or null.")
    return value


def _load_storage_config(raw: dict[str, Any]) -> StorageConfig:
    log_dir = _storage_path_value(raw, "log_dir", DEFAULT_LOG_DIR)
    return StorageConfig(log_dir=log_dir)


def _load_conversation_config(raw: dict[str, Any]) -> ConversationConfig:
    max_messages = raw.get("max_messages", DEFAULT_MAX_MESSAGES)
    if isinstance(max_messages, bool) or not isinstance(max_messages, int):
        raise ConfigError("conversation.max_messages must be an integer.")
    if max_messages < 4:
        raise ConfigError("conversation.max_messages must be at least 4.")
    return ConversationConfig(max_messages=max_messages)


def _storage_path_value(raw: dict[str, Any], key: str, default: str) -> str:
    value = _string_value(raw, key, default)
    if not value:
        raise ConfigError(f"storage.{key} must not be empty.")
    expanded = os.path.expandvars(value)
    return str(Path(expanded).expanduser())


def _validate_loopback_base_url(base_url: str) -> None:
    parsed = urlparse(base_url)
    if parsed.scheme not in {"http", "https"}:
        raise ConfigError("runtime.base_url must use http or https.")
    if parsed.path not in {"", "/"} or parsed.params or parsed.query or parsed.fragment:
        raise ConfigError("runtime.base_url must not include a path, query, or fragment.")
    host = parsed.hostname
    if host is None:
        raise ConfigError("runtime.base_url must include a host.")
    if host == "localhost" or host == "::1" or host.startswith("127."):
        return
    raise ConfigError("runtime.base_url must target a loopback host.")


def _validate_chat_endpoint(chat_endpoint: str) -> None:
    if not chat_endpoint.startswith("/"):
        raise ConfigError("runtime.chat_endpoint must start with '/'.")
    parsed = urlparse(chat_endpoint)
    if parsed.scheme or parsed.netloc or parsed.params or parsed.query or parsed.fragment:
        raise ConfigError("runtime.chat_endpoint must be a local path only.")
