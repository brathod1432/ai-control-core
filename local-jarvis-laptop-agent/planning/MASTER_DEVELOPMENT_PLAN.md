# Master Development Plan

## 1. Project Vision

Build a local-first Jarvis-like laptop assistant that can run on a personal Windows laptop using a local/offline model such as Qwen. Jarvis should help with reasoning, planning, local files, coding, browser inspection, Office documents, memory, and eventually voice interaction while preserving privacy and requiring approval for risky actions.

The north star is not "an AI that can do anything". The north star is "a dependable local chief-of-staff for the laptop" with clear permissions, visible actions, safe defaults, and incremental trust.

## 2. Product Principles

Local-first:
- No cloud model calls by default.
- No telemetry, analytics, or uploads by default.
- External network requires explicit approval for destination, data, credentials, and purpose.

Permissioned autonomy:
- Chat, inspect, propose, edit, execute, automate, and external actions are separate levels.
- The assistant starts at read-only/proposal mode.
- Higher autonomy is enabled per tool, per target, or per session.

Observable operation:
- Tool calls are visible.
- Actions are summarized in a local audit log.
- Risky operations have dry-run or confirmation.
- Failures are reported, not hidden.

Modular architecture:
- Model runtime, orchestrator, memory, tools, voice, desktop control, and multi-agent crews are independently testable.
- A broken voice module should not break the text assistant.
- A tool integration should be removable without rewiring the core.

Human-centered personality:
- Calm, concise, capable, and lightly personable.
- Does not pretend to have done things it did not do.
- Asks for confirmation without being annoying.
- Explains risk in plain language.

## 3. Non-Goals

The initial project will not:
- Replace a full operating system shell.
- Run arbitrary commands without approval.
- Read secrets, browser profiles, cookies, password managers, or personal folders by default.
- Download models or packages automatically.
- Use cloud services silently.
- Control email, messaging, payments, deployments, or public posting without per-action approval.
- Implement always-listening wake word before push-to-talk and transcript review are stable.
- Build a fully autonomous "do everything" agent without human gates.

## 4. Target User Experience

MVP experience:
- User starts a local text loop.
- Jarvis answers questions through a local model endpoint.
- Jarvis can inspect explicitly approved files.
- Jarvis can propose commands or edits.
- Jarvis asks before executing commands, writing files, using network, or controlling apps.
- User can inspect logs and config.

Intermediate experience:
- Jarvis can search local project files, summarize documents, propose patches, and run safe checks after approval.
- Jarvis remembers approved preferences and project facts.
- Jarvis can inspect a local browser tab or Office document through separate approved modules.

Advanced experience:
- User uses push-to-talk voice.
- Jarvis shows the transcript and responds with local TTS.
- Jarvis can coordinate specialist subagents for coding, browser inspection, document work, and verification.
- Jarvis can use local app skills while preserving explicit approvals.

## 5. System Architecture

Primary runtime components:
- Interface layer: CLI first, then local web UI, then voice.
- Safety gate: policy engine for risk classification and approval.
- Core orchestrator: intent classification, context assembly, model call, tool routing, response synthesis.
- Local model provider: Qwen via Ollama, llama.cpp, LM Studio, or OpenAI-compatible local endpoint.
- Tool registry: typed local tools with permission metadata.
- Memory/RAG: session, task, project, and user-approved long-term memory.
- Audit log: local structured events.
- Optional multi-agent crew: specialists coordinated by core orchestrator.

Data flow:
1. User input enters interface layer.
2. Input is normalized and sent to safety gate.
3. Orchestrator classifies intent and builds context.
4. Memory retrieval runs if allowed.
5. Local model produces response or tool request.
6. Safety gate validates tool request.
7. Tool executes if allowed or approval is requested.
8. Result is verified and summarized.
9. Audit event is written.
10. Response is returned to user.

## 6. Development Strategy

Use a staged trust ladder:
- First make it answer safely.
- Then make it inspect safely.
- Then make it propose safely.
- Then make it act safely.
- Then make it speak.
- Then make it coordinate specialists.

Use feature flags:
- `enable_memory_write`
- `enable_shell_execute`
- `enable_file_write`
- `enable_browser_control`
- `enable_office_control`
- `enable_voice`
- `enable_wake_word`
- `enable_multi_agent`
- `enable_network`

Use local artifacts:
- Keep project templates in repo.
- Keep runtime memory/logs outside repo, such as `%USERPROFILE%\.local-jarvis`.
- Never commit sensitive runtime logs or memories.

## 7. Milestone Plan

### Milestone 0: Planning And Skeleton

Goal:
- Establish project shape, docs, configs, and safety model.

Deliverables:
- Planning docs.
- Architecture docs.
- Security model.
- Config schema draft.
- Tool registry schema draft.
- Minimal local loop example.

Acceptance criteria:
- No default network dependency.
- No package install required for docs/examples.
- Safety gates are specified before any powerful tools.

Exit risks:
- Local model runtime not selected.
- Hardware constraints unknown.
- Voice stack not selected.

### Milestone 1: Text MVP

Goal:
- A local text assistant that can chat with a local model endpoint and enforce approval boundaries.

Core features:
- CLI entrypoint.
- Config loader.
- Local model client.
- Basic system prompt.
- Intent classifier.
- Safety gate.
- Audit log.
- Approval prompt abstraction.

Implementation tasks:
- Create Python package skeleton.
- Add config validation.
- Implement local model adapter for Ollama-style `/api/chat`.
- Add OpenAI-compatible local adapter abstraction.
- Implement `RiskDecision` object.
- Add local audit event writer.
- Add deterministic dry-run mode for tests.

Acceptance criteria:
- Starts without external network.
- If local model endpoint is unavailable, reports a local connection error.
- Refuses or asks approval for network, shell, file write, desktop control, and high-impact actions.
- Logs non-sensitive summaries locally.
- Unit tests cover intent/risk decisions.

### Milestone 2: Read-Only Local Tools

Goal:
- Jarvis can inspect explicitly scoped local data without unsafe broad access.

Core features:
- File metadata tool.
- Text file read tool with line limits.
- Directory list tool with explicit root scope.
- Search tool with exclude patterns.
- Runtime environment info tool that avoids secrets.
- Tool registry with schemas and permission classes.

Implementation tasks:
- Define `ToolSpec`.
- Define `ToolResult`.
- Add path scope validation.
- Add output truncation.
- Add secret-pattern redaction.
- Add tests for path traversal and out-of-scope denial.

Acceptance criteria:
- Cannot read outside approved workspace/root.
- Refuses `.env`, private keys, credential paths, and browser profiles by default.
- Tool outputs are bounded.
- Audit log records tool name and summary, not raw sensitive content.

### Milestone 3: Proposal And Patch Mode

Goal:
- Jarvis can propose safe file changes and optionally write scoped changes after confirmation.

Core features:
- Patch proposal generation.
- Apply patch tool behind explicit scope.
- Backup policy for important documents.
- Diff summary.
- Verification command proposal.

Implementation tasks:
- Create patch format contract.
- Add write-scope allowlist.
- Add "propose only" mode.
- Add "apply after approval" mode.
- Add changed file summary.
- Add rollback-neutral guidance.

Acceptance criteria:
- No broad rewrites.
- No overwrite outside scope.
- Shows proposed files before applying.
- Reports changed files and verification.

### Milestone 4: Local Command Runner

Goal:
- Jarvis can run safe local commands only when approved and bounded.

Core features:
- Command proposal.
- Approval prompt.
- Safe command allowlist.
- Working directory enforcement.
- Timeout.
- Output redaction/truncation.

Implementation tasks:
- Add command classifier.
- Block destructive patterns by default.
- Require explicit approval for shell commands.
- Add timeout and process cleanup.
- Add test fixtures.

Acceptance criteria:
- Blocks `git reset --hard`, broad deletes, forced checkouts, recursive deletes, permission changes, and network installers.
- Runs harmless local checks when approved.
- Redacts secrets from output.
- Reports command, cwd, exit code, and summary.

### Milestone 5: Local Memory And RAG

Goal:
- Jarvis remembers approved facts and project notes locally.

Core features:
- Memory record schema.
- Memory write approval.
- Memory search.
- Memory edit/delete/export.
- Optional local embeddings adapter.
- Source attribution.

Implementation tasks:
- Start with JSONL memory store.
- Add memory types: user preference, project note, task summary.
- Add memory review command.
- Add forgetting commands.
- Add retrieval budget.
- Add stale-memory warning.

Acceptance criteria:
- Memory writes require approval.
- User can inspect and delete memory.
- Sensitive data is not persisted by default.
- Retrieved memory never overrides current local evidence.

### Milestone 6: Local Browser And Office Awareness

Goal:
- Jarvis can use approved local browser and Office inspection workflows by integrating the previously created skills.

Core features:
- Chrome/CDP tab list and screenshot through loopback only.
- DOM/accessibility summary.
- Console/network metadata summary.
- Office file inventory and safe copy workflow.
- Render/validation hooks where available.

Implementation tasks:
- Add browser tool specs.
- Add Office tool specs.
- Add explicit target selection.
- Add screenshot artifact policy.
- Add cookie/storage refusal rules.
- Add macro/link refusal rules.

Acceptance criteria:
- Does not dump cookies, storage, tokens, hidden fields, or private profile data.
- Does not run macros or refresh external links without approval.
- Writes artifacts under approved local directory.
- Can summarize approved local app state.

### Milestone 7: Voice Interface

Goal:
- Add local voice input/output without weakening safety.

Core features:
- Push-to-talk.
- Local STT adapter.
- Visible transcript.
- Local TTS adapter.
- Interrupt/cancel.
- Confirmation phrase for risky actions.

Implementation tasks:
- Select STT/TTS with explicit user approval if installs/models are needed.
- Add voice config.
- Add transcript review.
- Add "cancel" and "stop" handling.
- Add confidence threshold.
- Add noisy-room tests.

Acceptance criteria:
- No external audio processing by default.
- Transcript is visible before risky action.
- Low confidence transcription does not execute actions.
- User can disable voice.

### Milestone 8: Multi-Agent Crew

Goal:
- Add optional specialist workers for complex tasks.

Core features:
- Coordinator prompts.
- Worker manifests.
- Disjoint ownership.
- Fan-out/fan-in.
- Verifier/critic role.
- Shared artifact handoff.

Implementation tasks:
- Implement local agent task manifests.
- Add worker prompt templates.
- Add result schema.
- Add conflict detection for overlapping paths.
- Add verifier gate.

Acceptance criteria:
- Coordinator always owns final integration.
- Workers do not overlap write scopes.
- Sensitive context is minimized.
- Verification happens before final response.

### Milestone 9: Local UI And Dashboard

Goal:
- Make Jarvis usable beyond CLI while keeping local boundaries.

Core features:
- Loopback-only web UI.
- Conversation view.
- Approval queue.
- Tool call timeline.
- Memory browser.
- Config editor.

Implementation tasks:
- Choose local UI stack.
- Bind to `127.0.0.1`.
- Add CSRF/local auth consideration.
- Add log viewer.
- Add permission toggles.

Acceptance criteria:
- UI is not exposed on LAN by default.
- Approval decisions are explicit.
- Memory can be inspected and deleted.
- Tool timeline is readable.

### Milestone 10: Personal OS Layer

Goal:
- Jarvis becomes a practical local executive assistant.

Core features:
- Local notes integration.
- Local task list.
- Calendar integration only if local/approved.
- Routine automations.
- Daily brief generated from approved local sources.

Implementation tasks:
- Define connector contracts.
- Add local notes folder connector.
- Add task JSON store.
- Add brief generation.
- Add schedule/reminder policy.

Acceptance criteria:
- No cloud sync unless approved.
- User controls sources.
- Generated briefs cite local sources.
- Automations can be paused or disabled.

## 8. Workstreams

### Workstream A: Core Runtime

Owns:
- Config loader.
- Model clients.
- Orchestrator.
- Intent/risk classifier.
- Audit logging.

Dependencies:
- None for skeleton.
- Model endpoint for live tests.

### Workstream B: Safety And Permissions

Owns:
- Policy engine.
- Approval UX.
- Secret/path guards.
- Redaction.
- High-impact action gates.

Dependencies:
- Tool registry.

### Workstream C: Tools And MCP

Owns:
- Tool specs.
- Tool executor.
- Local filesystem tools.
- Command runner.
- Browser/Office adapters.

Dependencies:
- Safety engine.

### Workstream D: Memory

Owns:
- Memory schema.
- Memory store.
- Retrieval.
- Forgetting.
- Optional embeddings.

Dependencies:
- Config and safety engine.

### Workstream E: Interfaces

Owns:
- CLI.
- Local UI.
- Voice.
- Transcript/approval surfaces.

Dependencies:
- Core runtime and safety.

### Workstream F: Multi-Agent

Owns:
- Worker manifests.
- Handoff contracts.
- Coordinator logic.
- Verifier loop.

Dependencies:
- Core runtime, tools, safety, memory.

### Workstream G: Evaluation And Ops

Owns:
- Test suite.
- Golden tasks.
- Safety tests.
- Regression tests.
- Release checklist.
- Incident runbook.

Dependencies:
- All feature workstreams.

## 9. Suggested Repository Structure For Implementation

If implementation code is added later, use:

```text
local-jarvis-laptop-agent/
  src/
    jarvis/
      __init__.py
      app.py
      config.py
      orchestrator.py
      safety.py
      model_runtime/
      tools/
      memory/
      audit/
      interfaces/
      agents/
  tests/
    unit/
    integration/
    safety/
  planning/
  architecture/
  config/
  examples/
  validation/
```

Do not put runtime secrets, logs, memory, or downloaded models in the repo.

## 10. Risk Register

Risk: model hallucination causes false claims.
- Mitigation: require tool evidence before claiming action completion.

Risk: unsafe shell execution.
- Mitigation: proposal-first, explicit approval, blocklist, allowlist, timeouts.

Risk: accidental secret exposure.
- Mitigation: forbidden paths, redaction, no secret memory, no broad scans.

Risk: browser privacy leak.
- Mitigation: no cookies/storage dumps, loopback-only CDP, user-selected tabs.

Risk: voice misrecognition triggers action.
- Mitigation: transcript display, confirmation, confidence threshold, push-to-talk first.

Risk: memory becomes creepy or stale.
- Mitigation: approval for writes, inspect/delete/export, source/confidence/expiry.

Risk: multi-agent chaos.
- Mitigation: coordinator-owned integration, disjoint scopes, bounded handoffs, verifier gate.

Risk: local model too slow.
- Mitigation: model profiles, small classifier model, caching, task routing.

Risk: UI exposed on network.
- Mitigation: bind to loopback, require local auth if needed.

## 11. Definition Of Done

For any feature:
- It has a clear permission class.
- It has tests or documented manual validation.
- It logs safe summaries.
- It handles failure gracefully.
- It does not require network by default.
- It does not read secrets by default.
- It has user-facing documentation.
- It can be disabled.

For any milestone:
- Acceptance criteria pass.
- Safety tests pass.
- Known limitations are documented.
- Next milestone risks are updated.

## 12. First Build Recommendation

Start with Milestones 1 and 2 only:
- Text CLI.
- Local model adapter.
- Safety gate.
- Audit log.
- Read-only file tools.

Do not start with:
- Wake word.
- Desktop clicking.
- Email integration.
- Always-on memory.
- Multi-agent autonomy.

The glamorous parts will be more fun once the boring spine is trustworthy. Very Jarvis, actually: all elegance on the outside, very disciplined machinery underneath.

