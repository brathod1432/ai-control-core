# Third-Party Attribution

This repository is an internally unified derivative aggregation. Upstream branding, badges, marketplace installation flows, and marketing claims were not preserved as repo identity.

## ComposioHQ/awesome-claude-skills

- Source: `https://github.com/ComposioHQ/awesome-claude-skills`
- Imported areas:
  - unique standalone skills
  - Composio integration skill catalog as disabled-by-default reference skills
  - template material
  - selected plugin metadata as inert `.disabled` reference
- License notes:
  - Upstream README asserts Apache 2.0 for the collection.
  - No root license file was present in the downloaded tree.
  - Per-skill `LICENSE.txt` files were preserved where present in imported skill folders.
- Major modifications:
  - normalized paths and metadata
  - added safety overrides
  - disabled network/app integrations by default
  - removed active plugin surfaces and standalone upstream repo framing

## anthropics/skills

- Source: `https://github.com/anthropics/skills`
- Imported areas:
  - canonical skill format examples
  - reference skills
  - `spec/agent-skills-spec.md`
  - `template/SKILL.md`
  - MCP builder reference docs
  - third-party notices
- License notes:
  - Mixed licensing.
  - Many skills are Apache 2.0 with per-skill `LICENSE.txt`.
  - Document skills and `claude-api` materials may have source-available or restrictive Anthropic terms and must not be represented as ordinary open source.
  - `docs/licenses/anthropic-THIRD_PARTY_NOTICES.md` preserves upstream third-party notices.
- Major modifications:
  - used as canonical structure baseline
  - added safety overrides and metadata
  - disabled or opt-in guarded command/network helpers
  - removed official-brand/marketplace framing from repo-level docs

## alirezarezvani/claude-skills

- Source: `https://github.com/alirezarezvani/claude-skills`
- Imported areas:
  - root domain skills from business, engineering, finance, marketing, product, project management, and regulatory/security groups
  - agents
  - command templates
  - standards and conventions
  - templates
  - selected plugin/MCP metadata as inert `.disabled` reference
- License notes:
  - Root license is MIT and is preserved at `docs/licenses/alirezarezvani-claude-skills-MIT-LICENSE.txt`.
  - Nested MIT license files in imported bundle content remain in place where copied.
- Major modifications:
  - skipped generated `.gemini/skills/*` wrappers and `.codex/skills/*` pointers as primary content
  - demoted nested bundle-local `SKILL.md` files to `SKILL_REFERENCE.md`
  - added safety overrides and metadata
  - disabled installer, plugin, and MCP surfaces by default

## Attribution Policy

- Preserve upstream license files that ship inside imported skill folders.
- Do not imply endorsement by upstream maintainers.
- Do not restore upstream badges or marketing claims as internal repo identity.
- Treat restricted/source-available content according to upstream terms before redistribution outside this private/internal repo.
