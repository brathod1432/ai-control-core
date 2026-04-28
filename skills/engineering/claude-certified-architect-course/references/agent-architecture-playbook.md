# Agent Architecture Playbook

## Agent Charter

Every agent starts with a charter:
- Name: memorable and role-specific.
- Mission: one sentence outcome.
- Scope: what the agent owns.
- Non-goals: what it must refuse or escalate.
- Authority: allowed actions and required approvals.
- Inputs: accepted formats and required context.
- Tools: tool names, purpose, and side-effect level.
- Memory: what can be read, written, or retained.
- Output: schema, tone, and evidence requirements.
- Stop conditions: when the agent is done.
- Escalation: when to ask a human or coordinator.

## Autonomy Levels

Level 0: Advisory only.
- Reads context and proposes actions.
- No writes, tool side effects, or external calls.

Level 1: Local read-only operator.
- Can inspect local files or app state.
- No modification.

Level 2: Local scoped editor.
- Can modify explicitly scoped files.
- Must verify and report.

Level 3: Local workflow executor.
- Can run tests, formatters, generators, and non-destructive scripts.
- Must avoid destructive commands.

Level 4: External integrator.
- Can call approved external APIs or services.
- Requires explicit destination, data scope, and credential source.

Level 5: High-impact actor.
- Can deploy, publish, send messages, spend money, or modify production data.
- Requires strong human-in-the-loop approval and audit logs.

## Single-Agent Runtime Loop

Use this loop for most coding, document, and analysis agents:

```text
INTAKE -> SCOPE -> INSPECT -> PLAN -> ACT -> VERIFY -> REPORT
```

Rules:
- Do not plan from memory when local evidence is available.
- Prefer small patches and reversible changes.
- Verify proportional to risk.
- Report skipped checks.
- Preserve user changes and avoid unrelated refactors.

## System Prompt Template

```text
You are <name>, a <role>.

Mission:
<clear outcome>

Operating principles:
- Inspect before acting.
- Prefer the smallest safe change.
- Preserve user changes.
- Ask only when missing information creates material risk.

Allowed actions:
- <reads>
- <writes>
- <commands/tools>

Forbidden actions:
- <network/upload/deploy/delete/secrets/etc.>

Workflow:
1. Build context from approved sources.
2. Identify constraints and assumptions.
3. Execute focused work.
4. Validate with local checks.
5. Report changed artifacts, verification, and residual risk.

Output contract:
<format/schema>
```

## Tool Permission Matrix

| Tool Class | Examples | Default Permission | Required Guardrail |
|---|---|---|---|
| Read-only local | file read, directory list, metadata | Usually allowed in scope | Do not read secrets or unrelated personal files |
| Local write | patch files, generate docs, create artifacts | Scoped approval implied by task | Preserve originals, validate, avoid broad rewrites |
| Shell command | tests, formatters, build | Bounded local commands | Avoid destructive commands and secrets in output |
| Browser/app automation | Chrome CDP, Office COM | Explicit or task-implied local target | Avoid credentials, destructive UI actions, hidden sync |
| Network/API | docs, GitHub, SaaS | Explicit approval only | State destination, data, credential source, purpose |
| High-impact action | deploy, publish, email, payment | Explicit approval per action | Human confirmation, dry-run, audit log |

## Output Schemas

Agent design output:

```json
{
  "agent_name": "string",
  "mission": "string",
  "autonomy_level": 0,
  "inputs": [],
  "tools": [],
  "memory_policy": "string",
  "workflow": [],
  "outputs": {},
  "evals": [],
  "risks": []
}
```

Agent execution report:

```json
{
  "task": "string",
  "actions_taken": [],
  "files_changed": [],
  "verification": [],
  "skipped_checks": [],
  "open_risks": [],
  "next_steps": []
}
```

