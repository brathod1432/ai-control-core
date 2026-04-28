"""Minimal local Jarvis loop.

This example uses only Python standard library and an Ollama-style local endpoint.
It does not install packages or contact external services. Configure the endpoint
in config/jarvis.local.example.json or edit BASE_URL and MODEL for a local server.
"""

from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request


BASE_URL = "http://127.0.0.1:11434"
MODEL = "qwen2.5:3b"


SYSTEM_PROMPT = """You are Jarvis, a local-first laptop assistant.
You may answer questions and propose local actions.
You must not claim you performed actions unless a tool result confirms it.
You must ask before network access, shell commands, file writes, desktop control,
browser automation, Office automation, or high-impact actions.
Keep responses concise and practical.
"""


def chat(messages: list[dict[str, str]]) -> str:
    payload = {
        "model": MODEL,
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": 0.2
        },
    }
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        f"{BASE_URL}/api/chat",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            body = json.loads(response.read().decode("utf-8"))
    except urllib.error.URLError as exc:
        return (
            "Local model endpoint is not reachable. "
            f"Expected Ollama-style endpoint at {BASE_URL}/api/chat. Error: {exc}"
        )
    return body.get("message", {}).get("content", str(body))


def main() -> int:
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    print("Local Jarvis minimal loop. Type 'exit' to quit.")
    while True:
        try:
            user_input = input("you> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if user_input.lower() in {"exit", "quit"}:
            return 0
        if not user_input:
            continue
        messages.append({"role": "user", "content": user_input})
        response = chat(messages)
        messages.append({"role": "assistant", "content": response})
        print(f"jarvis> {response}")


if __name__ == "__main__":
    sys.exit(main())
