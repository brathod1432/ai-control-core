---
name: wiki-init
description: Bootstrap a fresh LLM Wiki vault with the three-layer structure, schema files, and starter templates. Usage /wiki-init <path> --topic "<topic>" [--tool all|claude-code|codex|cursor|antigravity]
---

# /wiki-init

Bootstrap a new LLM Wiki vault. Creates `raw/`, `wiki/{entities,concepts,sources,comparisons,synthesis}`, the index and log, and installs the schema file(s) for your LLM CLI of choice.

## Usage

```
/wiki-init <path> --topic "<one-line topic>"
/wiki-init <path> --topic "<topic>" --tool <claude-code|codex|cursor|antigravity|opencode|gemini-cli|all>
/wiki-init <path> --topic "<topic>" --force    # overwrite non-empty dir
```

## Examples

```
/wiki-init ~/vaults/research --topic "LLM interpretability"
/wiki-init ./book-wiki --topic "The Power Broker â€” Robert Caro" --tool all
/wiki-init ~/vaults/founders --topic "SaaS founder playbook" --tool codex
```

## What it creates

```
<path>/
â”œâ”€â”€ raw/
â”‚   â””â”€â”€ assets/
â”œâ”€â”€ wiki/
â”‚   â”œâ”€â”€ index.md              # from template
â”‚   â”œâ”€â”€ log.md                # from template
â”‚   â”œâ”€â”€ entities/
â”‚   â”œâ”€â”€ concepts/
â”‚   â”œâ”€â”€ sources/
â”‚   â”œâ”€â”€ comparisons/
â”‚   â”œâ”€â”€ synthesis/
â”‚   â””â”€â”€ .templates/           # page templates for reference
â”œâ”€â”€ AI_RUNTIME_GUIDE.md                 # if --tool claude-code or all
â”œâ”€â”€ AGENTS.md                 # if --tool codex|cursor|antigravity|opencode|gemini-cli|all
â”œâ”€â”€ .cursorrules              # if --tool cursor or all
â””â”€â”€ .gitignore
```

## Next steps

After init:
1. Open the vault in Obsidian
2. Drop a source into `raw/`
3. Run `/wiki-ingest raw/<your-file>`

## Script

- `engineering/llm-wiki/scripts/init_vault.py`

## Skill Reference

â†’ `engineering/llm-wiki/SKILL.md`
