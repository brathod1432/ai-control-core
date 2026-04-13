# Obsidian Setup

Recommended Obsidian configuration for an LLM Wiki vault. None of this is strictly required â€” the wiki is just markdown files â€” but these settings remove friction.

## Open the vault

1. Obsidian â†’ "Open folder as vault" â†’ pick your initialized vault
2. The vault already has `wiki/`, `raw/`, `AI_RUNTIME_GUIDE.md`, `AGENTS.md`

## Settings â†’ Files and Links

- **Default location for new notes:** `wiki/`
- **New link format:** `Shortest path when possible` (keeps wikilinks clean)
- **Use `[[Wikilinks]]`:** ON
- **Attachment folder path:** `raw/assets/` (so clipped images land in `raw/`, not `wiki/`)
- **Automatically update internal links:** ON

## Settings â†’ Hotkeys

Search for and bind:
- **"Download attachments for current file"** â†’ `Ctrl/Cmd + Shift + D`
- **"Open graph view"** â†’ `Ctrl/Cmd + G`

## Core plugins to enable

- **Graph view** â€” see the shape of your wiki. Hubs, orphans, clusters.
- **Backlinks** â€” pane showing who links to the current page. Critical for browsing.
- **Outgoing links** â€” complementary pane.
- **Templates** â€” enable and set the template folder to `wiki/.templates`
- **Tag pane** â€” tag-driven navigation
- **Search** â€” obviously
- **Page preview** â€” hover a wikilink to preview
- **Canvas** â€” visual exploration, useful for synthesis work

## Recommended community plugins

- **Obsidian Web Clipper** (browser extension, not a plugin) â€” clip articles to `raw/articles/` as markdown
- **Dataview** â€” query over frontmatter. Dynamic tables of "all concept pages touched by 3+ sources".
- **Marp for Obsidian** â€” render any markdown with `marp: true` frontmatter as a slide deck inside Obsidian. Pairs with `scripts/export_marp.py`.
- **Templater** â€” dynamic templates (optional, you can use the LLM for this)
- **Advanced Tables** â€” easier markdown table editing
- **Git** â€” commit on save, or hook into system git

## Dataview examples

Pages with 3+ sources:
```dataview
table updated, sources
from "wiki/concepts"
where sources >= 3
sort updated desc
```

Recently updated synthesis pages:
```dataview
list
from "wiki/synthesis"
sort updated desc
limit 10
```

Orphans (Dataview can't see inbound links â€” use the lint script for this).

## Git workflow

```bash
cd <vault>
git init
git add .
git commit -m "init wiki"

# After every session:
git add wiki/ log.md index.md
git commit -m "ingest: <source>"
```

The vault is a plain markdown repo. Version history, branching, collaboration â€” free.

## Tips

- **Use the graph view daily** â€” it's the fastest way to see structural drift
- **Pin `index.md`, `log.md`, and the active `synthesis/` page** to the sidebar tabs
- **Split view** â€” wiki on the left, chat/CLI on the right. You browse while the LLM edits.
- **Enable "strict line breaks"** so your LLM's markdown renders the way the LLM expects
- **Use images aggressively** â€” download them locally, reference from pages. The LLM can read them with its vision tool when needed.
