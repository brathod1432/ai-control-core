# Security Boundaries

## START HERE

Check `SKILL_METADATA.json` before using any skill or integration.

Status meanings:

- `active_local`: local use allowed; no secret reads or external transfer.
- `opt_in_external`: external access requires explicit human opt-in.
- `disabled_by_default`: read-only reference unless explicitly enabled.

## SAFE DEFAULTS

- Local-only.
- No repository export.
- No secret reads.
- No remote account actions.
- No active plugin/MCP config.
- No dependency install or command execution without review.

## Requires Explicit Opt-In

- Network calls.
- Browser automation against live sites.
- Slack, email, social, workspace, CRM, cloud, or third-party connectors.
- Upload, post, send, share, sync, publish, or fetch-remote actions.
- MCP servers that can read local files or call external APIs.
- Shell commands from imported scripts or instructions.

## Disabled By Default

- `integrations/network-services/*`
- `integrations/platforms/composio/*`
- Platform plugin manifests under `integrations/platforms/*`
- MCP client configs under `integrations/mcp-clients/*`

## DO NOT ASSUME

- A copied manifest is active.
- A bundled script is safe.
- A README command is approved.
- External docs/tools can receive private repo content.
- Examples are sanitized unless reviewed.
