# Certification-Style Assessment

This is an original local assessment for architect-level agent design. It does not represent an official certification unless a user-approved source later confirms alignment.

## Practical Exam

Design an agentic system for this scenario:

```text
A local-first engineering assistant must inspect a repository, plan a feature, coordinate independent implementation workers, verify the result, and produce a release-ready summary. It may not use network access unless the user approves a specific destination.
```

Deliverables:
- Agent charter.
- Multi-agent architecture diagram.
- Tool permission matrix.
- Context and memory policy.
- Handoff contracts.
- Evaluation suite.
- Safety and privacy policy.
- Operations checklist.
- Example prompts.

## Scoring Rubric

Architecture clarity: 20 points
- Clear single-agent vs multi-agent rationale.
- Correct pattern selection.
- No unnecessary agents.

Boundary design: 20 points
- Explicit permissions.
- Clear non-goals.
- Human approval gates for risky actions.

Context engineering: 15 points
- Bounded evidence.
- Memory tiers.
- Compression strategy.
- Secret avoidance.

Tool/MCP design: 15 points
- Typed schemas.
- Least privilege.
- Idempotency or dry-run.
- Structured errors.

Evaluation: 15 points
- Golden cases.
- Adversarial cases.
- Tool failure cases.
- Regression plan.

Operations: 10 points
- Logs, monitoring, incident response, versioning.

Communication: 5 points
- Clear diagrams, contracts, and final report.

Passing threshold:
- 80 or higher overall.
- No critical failure in privacy, destructive action, or unauthorized network access.

## Short Drills

Drill 1:
- Convert a vague agent request into a charter.

Drill 2:
- Choose between single-agent, sequential workflow, and multi-agent orchestration.

Drill 3:
- Write a safe tool schema for modifying files.

Drill 4:
- Add a critic loop without creating infinite revision cycles.

Drill 5:
- Design a memory policy that prevents stale project decisions from overriding current code.

Drill 6:
- Create a red-team eval for prompt injection through retrieved documents.

## Critical Fail Conditions

Fail immediately if the design:
- Allows network access without explicit approval.
- Allows destructive actions without human confirmation.
- Copies secrets into prompts, logs, or memory.
- Gives multiple workers overlapping write ownership without conflict handling.
- Has no evaluation or verification plan.
- Claims official certification without evidence.

