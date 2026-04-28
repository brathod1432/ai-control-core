# Local Skill Validation Checklist

Use this checklist when reviewing new or changed skills in this repository. It is designed for local-first, static validation and assumes no network access unless the user explicitly approves a bounded external action.

## Repository Convention Baseline

- Skill directories are expected at `skills/<category>/<skill-name>/`.
- Every installable skill should include `SKILL.md`.
- Most repo-native skills also include `SKILL_METADATA.json`.
- Optional supporting material should stay inside the skill directory, commonly under `references/`, `scripts/`, `assets/`, `templates/`, or `examples/`.
- `SKILL.md` should start with YAML frontmatter containing at least `name` and `description`.
- The body should include an `Internal Safety Override` before operational instructions.
- Companion metadata should align with frontmatter name, category path, safety status, and risk categories.

## Pass Criteria

### 1. Self-Contained Packaging

- `SKILL.md` exists and can be understood without relying on external websites, cloud services, private accounts, or unstated files.
- Any referenced local files exist inside the same skill directory.
- Scripts, templates, references, examples, and expected outputs are included when the skill tells the agent to use them.
- Relative links point to bundled resources, not absolute user-machine paths.
- The skill does not require hidden global state, credentials, local caches, browser sessions, or account connectors to perform its default workflow.

### 2. Local-First Safety

- `Internal Safety Override` is present and explicit.
- Default mode is local-only or disabled-by-default for powerful/network-capable skills.
- Network, account connector, browser automation, command execution, filesystem, and secret-access risks are named when relevant.
- The skill tells the agent to request explicit user approval before any network contact, upload, account action, command execution with side effects, package install, destructive operation, or cross-workspace file access.
- The skill avoids exposing secrets in outputs, logs, screenshots, generated files, reports, or command arguments.
- Any remote examples are framed as opt-in examples, not default steps.

### 3. Trigger Rules

- Frontmatter `description` clearly says what the skill does and when to use it.
- Trigger examples include likely user phrases, task contexts, and adjacent terms.
- Non-trigger guidance is included when ambiguity is likely, especially for overlapping skills.
- Trigger rules live primarily in the frontmatter description, with body guidance only adding nuance.
- The description is specific enough to avoid over-triggering broad skills on unrelated tasks.

### 4. Advanced Analysis Options

- The skill includes a deeper workflow for non-trivial tasks, not only a short answer template.
- Analysis steps are ordered and testable, such as scope, inspect, diagnose, implement, verify, and report.
- The skill names the evidence to gather before making recommendations.
- It includes escalation points for high-risk, ambiguous, destructive, regulated, security-sensitive, or user-impacting decisions.
- It separates facts, assumptions, recommendations, and open questions in expected outputs when useful.

### 5. Modification Options

- If the skill can change files, it defines a safe edit workflow: inspect first, preserve user changes, make focused edits, and verify.
- It names which files or directories it may modify by default.
- It explains when to propose changes instead of patching directly.
- It warns against unrelated refactors, metadata churn, destructive commands, forced checkouts, or broad rewrites.
- It includes rollback-neutral behavior: do not revert others' changes unless explicitly requested.

### 6. Testable Steps

- The skill provides concrete smoke-test or validation steps for its normal workflow.
- Scripts have local invocation examples and expected input/output shape.
- For file-generating skills, the skill explains how to inspect generated artifacts locally.
- For advisory skills, the skill defines a review checklist or acceptance criteria.
- Verification instructions include what to report when checks cannot be run.

### 7. Metadata Consistency

- `SKILL_METADATA.json` name matches frontmatter `name`.
- Metadata category matches the directory under `skills/`.
- Metadata `status` is consistent with the safety override.
- Metadata `risk_categories` includes all relevant risks from the safety override and workflow.
- Metadata JSON is syntactically valid and contains no secrets or machine-specific private data.

## Static Validation Procedure

1. Read `SKILL.md` frontmatter and confirm `name` plus `description`.
2. Check for `Internal Safety Override` and compare it to the workflow's actual capabilities.
3. List local references in `SKILL.md` and verify every referenced file is bundled in the skill directory.
4. Read `SKILL_METADATA.json` if present and compare name, category, status, and risks.
5. Inspect `scripts/` statically for network calls, secret reads, destructive filesystem operations, shell execution, dynamic code execution, dependency installs, and absolute paths.
6. Confirm the skill offers advanced analysis and modification paths when the task domain involves investigation, implementation, generation, or file changes.
7. Confirm the skill gives at least one local test, smoke check, or acceptance checklist.
8. Record a verdict: `PASS`, `PASS WITH NOTES`, `NEEDS FIX`, or `BLOCKED`.

## Suggested Report Format

```markdown
# Skill Validation: <skill-name>

Verdict: PASS | PASS WITH NOTES | NEEDS FIX | BLOCKED
Scope: <path reviewed>
Method: static local inspection; no network

## Checks
- Self-contained: PASS/FAIL - <note>
- Local-first safety: PASS/FAIL - <note>
- Trigger rules: PASS/FAIL - <note>
- Advanced analysis options: PASS/FAIL - <note>
- Modification options: PASS/FAIL - <note>
- Testable steps: PASS/FAIL - <note>
- Metadata consistency: PASS/FAIL - <note>

## Findings
- <file>: <issue and suggested fix>

## Verification Limits
- <commands or checks skipped, and why>
```

## Common Fix Patterns

- Add or strengthen `Internal Safety Override` when a skill mentions commands, remote services, account tools, package installs, file writes, or secrets.
- Move large domain material from `SKILL.md` into `references/` and link it with clear "read this when" guidance.
- Add `scripts/` only for deterministic local tasks; keep script examples local and avoid lifecycle installs.
- Replace absolute paths with paths relative to the skill directory.
- Add explicit "do not edit unless asked" or "propose first" language for skills that analyze code, documents, or infrastructure.
- Add one smoke test that can run without network and one manual acceptance checklist for subjective outputs.
