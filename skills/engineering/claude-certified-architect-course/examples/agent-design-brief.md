# Agent Design Brief Template

## Agent

Name:
Role:
Mission:

## Scope

Owns:
Does not own:
Allowed files/data:
Forbidden files/data:

## Autonomy

Level:
Can act without asking:
Must ask before:
Must refuse:

## Inputs

Required:
Optional:
Assumptions allowed:

## Tools

| Tool | Purpose | Side effects | Approval needed |
|---|---|---|---|
| read_file | Inspect scoped files | None | No |
| apply_patch | Make focused edits | Local file writes | Task-implied scope |
| test_runner | Verify changes | Local command | No destructive commands |

## Workflow

1. Inspect.
2. Plan.
3. Act.
4. Verify.
5. Report.

## Output Contract

```json
{
  "summary": "string",
  "changed_files": [],
  "verification": [],
  "risks": [],
  "next_steps": []
}
```

## Evals

Golden cases:
Adversarial cases:
Tool failure cases:
Human acceptance criteria:

## Example Invocation

User:
```text
Inspect the auth module and add tests for expired tokens.
```

Agent expected behavior:
- Read auth files and existing tests.
- Patch only auth test files unless implementation bug is found.
- Run focused tests.
- Report changed files and failures.

