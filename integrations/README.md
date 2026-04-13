# Integrations

Optional platform, model-client, vendor, MCP-client, and remote-service compatibility material lives here.

Nothing in this folder is active by default.

## Layout

- `platforms/` - named platform or model-client compatibility material.
- `network-services/` - disabled-by-default remote service integration skills.
- `mcp-clients/` - disabled MCP client config examples.

## Use Rules

- Read only unless a task explicitly requires the named integration.
- Check `SKILL_METADATA.json` before use.
- Do not connect accounts, call APIs, upload files, or transmit repository data without explicit human opt-in.
- Do not copy `.disabled` files into active config locations automatically.

## Adding Integrations

Use a functional folder under `platforms/`, `network-services/`, or `mcp-clients/`. Keep provider-specific details here rather than in core `skills/`, `rules/`, `templates/`, or `standards/`.
