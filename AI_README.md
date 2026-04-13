# AI README

START HERE before reading the repository.

This is a model-agnostic AI operations repository. Core files should work for any capable AI assistant or agent runtime. Platform-specific files live under `integrations/`.

Read, in order:

1. `context/AI_PROJECT_CONTEXT.md`
2. `context/SECURITY_BOUNDARIES.md`
3. `context/USAGE_RULES.md`
4. `context/SKILLS_INDEX.md`
5. Target `SKILL_METADATA.json`
6. Target `SKILL.md`

Status meanings:

- `active_local` - local use is allowed; do not read secrets or transmit repo data.
- `opt_in_external` - external access requires explicit human opt-in and bounded data scope.
- `disabled_by_default` - read-only reference unless explicitly enabled.

Source-of-truth docs:

- `docs/GENERALIZATION_REPORT.md`
- `docs/COMPATIBILITY_NOTES.md`
- `docs/REPO_STRUCTURE.md`
- `docs/SECURITY_AUDIT_REPORT.md`
- `security/SECURITY_POLICY.md`

Do not assume named platforms in `integrations/` are active. Treat them as optional compatibility examples.
