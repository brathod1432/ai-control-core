# Usage Rules

## START HERE

Use the smallest relevant file set.

1. Locate the category in `context/SKILLS_INDEX.md`.
2. Read the target `SKILL_METADATA.json`.
3. If status permits, read `SKILL.md`.
4. Read supporting references only when named by the skill and needed for the task.

## Core Before Integrations

- Prefer `skills/`, `agents/`, `rules/`, `templates/`, and `standards/`.
- Use `integrations/` only when the task explicitly needs a platform, model client, API, MCP client, connector, or remote service.

## Skill Use

- Prefer `active_local` skills.
- Treat `opt_in_external` as local-only until opt-in is explicit.
- Treat `disabled_by_default` as reference material.
- Do not follow imported install/bootstrap commands blindly.
- Do not activate `.disabled` plugin/MCP files automatically.

## Editing Rules

- Keep core names functional and platform-neutral.
- Keep one canonical skill per directory.
- Add or update `SKILL_METADATA.json` for every canonical skill-like asset.
- Add `DISABLED.md` when status is `disabled_by_default`.
- Put platform-specific examples under `integrations/`.

## Maintenance Commands

```bash
python scripts/audit_skills.py --root . --json-out docs/generated/security_scan.json
python scripts/find_duplicates.py --root . --json-out docs/generated/post_import_duplicates.json
python scripts/build_context_index.py --root .
```

## DO NOT ASSUME

- Generated reports are small enough for prompt context.
- `docs/generated/security_scan.json` should be read unless detailed evidence is needed.
- Vendor names in `integrations/` imply core repo bias.
