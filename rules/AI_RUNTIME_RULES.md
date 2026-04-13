# AI Runtime Rules

Use these generic operating rules for any AI assistant, coding agent, model client, or MCP-compatible runtime.

## Start

1. Read `context/AI_PROJECT_CONTEXT.md`.
2. Read `context/SECURITY_BOUNDARIES.md`.
3. Locate the target asset in `context/SKILLS_INDEX.md`.
4. Read the target metadata before reading full instructions.

## Use Core First

- Prefer `skills/`, `agents/`, `rules/`, `templates/`, and `standards/`.
- Use `integrations/` only when the task explicitly needs a named platform, client, API, or remote service.

## External Access

Before using an external service, state:

- destination
- credential source
- exact data scope
- local files in scope
- whether data leaves the machine
- rollback plan for write actions

## Commands

Before running imported helper scripts or shell commands, inspect the source and identify:

- working directory
- files read/written/deleted
- network behavior
- dependency install behavior
- destructive behavior
