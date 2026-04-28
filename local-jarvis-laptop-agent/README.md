# Local Jarvis Laptop Agent

This directory is a standalone local-first skill and architecture pack for building a Jarvis-like laptop agent powered by an offline or locally hosted model such as Qwen.

The goal is not to create a flashy chatbot. The goal is a useful local executive assistant that can listen, reason, remember, inspect the laptop state, operate approved local tools, and ask before doing risky things.

## Principles

- Local-first: no cloud calls by default.
- Offline-capable: model runtime should work without internet after models are already present.
- Permissioned autonomy: read, propose, modify, and execute are separate authority levels.
- Human-in-the-loop: destructive, external, financial, credential, or identity-affecting actions require explicit approval.
- Observable: every tool call should be visible, logged locally, and reversible where practical.
- Modular: voice, memory, planning, model runtime, desktop control, and app integrations are separate skills.

## Recommended Stack

Offline model runtime options:
- Ollama with Qwen models for easiest local serving.
- llama.cpp server with GGUF Qwen models for tighter local control.
- LM Studio local server for UI-driven model management.
- vLLM only when GPU/server-style setup is available.

Suggested model families:
- Qwen2.5 or Qwen3 instruct models for general reasoning.
- Qwen coder models for code tasks.
- Small local embedding model for private memory retrieval.
- Optional local speech-to-text and text-to-speech models for voice.

No model download, package install, or external lookup is performed by this pack. Add models only with explicit user approval.

## Directory Map

- `SKILL.md`: root skill for using this pack.
- `SKILL_METADATA.json`: local metadata for the root skill.
- `architecture/ARCHITECTURE.md`: full system architecture.
- `architecture/ROADMAP.md`: MVP to advanced rollout plan.
- `architecture/SECURITY_MODEL.md`: local safety and permission design.
- `skills/`: subskills needed to build Jarvis.
- `examples/minimal_local_loop.py`: dependency-light local model loop example.
- `examples/agent_manifest.json`: example agent and tool registry.
- `config/jarvis.local.example.json`: local configuration template.
- `validation/SMOKE_TESTS.md`: local validation checklist.

## Minimum Viable Jarvis

The smallest useful version has:
1. Local model endpoint.
2. Typed tool registry with read-only tools.
3. Planner loop that decides whether to answer, inspect, or ask.
4. Local memory folder with summaries and user-approved facts.
5. Text interface before voice.
6. Audit log.
7. Safety gate for writes, shell commands, browser actions, Office automation, and external network.

## Advanced Jarvis

The richer version adds:
- Wake word and push-to-talk.
- Local speech-to-text and text-to-speech.
- Screen and active-window understanding.
- Local Chrome/CDP and Office automation skills.
- Calendar/file/task awareness through local connectors.
- Long-term memory with embeddings and source attribution.
- Multi-agent workers for research, coding, document work, browser inspection, and validation.
- Local MCP server for tool isolation.

