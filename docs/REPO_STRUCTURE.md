# Repository Structure

## Core

- `agents/`
  - Model-neutral agent and persona guidance.
- `rules/`
  - Generic operating rules and command templates.
- `skills/`
  - Canonical reusable skills.
  - Current core skill count: 237.
- `templates/`
  - Skill, agent, and operational templates.
- `standards/`
  - Authoring, quality, documentation, git, and security standards.
- `mcp/`
  - Generic Model Context Protocol references.
- `security/`
  - Security policy and safe-use boundaries.
- `docs/`
  - Human-readable reports and generated evidence.
- `context/`
  - Compact AI-readable navigation files.
- `scripts/`
  - Deterministic maintenance and validation scripts.

## Optional Integrations

- `integrations/platforms/`
  - Platform or model-client compatibility material.
  - Examples: Anthropic, Codex, Google Gemini, Composio.
- `integrations/network-services/`
  - Disabled-by-default remote service integration skills.
- `integrations/mcp-clients/`
  - Disabled client-specific MCP config examples.

## Canonical Skill Convention

Each canonical skill or integration skill-like asset contains:

- `SKILL.md`
- `SKILL_METADATA.json`
- optional references/assets/scripts
- `DISABLED.md` when status is `disabled_by_default`

`SKILL_METADATA.json` is the source of truth for:

- name
- category
- status
- location type
- source repository
- risk categories

## Generated Reports

- `docs/generated/current_inventory_summary.json`
- `docs/generated/import_manifest.json`
- `docs/generated/import_summary.json`
- `docs/generated/duplicate_report.json`
- `docs/generated/post_import_duplicates.json`
- `docs/generated/generalization_renames.json`
- `docs/generated/security_scan.json`
