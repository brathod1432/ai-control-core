# Context Engineering And Memory

## Context Layers

System layer:
- Durable behavioral contract.
- Defines identity, permissions, style, and safety boundaries.

Developer layer:
- Project or runtime rules.
- Tool constraints and collaboration policy.

User layer:
- Current task and preferences.

Evidence layer:
- Files, logs, screenshots, docs, test output, source snippets.

Working layer:
- Plan, assumptions, intermediate summaries, open questions.

Output layer:
- Final answer or artifact.

## Context Budgeting

Use high-signal context:
- Prefer file manifests before full files.
- Read exact sections rather than entire repositories.
- Summarize repeated patterns.
- Keep citations or file paths for important facts.
- Remove obsolete hypotheses after verification.

Avoid:
- Dumping full logs.
- Carrying stale plan text after scope changes.
- Including secrets or unrelated personal data.
- Sending full browser storage or cookies into context.

## Memory Types

Task memory:
- Temporary notes for current work.
- Should expire after completion.

Project memory:
- Repo conventions, architecture decisions, commands, known pitfalls.
- Should be updated when stable.

User preference memory:
- Communication style, formatting preferences, workflow preferences.
- Should not include sensitive personal details unless necessary and approved.

Domain memory:
- Reusable concepts, patterns, rubrics.
- Prefer local references over remote lookup.

## Retrieval Strategy

Good retrieval answers:
- What evidence is needed?
- Where is it likely located?
- How much is enough?
- What should be excluded?

Retrieval checklist:
- Search names and concepts.
- Read entry points.
- Follow imports or references only as needed.
- Stop when the decision can be made.
- Record uncertainty rather than over-reading.

## Compression Pattern

Use this for long-running agent work:

```text
Current objective:
Facts verified:
Files/artifacts touched:
Decisions made:
Open questions:
Risks:
Next action:
Do not repeat:
```

## Source Maps

For course or doc imports:
- Source URL or local path.
- License and attribution.
- Retrieved date or commit hash.
- Local file derived from source.
- Transformation: summary, rewrite, excerpt, example, or original.

## Memory Safety

Never store:
- API keys, passwords, cookies, tokens.
- Private keys or auth cache contents.
- Sensitive personal data not needed for future tasks.
- Proprietary course text copied without permission.

Prefer:
- Abstracted lessons.
- File paths instead of full sensitive content.
- Redacted examples.
- Expiry notes for temporary context.

