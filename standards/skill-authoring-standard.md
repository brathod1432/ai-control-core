# Skill Authoring Standard

The DNA of every skill in this repository. Follow this standard when creating new skills or upgrading existing ones.

---

## SKILL.md Template

```markdown
---
name: skill-name
description: "When to use this skill. Include trigger keywords and phrases users might say. Mention related skills for disambiguation."
license: MIT
metadata:
  version: 1.0.0
  author: Alireza Rezvani
  category: domain-name
  updated: YYYY-MM-DD
---

# Skill Name

You are an expert in [domain]. Your goal is [specific outcome for the user].

## Before Starting

**Check for context first:**
If `[domain]-context.md` exists, read it before asking questions. Use that context and only ask for information not already covered or specific to this task.

Gather this context (ask if not provided):

### 1. Current State
- What exists today?
- What's working / not working?

### 2. Goals
- What outcome do they want?
- What constraints exist?

### 3. [Domain-Specific Context]
- [Questions specific to this skill]

## How This Skill Works

This skill supports [N] modes:

### Mode 1: Build from Scratch
When starting fresh â€” no existing [artifact] to work with.

### Mode 2: Optimize Existing
When improving something that already exists. Analyze what's working, identify gaps, recommend changes.

### Mode 3: [Situation-Specific]
When [specific scenario that needs a different approach].

## [Core Content Sections]

[Action-oriented workflow. Not a textbook â€” a practitioner guiding you through it.]

[Tables for structured information. Checklists for processes. Examples for clarity.]

## Proactive Triggers

Surface these issues WITHOUT being asked when you notice them in context:

- [Trigger 1: specific condition â†’ what to flag]
- [Trigger 2: specific condition â†’ what to flag]
- [Trigger 3: specific condition â†’ what to flag]

## Output Artifacts

| When you ask for... | You get... |
|---------------------|------------|
| [Common request 1] | [Specific deliverable with format] |
| [Common request 2] | [Specific deliverable with format] |
| [Common request 3] | [Specific deliverable with format] |

## Communication

All output follows the structured communication standard:
- **Bottom line first** â€” answer before explanation
- **What + Why + How** â€” every finding has all three
- **Actions have owners and deadlines** â€” no "we should consider"
- **Confidence tagging** â€” ðŸŸ¢ verified / ðŸŸ¡ medium / ðŸ”´ assumed

## Related Skills

- **skill-name**: Use when [specific scenario]. NOT for [disambiguation].
- **skill-name**: Use when [specific scenario]. NOT for [disambiguation].
- **skill-name**: Use when [specific scenario]. NOT for [disambiguation].
```

---

## The 10 Patterns

### Pattern 1: Context-First

Every skill checks for domain context before asking questions. Only ask for what's missing.

**Implementation:**
```markdown
## Before Starting

**Check for context first:**
If `marketing-context.md` exists, read it before asking questions.
Use that context and only ask for information not already covered.
```

**Domain context files:**

| Domain | Context File | Created By |
|--------|-------------|-----------|
| C-Suite | `company-context.md` | `/cs:setup` (cs-onboard skill) |
| Marketing | `marketing-context.md` | marketing-context skill |
| Engineering | `project-context.md` | codebase-onboarding skill |
| Product | `product-context.md` | product-strategist skill |
| RA/QM | `regulatory-context.md` | regulatory-affairs-head skill |

**Rules:**
- If context exists â†’ read it, use it, only ask for gaps
- If context doesn't exist â†’ offer to create it (auto-draft from available info)
- Never dump all questions at once â€” conversational, one section at a time
- Push for verbatim language â€” exact customer/user phrases beat polished descriptions

---

### Pattern 2: Practitioner Voice

Every skill opens with an expert persona and clear goal. Not a textbook â€” a senior practitioner coaching you.

**Implementation:**
```markdown
You are an expert in [domain]. Your goal is [outcome].
```

**Rules:**
- Write as someone who has done this 100 times
- Use contractions, direct language
- If something sounds like a Wikipedia article, rewrite it
- Opinionated > neutral. State what works and what doesn't.
- "Do X" beats "You might consider X"
- Industry jargon is fine when talking to practitioners â€” explain when talking to founders

**Anti-patterns:**
- âŒ "This skill provides comprehensive coverage of..."
- âŒ "The following section outlines the various approaches to..."
- âŒ "It is recommended that one should consider..."
- âœ… "You are an expert in SaaS pricing. Your goal is to help design pricing that captures value."
- âœ… "Lead with their world, not yours."
- âœ… "If it sounds like marketing copy, rewrite it."

---

### Pattern 3: Multi-Mode Workflows

Most skills have 2-3 natural entry points. Design for all of them.

**Implementation:**
```markdown
## How This Skill Works

### Mode 1: Build from Scratch
When starting fresh â€” [describe the greenfield scenario].

### Mode 2: Optimize Existing  
When [artifact] exists but isn't performing. Analyze â†’ identify gaps â†’ recommend.

### Mode 3: [Situation-Specific]
When [edge case or specific scenario that needs a different approach].
```

**Common mode pairs:**

| Skill Type | Mode 1 | Mode 2 | Mode 3 |
|-----------|--------|--------|--------|
| CRO skills | Audit a page | Redesign flow | A/B test specific element |
| Content skills | Write new | Rewrite/optimize | Repurpose for channel |
| SEO skills | Full audit | Fix specific issue | Competitive gap analysis |
| Strategy skills | Create plan | Review/critique plan | Pivot existing plan |
| Analytics skills | Set up tracking | Debug tracking | Analyze data |

**Rules:**
- Mode 2 (optimize) should ask for current performance data
- If user has performance data â†’ use it to inform recommendations
- Each mode should be self-contained (don't assume they read the other modes)

---

### Pattern 4: Related Skills Navigation

Every skill ends with a curated list of related skills. Not just links â€” **when to use each and when NOT to.**

**Implementation:**
```markdown
## Related Skills

- **copywriting**: For landing page and web copy. NOT for email sequences or ad copy.
- **page-cro**: For optimizing any marketing page. NOT for signup flows (use signup-flow-cro).
- **email-sequence**: For lifecycle/nurture emails. NOT for cold outreach (use cold-email).
```

**Rules:**
- Include 3-7 related skills (not all of them â€” curate)
- Each entry: skill name + WHEN to use + WHEN NOT TO (disambiguation)
- Cross-references must be bidirectional (A mentions B, B mentions A)
- Include cross-domain references when relevant (e.g., marketing skill â†’ business-growth skill)
- Group by relationship type if >5: "Works with", "Instead of", "After this"

---

### Pattern 5: Reference Separation

SKILL.md is the workflow. Reference docs are the knowledge base. Keep them separate.

**Implementation:**
```
skill-name/
â”œâ”€â”€ SKILL.md              # â‰¤10KB â€” what to do, how to decide, when to act
â”œâ”€â”€ references/
â”‚   â”œâ”€â”€ frameworks.md      # Deep framework catalog
â”‚   â”œâ”€â”€ benchmarks.md      # Industry data and benchmarks
â”‚   â”œâ”€â”€ platform-specs.md  # Platform-specific details
â”‚   â””â”€â”€ examples.md        # Real-world examples
â”œâ”€â”€ templates/
â”‚   â””â”€â”€ template.md        # User-fillable templates
â””â”€â”€ scripts/
    â””â”€â”€ tool.py            # Python automation
```

**Rules:**
- SKILL.md â‰¤10KB â€” if it's longer, move content to references
- SKILL.md links to references inline: `See `references/frameworks.md` for the full catalog.`
- References are loaded on demand â€” zero startup cost
- Each reference doc is self-contained (can be read independently)
- Templates are user-fillable files with clear placeholder markers

---

### Pattern 6: Proactive Triggers

Skills surface issues without being asked when they detect patterns in context.

**Implementation:**
```markdown
## Proactive Triggers

Surface these without being asked:

- **[Condition]** â†’ [What to flag and why]
- **[Condition]** â†’ [What to flag and why]
```

**Rules:**
- 4-6 triggers per skill
- Each trigger: specific condition + business consequence
- Triggers should be things the user wouldn't think to ask about
- Format: condition â†’ flag â†’ recommended action
- Don't trigger on obvious things â€” trigger on hidden risks

**Examples:**
- SEO: "Keyword cannibalization detected â€” two pages targeting the same term" â†’ flag
- Pricing: "Conversion rate >40% â€” likely underpriced" â†’ flag
- Content: "No content updated in 6+ months" â†’ flag
- CRO: "Form has >7 fields with no multi-step" â†’ flag

---

### Pattern 7: Output Artifacts

Map common requests to specific, concrete deliverables.

**Implementation:**
```markdown
## Output Artifacts

| When you ask for... | You get... |
|---------------------|------------|
| "Help with pricing" | Pricing recommendation with tier structure, value metrics, and competitive positioning |
| "Audit my SEO" | SEO scorecard (0-100) with prioritized fixes and quick wins |
```

**Rules:**
- 4-6 artifacts per skill
- Each artifact has a specific format (scorecard, matrix, plan, audit, template)
- Artifacts are actionable â€” not just analysis, but recommendations with next steps
- Include what the output looks like (table? checklist? narrative?)

---

### Pattern 8: Quality Loop

Skills self-verify before presenting findings.

**Implementation:**
```markdown
## Communication

All output passes quality verification:
- Self-verify: source attribution, assumption audit, confidence scoring
- Peer-verify: cross-functional claims validated by the owning skill
- Output format: Bottom Line â†’ What (with confidence) â†’ Why â†’ How to Act â†’ Your Decision
- Results only. Every finding tagged: ðŸŸ¢ verified, ðŸŸ¡ medium, ðŸ”´ assumed.
```

**Rules:**
- Every finding tagged with confidence level
- Assumptions explicitly marked as assumptions
- "I don't know" > fake confidence
- Cross-functional claims reference the relevant skill
- High-stakes recommendations get extra scrutiny

---

### Pattern 9: Communication Standard

Structured output format for all skill output.

**Standard output:**
```
BOTTOM LINE: [One sentence answer]

WHAT:
â€¢ [Finding 1] â€” ðŸŸ¢/ðŸŸ¡/ðŸ”´
â€¢ [Finding 2] â€” ðŸŸ¢/ðŸŸ¡/ðŸ”´

WHY THIS MATTERS: [Business impact]

HOW TO ACT:
1. [Action] â†’ [Owner] â†’ [Deadline]

YOUR DECISION (if needed):
Option A: [Description] â€” [Trade-off]
Option B: [Description] â€” [Trade-off]
```

**Rules:**
- Bottom line first â€” always
- Max 5 bullets per section
- Actions have owners and deadlines
- Decisions framed as options with trade-offs
- No process narration ("First I analyzed...") â€” results only

---

### Pattern 10: Python Tools

Stdlib-only automation that provides quantitative analysis.

**Implementation:**
```python
#!/usr/bin/env python3
"""Tool description â€” what it does in one line."""

import json
import sys
from collections import Counter

def main():
    # Accept input from file arg or stdin
    # Process with stdlib only
    # Output JSON for programmatic use
    # Also print human-readable summary
    pass

if __name__ == "__main__":
    main()
```

**Rules:**
- **stdlib-only** â€” zero external dependencies (no pip install)
- **CLI-first** â€” run from command line with file args or stdin
- **JSON output** â€” structured output for integration
- **Sample data embedded** â€” runs with zero config for demo/testing
- **One tool, one job** â€” focused, not Swiss Army knife
- **Scoring tools output 0-100** â€” consistent scale across all tools

**Naming convention:** `snake_case_verb_noun.py` (e.g., `seo_checker.py`, `headline_scorer.py`, `churn_risk_scorer.py`)

---

## File Structure Standard

```
skill-name/
â”œâ”€â”€ SKILL.md                    # â‰¤10KB â€” workflow, decisions, actions
â”œâ”€â”€ references/                  # Deep knowledge (loaded on demand)
â”‚   â”œâ”€â”€ [topic]-guide.md        # Comprehensive guide
â”‚   â”œâ”€â”€ [topic]-benchmarks.md   # Industry data
â”‚   â””â”€â”€ [topic]-examples.md    # Real-world examples
â”œâ”€â”€ templates/                   # User-fillable templates
â”‚   â””â”€â”€ [artifact]-template.md  # With placeholder markers
â””â”€â”€ scripts/                     # Python automation
    â””â”€â”€ [verb]_[noun].py        # Stdlib-only, CLI-first
```

**Naming rules:**
- Skill folder: `kebab-case`
- Python scripts: `snake_case.py`
- Reference docs: `kebab-case.md`
- Templates: `kebab-case-template.md`

---

## Quality Checklist

Before a skill is considered done:

### Structure
- [ ] YAML frontmatter with name, description (trigger keywords), version
- [ ] Practitioner voice â€” "You are an expert in X. Your goal is Y."
- [ ] Context-first â€” checks domain context before asking questions
- [ ] Multi-mode â€” at least 2 workflows (build/optimize)
- [ ] SKILL.md â‰¤10KB â€” heavy content in references/

### Content
- [ ] Action-oriented â€” tells you what to do, not just what exists
- [ ] Opinionated â€” states what works, not just options
- [ ] Tables for structured comparisons
- [ ] Checklists for processes
- [ ] Examples for clarity

### Integration
- [ ] Related Skills section with WHEN/NOT disambiguation
- [ ] Cross-references are bidirectional
- [ ] Listed in domain AI_RUNTIME_GUIDE.md
- [ ] Listed in `.codex/skills-index.json`
- [ ] Listed in `.claude-plugin/marketplace.json`
- [ ] Listed in `.gemini/skills-index.json` (run `./scripts/gemini-install.sh`)

### Quality Standard
- [ ] Proactive Triggers (4-6 per skill)
- [ ] Output Artifacts table (4-6 per skill)
- [ ] Communication standard reference
- [ ] Confidence tagging on findings

### Automation (if applicable)
- [ ] Python tool(s) â€” stdlib-only, CLI-first, JSON output
- [ ] Sample data embedded â€” runs with zero config
- [ ] Scoring uses 0-100 scale

---

## Domain Context Files

| Domain | File | Sections |
|--------|------|----------|
| **C-Suite** | `company-context.md` | Stage, team, burn rate, competitive landscape, strategic priorities |
| **Marketing** | `marketing-context.md` | Brand voice, style guide, target keywords, internal links map, competitor analysis, audience personas, writing examples, customer language |
| **Engineering** | `project-context.md` | Tech stack, architecture, conventions, CI/CD, testing strategy |
| **Product** | `product-context.md` | Roadmap, personas, metrics, feature priorities, user research |
| **RA/QM** | `regulatory-context.md` | Device classification, applicable standards, audit schedule, SOUP list |

Each domain's context skill creates this file via guided interview + auto-draft from available information.

---

*This standard applies to all new skills and skill upgrades across the entire repository.*
*Version: 1.0.0 | Created: 2026-03-06*
