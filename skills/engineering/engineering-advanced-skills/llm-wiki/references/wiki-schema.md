# Wiki Schema

The vault has three layers. The LLM must respect the boundaries.

## Layout

```
<vault>/
â”œâ”€â”€ raw/                        # IMMUTABLE sources (you own)
â”‚   â”œâ”€â”€ articles/*.md           # Obsidian Web Clipper output
â”‚   â”œâ”€â”€ papers/*.pdf
â”‚   â”œâ”€â”€ notes/*.md              # your own notes, journal entries
â”‚   â””â”€â”€ assets/                 # images downloaded by Obsidian
â”œâ”€â”€ wiki/                       # LLM-owned knowledge base
â”‚   â”œâ”€â”€ index.md                # content catalog â€” updated every ingest
â”‚   â”œâ”€â”€ log.md                  # append-only timeline
â”‚   â”œâ”€â”€ entities/               # people, orgs, places, products
â”‚   â”œâ”€â”€ concepts/               # ideas, theories, frameworks, methods
â”‚   â”œâ”€â”€ sources/                # one summary page per ingested source
â”‚   â”œâ”€â”€ comparisons/            # cross-source analysis / contrasts
â”‚   â”œâ”€â”€ synthesis/              # high-level theses, overviews
â”‚   â””â”€â”€ .templates/             # page templates (reference only, not indexed)
â”œâ”€â”€ AI_RUNTIME_GUIDE.md                   # schema file for an agent runtime
â”œâ”€â”€ AGENTS.md                   # same schema for Codex/Cursor/Antigravity
â””â”€â”€ .cursorrules                # (optional) Cursor legacy
```

## Iron rules

1. **`raw/` is immutable.** The LLM reads from `raw/` but never writes to it. Never rename, never delete, never edit. If a source is wrong, the user edits it.
2. **All LLM writes go to `wiki/`.** No exceptions.
3. **Every ingest updates 5 files minimum:** the new source summary, the relevant entity/concept pages, `index.md`, `log.md`. A rich ingest touches 10-15.
4. **Every wiki page carries YAML frontmatter.** Without frontmatter, `update_index.py` and `lint_wiki.py` can't see it.

## Required page frontmatter

```yaml
---
title: Mechanistic Interpretability
category: concept            # entity | concept | source | comparison | synthesis
summary: Reverse-engineering neural networks into human-understandable circuits
tags: [interpretability, circuits, anthropic]
sources: 3                   # optional â€” number of sources touching this page
updated: 2026-04-10          # LLM updates this on every edit
---
```

Allowed `category` values: `entity`, `concept`, `source`, `comparison`, `synthesis`.

## Naming conventions

- **Filenames:** `kebab-case.md` â€” lowercase, hyphens, no spaces
- **Entities:** `entities/<kebab-case-name>.md` â€” e.g. `entities/chris-olah.md`
- **Concepts:** `concepts/<kebab-case-name>.md` â€” e.g. `concepts/sparse-autoencoder.md`
- **Sources:** `sources/<short-slug>.md` â€” e.g. `sources/monosemanticity.md`
- **Comparisons:** `comparisons/<topic-a>-vs-<topic-b>.md`
- **Synthesis:** `synthesis/<topic>-overview.md` or `synthesis/<topic>-thesis.md`

## Linking

Use Obsidian wikilinks. Three forms:

```
[[concepts/sparse-autoencoder]]                           # full path
[[concepts/sparse-autoencoder|sparse autoencoders]]       # custom display text
[[sparse-autoencoder]]                                    # stem â€” resolves if unique
```

The linter resolves stem links by matching against filenames. Prefer full paths when ambiguous.

## Cross-reference rules

- **Every entity mentioned in a concept/source page must be a wikilink.** If the entity page doesn't exist yet, create it.
- **Every concept mentioned in a source summary must be a wikilink.** Same rule.
- **Contradictions get flagged inline** with a `> âš ï¸ Contradiction:` callout, and the source pages that disagree are linked from the callout.
- **Synthesis pages link back to every concept and source they draw on.**

## Index discipline

`wiki/index.md` is regenerated, not hand-edited. Either:

- Run `python scripts/update_index.py --vault .` after every ingest, OR
- Have the LLM rewrite the relevant section inline.

The index groups pages by `category`, alphabetized by title. Each entry is one line with a wikilink, summary, and optional metadata.

## Log discipline

`wiki/log.md` is append-only. Every entry starts with a standardized header so `grep "^## \[" log.md | tail -5` returns the last 5 entries.

```
## [2026-04-10] ingest | Anthropic Monosemanticity
Added sources/monosemanticity.md. Updated concepts/sparse-autoencoder,
concepts/polysemanticity, entities/anthropic-interpretability-team. Flagged
contradiction with sources/distributed-representations on feature basis claim.
```

Valid ops: `ingest`, `query`, `lint`, `create`, `update`, `delete`, `note`.
