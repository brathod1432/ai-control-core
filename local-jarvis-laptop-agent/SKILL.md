---
name: local-jarvis-laptop-agent
description: Use when designing or building a local Jarvis-like laptop assistant with offline/local models such as Qwen, local tools, voice, memory, desktop control, app automation, local browser/Office integration, MCP tools, safety gates, and optional multi-agent workflows. Keep all work local by default and require explicit approval before network, installs, model downloads, or high-impact actions.
category: local-agent
---

## Internal Safety Override

- Status: active for local design and local prototype creation only.
- Do not download models, install packages, contact model hubs, browse docs, call cloud APIs, upload logs, or transmit local data unless the user explicitly approves the exact destination and purpose.
- Do not read secrets, `.env`, browser profiles, cookies, tokens, password managers, SSH keys, cloud credentials, private documents, or unrelated personal folders by default.
- Do not run shell commands, desktop automation, browser automation, Office automation, file writes, or app-control actions unless the user request clearly authorizes that local action and the target scope is explicit.
- Never perform destructive actions, purchases, messages, emails, account changes, deployments, public posts, or security-sensitive operations without explicit per-action approval.
- Prefer text-only prototype before voice. Prefer read-only tools before write tools.
- Audit categories: command, network, secrets, privacy, desktop automation, browser automation, local app state, agent autonomy.

# Local Jarvis Laptop Agent

Use this pack to design and build a local personal assistant that runs on the user's laptop and uses a local/offline model such as Qwen.

## Current Model Baseline

All agents and subagents use the same single local Ollama `qwen2.5:3b` model through `http://127.0.0.1:11434`. No cloud LLMs, remote model APIs, separate providers, or per-agent model pools are allowed by the current design.

## Subskills

Read only the relevant subskill:
- `skills/jarvis-core-orchestrator/SKILL.md`: central planner, autonomy ladder, conversation loop, routing, and audit log.
- `skills/offline-qwen-runtime/SKILL.md`: local Qwen runtime choices, model profiles, endpoint contracts, and hardware-aware configuration.
- `skills/voice-interface/SKILL.md`: wake word, push-to-talk, local STT/TTS, interruption, and voice safety.
- `skills/desktop-and-app-control/SKILL.md`: OS/app automation, screenshots, active window analysis, browser and Office control, and approval gates.
- `skills/local-memory-rag/SKILL.md`: private long-term memory, retrieval, embeddings, source maps, and forgetting.
- `skills/tool-orchestration-mcp/SKILL.md`: tool registry, MCP server design, schemas, permissions, and dry-run behavior.
- `skills/multi-agent-crew/SKILL.md`: optional specialist workers for coding, browser inspection, document work, research, and verification.

## Standard Design Workflow

1. Define Jarvis persona and boundaries: helpful, calm, local-first, does not pretend to be omniscient.
2. Choose MVP interface: command-line text first, then local UI, then voice.
3. Choose local model runtime: Ollama, llama.cpp server, LM Studio local server, or another approved local runtime.
4. Define autonomy levels and tool permissions.
5. Build read-only tool registry first.
6. Add memory with explicit user-approved writes.
7. Add write tools only behind confirmation gates.
8. Add browser, Office, and desktop automation as separate modules.
9. Add voice only after text loop is safe and observable.
10. Add multi-agent workers only for tasks that benefit from parallel specialist work.
11. Validate with local smoke tests before increasing autonomy.

## Jarvis Autonomy Ladder

Level 0: Chat only.
- No tools. Answers from current context.

Level 1: Local read-only assistant.
- Can inspect approved files, app state, or screen summaries.

Level 2: Local proposal assistant.
- Can draft plans, commands, patches, emails, and workflows but does not execute them.

Level 3: Scoped local executor.
- Can edit approved files, run approved local checks, and operate approved local apps.

Level 4: Coordinated multi-agent operator.
- Can delegate to approved local subagents with disjoint scopes.

Level 5: External actor.
- Can contact external services only with exact approval for destination, data, and purpose.

Default target: Level 1 to Level 2 until the user trusts the system.

## Minimum Loop

```text
User input
-> classify intent
-> retrieve local memory if allowed
-> decide: answer | inspect | propose | ask approval
-> call local model
-> optionally call approved tool
-> verify result
-> respond with actions, assumptions, and next safe step
-> append local audit log
```

## Output Expectations

When designing or implementing Jarvis, produce:
- Architecture.
- Model runtime plan.
- Tool registry.
- Permission model.
- Memory policy.
- Voice policy if relevant.
- MVP implementation steps.
- Smoke tests.
- Known risks and stop points.
