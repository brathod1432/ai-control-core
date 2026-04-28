---
name: voice-interface
description: Use to design Jarvis voice input/output with local speech-to-text, local text-to-speech, wake word or push-to-talk, interruption, transcript display, and safety confirmations.
category: local-agent
---

## Internal Safety Override

- Status: advisory until local audio tools are approved.
- Prefer push-to-talk before always-listening wake word.
- Do not record, store, upload, or transcribe audio externally without explicit approval.
- Keep transcripts local and redact sensitive content from logs.

# Voice Interface

## Recommended Progression

1. Text-only CLI.
2. Push-to-talk with visible transcript.
3. Local TTS response.
4. Wake word.
5. Interrupt/cancel command.

## Local STT Options

- whisper.cpp.
- faster-whisper local.
- Windows speech APIs if acceptable locally.

## Local TTS Options

- Piper.
- Coqui TTS local.
- Windows built-in voices.

## Voice Safety Rules

- Show transcript before risky actions.
- Require spoken or typed confirmation for high-impact actions.
- Support "cancel", "stop", and "forget that".
- Do not execute commands from uncertain transcription.
- Avoid wake-word for private environments until false positives are tested.

## Interaction Pattern

```text
Wake/push -> transcribe -> display transcript -> classify risk -> answer or ask confirmation -> speak concise response -> log summary
```

