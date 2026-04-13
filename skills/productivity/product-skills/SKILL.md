---
name: "product-skills"
description: "10 product agent skills and plugins for an agent runtime, Codex, an agent runtime, Cursor, OpenClaw. PM toolkit (RICE), agile PO, product strategist (OKR), UX researcher, UI design system, competitive teardown, landing page generator, SaaS scaffolder, research summarizer. Python tools (stdlib-only)."
version: 1.1.0
author: Alireza Rezvani
license: MIT
tags:
  - product
  - product-management
  - ux
  - ui
  - saas
  - agile
agents:
  - claude-code
  - codex-cli
  - openclaw
---

## Internal Safety Override

- Status: active for local use.
- Keep operation local by default. Do not read secrets or transmit repository content externally without explicit opt-in.
- Audit categories: secrets.

# Product Team Skills

8 production-ready product skills covering product management, UX/UI design, and SaaS development.

## Quick Start

### an agent runtime
```
/read product-team/product-manager-toolkit/SKILL.md
```

### an agent runtime
```bash
npx agent-skills-cli add alirezarezvani/ai-ops-skills/product-team
```

## Skills Overview

| Skill | Folder | Focus |
|-------|--------|-------|
| Product Manager Toolkit | `product-manager-toolkit/` | RICE prioritization, customer discovery, PRDs |
| Agile Product Owner | `agile-product-owner/` | User stories, sprint planning, backlog |
| Product Strategist | `product-strategist/` | OKR cascades, market analysis, vision |
| UX Researcher Designer | `ux-researcher-designer/` | Personas, journey maps, usability testing |
| UI Design System | `ui-design-system/` | Design tokens, component docs, responsive |
| Competitive Teardown | `competitive-teardown/` | Systematic competitor analysis |
| Landing Page Generator | `landing-page-generator/` | Conversion-optimized pages |
| SaaS Scaffolder | `saas-scaffolder/` | Production SaaS boilerplate |

## Python Tools

9 scripts, all stdlib-only:

```bash
python3 product-manager-toolkit/scripts/rice_prioritizer.py --help
python3 product-strategist/scripts/okr_cascade_generator.py --help
```

## Rules

- Load only the specific skill SKILL.md you need
- Use Python tools for scoring and analysis, not manual judgment
