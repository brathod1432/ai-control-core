# Technical Decisions

## Current Model Baseline

All agents and subagents use the same single local Ollama `qwen2.5:3b` model through `http://127.0.0.1:11434`. No cloud LLMs, remote model APIs, separate providers, or per-agent model pools are currently accepted.

## Accepted Decisions

### ADR-001: Local-First By Default

Decision:
- Jarvis will not use cloud APIs, model hubs, telemetry, or external docs by default.

Reason:
- The product promise is privacy-preserving local assistance.

Consequence:
- Setup may require manual model installation.
- Some features need explicit network approval.

### ADR-002: Text Interface Before Voice

Decision:
- Build and harden CLI/text interaction before voice.

Reason:
- Text is easier to debug, test, log, and confirm.
- Voice misrecognition creates action risk.

Consequence:
- The first version feels less magical but is much safer.

### ADR-003: Tool Registry Before Powerful Tools

Decision:
- All tools must be registered with permission class, side effects, approval requirement, schema, and redaction policy.

Reason:
- Ad hoc tool execution is the easiest way to make a local assistant dangerous.

Consequence:
- More upfront design, fewer unsafe surprises.

### ADR-004: Read-Only Tools Before Write Tools

Decision:
- Implement local read-only inspection before write, command, browser, Office, or desktop control.

Reason:
- Most useful assistance begins with understanding context.

Consequence:
- Early MVP can answer and inspect but not yet act autonomously.

### ADR-005: Runtime Storage Outside Repo

Decision:
- Runtime memory, logs, artifacts, models, and temporary files should live outside the repo, for example `%USERPROFILE%\.local-jarvis`.

Reason:
- Avoid committing sensitive runtime data.

Consequence:
- Config must clearly distinguish repo templates from runtime state.

### ADR-006: Loopback-Only Local Services

Decision:
- Local model and UI services bind to `127.0.0.1` by default.

Reason:
- Avoid exposing Jarvis or model endpoints on LAN.

Consequence:
- Remote/mobile access requires a separate explicit design.

### ADR-007: Qwen Runtime Uses One Local Ollama Provider

Decision:
- The orchestrator talks to a `ModelClient` interface, and the current accepted provider is local Ollama at `http://127.0.0.1:11434` using `qwen2.5:3b`.
- Every agent, subagent, profile, and verifier prompt uses that same model.

Reason:
- The current MVP needs one predictable local model boundary with no cloud fallback or hidden provider variation.

Consequence:
- Future adapters can be designed, but they are not active providers unless this decision is explicitly revised.

## Proposed Decisions Needing User Choice

### PDR-001: Preferred Local Model Runtime

Options:
- Current accepted baseline: Ollama on `http://127.0.0.1:11434` with `qwen2.5:3b`.
- Future-only alternatives: llama.cpp server, LM Studio, vLLM, or OpenAI-compatible local servers.

Recommendation:
- Keep the live target as Ollama `qwen2.5:3b` until there is a concrete reason to revise the single-provider baseline.

Decision needed:
- Whether any future adapter is valuable enough to justify revising the current single-provider baseline.

### PDR-002: Implementation Language

Options:
- Python: best fit for local automation, scripts, STT/TTS ecosystem, Office/Windows automation.
- TypeScript: strong for UI and MCP servers.
- Hybrid: Python core plus optional local web UI.

Recommendation:
- Python core first, optional TypeScript/HTML UI later.

Decision needed:
- Confirm Python-first.

### PDR-003: UI Strategy

Options:
- CLI only.
- Local web UI.
- Tray app.
- Desktop overlay.

Recommendation:
- CLI first, loopback web UI second.

Decision needed:
- Whether to build web UI before voice.

### PDR-004: Voice Stack

Options:
- whisper.cpp.
- faster-whisper.
- Windows speech APIs.
- Piper or Windows voices for TTS.

Recommendation:
- Decide after text MVP. Use push-to-talk first.

Decision needed:
- Which local STT/TTS stack to install or use.

### PDR-005: Memory Store

Options:
- JSONL only.
- SQLite.
- SQLite plus local vector index.
- Filesystem markdown memory.

Recommendation:
- JSONL for MVP, SQLite plus embeddings later.

Decision needed:
- Whether inspectability or query complexity matters more initially.

## Open Technical Questions

- What are the laptop specs: RAM, GPU, VRAM, CPU?
- Which Qwen model sizes are already installed, if any?
- Is Ollama, LM Studio, or llama.cpp already installed?
- Should Jarvis integrate with existing Codex skills directly or copy selected workflows into its own tool registry?
- Should runtime logs be encrypted locally?
- Should Jarvis have a local password/PIN for high-impact approvals?
- Should memory be per-project, global, or both?
- Should voice be always-on eventually or only push-to-talk?
- Should app automation use APIs only, or allow UI automation with coordinates after approval?

## Decision Review Cadence

Review ADRs:
- After Text MVP.
- Before adding command execution.
- Before adding voice.
- Before adding desktop/app automation.
- Before adding multi-agent autonomy.
