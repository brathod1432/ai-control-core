# Roadmap

## Current Model Baseline

All agents and subagents use the same single local Ollama `qwen2.5:3b` model through `http://127.0.0.1:11434`. No cloud LLMs, remote model APIs, separate providers, or per-agent model pools are part of this roadmap.

## Phase 0: Design

Deliverables:
- Architecture.
- Permission model.
- Tool registry.
- Local config template.
- Smoke tests.

Exit criteria:
- No unsafe default actions.
- Model runtime choices are documented.

## Phase 1: Text MVP

Capabilities:
- CLI text chat.
- Local model endpoint.
- Read-only tools.
- Local audit log.
- Approval prompts.

Exit criteria:
- Can answer local questions.
- Can inspect a scoped file.
- Refuses network and destructive actions without approval.

## Phase 2: Local Tools

Capabilities:
- Filesystem read/search.
- Safe patch proposal.
- Local command dry-run.
- Project memory.

Exit criteria:
- Can produce a plan and patch proposal.
- Can run safe local checks when approved.

## Phase 3: App Awareness

Capabilities:
- Local Chrome/CDP inspection.
- Office file automation.
- Screenshot or active-window summaries.

Exit criteria:
- Can inspect approved local app state.
- Does not dump cookies, secrets, or private storage.

## Phase 4: Voice

Capabilities:
- Push-to-talk.
- Local STT.
- Local TTS.
- Interrupt/cancel.

Exit criteria:
- Text transcript is visible.
- Risky actions still require explicit confirmation.

## Phase 5: Multi-Agent

Capabilities:
- Specialist workers.
- Critic/verifier.
- Multi-agent coding/document/browser workflows.

Exit criteria:
- Coordinator owns final integration.
- Workers have disjoint scopes.
- Verification is required before final response.

## Phase 6: Personal OS Layer

Capabilities:
- Local calendar/task/note connectors.
- User-approved long-term memory.
- Routine automation.
- Local dashboard.

Exit criteria:
- Memory is inspectable and editable.
- User can revoke permissions.
- All external sync remains opt-in.
