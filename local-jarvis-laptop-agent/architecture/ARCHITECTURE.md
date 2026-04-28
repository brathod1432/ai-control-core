# Architecture

## Current Model Baseline

All agents and subagents use the same single local Ollama `qwen2.5:3b` model through `http://127.0.0.1:11434`. No cloud LLMs, remote model APIs, separate providers, or per-agent model pools are part of this architecture.

## System Overview

```mermaid
flowchart TD
  U["User: text or voice"] --> I["Interface Layer"]
  I --> S["Safety Gate"]
  S --> O["Jarvis Core Orchestrator"]
  O --> M["Local Model Runtime: Ollama qwen2.5:3b on 127.0.0.1:11434"]
  O --> R["Local Memory/RAG"]
  O --> T["Tool Registry/MCP"]
  T --> F["Filesystem Tools"]
  T --> B["Local Browser/CDP Tools"]
  T --> D["Desktop/App Control"]
  T --> W["Office Automation"]
  T --> C["Calendar/Tasks/Notes Connectors"]
  O --> A["Audit Log"]
  O --> G["Optional Multi-Agent Crew"]
  G --> O
```

## Components

### Interface Layer

Interfaces should be added in this order:
1. CLI text loop.
2. Local web UI on loopback.
3. Push-to-talk voice.
4. Wake-word voice.
5. Screen overlay or tray assistant.

Reason: text is easiest to debug and safest to audit.

### Safety Gate

The safety gate decides whether a request can proceed:
- Is the target local and in scope?
- Does it require network?
- Does it read secrets?
- Does it modify files or app state?
- Is the action destructive or high impact?
- Is explicit approval required?

### Jarvis Core Orchestrator

Responsibilities:
- Maintain conversation state.
- Classify intent.
- Select model profile.
- Retrieve memory.
- Select tools.
- Ask for approval when needed.
- Verify outputs.
- Write audit events.
- Route to subagents only when beneficial and authorized.

### Local Model Runtime

The runtime exposes a local Ollama endpoint:
- Base URL: `http://127.0.0.1:11434`
- Model: `qwen2.5:3b`
- API shape: `POST /api/chat`

Every role uses the same runtime and model. Model profiles are prompt/parameter profiles over `qwen2.5:3b`; they are not separate models or providers.

Preferred shape:
- `POST /api/chat` for chat.

Model profiles:
- Fast: `qwen2.5:3b` with a short, low-temperature prompt.
- Balanced: `qwen2.5:3b` with normal Jarvis prompt and broader token budget.
- Coder: `qwen2.5:3b` with a coding-focused prompt.
- Critic: `qwen2.5:3b` with a reviewer/verifier prompt.

### Memory/RAG

Memory tiers:
- Session memory: current conversation.
- Task memory: temporary summaries and artifacts.
- Long-term memory: user-approved facts and preferences.
- Project memory: repo conventions, local setup, reusable notes.

Every long-term memory item should have:
- Source.
- Timestamp.
- Confidence.
- Expiry or review policy.

### Tool Registry/MCP

Every tool has:
- Name.
- Description.
- Input schema.
- Side-effect class.
- Permission requirement.
- Dry-run support where relevant.
- Redaction policy.
- Error contract.

### Multi-Agent Crew

Optional specialists:
- Researcher.
- Coder.
- Browser inspector.
- Office/document worker.
- Local system diagnostician.
- Verifier/critic.

Coordinator rule:
- The core orchestrator remains accountable for task decomposition, integration, and final response.
- Specialists are subagent prompts over the same local Ollama `qwen2.5:3b` runtime.

## Data Flow

1. User speaks or types.
2. Interface normalizes input.
3. Safety gate labels risk.
4. Orchestrator builds compact context.
5. Model proposes answer, tool call, or clarification.
6. Safety gate validates tool call.
7. Tool executes if allowed.
8. Orchestrator verifies result.
9. Response is returned.
10. Audit log records safe summary.

## Local Storage Layout

Recommended runtime storage:

```text
~/.local-jarvis/
  config/
  memory/
  logs/
  artifacts/
  models/
  tmp/
```

Inside this repo, keep only templates, examples, and non-sensitive validation artifacts.
