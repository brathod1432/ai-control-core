---
name: offline-qwen-runtime
description: Use to configure or design a local/offline model runtime for Jarvis using Qwen through Ollama, llama.cpp, LM Studio, or an OpenAI-compatible local server. Covers model profiles, hardware tradeoffs, endpoint contracts, and no-network constraints.
category: local-agent
---

## Internal Safety Override

- Status: advisory until the user approves installs, downloads, or runtime commands.
- Do not download models, install runtimes, or contact model hubs without explicit approval.
- Do not send prompts, files, memory, logs, or diagnostics to remote model APIs by default.

# Offline Qwen Runtime

## Current Model Baseline

All agents and subagents use the same single local Ollama `qwen2.5:3b` model through `http://127.0.0.1:11434`. No cloud LLMs, remote model APIs, separate providers, or per-agent model pools are allowed by the current runtime plan.

## Runtime Options

Ollama:
- Current active runtime.
- Endpoint: `http://127.0.0.1:11434/api/chat`.
- Model: `qwen2.5:3b`.

llama.cpp server:
- Future-only alternative requiring explicit redesign and approval.

LM Studio:
- Future-only alternative requiring explicit redesign and approval.

vLLM:
- Future-only alternative requiring explicit redesign and approval.

## Model Profiles

Fast:
- `qwen2.5:3b` with a fast prompt/parameter profile.
- Used for intent classification and short answers.

Balanced:
- `qwen2.5:3b` with the normal Jarvis prompt/parameter profile.
- Used for normal Jarvis reasoning.

Coder:
- `qwen2.5:3b` with a coding prompt/parameter profile.
- Used for code and repo work.

Critic:
- `qwen2.5:3b` with a critic prompt.
- Used for verification and review.

## Endpoint Contract

Jarvis should abstract the runtime behind one local interface:

```json
{
  "provider": "ollama|llama_cpp|lm_studio|openai_compatible_local",
  "base_url": "http://127.0.0.1:11434",
  "model": "qwen2.5:3b",
  "timeout_seconds": 120,
  "temperature": 0.2,
  "max_tokens": 2048
}
```

## Hardware Tradeoffs

- Current target: `qwen2.5:3b` on local Ollama.
- Larger or specialized models require explicit redesign and approval before use.

## Validation

- Runtime listens only on loopback.
- Model responds to a harmless local prompt.
- No remote endpoint is configured.
- Logs do not include secrets or private file content.
- Timeout and cancellation work.
