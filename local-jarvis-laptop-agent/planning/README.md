# Planning Index

This folder contains the detailed development plan for the Local Jarvis Laptop Agent.

Read in this order:

1. `MASTER_DEVELOPMENT_PLAN.md` - complete project plan, milestones, workstreams, and gates.
2. `IMPLEMENTATION_BACKLOG.md` - detailed epics, user stories, tasks, dependencies, and acceptance criteria.
3. `TECHNICAL_DECISIONS.md` - architecture decisions and unresolved choices.
4. `TEST_EVALUATION_PLAN.md` - smoke tests, safety tests, model tests, tool tests, and release gates.
5. `STATUS_TRACKING.md` - durable current-state reference for persona, prompts, architecture, memory, roadmap, status, limits, and local test commands.

Planning stance:
- Build a boringly safe core before adding magical-feeling features.
- Keep all default behavior local.
- Prefer inspect/propose over act.
- Voice, desktop control, and multi-agent autonomy come after text, audit, and approval gates are solid.
- All agents and subagents use the same single local Ollama `qwen2.5:3b` model through `http://127.0.0.1:11434`; no cloud LLMs or separate providers are part of the current plan.
