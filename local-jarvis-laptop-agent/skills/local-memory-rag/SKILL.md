---
name: local-memory-rag
description: Use to design private local memory and retrieval for Jarvis, including approved long-term memory, project memory, embeddings, source attribution, forgetting, summarization, and sensitive-data boundaries.
category: local-agent
---

## Internal Safety Override

- Status: active for local design only.
- Do not persist sensitive personal data, secrets, credentials, or private document content without explicit user approval.
- Memory must be inspectable, editable, and deletable.
- Prefer source-linked summaries over raw full-content storage.

# Local Memory RAG

## Memory Tiers

Session:
- Current conversation only.
- Cleared automatically.

Task:
- Temporary working notes.
- Cleared after task or retained as artifact with approval.

Project:
- Repo conventions, commands, architecture notes.
- Source-linked.

User:
- Stable preferences explicitly approved by the user.
- Editable and forgettable.

## Memory Record

```json
{
  "id": "string",
  "type": "user_preference|project_note|task_summary",
  "text": "string",
  "source": "string",
  "created_at": "iso-8601",
  "confidence": 0.0,
  "expires_at": null,
  "sensitive": false
}
```

## Retrieval Policy

- Retrieve only relevant records.
- Prefer recent source-backed memory.
- Do not let memory override current evidence.
- Show memory used when it materially affects an answer.

## Forgetting

Jarvis must support:
- Delete one memory.
- Delete all memories of a type.
- Disable memory writes.
- Export memory index.

