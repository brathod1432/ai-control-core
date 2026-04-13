---
name: "finance-skills"
description: "Financial analyst agent skill and plugin for an agent runtime, Codex, an agent runtime, Cursor, OpenClaw. Ratio analysis, DCF valuation, budget variance, rolling forecasts. 4 Python tools (stdlib-only)."
version: 1.0.0
author: Alireza Rezvani
license: MIT
tags:
  - finance
  - financial-analysis
  - dcf
  - valuation
  - budgeting
agents:
  - claude-code
  - codex-cli
  - openclaw
---

## Internal Safety Override

- Status: active for local use.
- Keep operation local by default. Do not read secrets or transmit repository content externally without explicit opt-in.
- Audit categories: secrets.

# Finance Skills

Production-ready financial analysis skill for strategic decision-making.

## Quick Start

### an agent runtime
```
/read finance/financial-analyst/SKILL.md
```

### an agent runtime
```bash
npx agent-skills-cli add alirezarezvani/ai-ops-skills/finance
```

## Skills Overview

| Skill | Folder | Focus |
|-------|--------|-------|
| Financial Analyst | `financial-analyst/` | Ratio analysis, DCF, budget variance, forecasting |

## Python Tools

4 scripts, all stdlib-only:

```bash
python3 financial-analyst/scripts/ratio_calculator.py --help
python3 financial-analyst/scripts/dcf_valuation.py --help
python3 financial-analyst/scripts/budget_variance_analyzer.py --help
python3 financial-analyst/scripts/forecast_builder.py --help
```

## Rules

- Load only the specific skill SKILL.md you need
- Always validate financial outputs against source data
