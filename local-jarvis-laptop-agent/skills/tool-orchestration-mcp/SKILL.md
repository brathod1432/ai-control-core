---
name: tool-orchestration-mcp
description: Use to design Jarvis tool registry and local MCP-style tool orchestration with typed schemas, permissions, dry-run modes, audit logs, loopback-only services, and safe tool execution.
category: local-agent
---

## Internal Safety Override

- Status: active for local design and scoped local implementation.
- Tools must default to least privilege.
- Network-capable tools must be disabled until explicitly approved.
- Destructive tools require dry-run and confirmation.

# Tool Orchestration MCP

## Current Model Baseline

All agents and subagents use the same single local Ollama `qwen2.5:3b` model through `http://127.0.0.1:11434`. No cloud LLMs, remote model APIs, separate providers, or per-agent model pools are used by tool orchestration.

## Tool Registry Fields

```json
{
  "name": "string",
  "description": "string",
  "permission": "read_local|write_local|execute_local|automate_app|network|high_impact",
  "side_effects": false,
  "dry_run": true,
  "input_schema": {},
  "output_schema": {},
  "redaction": "string",
  "approval_required": false
}
```

## Tool Classes

Read local:
- File read, search, metadata, local app state.

Write local:
- Patch file, create note, update memory.

Execute local:
- Tests, formatters, safe scripts.

Automate app:
- Browser, Office, desktop UI.

Network:
- External docs, APIs, cloud.

High impact:
- Send, publish, deploy, delete, buy, account/security changes.

## MCP Server Guidelines

- Bind to loopback only.
- Use explicit schemas.
- Bound output length.
- Redact secrets at source.
- Separate read tools from write tools.
- Add dry-run to risky tools.
- Log tool summaries, not raw sensitive payloads.
