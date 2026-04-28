# Local Jarvis Laptop Agent

This directory is a standalone local-first skill and architecture pack for building a Jarvis-like laptop agent powered by an offline or locally hosted model such as Qwen.

The goal is not to create a flashy chatbot. The goal is a useful local executive assistant that can listen, reason, remember, inspect the laptop state, operate approved local tools, and ask before doing risky things.

## Current Model Baseline

All agents and subagents use the same single local Ollama model, `qwen2.5:3b`, through `http://127.0.0.1:11434`. No cloud LLMs, remote model APIs, separate model providers, or per-agent model pools are part of the current design.

## Principles

- Local-first: no cloud calls by default.
- Offline-capable: model runtime should work without internet after models are already present.
- Permissioned autonomy: read, propose, modify, and execute are separate authority levels.
- Human-in-the-loop: destructive, external, financial, credential, or identity-affecting actions require explicit approval.
- Observable: every tool call should be visible, logged locally, and reversible where practical.
- Modular: voice, memory, planning, model runtime, desktop control, and app integrations are separate skills.

## Recommended Stack

Current local MVP runtime:
- Ollama endpoint: `http://127.0.0.1:11434`
- Model: `qwen2.5:3b`
- Scope: every agent, subagent, profile, and verifier prompt uses this same model.

Future runtime alternatives such as llama.cpp, LM Studio, vLLM, coder-specific models, embedding models, or local speech models require explicit redesign and approval before use. They are not active providers in the current pack.

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

## Current Implemented Capabilities

- Chat through local Ollama `qwen2.5:3b`.
- Safety classification for chat, read-only inspection, local writes, command execution, app automation, network, and high-impact requests.
- Read-only inspection of explicitly scoped local files or folders under the approved local project root, currently `C:\Users\kbrat\PycharmProjects`.
- Bounded project evidence collection: recursive file listing, file type/size counts, safe text snippets, noisy directory exclusions, binary skipping, secret-path snippet skipping, and hard limits for depth/files/bytes.
- Local audit logs and local session transcripts.

Not implemented yet:
- Web browsing/search.
- Reminders, alarms, email, messaging, or calendar actions.
- Desktop/app automation.
- File creation/modification tools for user requests.

## Minimum Viable Jarvis

The smallest useful version has:
1. Local model endpoint.
2. Typed tool registry with read-only tools.
3. Planner loop that decides whether to answer, inspect, or ask.
4. Local memory folder with summaries and user-approved facts.
5. Text interface before voice.
6. Audit log.
7. Safety gate for writes, shell commands, browser actions, Office automation, and external network.

## PowerShell Quick Start

From the repository root:

```powershell
.\local-jarvis-laptop-agent\start_jarvis.ps1
```

From inside `local-jarvis-laptop-agent`:

```powershell
.\start_jarvis.ps1
```

To run unit tests in PowerShell:

```powershell
cd .\local-jarvis-laptop-agent
$env:PYTHONPATH = "src"
python -m unittest discover -s tests/unit
```

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
