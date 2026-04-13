---
description: Update repository documentation, context indexes, and validation reports.
---

After creating or changing skills, agents, rules, templates, standards, or integrations, update the compact context and validation reports.

## Steps

1. Inspect changed files.

```bash
git status --short
```

2. Rebuild the compact skill index.

```bash
python scripts/build_context_index.py --root .
```

3. Re-run duplicate detection.

```bash
python scripts/find_duplicates.py --root . --json-out docs/generated/post_import_duplicates.json
```

4. Re-run security scanning.

```bash
python scripts/audit_skills.py --root . --json-out docs/generated/security_scan.json
```

5. Update human docs if paths, counts, or safety boundaries changed.

## Compatibility Notes

Platform-specific sync scripts, plugin publishing, or marketplace updates belong under `integrations/` and must remain opt-in. Do not run client-specific sync or publishing commands unless the task explicitly asks for that platform.
