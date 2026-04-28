---
name: jarvis-core-orchestrator
description: Use to design or implement the central Jarvis planner loop, intent router, safety gate integration, autonomy ladder, tool-call decision policy, audit log, and final response synthesis for a local laptop assistant.
category: local-agent
---

## Internal Safety Override

- Status: active for local design and scoped local implementation.
- Do not grant tool access by default. Every tool must declare permission class and side effects.
- Do not route work to subagents unless the user authorized delegation or the runtime policy allows it.
- Do not hide failed tool calls, skipped checks, or approval gates.

# Jarvis Core Orchestrator

## Responsibilities

- Classify user intent.
- Decide whether to answer, inspect, propose, act, or ask.
- Build compact context for the local model.
- Select model profile.
- Select approved tools.
- Enforce the autonomy ladder.
- Coordinate optional specialist agents.
- Verify tool results.
- Maintain local audit logs.

## Intent Classes

- Chat: answer from current context.
- Recall: retrieve approved memory.
- Inspect: read local files/app state.
- Plan: propose steps.
- Act: modify local state.
- Automate: control app/browser/desktop.
- External: network or cloud action.
- High-impact: send/publish/deploy/delete/buy/account/security action.

## Decision Policy

```text
If external or high-impact: ask approval.
If destructive: ask approval.
If secret access: refuse or ask for scoped user-provided input.
If local read and scoped: proceed.
If local write and scoped by user request: propose or act depending on autonomy level.
If ambiguous: ask one concise question.
```

## Orchestrator Output Schema

```json
{
  "intent": "chat|recall|inspect|plan|act|automate|external|high_impact",
  "risk": "low|medium|high|blocked",
  "decision": "answer|tool_call|ask_approval|ask_clarification|refuse",
  "tool": null,
  "approval_required": false,
  "reason": "string"
}
```

## Audit Log Minimum

```json
{
  "timestamp": "iso-8601",
  "request_summary": "string",
  "intent": "string",
  "risk": "string",
  "tools_called": [],
  "approval": "not_required|approved|denied",
  "result_summary": "string"
}
```

