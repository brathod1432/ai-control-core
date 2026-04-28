---
name: multi-agent-crew
description: Use to design optional Jarvis specialist subagents and multi-agent workflows for coding, research, browser inspection, Office/document work, memory curation, and verification, with coordinator-owned integration and disjoint scopes.
category: local-agent
---

## Internal Safety Override

- Status: advisory unless the user authorizes subagents/delegation.
- Do not duplicate sensitive context into multiple agents unless necessary.
- Workers need disjoint ownership and must not revert others' changes.
- Coordinator remains accountable for integration and final response.

# Multi-Agent Crew

## When To Use

Use specialists when:
- Work can run in parallel.
- Expertise differs.
- Verification benefits from independence.
- Write scopes can be separated.

Avoid specialists when:
- The task is small.
- The next action is blocking.
- Context is too sensitive to fan out.
- Agents would duplicate work.

## Suggested Crew

Coordinator:
- Plans, delegates, integrates, reports.

Researcher:
- Finds local facts and summarizes evidence.

Coder:
- Implements scoped local code changes.

Browser inspector:
- Uses local Chrome/CDP for approved loopback pages.

Office worker:
- Modifies approved Office files locally.

Memory curator:
- Proposes memory writes and cleanup.

Verifier:
- Runs tests/checklists and reports risks.

## Worker Prompt Template

```text
You are <role> in the local Jarvis crew.
You are not alone in the workspace.
Ownership: <paths or domain>.
Do not revert edits made by others.
Task: <bounded task>.
Allowed tools: <tools>.
Forbidden actions: <actions>.
Output: changed files, verification, risks.
```

