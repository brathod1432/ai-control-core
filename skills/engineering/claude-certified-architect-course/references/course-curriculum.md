# Course Curriculum

This is an original local curriculum for Claude-oriented agent architecture. It is designed to teach the mental models and production practices needed to build reliable single-agent and multi-agent systems.

## Course Outcomes

By the end, the learner can:
- Explain when not to use agents.
- Design a bounded single agent with tools, memory, evals, and escalation rules.
- Select multi-agent patterns based on dependency shape, risk, and coordination cost.
- Write system prompts and handoff contracts that preserve intent and limit context bloat.
- Design tool/MCP interfaces with least privilege and observable side effects.
- Build evaluation suites that catch regressions, unsafe autonomy, and brittle orchestration.
- Create a production-readiness checklist for agent deployment.

## Module 1: Architect Mindset

Learning objectives:
- Treat an agent as a sociotechnical system, not a magic prompt.
- Separate capability, authority, and responsibility.
- Prefer simpler designs until complexity buys measurable value.

Key ideas:
- Agent architecture is mostly boundary design.
- The model is only one component; tools, context, policy, evals, and operations matter as much.
- Autonomy should be granted in layers.

Lab:
- Rewrite a vague request, "build me an agent", into an agent charter with scope, non-goals, and escalation points.

Rubric:
- Clear mission.
- Explicit non-goals.
- Permission boundaries.
- Observable success criteria.

## Module 2: Model Behavior And Instruction Layers

Learning objectives:
- Understand system, developer, user, tool, and retrieved-context priority.
- Create prompts that are durable under ambiguity.
- Avoid contradictory instructions and hidden assumptions.

Key ideas:
- Good instructions are behavioral contracts.
- Examples should demonstrate edge cases, not just happy paths.
- Prompts should include refusal/escalation behavior for risky actions.

Lab:
- Write a system prompt for a local file organizer that cannot delete files without approval.

## Module 3: Context Engineering

Learning objectives:
- Design context windows intentionally.
- Decide what belongs in long-term memory, short-term task context, retrieved docs, and scratch artifacts.
- Compress without losing decision-critical facts.

Key ideas:
- Context is an interface, not a dumping ground.
- Use manifests, summaries, and source maps for large inputs.
- Keep secrets and unrelated private data out of context.

Lab:
- Convert a 20-file code investigation into a compact evidence bundle with citations and open questions.

## Module 4: Tool Use And MCP Interfaces

Learning objectives:
- Design tools with clear schemas and side-effect boundaries.
- Separate read tools, write tools, and destructive tools.
- Use MCP resources/templates when shared context is safer than free-form tool calls.

Key ideas:
- Tool descriptions are part of the safety surface.
- Idempotency and dry-run modes reduce operational risk.
- Tool outputs should be structured and bounded.

Lab:
- Design a local filesystem MCP tool set for reading project files and proposing patches without granting delete permission.

## Module 5: Single-Agent Runtime Loops

Learning objectives:
- Build inspect-plan-act-verify-report loops.
- Add stop conditions, retries, and escalation.
- Avoid infinite tool loops and premature action.

Common loop:
1. Intake.
2. Scope.
3. Gather evidence.
4. Plan.
5. Act.
6. Verify.
7. Report.

Lab:
- Create a bug-fix agent that must reproduce, patch, run tests, and report skipped checks.

## Module 6: Memory And Knowledge

Learning objectives:
- Distinguish user memory, project memory, task memory, and domain references.
- Decide retention, update, and deletion rules.
- Prevent stale memory from overriding fresh evidence.

Lab:
- Design memory policy for an agent that tracks product decisions across a repo.

## Module 7: Multi-Agent Fundamentals

Learning objectives:
- Know when multi-agent designs help and when they make things worse.
- Define coordinator, worker, critic, verifier, and specialist roles.
- Manage handoffs and fan-in synthesis.

Key ideas:
- Parallelism is useful only when write scopes or questions are independent.
- Every agent needs ownership.
- The coordinator owns integration and final accountability.

Lab:
- Split a feature implementation into three non-overlapping worker tasks and one verifier task.

## Module 8: Orchestration Patterns

Learning objectives:
- Select among sequential, parallel, router, supervisor, debate, critic, blackboard, and tournament patterns.
- Handle timeouts, failures, partial outputs, and conflicts.
- Use diagrams to communicate workflows.

Lab:
- Design a research-to-implementation workflow with explorer agents, implementation workers, and a final reviewer.

## Module 9: Evaluation And Red Teaming

Learning objectives:
- Build golden tests, regression tests, adversarial prompts, and tool misuse checks.
- Evaluate both final answer quality and process quality.
- Measure cost, latency, reliability, and safety.

Lab:
- Create an eval suite for a multi-agent code review workflow.

## Module 10: Safety, Privacy, And Governance

Learning objectives:
- Apply least privilege, explicit approval, and data minimization.
- Design human-in-the-loop gates for high-impact actions.
- Write audit logs that are useful without leaking secrets.

Lab:
- Add a safety gate to an agent that can send emails, deploy, or modify production data.

## Module 11: Production Operations

Learning objectives:
- Monitor agent traces, tool calls, budgets, retries, and incidents.
- Create rollback plans and release gates.
- Distinguish experimental prototypes from production systems.

Lab:
- Create a production readiness checklist for an agentic support triage system.

## Module 12: Capstone

Prompt:
- Design a local-first multi-agent coding assistant that can inspect a repo, propose a plan, implement scoped changes, run tests, and generate a PR summary without network access unless approved.

Deliverables:
- Architecture diagram.
- Agent roster.
- Prompt pack.
- Tool/MCP interface list.
- Handoff contracts.
- Eval suite.
- Safety policy.
- Rollout plan.

