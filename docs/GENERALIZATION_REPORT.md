# Generalization Report

Date: 2026-04-13

## Platform-Specific Content Found

- Core files named for single runtimes:
  - `agents/CLAUDE.md`
  - `rules/CLAUDE.md`
  - `rules/GEMINI.md`
- Hidden client adapter folders:
  - `skills/**/.codex`
- Vendor/API-specific skill content:
  - `skills/engineering/claude-api`
  - `skills/automation/network-integrations/*`
  - `skills/automation/connect`
  - `skills/automation/connect-apps`
- Disabled plugin and MCP examples mixed into core `mcp/`.
- Template and standard folders under `skills/_templates` and `skills/_standards`.

## What Was Generalized

- Promoted templates to top-level `templates/`.
- Renamed the core upstream-derived template to `templates/skill-template/`.
- Moved the Composio-specific template to `integrations/platforms/composio/template-skill/`.
- Promoted standards to top-level `standards/`.
- Rewrote root/context/security docs to describe a model-agnostic AI operations repository.
- Added generic `rules/AI_RUNTIME_RULES.md`.
- Added generic `agents/README.md`.
- Updated scripts to scan and index both core skills and optional integrations.

## What Was Renamed Or Moved

See `docs/RENAMING_MAP.md` and `docs/generated/generalization_renames.json`.

Major moves:

- `skills/automation/network-integrations` -> `integrations/network-services`
- `skills/automation/connect` -> `integrations/platforms/composio/connect`
- `skills/automation/connect-apps` -> `integrations/platforms/composio/connect-apps`
- `skills/engineering/claude-api` -> `integrations/platforms/anthropic/claude-api`
- `rules/CLAUDE.md` -> `integrations/platforms/anthropic/legacy-claude-runtime-guide.md`
- `rules/GEMINI.md` -> `integrations/platforms/google/gemini-cli-guide.md`
- `agents/CLAUDE.md` -> `integrations/platforms/anthropic/agent-development-guide.md`
- `skills/**/.codex` -> `integrations/platforms/codex/skill-adapters/...`

## What Remained Platform-Specific And Why

- Source attribution docs retain upstream repository and vendor names for legal/provenance accuracy.
- `integrations/platforms/*` keeps platform names because those files are compatibility content.
- `integrations/network-services/*` keeps service names because each folder describes a specific remote integration.
- Anthropic/Claude API references remain named inside `integrations/platforms/anthropic/claude-api` because the API itself is vendor-specific.

## Compatibility Sections Created

- `integrations/README.md`
- `docs/COMPATIBILITY_NOTES.md`
- `rules/AI_RUNTIME_RULES.md`

## References Updated

- Compact context files now point to `integrations/` for optional adapters.
- Security policy now treats `integrations/` as inert/opt-in by default.
- `context/SKILLS_INDEX.md` is generated from the live filesystem rather than stale import paths.
- Maintenance scripts scan `skills/` and `integrations/`.

## Risks And Caveats

- Some imported skill prose may still mention platform names where the original subject is a platform, model, API, or provider.
- Generated provenance reports still include old source repository names and historical source paths by design.
- Optional integrations remain high risk and must not be auto-enabled.
