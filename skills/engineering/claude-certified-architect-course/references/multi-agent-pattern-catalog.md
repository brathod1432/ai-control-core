# Multi-Agent Pattern Catalog

## Pattern Selection Heuristic

Ask three questions:
- Dependency: can subtasks run independently?
- Expertise: do roles need genuinely different context or tools?
- Verification: does a separate critic or verifier reduce real risk?

If the answer is mostly no, use a single agent or workflow agent.

## Coordinator And Workers

Use when:
- A main coordinator can decompose work into independent slices.
- Workers have disjoint ownership.
- The coordinator can integrate outputs.

Roles:
- Coordinator: owns plan, decomposition, integration, final answer.
- Worker: owns a bounded implementation or analysis slice.
- Verifier: checks outputs against acceptance criteria.

Failure modes:
- Coordinator delegates blocking work and waits uselessly.
- Workers overlap files and conflict.
- Handoffs are too vague.

Controls:
- Define write scopes.
- State that agents are not alone in the codebase.
- Require changed file lists.
- Keep coordinator accountable for final integration.

## Parallel Explorers

Use when:
- Several independent codebase questions can be answered at once.
- The coordinator can continue useful work while explorers run.

Example:
- Explorer A: auth flow.
- Explorer B: database schema.
- Explorer C: frontend route.

Avoid:
- Asking all explorers the same broad question.
- Treating exploration as a substitute for implementation.

## Router Pattern

Use when:
- Incoming tasks fall into known categories.
- Each category has a specialist.

Flow:
1. Classify request.
2. Route to specialist.
3. Validate specialist output.
4. Escalate unknown categories.

Example:
- Support triage routes billing, technical, security, and product feedback tickets.

## Sequential Pipeline

Use when:
- Each step depends on the previous output.
- Intermediate validation is possible.

Example:
- Intake -> extract requirements -> design -> implement -> test -> document.

Risk:
- One weak early output contaminates the rest.

Control:
- Add validation gates between stages.

## Critic Or Evaluator Loop

Use when:
- Quality matters and a second perspective catches issues.
- The generator and critic can use different rubrics.

Flow:
1. Generator drafts.
2. Critic reviews against rubric.
3. Generator revises.
4. Stop after max iterations or pass threshold.

Rules:
- The critic should not rewrite everything by default.
- The generator should explain which critique items were accepted or rejected.

## Debate Pattern

Use when:
- There are real tradeoffs with no obvious winner.
- You need competing arguments before synthesis.

Roles:
- Advocate A.
- Advocate B.
- Judge/synthesizer.

Control:
- Require evidence and decision criteria.
- Timebox debate.
- Avoid theatrical disagreement without facts.

## Blackboard Pattern

Use when:
- Agents contribute to a shared artifact over time.
- The problem is exploratory and stateful.

Shared state:
- Problem statement.
- Facts.
- Hypotheses.
- Experiments.
- Decisions.
- Open questions.

Risk:
- Blackboard becomes messy context soup.

Control:
- Use structured sections and ownership.
- Periodically compact state.

## Swarm Pattern

Use when:
- Many small agents explore a broad solution space.
- The task benefits from diversity more than deterministic sequencing.
- Individual failures are acceptable.

Examples:
- Ideation.
- Search over prompt variants.
- Independent issue clustering.
- Design alternatives.

Risks:
- High coordination cost.
- Duplicate work.
- Hard-to-debug emergent behavior.

Controls:
- Set hard budgets.
- Require compact outputs.
- Use a coordinator to deduplicate and rank results.
- Avoid swarms for sensitive data or high-impact actions.

## Market Or Auction Pattern

Use when:
- Agents can bid for tasks based on capability, confidence, or cost.
- Work items vary in difficulty or required expertise.

Flow:
1. Coordinator posts tasks with success criteria.
2. Agents submit capability/confidence bids.
3. Coordinator assigns work based on fit and budget.
4. Outputs are scored and reputation is updated.

Good for:
- Large backlog triage.
- Routing mixed support tickets.
- Assigning repo modules to specialist workers.

Avoid when:
- The routing decision is simple.
- The bidding protocol would cost more than the work.

## Committee Pattern

Use when:
- A decision needs multiple independent reviews.
- The final output must represent consensus or documented dissent.

Flow:
1. Each reviewer evaluates independently.
2. Coordinator merges findings.
3. Conflicts are resolved by evidence and rubric.
4. Final report records majority view and dissent.

Good for:
- Architecture decisions.
- Risk reviews.
- Legal/security/product tradeoff discussions.

## Tree-Of-Agents Pattern

Use when:
- A complex problem can be recursively decomposed.
- Managers coordinate subteams.

Risk:
- Deep hierarchies amplify miscommunication.

Controls:
- Keep depth shallow.
- Require summaries at each level.
- Escalate uncertainties upward quickly.

## Tournament Pattern

Use when:
- Multiple solutions can be objectively evaluated.
- Work can be isolated, such as benchmark optimization or copy variants.

Flow:
1. Spawn competitors with same objective.
2. Run same eval.
3. Judge by metric plus human review.
4. Merge or adopt winner.

Risk:
- Wasted compute and merge conflicts.

Control:
- Use isolated branches/worktrees.
- Keep scope narrow.

## Red-Team Pattern

Use when:
- Safety, privacy, security, or compliance risk is high.

Roles:
- Builder.
- Red teamer.
- Safety reviewer.
- Release owner.

Checks:
- Prompt injection.
- Tool misuse.
- Secret exposure.
- Data exfiltration.
- Overbroad autonomy.
- Unsafe persistence.

## Handoff Contract

Every agent handoff should include:

```json
{
  "from": "agent",
  "to": "agent",
  "task": "bounded instruction",
  "owned_scope": ["paths or artifacts"],
  "inputs": ["specific evidence"],
  "output_schema": {},
  "constraints": ["safety and style"],
  "deadline_or_budget": "optional",
  "escalate_if": ["conditions"]
}
```
