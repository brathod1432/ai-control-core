# Local Jarvis Status Tracking

Date: 2026-04-28

## Model Baseline

All Jarvis agents and subagents use the same single local Ollama model:
- Endpoint: `http://127.0.0.1:11434`
- Model: `qwen2.5:3b`
- Provider: local Ollama only

No cloud LLMs, remote model APIs, separate model providers, or per-agent model pools are part of the current design. Specialist roles may use different prompts, tools, scopes, and verification duties, but they share this one local model runtime.

## Persona, Values, And Moral Boundaries

Jarvis is designed as a calm, capable local chief-of-staff for the laptop. The persona should feel useful and lightly personable without pretending to be omniscient or autonomous beyond granted permissions.

Durable values:
- Privacy: keep prompts, files, memory, logs, screenshots, and diagnostics local unless the user explicitly approves a specific external destination and purpose.
- Honesty: report what was done, what was skipped, what failed, and what remains uncertain.
- User agency: ask before risky actions and preserve the user's ability to inspect, revoke, delete, or deny.
- Least privilege: prefer chat, inspection, and proposals before writes, commands, automation, or network.
- Non-harm: stop before destructive, credential, account, financial, deployment, messaging, or publishing actions unless explicitly approved per action.

## System Prompt Strategy

The core system prompt should be stable and small enough for the local `qwen2.5:3b` context budget. It should include:
- Identity: local Jarvis laptop assistant.
- Runtime: single local Ollama `qwen2.5:3b` at `http://127.0.0.1:11434`.
- Safety: local-first, default-deny for network and high-impact actions, no secret access, explicit approvals.
- Behavior: concise, honest, asks one clarifying question when blocked by ambiguity.
- Tool policy: no tool call unless the orchestrator and safety gate allow it.

Task prompts and subagent prompts should add only the role, scope, allowed tools, forbidden actions, and expected output. Subagents should not receive broad conversation history when a narrower brief is enough.

## Agent And Subagent Architecture

Current architecture:
- Interface layer: CLI text loop and one-shot mode.
- Safety gate: intent, risk, permission, refusal, and approval decisions.
- Core orchestrator: builds context, calls the model client, applies safety decisions, and writes audit events.
- Model runtime: Ollama-style local chat adapter for the single shared `qwen2.5:3b` model.
- Audit: local JSONL audit writer with redaction.

Planned modules:
- Read-only filesystem tools.
- Patch proposal and scoped apply-patch flow.
- Command runner with approval and bounded output.
- Local memory store and retrieval.
- Browser, app, screenshot, and Office inspection/control modules.
- Voice interface.
- Optional specialist subagents coordinated by the core orchestrator.

Subagent rule:
- The coordinator owns decomposition, context minimization, final integration, and final response.
- Subagents are role prompts over the same local model, not separate cloud services or separate model providers.

## Conversation And Memory Strategy

Conversation state:
- Keep current-session messages in memory.
- Compact long sessions into source-aware summaries when needed.
- Do not let summaries override current evidence.

Memory tiers:
- Session memory: current conversation only.
- Task memory: temporary working notes and artifacts.
- Project memory: repo conventions, commands, and architecture notes with sources.
- User memory: stable preferences only after explicit approval.

Memory rules:
- Memory writes require approval.
- Sensitive personal data, secrets, credentials, private document content, and screenshots are not persisted by default.
- Memory must be inspectable, editable, exportable, and deletable.
- Retrieval should cite or expose the memory source when it materially affects an answer.

## Browser, App, And Screenshot Capability Roadmap

Current status:
- Browser, app, desktop, screenshot, and Office automation are not implemented as runtime tools.
- They remain roadmap capabilities behind approval gates.

Roadmap:
- Screenshot or active-window summaries for approved targets.
- Read-only browser inspection through local loopback Chrome/CDP.
- Local web-app inspection for approved loopback pages.
- Office file inspection with copy-before-edit behavior.
- Reversible app-local visual mutations or highlighting.
- Scoped app interaction only after read-only inspection is reliable.

Hard stops:
- Do not read cookies, browser storage, passwords, hidden fields, credential stores, or unrelated private app data.
- Do not submit forms, send messages, publish, buy, deploy, or change accounts without per-action approval.
- Prefer file APIs and app APIs over coordinate-based UI automation.

## Completed Work And Current Status

Milestone 1 text MVP foundation is implemented:
- Python package skeleton under `src/jarvis/`.
- Shared contracts for intents, permissions, risk levels, safety decisions, model messages, tool specs, and tool results.
- Local config template with loopback Ollama endpoint and `qwen2.5:3b`.
- CLI text loop and one-shot prompt mode.
- Config loader with loopback runtime validation.
- Ollama-compatible local model adapter.
- Jarvis persona/system prompt builder with local-model and verified-action constraints.
- Local JSONL and Markdown session transcripts with bounded in-memory context compression.
- Lightweight logical agent/subagent role prompts that share the same single Qwen model client.
- Read-only local filesystem inspection for explicitly scoped paths under `C:\Users\kbrat\PycharmProjects`, with excluded noisy directories, bounded snippets, secret-path snippet skipping, binary skipping, and hard depth/file/byte caps.
- Capability gate scaffolding for web, local browser/CDP, screenshots, app inspection, and desktop automation.
- `start_jarvis.ps1` local starter that checks Ollama and `qwen2.5:3b` before launching the CLI.
- Intent classifier and safety decision engine.
- Approval prompt abstraction.
- Redacted local JSONL audit writer.
- Unit tests for contracts, config, model runtime, safety, audit, orchestrator, persona, history, agent roles, capability gates, read-only filesystem inspection, and the start script.

Existing validation record:

```text
PYTHONPATH=src python -m unittest discover -s tests/unit
Ran 50 tests in 0.136s
OK
```

Live local model validation recorded in existing docs:
- `GET http://127.0.0.1:11434/api/tags` found `qwen2.5:3b`.
- Direct Ollama chat smoke test returned `local qwen ready`.
- Jarvis CLI smoke test returned a local Jarvis safety confirmation.

## Limitations And Next Steps

Current limitations:
- Read-only filesystem inspection is implemented for explicitly scoped local project paths, but it is not a general unrestricted disk crawler.
- No patch proposal/apply workflow yet.
- No command runner yet.
- No memory store or retrieval implementation yet.
- No browser, Office, screenshot, app-control, voice, or multi-agent runtime yet.
- No OpenAI-compatible local adapter is currently implemented; the current committed runtime target is Ollama.

Recommended next steps:
1. Add a more formal tool registry wrapper around the read-only filesystem inspector before enabling write or command tools.
2. Add richer deterministic project summarization for common stacks while keeping Qwen evidence-bounded.
3. Add memory store only after approval, inspect, delete, and export flows are designed.
4. Add browser/app/screenshot inspection as read-only modules before any control actions.
5. Keep all subagent prompts bound to the same single local Ollama `qwen2.5:3b` runtime.

## Local Run And Test Instructions

From `local-jarvis-laptop-agent`:

```powershell
$env:PYTHONPATH = "src"
python -m unittest discover -s tests/unit
```

With Ollama already running locally and `qwen2.5:3b` already available:

```powershell
$env:PYTHONPATH = "src"
python -m jarvis --config config\jarvis.local.example.json --once "Say local model ready and do not call any tools."
```

From the repository root, start the interactive assistant with:

```powershell
.\local-jarvis-laptop-agent\start_jarvis.ps1
```

Expected constraints:
- These commands should not contact external network services.
- Model traffic should stay on `http://127.0.0.1:11434`.
- Tests should pass without package installs because `pyproject.toml` declares no runtime dependencies.
