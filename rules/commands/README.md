# AI Operations Commands

Reusable command templates for repository maintenance, quality checks, documentation updates, and security review.

These files are inert markdown instructions. A model client or agent runtime may adapt them, but no command should execute automatically.

## Command Groups

- Git workflow helpers.
- Quality and review helpers.
- Security scan helpers.
- Documentation and index maintenance helpers.

## Safety

- Inspect command content before use.
- Confirm working directory and file scope.
- Do not push, publish, sync, or call remote services unless explicitly requested.
- Keep platform-specific sync steps under compatibility notes or `integrations/`.
