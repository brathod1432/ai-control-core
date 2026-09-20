# Milestone 1 Status

Date: 2026-04-28

## Current Model Baseline

All agents and subagents use the same single local Ollama `qwen2.5:3b` model through `http://127.0.0.1:11434`. No cloud LLMs, remote model APIs, separate providers, or per-agent model pools are part of the current status.

## Current Status

Milestone 1 is now implemented as a safe text MVP foundation.

Implemented or present:
- Python package skeleton under `src/jarvis/`.
- Shared contracts for intents, permissions, risk levels, safety decisions, model messages, tool specs, and tool results.
- Local-first config template with loopback model endpoint defaults.
- Planning, architecture, security, smoke-test, and evaluation documentation.
- CLI text loop and one-shot prompt mode.
- Config loader and loopback runtime validation.
- Ollama-compatible local model adapter.
- Intent classifier and safety decision engine.
- Approval prompt abstraction.
- Redacted local JSONL audit writer.
- Unit tests for contracts, config, model adapter, safety, audit, and orchestrator behavior.

Not yet implemented:
- OpenAI-compatible local adapter; this remains future-only unless the single local Ollama provider baseline is deliberately revised.
- Read-only filesystem tools.
- Patch proposal/apply workflow.
- Command runner.
- Memory store.
- Browser, Office, voice, and multi-agent runtime features.

## Validation Notes

Validation command run through local Node fallback because PowerShell fails in this session:

```text
PYTHONPATH=src python -m unittest discover -s tests/unit
```

Result:

```text
Ran 32 tests in 0.093s
OK
```

Live local model validation:

```text
Ollama endpoint: http://127.0.0.1:11434
Model: qwen2.5:3b
Direct smoke response: local qwen ready
Jarvis CLI smoke response: I am local Jarvis using Qwen. Always ensure privacy and local control by not performing any action without explicit user consent.
```

Note:
- Running tests created `__pycache__` folders. `.gitignore` now excludes them, but they were not deleted in this pass.

## Gate Assessment

Gate B: Text MVP foundation is ready.

Reasons:
- CLI import path is complete.
- Model success/down behavior is covered with mocks.
- Safety approval/refusal behavior is covered.
- Audit summary redaction is covered.
- No external network calls are required for tests.

Recommended next step:
- Start Milestone 2: read-only local filesystem tools with strict scope validation, forbidden secret paths, bounded output, and tool registry enforcement.
