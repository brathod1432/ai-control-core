---
name: claude-certified-architect-course
description: Use when the user wants a Claude/LLM architect course, agent architecture training, single-agent or multi-agent design help, agent prompt/system-instruction creation, orchestration patterns, tool/MCP design, context engineering, evaluation, safety, or production readiness for agentic systems. This is a local course-style skill pack and builder for creating agents and multi-agent workflows; do not claim official certification unless a user-approved source confirms it.
category: engineering
---

## Internal Safety Override

- Status: active for local course design, agent architecture, and local skill/workflow creation.
- Work local-first. Do not fetch course pages, GitHub repositories, docs, transcripts, examples, telemetry, or model outputs from external services unless the user explicitly approves the exact destination and purpose in the current thread.
- Do not reproduce proprietary course text verbatim unless the license permits it or the user owns/provides the material. Prefer original summaries, source maps, exercises, and local examples.
- Do not read secrets, `.env`, auth caches, browser profiles, private docs, or credential stores while designing agents.
- When creating executable agents, tools, MCP servers, or automations, define permission boundaries, data scopes, rollback behavior, logs, and evaluation gates before implementation.
- Follow the host runtime's delegation rules. In Codex, spawn subagents only when the user explicitly authorizes subagents, delegation, or parallel agent work.
- Audit categories: command, network, secrets, privacy, agent autonomy, local file changes.

# Claude Certified Architect Course

This skill is a local, course-style architect playbook for designing Claude-like LLM applications, agents, and multi-agent systems. It combines curriculum, architecture checklists, pattern catalogs, prompt contracts, tool/MCP design guidance, evaluation practices, and production readiness workflows.

Use it in two modes:
- Learning mode: teach or summarize agent architecture concepts as a structured course.
- Builder mode: create concrete single-agent or multi-agent designs, prompts, handoff contracts, eval plans, and implementation tasks.

Important naming note: this folder uses the user's requested course name. Unless an approved source proves the course is official, describe outputs as "course-style", "Claude-oriented", or "Claude architect inspired", not as an official certification.

## Bundled Resources

Read only what is needed:
- `references/course-curriculum.md`: complete local curriculum, modules, labs, capstone, and study path.
- `references/agent-architecture-playbook.md`: single-agent architecture, role specs, tool contracts, memory, runtime loops, and prompt structure.
- `references/multi-agent-pattern-catalog.md`: coordinator, router, parallel, debate, critic, blackboard, market, swarm, and escalation patterns.
- `references/context-engineering-and-memory.md`: context budgets, retrieval, compression, memory tiers, trace discipline, and long-running work.
- `references/tool-use-and-mcp.md`: tool design, MCP/resource patterns, schemas, side-effect boundaries, permissions, and local-first integration.
- `references/evaluation-safety-operations.md`: eval suites, red-team checks, observability, incident response, cost controls, and release gates.
- `references/agent-factory.md`: step-by-step process for creating new agents, subagents, and skill-backed agent workflows.
- `references/certification-assessment.md`: practical exam, scoring rubric, drills, and project requirements for architect-level mastery.
- `references/source-map.md`: source and attribution ledger; currently local-original unless the user approves importing external course material.
- `examples/agent-design-brief.md`: fill-in template for a production-ready agent.
- `examples/multi-agent-blueprints.md`: concrete example systems with roles, handoffs, and failure handling.
- `examples/prompts-and-handoff-contracts.md`: reusable system prompts, coordinator prompts, worker prompts, critic prompts, and JSON handoff contracts.

## Standard Workflow

1. Identify whether the user wants learning, architecture design, implementation scaffolding, review, or source import.
2. If source import is requested, stop before network access. State the exact URLs or GitHub repo to contact, what will be fetched, and why.
3. Choose the smallest useful agent shape: single agent, workflow agent, or multi-agent system.
4. Write the agent charter: objective, non-goals, autonomy level, tools, data scope, output contract, stop conditions, and escalation rules.
5. Choose an orchestration pattern from `references/multi-agent-pattern-catalog.md` only if the task benefits from decomposition.
6. Define context architecture: system instructions, task context, retrieved knowledge, memory, scratch artifacts, and what must not enter context.
7. Define tools and MCP resources with strict schemas, least privilege, idempotency, audit logging, and safe defaults.
8. Add evals: golden tasks, adversarial tasks, tool misuse checks, hallucination checks, cost/latency limits, and human acceptance criteria.
9. Produce the requested artifact: lesson plan, architecture diagram, agent spec, multi-agent spec, prompt set, test plan, implementation checklist, or local skill.
10. Report assumptions, risks, and verification limits.

## Builder Outputs

For a single agent, produce:
- Agent name and purpose.
- Scope and non-goals.
- System prompt.
- Tool list with permissions.
- Context and memory policy.
- Runtime loop.
- Output schema.
- Evals and safety checks.
- Example invocation.

For a multi-agent system, produce:
- Coordinator charter.
- Agent roster with disjoint responsibilities.
- Handoff graph.
- Message contracts.
- Shared state policy.
- Concurrency plan.
- Conflict resolution.
- Fan-in synthesis rule.
- Failure and timeout handling.
- Evaluation and release gates.

For a course module, produce:
- Learning objectives.
- Concept map.
- Instructor notes.
- Worked example.
- Lab exercise.
- Rubric.
- Common mistakes.
- Stretch challenge.

## Architecture Decision Rules

Prefer a single agent when:
- The task is linear, small, or tightly coupled.
- One context window can hold the needed evidence.
- Tool access is simple and low-risk.
- A coordinator would add overhead without improving quality.

Use a workflow agent when:
- The task has repeatable phases such as inspect, plan, implement, verify, report.
- Intermediate artifacts can be validated.
- Determinism and observability matter more than autonomy.

Use multi-agent orchestration when:
- Subtasks are independent enough to run in parallel.
- Different expertise is required.
- A critic, verifier, or red-team role materially reduces risk.
- Competing approaches can be evaluated against objective criteria.
- The coordination overhead is justified by quality, speed, or resilience.

Avoid multi-agent orchestration when:
- The next step is blocked on a single unknown.
- Agents would need the same context and duplicate work.
- The task involves sensitive data that should not be copied into multiple contexts.
- The user has not authorized subagents in a runtime that requires explicit authorization.

## Prompt Architecture Skeleton

Use this structure for most agent prompts:

```text
You are <agent-name>, responsible for <single responsibility>.

Mission:
- <outcome>

Authority:
- You may <allowed actions>.
- You must not <forbidden actions>.

Inputs:
- <input contract>

Tools:
- <tool name>: use only for <bounded purpose>.

Workflow:
1. Inspect inputs.
2. State assumptions.
3. Execute only in scope.
4. Validate output.
5. Report results and residual risks.

Output:
- Return <schema or format>.

Escalate when:
- <ambiguity, safety, privacy, destructive action, missing permission>
```

## Source Import Workflow

If the user approves fetching a course repo or pages:
1. Fetch only the approved URLs or repository.
2. Inspect license, README, attribution requirements, and terms before importing.
3. Create `references/source-map.md` with URLs, commit hash or retrieval date, license, and which local files were derived from each source.
4. Summarize or transform content into original local guidance unless the license clearly permits copying.
5. Keep examples local and remove secrets, analytics, trackers, external images, and remote embeds.
6. Add a validation note explaining what was fetched, what was not fetched, and any licensing uncertainty.

## Validation Checklist

Before delivering an agent or course artifact:
- Frontmatter and metadata are present for any created skill.
- The design states autonomy level and tool/data permissions.
- The system has a clear stop condition.
- Side effects are opt-in and reversible where possible.
- Multi-agent roles have disjoint ownership and no accidental duplicate work.
- Handoff contracts are explicit and bounded.
- Evaluation covers normal, edge, adversarial, and tool-failure cases.
- The final report distinguishes facts, assumptions, recommendations, and open risks.
