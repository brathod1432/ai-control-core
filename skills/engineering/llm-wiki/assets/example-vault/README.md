# Example Vault â€” "LLM Interpretability"

A minimal worked example to study before initializing your own.

**Not** a runnable vault â€” it's missing most files. The goal is to show what a healthy small vault looks like after ingesting 2-3 sources on one topic.

## Layout

```
example-vault/
â”œâ”€â”€ raw/
â”‚   â””â”€â”€ assets/
â”œâ”€â”€ wiki/
â”‚   â”œâ”€â”€ index.md
â”‚   â”œâ”€â”€ log.md
â”‚   â”œâ”€â”€ entities/
â”‚   â”‚   â””â”€â”€ anthropic.md
â”‚   â”œâ”€â”€ concepts/
â”‚   â”‚   â””â”€â”€ sparse-autoencoder.md
â”‚   â”œâ”€â”€ sources/
â”‚   â”‚   â””â”€â”€ monosemanticity.md
â”‚   â””â”€â”€ synthesis/
â”‚       â””â”€â”€ interpretability-overview.md
â”œâ”€â”€ AI_RUNTIME_GUIDE.md
â””â”€â”€ AGENTS.md
```

## What to notice

1. **Every page has frontmatter.** This is what makes the index + lint scripts work.
2. **The source page is the single source of truth** for claims from that paper. Other pages cite it rather than duplicating content.
3. **`index.md` is organized by category**, not chronologically.
4. **`log.md` uses the standardized header format** `## [YYYY-MM-DD] <op> | <title>`.
5. **Cross-references are wikilinks**, not prose references. `[[sources/monosemanticity]]`, not "see the Monosemanticity paper".
6. **The synthesis page has a `How this synthesis has changed` section.** Append-only history so you can see the thesis evolve.
