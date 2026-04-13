# Compatibility Notes

## Intended Clients

The core repository is intended for any capable AI assistant, coding agent, model client, or MCP-compatible runtime.

Examples of compatible runtime families include:

- local coding agents
- chat-based AI assistants
- IDE agents
- MCP-compatible clients
- automation runners with explicit human approval

## Generic Core

Generic core lives in:

- `agents/`
- `rules/`
- `skills/`
- `templates/`
- `standards/`
- `mcp/`
- `security/`
- `context/`

These files should not require one model vendor or one client.

## Optional Integrations

Optional platform-specific or remote-service content lives in:

- `integrations/platforms/`
- `integrations/network-services/`
- `integrations/mcp-clients/`

These files may use vendor or client names because they describe compatibility surfaces. They are disabled or opt-in by default.

## Platform-Specific Examples

- Anthropic/Claude compatibility: `integrations/platforms/anthropic/`
- Codex compatibility metadata: `integrations/platforms/codex/`
- Google Gemini compatibility notes: `integrations/platforms/google/`
- Composio compatibility surfaces: `integrations/platforms/composio/`
- Remote service catalog: `integrations/network-services/`
- MCP client examples: `integrations/mcp-clients/`

## Adding Future Platforms

1. Add platform-specific files under `integrations/platforms/<platform>/`.
2. Keep core instructions generic.
3. Mark remote or credentialed behavior `opt_in_external` or `disabled_by_default`.
4. Add compatibility notes here.
5. Re-run validation scripts.
