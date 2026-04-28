# Multi-Agent Blueprints

## Blueprint 1: Coding Feature Team

Use when a feature spans independent layers.

Agents:
- Coordinator: owns plan, integration, final answer.
- Backend worker: API and data layer.
- Frontend worker: UI and state.
- Test worker: focused tests and fixtures.
- Reviewer: static review and risk check.

Handoffs:
- Coordinator assigns disjoint files.
- Workers list changed files and verification.
- Reviewer checks only final integrated diff.

Failure handling:
- If write scopes collide, coordinator pauses and resolves ownership.
- If tests fail outside scope, report as residual risk unless clearly caused by changes.

## Blueprint 2: Research To Decision

Use when a technical choice has several dimensions.

Agents:
- Explorer A: current codebase constraints.
- Explorer B: operational/cost constraints.
- Explorer C: security/privacy constraints.
- Synthesizer: ADR and recommendation.

Output:
- Decision matrix.
- Recommendation.
- Rejected alternatives.
- Open questions.

## Blueprint 3: Document Production Line

Use when creating a complex doc or deck.

Agents:
- Content strategist.
- Evidence gatherer.
- Visual/layout designer.
- QA checker.

Controls:
- Keep source citations.
- Validate formatting locally.
- Do not use external images or uploads without approval.

## Blueprint 4: Support Triage Router

Agents:
- Intake classifier.
- Billing specialist.
- Technical specialist.
- Security specialist.
- Response editor.

Rules:
- Security and privacy issues escalate.
- No account changes without approval.
- Response editor harmonizes tone and checks policy.

## Blueprint 5: Red-Team Release Gate

Agents:
- Builder.
- Prompt injection tester.
- Tool misuse tester.
- Privacy reviewer.
- Release owner.

Pass criteria:
- No unauthorized tool use.
- No secret disclosure.
- Destructive actions require approval.
- Regression cases added for any discovered issue.

## Blueprint 6: Local Browser App Debug Team

Agents:
- Browser inspector: screenshots, console, network metadata.
- Source mapper: maps UI issue to files.
- Fix worker: implements scoped patch.
- Verification worker: reruns local browser smoke checks.

Controls:
- Loopback targets only by default.
- No cookies/storage dumps.
- Reversible page mutations only unless code fix is requested.

## Blueprint 7: Office Automation Team

Agents:
- File inventory agent.
- Content editor.
- Render/layout validator.
- Macro/link risk reviewer.

Controls:
- Work on copies by default.
- Do not run macros or refresh external links without approval.
- Validate output by reopening and rendering when possible.

## Blueprint 8: Agent Skill Factory

Agents:
- Curriculum designer.
- Skill author.
- Example author.
- Safety reviewer.
- Skill tester.

Deliverables:
- `SKILL.md`.
- Metadata.
- References.
- Examples.
- Validation report.

