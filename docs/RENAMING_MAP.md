# Renaming Map

Machine-readable details: `docs/generated/generalization_renames.json`.

## Major Moves

- `skills/_templates` -> `templates`
- `templates/anthropic-skill-template` -> `templates/skill-template`
- `templates/composio-template-skill` -> `integrations/platforms/composio/template-skill`
- `skills/_standards` -> `standards`
- `skills/automation/network-integrations` -> `integrations/network-services`
- `skills/automation/connect` -> `integrations/platforms/composio/connect`
- `skills/automation/connect-apps` -> `integrations/platforms/composio/connect-apps`
- `skills/engineering/claude-api` -> `integrations/platforms/anthropic/claude-api`
- `rules/CLAUDE.md` -> `integrations/platforms/anthropic/legacy-claude-runtime-guide.md`
- `rules/GEMINI.md` -> `integrations/platforms/google/gemini-cli-guide.md`
- `agents/CLAUDE.md` -> `integrations/platforms/anthropic/agent-development-guide.md`
- `mcp/disabled-*` examples -> `integrations/platforms/*` or `integrations/mcp-clients/*`
- `skills/**/.codex` -> `integrations/platforms/codex/skill-adapters/...`

## Runtime Guide Renames

Remaining `CLAUDE.md` files in core skill/template/standard areas were renamed to `AI_RUNTIME_GUIDE.md`.
