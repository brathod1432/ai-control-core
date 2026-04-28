---
name: desktop-and-app-control
description: Use to design safe local desktop, browser, Office, screen, and application-control abilities for Jarvis on a laptop. Covers active window inspection, screenshots, Chrome/CDP, Office automation, keyboard/mouse control, and approval gates.
category: local-agent
---

## Internal Safety Override

- Status: disabled for direct control until the user approves a specific local target and action.
- Prefer inspection before control.
- Never click destructive UI controls, submit forms, send messages, buy, publish, deploy, or close unsaved work without explicit approval.
- Do not dump cookies, browser storage, passwords, hidden fields, or private app data.

# Desktop And App Control

## Current Model Baseline

All agents and subagents use the same single local Ollama `qwen2.5:3b` model through `http://127.0.0.1:11434`. No cloud LLMs, remote model APIs, separate providers, or per-agent model pools are used; browser, app, screenshot, and desktop-control workers are prompts over this same model.

## Capability Ladder

Level 1: Screenshot or active-window summary.
Level 2: Read-only app inspection.
Level 3: Reversible visual modification or highlighting.
Level 4: Scoped app interaction.
Level 5: High-impact app action requiring confirmation.

## Browser

Use local Chrome/CDP only on loopback.
Capabilities:
- List tabs.
- Inspect DOM and accessibility tree.
- Capture screenshot.
- Read console and failed network metadata.
- Apply reversible page-local mutations.

Stop before:
- Reading cookies/storage.
- Submitting forms.
- Sending messages.
- Modifying production data.

## Office

Use file-level libraries first. Use COM only when installed Office behavior matters.
Capabilities:
- Inspect Word/Excel/PowerPoint files.
- Create copies.
- Render/export locally.
- Recalculate approved workbooks.

Stop before:
- Running macros.
- Refreshing external links.
- Saving over originals.
- Closing user-open documents.

## OS Control

Keyboard/mouse automation is highest risk.
Rules:
- Prefer app APIs over coordinate clicks.
- Use dry-run descriptions.
- Require confirmation before clicks that change state.
- Keep an emergency stop.
