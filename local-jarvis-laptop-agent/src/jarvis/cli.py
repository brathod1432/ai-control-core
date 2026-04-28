"""Command-line interface for the Local Jarvis MVP."""

from __future__ import annotations

import argparse
from pathlib import Path

from .audit import AuditLogger
from .config import load_config
from .history import transcript_paths
from .model_runtime import create_model_client
from .orchestrator import JarvisOrchestrator


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Local Jarvis laptop assistant")
    parser.add_argument(
        "--config",
        type=Path,
        default=None,
        help="Path to a local Jarvis JSON config file.",
    )
    parser.add_argument(
        "--once",
        default=None,
        help="Run one prompt and exit.",
    )
    return parser


def create_orchestrator(config_path: Path | None = None) -> JarvisOrchestrator:
    config = load_config(str(config_path) if config_path else None)
    model_client = create_model_client(config)
    audit_logger = AuditLogger(config.storage.log_dir)
    return JarvisOrchestrator(
        config=config,
        model_client=model_client,
        audit_logger=audit_logger,
    )


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    orchestrator = create_orchestrator(args.config)

    if args.once:
        turn = orchestrator.handle_input(args.once)
        print(turn.assistant_response)
        return 0 if turn.error is None else 2

    print("Jarvis local assistant. Type '/exit' to quit, '/help' for commands.")
    print(f"Model: {orchestrator.config.runtime.default_model} at {orchestrator.config.runtime.base_url}")
    while True:
        try:
            user_input = input("you> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0

        if not user_input:
            continue
        if user_input in {"/exit", "/quit"}:
            return 0
        if user_input == "/help":
            print("Commands: /help, /status, /exit, /quit. Risky actions are proposal-only unless approved.")
            continue
        if user_input == "/status":
            paths = transcript_paths(orchestrator.history)
            print(f"Model: {orchestrator.config.runtime.default_model}")
            print(f"Transcript JSONL: {paths['jsonl']}")
            print(f"Transcript Markdown: {paths['markdown']}")
            continue

        turn = orchestrator.handle_input(user_input)
        print(f"Jarvis> {turn.assistant_response}")


if __name__ == "__main__":
    raise SystemExit(main())
