# AI Project Context

## START HERE

- Purpose: model-agnostic AI operations repository.
- Core assets are generic and reusable across AI assistants, coding agents, model clients, and MCP-compatible runtimes.
- Platform-specific content lives under `integrations/`.

## CHEAPEST FILES TO READ FIRST

1. `AI_README.md`
2. `context/AI_PROJECT_CONTEXT.md`
3. `context/SECURITY_BOUNDARIES.md`
4. `context/USAGE_RULES.md`
5. `context/SKILLS_INDEX.md`
6. target `SKILL_METADATA.json`
7. target `SKILL.md`

## Folder Map

- `agents/`: generic agent/persona guidance.
- `rules/`: generic operating rules and command templates.
- `skills/`: core skill library.
- `templates/`: reusable templates.
- `standards/`: authoring and operational standards.
- `mcp/`: generic MCP references.
- `security/`: safe-use policy.
- `integrations/`: optional platform/client/vendor/service adapters.
- `scripts/`: local maintenance scripts.
- `docs/`: reports and attribution.
- `context/`: low-token navigation files.

## Source Of Truth

- Skill status: `SKILL_METADATA.json`.
- Skill instruction: `SKILL.md`.
- Disabled reason: `DISABLED.md`.
- Compatibility: `docs/COMPATIBILITY_NOTES.md`.
- Security: `security/SECURITY_POLICY.md`.
- Structure: `docs/REPO_STRUCTURE.md`.

## DO NOT ASSUME

- Do not assume a platform integration is active.
- Do not assume vendor names in `integrations/` apply to core behavior.
- Do not assume repository files may be sent externally.
- Do not assume secrets may be read.
- Do not assume imported commands are safe to run without inspection.

## SAFE DEFAULTS

- Local-only.
- Core assets first.
- No external data transfer.
- No secret reads.
- Disabled content is read-only unless explicitly enabled.
