# Repository Conventions

These conventions apply to humans and AI assistants working in this repository.

## Core Principles

- Keep core assets model-agnostic and vendor-neutral.
- Put platform-specific clients, plugins, launch files, or API examples under `integrations/`.
- Prefer functional names over model or vendor names.
- Keep security guardrails in core docs and in every skill status.
- Preserve attribution and license references in `docs/`.

## Skill Structure

Canonical core skills live under `skills/<category>/<skill-name>/`.

Required files:

- `SKILL.md`
- `SKILL_METADATA.json`

Optional files:

- `DISABLED.md` for disabled-by-default skills.
- `references/` for detailed local knowledge.
- `scripts/` for inspectable local helper scripts.
- `assets/` for examples and templates.

Nested examples that look like skills must use `SKILL_REFERENCE.md`, not `SKILL.md`, unless they are intended to be first-class canonical skills.

## Integration Structure

Optional integrations live under:

- `integrations/platforms/<platform>/`
- `integrations/network-services/<service>/`
- `integrations/mcp-clients/<client>/`

Integration content is not active by default. It may contain platform names because that is its purpose.

## Naming

- Use lower-case kebab-case for skill and integration folders.
- Use functional names in core areas.
- Use explicit platform names only under `integrations/` or attribution docs.

## Safety

- Do not export repository data by default.
- Do not read secrets by default.
- Do not auto-enable plugins, MCP servers, browser automation, or remote connectors.
- Review local scripts before executing them.
