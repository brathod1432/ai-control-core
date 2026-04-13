# Merge Report

Date: 2026-04-13

## Sources Imported

- `ComposioHQ/awesome-claude-skills`
  - Imported unique standalone skills.
  - Imported Composio integration skill catalog as disabled-by-default network integrations.
  - Imported Composio template material.
  - Disabled plugin/app integration manifests.
- `anthropics/skills`
  - Used as canonical format baseline.
  - Imported reference skills, skill spec, template, MCP references, and third-party notices.
  - Preferred for duplicate shared skills such as document, design, MCP, and authoring skills.
- `alirezarezvani/claude-skills`
  - Imported root domain skill folders as primary content.
  - Imported agents, commands, conventions, standards, and templates.
  - Skipped generated `.gemini/skills/*` wrappers and `.codex/skills/*` pointer entries as primary sources.
  - Disabled upstream MCP/plugin manifests.

## Normalized Counts

- Skill-like assets imported: 1,050
- Core skills after generalization: 237
- Optional integrations after generalization: 813
- Duplicate/alias groups consolidated: 38
- Exact canonical duplicate names after import: 0
- Near-name pairs remaining: 135, mostly provider-specific `*-automation` names that are not functional duplicates.
- Nested upstream skill markers demoted to `SKILL_REFERENCE.md`: 262

Status counts:

- `active_local`: 49
- `opt_in_external`: 168
- `disabled_by_default`: 833

Category counts:

- optional integration assets: 813
- `automation`: 0 in core after generalization
- `business`: 79
- `data`: 8
- `engineering`: 86
- `mcp`: 1
- `media`: 6
- `productivity`: 39
- `research`: 2
- `security`: 14
- `writing`: 3

## Consolidation Decisions

- Anthropic versions were kept for shared reference skills:
  - `brand-guidelines`
  - `canvas-design`
  - `docx`
  - `internal-comms`
  - `mcp-builder`
  - `pdf`
  - `pptx`
  - `skill-creator`
  - `slack-gif-creator`
  - `theme-factory`
  - `webapp-testing`
  - `xlsx`
- `artifacts-builder` was canonicalized to `web-artifacts-builder`.
- `mcp-server-builder` was canonicalized to `mcp-builder`.
- `template`, `template-skill`, and template folders were normalized under top-level `templates/`.
- Generated Gemini/Codex wrapper skills were not promoted as canonical skills.
- Nested bundle-local skill files were retained as references but renamed from `SKILL.md` to `SKILL_REFERENCE.md`.

## Removed Or Disabled Import Surfaces

- Upstream `.git` metadata was not imported.
- Upstream `.github` workflows were not imported.
- `.claude-plugin` and `.codex-plugin` directories inside imported skills were not activated.
- Upstream MCP/plugin manifests were copied only to inert `.disabled` files and later isolated under `integrations/`.
- Install/bootstrap scripts and sync automation were not promoted as active repo automation.

## Detailed Evidence

- `docs/generated/import_manifest.json`
- `docs/generated/import_summary.json`
- `docs/generated/duplicate_report.json`
- `docs/generated/post_import_duplicates.json`
- `docs/generated/demoted_nested_skill_references.json`
- `docs/generated/supporting_content.json`
