# Marketing Team Expansion â€” Execution Plan

## Final Architecture

```
CMO Advisor (c-level-advisor/cmo-advisor/)
  â”‚
  â”‚ reads company-context.md + marketing-context.md
  â”‚
Marketing Ops (router + orchestrator)
  â”‚
  â”œâ”€â”€ Content Pod (8)
  â”‚   â”œâ”€â”€ content-creator .......... [UPGRADE] add context integration, quality loop
  â”‚   â”œâ”€â”€ content-strategy ......... [IMPORT]  from workspace
  â”‚   â”œâ”€â”€ copywriting .............. [IMPORT]  from workspace
  â”‚   â”œâ”€â”€ copy-editing ............. [IMPORT]  from workspace
  â”‚   â”œâ”€â”€ social-content ........... [IMPORT]  from workspace
  â”‚   â”œâ”€â”€ marketing-ideas .......... [IMPORT]  from workspace
  â”‚   â”œâ”€â”€ content-production ....... [NEW]     researchâ†’writeâ†’optimize pipeline
  â”‚   â””â”€â”€ content-humanizer ........ [NEW]     AI watermark removal, voice injection
  â”‚
  â”œâ”€â”€ SEO Pod (5)
  â”‚   â”œâ”€â”€ seo-audit ................ [IMPORT]  from workspace + add seo_checker.py
  â”‚   â”œâ”€â”€ programmatic-seo ......... [IMPORT]  from workspace
  â”‚   â”œâ”€â”€ ai-seo ................... [NEW]     AEO, GEO, LLMO optimization
  â”‚   â”œâ”€â”€ schema-markup ............ [NEW]     JSON-LD, structured data
  â”‚   â””â”€â”€ site-architecture ........ [NEW]     URL structure, nav, internal linking
  â”‚
  â”œâ”€â”€ CRO Pod (6)
  â”‚   â”œâ”€â”€ page-cro ................. [IMPORT]  from workspace
  â”‚   â”œâ”€â”€ form-cro ................. [IMPORT]  from workspace
  â”‚   â”œâ”€â”€ signup-flow-cro .......... [IMPORT]  from workspace
  â”‚   â”œâ”€â”€ onboarding-cro ........... [IMPORT]  from workspace
  â”‚   â”œâ”€â”€ popup-cro ................ [IMPORT]  from workspace
  â”‚   â””â”€â”€ paywall-upgrade-cro ...... [IMPORT]  from workspace
  â”‚
  â”œâ”€â”€ Channels Pod (5)
  â”‚   â”œâ”€â”€ email-sequence ........... [IMPORT]  from workspace
  â”‚   â”œâ”€â”€ paid-ads ................. [IMPORT]  from workspace
  â”‚   â”œâ”€â”€ social-media-manager ..... [UPGRADE] rename + expand from social-media-analyzer
  â”‚   â”œâ”€â”€ cold-email ............... [NEW]     B2B outreach sequences
  â”‚   â””â”€â”€ ad-creative .............. [NEW]     bulk ad generation + iteration
  â”‚
  â”œâ”€â”€ Growth Pod (3)
  â”‚   â”œâ”€â”€ ab-test-setup ............ [IMPORT]  from workspace
  â”‚   â”œâ”€â”€ referral-program ......... [NEW]     referral + affiliate programs
  â”‚   â””â”€â”€ free-tool-strategy ....... [NEW]     engineering as marketing
  â”‚
  â”œâ”€â”€ Intelligence Pod (4)
  â”‚   â”œâ”€â”€ campaign-analytics ....... [UPGRADE] add cross-channel synthesis
  â”‚   â”œâ”€â”€ competitor-alternatives .. [IMPORT]  from workspace
  â”‚   â”œâ”€â”€ marketing-psychology ..... [IMPORT]  from workspace
  â”‚   â””â”€â”€ analytics-tracking ....... [NEW]     GA4, GTM, event tracking setup
  â”‚
  â””â”€â”€ Sales & GTM Pod (2)
      â”œâ”€â”€ launch-strategy .......... [IMPORT]  from workspace
      â””â”€â”€ pricing-strategy ......... [NEW]     pricing, packaging, monetization

  Standalone (keep in place, no pod):
  â”œâ”€â”€ marketing-demand-acquisition . [KEEP]    already in repo
  â”œâ”€â”€ marketing-strategy-pmm ....... [KEEP]    already in repo
  â”œâ”€â”€ app-store-optimization ....... [KEEP]    already in repo
  â””â”€â”€ prompt-engineer-toolkit ...... [KEEP]    already in repo

  Cross-Domain References (marketing-ops routes to these):
  â”œâ”€â”€ business-growth/revenue-operations/     (RevOps)
  â”œâ”€â”€ business-growth/sales-engineer/         (Sales Enablement)
  â”œâ”€â”€ business-growth/customer-success-manager/ (Churn Prevention)
  â”œâ”€â”€ product-team/landing-page-generator/    (Landing Pages)
  â”œâ”€â”€ product-team/competitive-teardown/      (Competitive Analysis)
  â””â”€â”€ engineering-team/email-template-builder/ (Email Templates)
```

## Totals

| Action | Count |
|--------|-------|
| Import from workspace | 20 |
| Upgrade existing | 3 |
| Build new | 13 |
| Keep as-is | 4 |
| Cross-domain refs | 6 |
| **Total marketing skills** | **39** |
| **New Python tools** | ~20 |
| **New reference docs** | ~25 |
| **New agents** | 5-8 |

---

## Iteration 1: Foundation + Import (20 workspace skills + 2 new)

### 1A: Create branch and foundation skills

**marketing-context/** (NEW â€” the foundation every skill reads)
```
marketing-context/
â”œâ”€â”€ SKILL.md                    # How to use, interview flow
â”œâ”€â”€ templates/
â”‚   â”œâ”€â”€ brand-voice.md          # Voice pillars, tone by content type, terminology
â”‚   â”œâ”€â”€ style-guide.md          # Grammar, formatting, capitalization
â”‚   â”œâ”€â”€ target-keywords.md      # Keyword clusters, search intent, current rankings
â”‚   â”œâ”€â”€ internal-links-map.md   # Key pages, anchor text, topic clusters
â”‚   â”œâ”€â”€ competitor-analysis.md  # Primary competitors, strategies, gaps
â”‚   â”œâ”€â”€ writing-examples.md     # 3-5 exemplary pieces with annotations
â”‚   â””â”€â”€ audience-personas.md    # ICP, segments, pain points, buying triggers
â””â”€â”€ scripts/
    â””â”€â”€ context_validator.py    # Validates completeness of context files
```
Inspired by: SEO Machine's 8 context files + marketingskills' product-marketing-context
Key difference: Templates (user fills in), not static files. Validator script checks completeness.

**marketing-ops/** (NEW â€” the router)
```
marketing-ops/
â”œâ”€â”€ SKILL.md                    # Router logic, pod assignments, escalation
â”œâ”€â”€ references/
â”‚   â”œâ”€â”€ routing-matrix.md       # Trigger keywords â†’ skill mapping (all 39 + 6 cross-domain)
â”‚   â”œâ”€â”€ campaign-workflow.md    # End-to-end campaign orchestration steps
â”‚   â””â”€â”€ quality-checklist.md    # Pre-delivery quality gate (mirrors C-Suite standard)
â””â”€â”€ scripts/
    â””â”€â”€ campaign_tracker.py     # Track campaign status, tasks, owners, deadlines
```

### 1B: Import 20 workspace skills

For each imported skill:
1. Copy from `~/.openclaw/workspace/skills/{name}/` to `marketing-skill/{name}/`
2. Verify YAML frontmatter (name, description, license, metadata)
3. Add `## Related Skills` section with cross-references
4. Add `## Integration` table (which pod, which skills it works with, cross-domain refs)
5. Add `## Communication` section (references marketing quality standard)

**Import batch (parallel â€” 4 subagents):**

| Subagent | Skills | Pod |
|----------|--------|-----|
| content-importer | content-strategy, copywriting, copy-editing, social-content, marketing-ideas | Content |
| seo-cro-importer | seo-audit, programmatic-seo, page-cro, form-cro, signup-flow-cro | SEO + CRO |
| cro-channel-importer | onboarding-cro, popup-cro, paywall-upgrade-cro, email-sequence, paid-ads | CRO + Channels |
| growth-intel-importer | ab-test-setup, competitor-alternatives, marketing-psychology, launch-strategy, brand-guidelines | Growth + Intel + GTM |

Each subagent:
- Copies skill folder
- Adds Related Skills section
- Adds Integration table
- Adds Communication standard reference
- Standardizes YAML frontmatter
- Does NOT add Python tools yet (that's Iteration 3)

### 1C: Upgrade 3 existing skills

| Skill | Changes |
|-------|---------|
| content-creator | Add context integration (reads marketing-context), Related Skills, Communication standard |
| social-media-analyzer â†’ social-media-manager | Rename, expand SKILL.md from analyzer to full manager (scheduling, strategy, community) |
| campaign-analytics | Add cross-channel synthesis section, Related Skills, Communication standard |

### 1D: Update AI_RUNTIME_GUIDE.md + marketplace + skills-index

- Rewrite `marketing-skill/AI_RUNTIME_GUIDE.md` (like we did for C-Suite)
- Update `.claude-plugin/marketplace.json`
- Update `.codex/skills-index.json`
- Update root `AI_RUNTIME_GUIDE.md` skill counts
- Update `README.md` badge + counts

### Iteration 1 Deliverables
- [ ] Branch `feat/marketing-expansion`
- [ ] marketing-context/ (foundation)
- [ ] marketing-ops/ (router)
- [ ] 20 imported skills (standardized)
- [ ] 3 upgraded skills
- [ ] Updated AI_RUNTIME_GUIDE.md, marketplace, skills-index
- [ ] PR opened

---

## Iteration 2: Build 13 New Skills (parallel subagents)

### 2A: Content + SEO batch (5 skills â€” 2 subagents)

**Subagent: content-builder**
| Skill | Key Deliverables |
|-------|-----------------|
| content-production | SKILL.md, references/production-pipeline.md, references/content-brief-template.md, scripts/content_scorer.py (readability + SEO + humanity score), scripts/outline_generator.py |
| content-humanizer | SKILL.md, references/ai-patterns-checklist.md, references/voice-injection-guide.md, scripts/humanizer_scorer.py (detect AI patterns: em-dashes, filler, passive, hedging) |

**Subagent: seo-builder**
| Skill | Key Deliverables |
|-------|-----------------|
| ai-seo | SKILL.md, references/aeo-guide.md (answer engine optimization), references/llm-citation-tactics.md, references/ai-search-landscape.md |
| schema-markup | SKILL.md, references/schema-types-guide.md, references/implementation-patterns.md, scripts/schema_validator.py (validates JSON-LD) |
| site-architecture | SKILL.md, references/url-structure-guide.md, references/internal-linking-strategy.md, scripts/sitemap_analyzer.py |

### 2B: Channels + Growth batch (4 skills â€” 2 subagents)

**Subagent: channels-builder**
| Skill | Key Deliverables |
|-------|-----------------|
| cold-email | SKILL.md, references/outreach-frameworks.md (AIDA, PAS, BAB), references/deliverability-guide.md, templates/sequence-templates.md, scripts/email_sequence_analyzer.py |
| ad-creative | SKILL.md, references/ad-frameworks.md (by platform), references/creative-testing-guide.md, scripts/headline_scorer.py, scripts/ad_copy_generator.py |

**Subagent: growth-builder**
| Skill | Key Deliverables |
|-------|-----------------|
| referral-program | SKILL.md, references/referral-mechanics.md, references/program-types.md (one-sided, two-sided, tiered), scripts/referral_roi_calculator.py |
| free-tool-strategy | SKILL.md, references/tool-types.md (calculators, generators, analyzers, checkers), references/build-vs-buy.md, scripts/tool_roi_estimator.py |

### 2C: Intelligence + Sales batch (4 skills â€” 2 subagents)

**Subagent: intel-builder**
| Skill | Key Deliverables |
|-------|-----------------|
| analytics-tracking | SKILL.md, references/ga4-setup-guide.md, references/gtm-patterns.md, references/event-taxonomy.md, scripts/tracking_plan_generator.py |
| pricing-strategy | SKILL.md, references/pricing-models.md (value, cost-plus, competitor, dynamic), references/packaging-guide.md, scripts/pricing_modeler.py, scripts/willingness_to_pay_analyzer.py |

**Subagent: (main agent handles directly)**
These are kept lean â€” no subagent needed:
- Update marketing-ops routing matrix with all 13 new skills
- Cross-reference all new skills with existing pods

### Iteration 2 Deliverables
- [ ] 13 new skills built (SKILL.md + refs + scripts)
- [ ] All integrated into marketing-ops routing matrix
- [ ] All cross-referenced with Related Skills
- [ ] Commit + push

---

## Iteration 3: Python Tools for Knowledge-Only Skills

Add automation to the 20 imported workspace skills (currently zero scripts).

### Priority 1: SEO + Content tools (highest impact)
| Skill | Script | Purpose |
|-------|--------|---------|
| seo-audit | seo_checker.py | On-page SEO scoring (0-100): title, meta, headings, links, keyword density |
| seo-audit | keyword_density_analyzer.py | Keyword distribution + stuffing detection |
| content-strategy | topic_cluster_mapper.py | Map topic clusters, identify gaps, suggest pillar content |
| copywriting | headline_scorer.py | Score headlines: power words, emotional triggers, length, clarity |
| copy-editing | readability_scorer.py | Flesch Reading Ease, grade level, passive voice, sentence complexity |

### Priority 2: CRO tools
| Skill | Script | Purpose |
|-------|--------|---------|
| page-cro | conversion_audit.py | Above-fold analysis, CTA scoring, trust signals, friction points |
| form-cro | form_friction_analyzer.py | Field count, required fields, multi-step scoring |
| signup-flow-cro | signup_funnel_analyzer.py | Step analysis, drop-off estimation |

### Priority 3: Channel + Growth tools
| Skill | Script | Purpose |
|-------|--------|---------|
| paid-ads | roas_calculator.py | ROAS, CPA, budget allocation optimizer |
| email-sequence | email_flow_designer.py | Sequence timing, open/click estimation |
| ab-test-setup | sample_size_calculator.py | Statistical significance, test duration estimator |
| competitor-alternatives | competitor_matrix_builder.py | Feature comparison matrix generator |

### Priority 4: Intelligence tools
| Skill | Script | Purpose |
|-------|--------|---------|
| campaign-analytics | channel_mixer.py | Cross-channel attribution synthesis |
| marketing-psychology | persuasion_audit.py | Score content against Cialdini's 6 principles |
| launch-strategy | launch_readiness_scorer.py | Pre-launch checklist scoring |

### Iteration 3 Deliverables
- [ ] ~18 new Python scripts (stdlib-only, CLI-first, JSON output)
- [ ] All scripts have embedded sample data for zero-config runs
- [ ] Commit + push

---

## Iteration 4: Quality Upgrade (C-Suite Standard)

Apply to ALL 39 marketing skills:

### 4A: Add to every skill
- [ ] Proactive Triggers (5-6 context-driven alerts per skill)
- [ ] Output Artifacts table (request â†’ deliverable mapping)
- [ ] Communication standard reference
- [ ] Quality loop integration (self-verify, peer-verify)

### 4B: Add marketing-specific agents
| Agent | Location | Purpose |
|-------|----------|---------|
| content-analyzer | marketing-ops/agents/ | Analyzes content for SEO, readability, brand voice |
| seo-optimizer | marketing-ops/agents/ | On-page SEO recommendations |
| meta-creator | marketing-ops/agents/ | Meta title/description generation |
| headline-generator | marketing-ops/agents/ | Headline variations + scoring |
| cro-analyst | marketing-ops/agents/ | CRO audit for any page |

Inspired by SEO Machine's 10 agents, but lean (markdown agents, not Python services).

### 4C: Parity check
Run same audit as C-Suite:
- [ ] All 39 skills: Keywords âœ…, QuickStart âœ…, Related Skills âœ…, Integration âœ…, Proactive âœ…, Outputs âœ…, Communication âœ…
- [ ] All Python scripts: syntax valid, sample data works, JSON output
- [ ] All cross-references: bidirectional (A references B, B references A)
- [ ] Marketing-ops routing matrix: all 39 skills + 6 cross-domain

### Iteration 4 Deliverables
- [ ] Quality loop on all 39 skills
- [ ] 5 marketing agents
- [ ] Parity check passed
- [ ] Final commit + PR merge-ready

---

## Execution Timeline

| Iteration | Work | Subagents | Est. Files |
|-----------|------|-----------|-----------|
| 1: Foundation + Import | 22 skills (2 new + 20 import) + 3 upgrades + metadata | 4 | ~80 |
| 2: New Skills | 13 new skills | 6 | ~100 |
| 3: Python Tools | ~18 scripts | 2-3 | ~18 |
| 4: Quality Upgrade | Quality loop + agents + parity | 2-3 | ~50 |
| **Total** | **39 skills** | **~15** | **~250** |

---

## Success Criteria

1. **39 marketing skills** organized into 7 pods + orchestration
2. **~38 Python tools** (18 existing + ~20 new), all stdlib-only
3. **5 marketing agents** (content-analyzer, seo-optimizer, meta-creator, headline-generator, cro-analyst)
4. **Full orchestration** via marketing-ops router with routing matrix
5. **Context foundation** that every skill reads (brand voice, style guide, keywords, etc.)
6. **Cross-domain routing** to 6 skills in business-growth, product-team, engineering-team
7. **C-Suite quality standard** on all skills (proactive triggers, output artifacts, quality loop)
8. **Full cross-referencing** between all skills (Related Skills sections)
9. **CMO integration** â€” marketing-ops connects to c-level-advisor/cmo-advisor/
10. **Zero external dependencies** â€” all Python scripts stdlib-only

---

*Ready for execution on Reza's go.*
