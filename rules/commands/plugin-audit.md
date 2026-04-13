---
description: Run a safe local audit on a skill or integration directory.
---

Audit the skill or integration at `$ARGUMENTS`. If no argument is provided, ask for the path.

## Audit Scope

1. Confirm the path exists.
2. Confirm whether it contains `SKILL.md`, `SKILL_METADATA.json`, `DISABLED.md`, scripts, references, assets, or platform manifests.
3. Read `SKILL_METADATA.json` first when present.
4. Identify status:
   - `active_local`
   - `opt_in_external`
   - `disabled_by_default`

## Required Checks

- Local path references resolve or are clearly historical/plain text.
- No secrets or credential examples are exposed.
- No command executes without source inspection.
- No network, browser, upload, publish, sync, or account action runs without explicit opt-in.
- Optional platform manifests remain under `integrations/` and are not copied into active config locations.

## Validation Commands

```bash
python scripts/audit_skills.py --root . --json-out docs/generated/security_scan.json
python scripts/find_duplicates.py --root . --json-out docs/generated/post_import_duplicates.json
python scripts/validate_references.py --root . --json-out docs/generated/reference_validation.json
python scripts/build_context_index.py --root .
```

## Output

Report:

- audited path
- status
- risk categories
- broken references, if any
- security concerns
- recommended status change, if any
- whether human opt-in is required
