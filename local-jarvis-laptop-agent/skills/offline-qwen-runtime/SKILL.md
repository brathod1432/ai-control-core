---
name: offline-qwen-runtime
description: Use to configure or design a local/offline model runtime for Jarvis using Qwen through Ollama, llama.cpp, LM Studio, or an OpenAI-compatible local server. Covers model profiles, hardware tradeoffs, endpoint contracts, and no-network constraints.
category: local-agent
---

## Internal Safety Override

- Status: advisory until the user approves installs, downloads, or runtime commands.
- Do not download models, install runtimes, or contact model hubs without explicit approval.
- Do not send prompts, files, memory, logs, or diagnostics to remote model APIs by default.

# Offline Qwen Runtime

## Runtime Options

Ollama:
- Easiest local endpoint.
- Good for quick MVP.
- Common endpoint: `http://127.0.0.1:11434/api/chat`.

llama.cpp server:
- Strong control over GGUF models.
- Good for fully local, scriptable setups.
- Common endpoint can be OpenAI-compatible depending on launch flags.

LM Studio:
- UI-friendly local model management.
- Often exposes OpenAI-compatible local server.

vLLM:
- Strong throughput for GPU/server setups.
- Usually overkill for a laptop Jarvis MVP.

## Model Profiles

Fast:
- Small Qwen instruct model.
- Used for intent classification and short answers.

Balanced:
- Mid-size Qwen instruct model.
- Used for normal Jarvis reasoning.

Coder:
- Qwen coder model.
- Used for code and repo work.

Critic:
- Balanced or coder model with critic prompt.
- Used for verification and review.

## Endpoint Contract

Jarvis should abstract the runtime behind one local interface:

```json
{
  "provider": "ollama|llama_cpp|lm_studio|openai_compatible_local",
  "base_url": "http://127.0.0.1:11434",
  "model": "qwen-local",
  "timeout_seconds": 120,
  "temperature": 0.2,
  "max_tokens": 2048
}
```

## Hardware Tradeoffs

- 7B class models: practical on many laptops with quantization.
- 14B class models: better reasoning, more memory pressure.
- 32B+ class models: may be slow or require strong GPU/RAM.
- Quantized GGUF models reduce memory at quality cost.

## Validation

- Runtime listens only on loopback.
- Model responds to a harmless local prompt.
- No remote endpoint is configured.
- Logs do not include secrets or private file content.
- Timeout and cancellation work.

