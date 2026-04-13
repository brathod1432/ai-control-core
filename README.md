# AI Operations Core

Model-agnostic repository for reusable AI operations assets: skills, agent guidance, rules, templates, standards, MCP references, security policy, and optional integration adapters.

The core repo is vendor-neutral by default. Platform-specific material is isolated under `integrations/` and treated as optional compatibility content.

## Start Here

Future AI assistants should read these first:

1. `AI_README.md`
2. `context/AI_PROJECT_CONTEXT.md`
3. `context/SECURITY_BOUNDARIES.md`
4. `context/USAGE_RULES.md`
5. `context/SKILLS_INDEX.md`

Do not scan the whole repository by default. Use the compact context files and then read only the target skill, template, standard, or integration.

## Core Structure

- `agents/` - model-neutral agent and persona guidance.
- `rules/` - reusable operating rules and command templates.
- `skills/` - canonical generic skill library.
- `templates/` - skill, agent, and operational templates.
- `standards/` - authoring, quality, documentation, git, and security standards.
- `mcp/` - generic Model Context Protocol references.
- `security/` - safe-by-default policy and guardrails.
- `docs/` - reports, structure docs, attribution, and compatibility notes.
- `context/` - compact AI-readable navigation files.
- `integrations/` - optional platform, client, vendor, and remote-service adapters.
- `scripts/` - deterministic local maintenance and validation scripts.

## Current Inventory

- Core skills: 237
- Optional integration skill-like assets: 813
- Total skill-like assets indexed: 1,050
- Disabled-by-default assets remain disabled after generalization.

## Safety Defaults

- No repository data may be transmitted externally by default.
- No secrets, `.env` files, SSH keys, cloud credentials, auth caches, or token stores may be read by default.
- Optional integrations require explicit human opt-in and bounded scope.
- Platform/plugin/MCP examples under `integrations/` are inert references unless explicitly enabled.

## Maintenance

Use Python 3.11+ and standard-library scripts:

```bash
python scripts/audit_skills.py --root . --json-out docs/generated/security_scan.json
python scripts/find_duplicates.py --root . --json-out docs/generated/post_import_duplicates.json
python scripts/build_context_index.py --root .
```

See `docs/GENERALIZATION_REPORT.md`, `docs/COMPATIBILITY_NOTES.md`, and `docs/REPO_STRUCTURE.md`.
