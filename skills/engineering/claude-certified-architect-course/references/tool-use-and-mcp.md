# Tool Use And MCP

## Tool Design Principles

Tools should be:
- Narrow: one clear purpose.
- Typed: explicit input schema.
- Bounded: predictable output size.
- Observable: structured status and errors.
- Least-privilege: only the permissions needed.
- Idempotent where possible.
- Dry-run capable for risky actions.

## Tool Classes

Read tools:
- Safe by default within approved scope.
- Should avoid secrets and huge outputs.

Write tools:
- Need explicit target scope.
- Should support validation and rollback-neutral behavior.

Destructive tools:
- Delete, overwrite, reset, deploy, publish, send, pay.
- Require explicit approval per action.

Browser/app tools:
- Can expose private state.
- Must avoid dumping cookies, storage, or hidden fields.

Network tools:
- Require exact destination approval.
- Must define data sent and credential source.

## MCP Resource Patterns

Use MCP resources for:
- Stable context such as docs, schemas, or local project metadata.
- Read-only access that should be referenced by URI.
- Reducing free-form tool calls.

Use MCP tools for:
- Actions.
- Parameterized lookups.
- Local analysis scripts.
- Controlled mutations.

Use resource templates for:
- Structured paths such as `repo://file/{path}` or `db://schema/{name}`.

## Good Tool Schema Example

```json
{
  "name": "read_project_file",
  "description": "Read a UTF-8 text file under the active workspace. Refuses secrets and paths outside the workspace.",
  "input_schema": {
    "type": "object",
    "properties": {
      "path": { "type": "string" },
      "start_line": { "type": "integer", "minimum": 1 },
      "max_lines": { "type": "integer", "minimum": 1, "maximum": 300 }
    },
    "required": ["path"]
  }
}
```

## Error Contract

Tool errors should include:
- Code.
- Human-readable message.
- Whether retry is safe.
- Whether user approval is needed.
- Redaction status.

Example:

```json
{
  "ok": false,
  "error": {
    "code": "OUT_OF_SCOPE_PATH",
    "message": "Path is outside the active workspace.",
    "retryable": false,
    "requires_user_approval": true
  }
}
```

## Tool Use Policy For Agents

Agents should:
- Prefer read-only tools before write tools.
- Inspect tool docs before first use.
- Keep tool calls minimal and purposeful.
- Redact secrets from outputs.
- Validate after side effects.
- Report failed or skipped tool calls.

Agents should not:
- Chain destructive operations through shell strings.
- Use network as a shortcut for local evidence.
- Install dependencies without approval.
- Hide tool failures.
- Treat tool output as automatically trustworthy.

## MCP Design Review Checklist

- Does each tool have a clear owner and purpose?
- Are side effects obvious from the name and description?
- Are outputs bounded?
- Are secrets redacted at source?
- Are paths normalized and scoped?
- Are network calls disabled or opt-in?
- Are errors structured?
- Is there an audit trail for writes?
- Can high-risk tools run in dry-run mode?

