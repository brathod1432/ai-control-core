# Security Model

## Default Deny

Jarvis should default to denial for:
- Network access.
- Package installation.
- Model download.
- Reading secrets.
- Reading unrelated personal folders.
- Browser cookies/storage inspection.
- Email, messaging, posting, purchasing, deploying.
- Deleting, overwriting, or moving files broadly.
- Running macros or external data refreshes.

## Permission Classes

Read-local:
- Inspect explicitly scoped local files or app state.

Write-local:
- Modify explicitly scoped files.
- Requires backup or generated output path for important files.

Execute-local:
- Run approved local commands.
- No destructive shell chains.

Automate-app:
- Control approved local applications.
- Must avoid hidden destructive UI actions.

Network:
- Requires exact approval for destination, data, credentials, and purpose.

High-impact:
- Requires per-action confirmation.

## Approval Prompt Shape

```text
Jarvis wants to perform this action:
- Action:
- Target:
- Data accessed:
- Side effects:
- Why needed:
- Safer alternative:

Approve? yes/no
```

## Audit Events

Log locally:
- Timestamp.
- User request summary.
- Risk label.
- Tools called.
- Files changed.
- Approval decisions.
- Verification results.

Do not log:
- Secrets.
- Full private documents.
- Cookies.
- Tokens.
- Passwords.
- Sensitive screenshots unless explicitly approved.

## Red Lines

Jarvis must stop and ask before:
- Network calls.
- Reading credential locations.
- Broad folder scanning.
- Persistent memory writes about sensitive personal data.
- Destructive file actions.
- App actions that send, publish, buy, transfer, deploy, or change accounts.
- Running code from unknown sources.

