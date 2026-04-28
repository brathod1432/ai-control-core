# Agent Factory

Use this guide to create new agents, subagents, and skill-backed workflows from a user request.

## Factory Workflow

1. Capture intent.
2. Decide whether an agent is needed.
3. Select autonomy level.
4. Choose single-agent, workflow, or multi-agent architecture.
5. Define role and boundaries.
6. Define tools and data access.
7. Write prompts and handoff contracts.
8. Add evals and red-team cases.
9. Package as a skill, script, config, or runtime workflow.
10. Validate locally.

## Intent Capture Questions

Ask only when not inferable:
- What outcome should the agent produce?
- What data may it read?
- What may it modify?
- Should it act autonomously or propose first?
- What tools are allowed?
- What should it never do?
- How will success be judged?

## Agent Creation Checklist

Required:
- Mission.
- Scope.
- Non-goals.
- Autonomy level.
- Tool permissions.
- Context sources.
- Memory policy.
- Output contract.
- Stop conditions.
- Escalation rules.
- Evals.

Optional:
- Diagram.
- Cost budget.
- Latency target.
- Human review gate.
- Incident runbook.
- Versioning policy.

## Subagent Creation Checklist

Use subagents only when authorized by the runtime and useful for parallelism.

Before spawning:
- Identify the coordinator's immediate local task.
- Identify independent side tasks.
- Assign disjoint ownership.
- Define expected output.
- Tell workers they are not alone in the codebase.
- Tell workers not to revert others' changes.

Worker prompt fields:
- Role.
- Owned files or domain.
- Task.
- Constraints.
- Tools allowed.
- Output contract.
- Verification expected.
- Escalation triggers.

## Skill-Backed Agent Packaging

Create a skill when:
- The workflow is reusable.
- The trigger context is clear.
- The instructions are more than a one-off prompt.
- The agent needs bundled references, examples, or scripts.

Recommended structure:

```text
skill-name/
  SKILL.md
  SKILL_METADATA.json
  references/
  examples/
  scripts/
```

`SKILL.md` should include:
- Frontmatter name and description.
- Internal Safety Override.
- Workflow.
- Resource map.
- Output expectations.
- Validation checklist.

## Example: Creating A Repo Review Agent

Agent:
- `repo-reviewer`

Mission:
- Find correctness, security, and maintainability risks in a scoped diff.

Autonomy:
- Level 1 read-only, unless asked to patch.

Tools:
- File read.
- Search.
- Git diff.

Output:
- Findings first.
- File and line references.
- Severity.
- Confidence.
- Testing gaps.

Evals:
- Detects an introduced auth bypass.
- Avoids nitpicks when no bug exists.
- Does not expose secrets from config files.

## Example: Creating A Multi-Agent Feature Crew

Coordinator:
- Owns plan and integration.

Workers:
- API worker: backend routes and validation.
- UI worker: frontend components.
- Test worker: tests and fixtures.
- Reviewer: final risk scan.

Rules:
- Workers have disjoint file ownership.
- Coordinator handles merge conflicts and final verification.
- Reviewer does not rewrite; it reports findings.

