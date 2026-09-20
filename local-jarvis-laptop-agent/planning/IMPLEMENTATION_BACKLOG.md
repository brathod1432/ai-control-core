# Implementation Backlog

## Current Model Baseline

All agents and subagents use the same single local Ollama `qwen2.5:3b` model through `http://127.0.0.1:11434`. No cloud LLMs, remote model APIs, separate providers, or per-agent model pools are part of this backlog.

## Epic 1: Project Skeleton

### Story 1.1: Create Python Package Skeleton

Goal:
- Establish maintainable code layout for Jarvis implementation.

Tasks:
- Create `src/jarvis/`.
- Add `__init__.py`.
- Add `app.py` entrypoint.
- Add module folders: `model_runtime`, `tools`, `memory`, `audit`, `interfaces`, `agents`.
- Add `tests/` folders.

Acceptance criteria:
- Package imports locally.
- Entry point can print version/help without model runtime.
- No network required.

Dependencies:
- None.

### Story 1.2: Define Configuration Schema

Goal:
- Load safe local defaults from JSON.

Tasks:
- Define config dataclasses.
- Load `config/jarvis.local.example.json`.
- Validate loopback model URL.
- Validate storage paths.
- Validate feature flags.
- Add config error messages.

Acceptance criteria:
- Missing config falls back to safe defaults.
- Non-loopback model URLs are rejected unless network is explicitly enabled.
- Invalid permission values produce clear errors.

Dependencies:
- Story 1.1.

## Epic 2: Model Runtime

### Story 2.1: Local Model Client Interface

Goal:
- Abstract local model calls.

Tasks:
- Define `ModelClient`.
- Define request/response objects.
- Add timeout handling.
- Add cancellation-friendly structure.
- Add redacted error messages.

Acceptance criteria:
- Fake model client can be used in tests.
- Runtime errors do not crash the CLI.

### Story 2.2: Ollama-Compatible Adapter

Goal:
- Support local Qwen through Ollama-style `/api/chat`.

Tasks:
- Implement JSON request.
- Implement non-streaming response.
- Add friendly endpoint-down message.
- Add model profile selection.
- Add test with mocked HTTP response.

Acceptance criteria:
- Sends requests only to configured loopback URL by default.
- Handles unavailable endpoint.
- Handles malformed response.

### Story 2.3: OpenAI-Compatible Local Adapter

Goal:
- Keep a future local-only adapter option documented, but do not enable a second provider while the current baseline is single-model Ollama.

Tasks:
- Implement `/v1/chat/completions` adapter.
- Support model, temperature, max tokens.
- Block remote URLs by default.
- Add mocked tests.

Acceptance criteria:
- Works against fake local endpoint.
- Refuses non-loopback unless network is explicitly approved.
- Remains disabled unless the single-provider baseline is deliberately revised.

## Epic 3: Orchestrator

### Story 3.1: Intent Classifier

Goal:
- Classify user request risk before model/tool action.

Intent labels:
- chat
- recall
- inspect
- plan
- act
- automate
- external
- high_impact

Tasks:
- Implement keyword/rule baseline.
- Add model-assisted classifier later behind safe fallback.
- Add tests for obvious risky requests.

Acceptance criteria:
- "delete", "send", "deploy", "buy", "push", "download", and "read cookies" are high risk or approval-required.
- Local explanation requests are low risk.

### Story 3.2: Decision Engine

Goal:
- Decide answer/tool/approval/refusal.

Tasks:
- Define `RiskDecision`.
- Map intent to permission requirement.
- Integrate feature flags.
- Support one concise clarification question.

Acceptance criteria:
- Returns deterministic decision for test prompts.
- Blocks high-impact actions by default.

### Story 3.3: Conversation Loop

Goal:
- Run user input through safety, model, and response.

Tasks:
- Build CLI loop.
- Inject system prompt.
- Maintain session messages.
- Trim context when needed.
- Add `/exit`, `/config`, `/help`, `/permissions`.

Acceptance criteria:
- User can chat locally.
- User can inspect current permission status.
- Long sessions compact safely.

## Epic 4: Safety Gate

### Story 4.1: Permission Classes

Goal:
- Represent permissions consistently.

Classes:
- read_local
- write_local
- execute_local
- automate_app
- network
- high_impact

Tasks:
- Implement enum.
- Add policy map.
- Add approval requirements.

Acceptance criteria:
- Every tool declares a permission class.
- Unknown permission class fails closed.

### Story 4.2: Approval Flow

Goal:
- Ask clear approval before risky actions.

Tasks:
- Define approval request object.
- Add CLI approval prompt.
- Record approved/denied.
- Add safer alternative field.

Acceptance criteria:
- Approval prompt includes action, target, data, side effects, reason, safer alternative.
- Denial stops the action cleanly.

### Story 4.3: Redaction And Secret Guard

Goal:
- Prevent accidental secret exposure.

Tasks:
- Add forbidden path patterns.
- Add secret-like regex redaction.
- Add output truncation.
- Add tests with fake tokens.

Acceptance criteria:
- `.env`, private key names, browser profiles, credential caches are denied by default.
- Token-like strings are redacted in logs.

## Epic 5: Tool Registry

### Story 5.1: ToolSpec And ToolResult

Goal:
- Standardize tool execution.

Tasks:
- Define tool schema.
- Define output schema.
- Define error schema.
- Add side-effect metadata.
- Add dry-run flag.

Acceptance criteria:
- Tools can be listed.
- Tools can be disabled.
- Tool result includes success, summary, artifacts, and redaction status.

### Story 5.2: Tool Executor

Goal:
- Safely execute tools after safety checks.

Tasks:
- Implement registry.
- Implement `execute_tool`.
- Check permissions before execution.
- Log tool event.
- Return structured result.

Acceptance criteria:
- Disabled tools cannot run.
- Permission denial returns structured error.

## Epic 6: Read-Only Filesystem Tools

### Story 6.1: Scoped File Read

Goal:
- Read text files under approved roots.

Tasks:
- Validate paths.
- Deny secrets.
- Limit bytes/lines.
- Return line ranges.

Acceptance criteria:
- Path traversal denied.
- Out-of-root denied.
- Binary files handled safely.

### Story 6.2: Directory List

Goal:
- List approved directories safely.

Tasks:
- Exclude hidden/secret paths by default.
- Limit entry counts.
- Support file metadata.

Acceptance criteria:
- Broad user profile listing denied unless approved.
- Output bounded.

### Story 6.3: Search

Goal:
- Search approved roots.

Tasks:
- Support glob or ripgrep when available.
- Exclude `.git`, `.venv`, `node_modules`, secrets.
- Limit results.

Acceptance criteria:
- Does not search whole disk by default.
- Reports truncated results.

## Epic 7: Patch And Write Tools

### Story 7.1: Patch Proposal

Goal:
- Generate reviewable patches without applying.

Tasks:
- Create patch plan format.
- Include files affected.
- Include rollback note.

Acceptance criteria:
- User can review before applying.
- No file changes in proposal-only mode.

### Story 7.2: Scoped Apply Patch

Goal:
- Apply approved local edits.

Tasks:
- Enforce write root.
- Check existing file state.
- Apply patch.
- Verify file read-back.

Acceptance criteria:
- Cannot edit outside approved scope.
- Reports changed files.

## Epic 8: Command Runner

### Story 8.1: Command Proposal

Goal:
- Propose commands before running.

Tasks:
- Classify command risk.
- Explain why needed.
- Show working directory.

Acceptance criteria:
- Destructive commands are blocked or require explicit special approval.

### Story 8.2: Safe Execution

Goal:
- Run approved commands.

Tasks:
- Add timeout.
- Capture stdout/stderr.
- Redact output.
- Return exit code.

Acceptance criteria:
- Timeout kills process.
- Output is bounded.
- Exit code reported.

## Epic 9: Memory

### Story 9.1: JSONL Memory Store

Goal:
- Persist approved memories locally.

Tasks:
- Define record schema.
- Add write/read/delete.
- Add source and timestamp.

Acceptance criteria:
- User approval required for long-term writes.
- User can delete records.

### Story 9.2: Retrieval

Goal:
- Retrieve relevant memories.

Tasks:
- Start with keyword search.
- Add embedding adapter later.
- Enforce retrieval budget.

Acceptance criteria:
- Retrieved records include source.
- Sensitive memories are not used unless explicitly allowed.

## Epic 10: Browser And Office Modules

### Story 10.1: Browser Inspection Adapter

Goal:
- Integrate local CDP inspection.

Tasks:
- List tabs from loopback.
- Select tab by user.
- Screenshot approved tab.
- DOM/a11y summary.

Acceptance criteria:
- Loopback-only.
- No cookies/storage.
- User-selected target.

### Story 10.2: Office File Adapter

Goal:
- Inspect and modify Office files safely.

Tasks:
- File inventory.
- Macro/link detection.
- Copy-before-edit.
- Render validation hooks.

Acceptance criteria:
- Does not run macros by default.
- Does not overwrite originals by default.

## Epic 11: Voice

### Story 11.1: Push-To-Talk Interface

Goal:
- Add voice input after text core is safe.

Tasks:
- Select local STT.
- Add transcript display.
- Add confidence threshold.

Acceptance criteria:
- Risky actions require transcript confirmation.

### Story 11.2: TTS Response

Goal:
- Speak responses locally.

Tasks:
- Select local TTS.
- Add voice settings.
- Add mute/stop.

Acceptance criteria:
- User can disable TTS.
- No external audio.

## Epic 12: Multi-Agent Crew

### Story 12.1: Agent Manifest Loader

Goal:
- Load specialist definitions.

Tasks:
- Parse agent manifest.
- Validate ownership.
- Validate tool permissions.

Acceptance criteria:
- Invalid overlapping scopes are flagged.

### Story 12.2: Coordinator Handoff

Goal:
- Assign bounded tasks.

Tasks:
- Create handoff contract.
- Track worker outputs.
- Integrate summaries.

Acceptance criteria:
- Coordinator final answer includes worker outputs and verification.

### Story 12.3: Verifier Gate

Goal:
- Add critic/verifier before final response for complex tasks.

Tasks:
- Define verifier prompt.
- Define pass/fail rubric.
- Add max iteration count.

Acceptance criteria:
- No infinite loops.
- Verification failures are reported.

## Epic 13: Local UI

### Story 13.1: Loopback Web UI

Goal:
- Provide local dashboard.

Tasks:
- Choose minimal UI stack.
- Bind to 127.0.0.1.
- Add conversation view.
- Add approval queue.

Acceptance criteria:
- Not exposed on LAN by default.
- Approval decisions are clear.

### Story 13.2: Memory And Logs Browser

Goal:
- Make memory/logs inspectable.

Tasks:
- List memory records.
- Delete records.
- Show audit events.
- Redact sensitive details.

Acceptance criteria:
- User can inspect and delete memory.
