# Security Audit Report

Date: 2026-04-13

## Summary

Every imported skill, template, script, agent instruction, config, plugin manifest, and helper copied into this repo was passed through deterministic risk classification and static pattern scanning.

Static scan counts are intentionally broad and include disabled/inert content:

- `network_integration`: 15,855
- `secret_handling`: 8,689
- `data_exfiltration`: 5,423
- `command_execution`: 773
- `prompt_risk`: 11

The detailed scan is stored in `docs/generated/security_scan.json`.

## High-Risk Areas Found

- Remote service integration catalog:
  - Large remote app/action surface.
  - Repeated patterns for account connection, tool search, external API calls, and remote actions.
  - Remediation: isolated under `integrations/network-services/` and disabled by default.
- Composio connect/connect-apps surfaces:
  - Email, Slack, issue creation, app actions, and external account flows.
  - Remediation: isolated under `integrations/platforms/composio/` and disabled by default or explicit-opt-in only.
- Slack/email/browser/download/fetch/social integrations:
  - Potential transmission of repository, prompt, or user data to external systems.
  - Remediation: explicit opt-in with destination and data-scope disclosure.
- MCP/plugin configs:
  - Upstream `.mcp.json`, `.claude-plugin`, and `.codex-plugin` metadata could enable external tools.
  - Remediation: stored only as inert `.disabled` files under `integrations/`.
- Command helpers:
  - Shell execution, package install, subprocess, browser automation, and bootstrap patterns.
  - Remediation: disabled where risky; active use requires source review and explicit command scope.
- Secret handling examples:
  - Token, API key, `.env`, OAuth, service-account, and credential references.
  - Remediation: safety override blocks prohibit reading or logging secrets by default.

## Applied Remediations

- Injected `Internal Safety Override` into every canonical `SKILL.md`.
- Added `SKILL_METADATA.json` to every canonical skill with category, status, source, and risk categories.
- Added `DISABLED.md` to every `disabled_by_default` skill.
- Isolated all remote service integration skills under `integrations/` and kept them disabled by default.
- Marked external/API/browser/Slack/email/download/upload/MCP skills as opt-in or disabled.
- Removed active upstream plugin directories from imported skill trees.
- Renamed nested non-canonical `SKILL.md` files to `SKILL_REFERENCE.md`.
- Copied upstream plugin/MCP configs only as `.disabled` files under `integrations/`.
- Preserved generated audit outputs for repeatable review.

## Safe Defaults

- Do not transmit repository data externally.
- Do not read secrets or private credential stores.
- Do not install packages or execute shell commands from imported instructions without review.
- Do not auto-enable MCP servers, plugins, account connectors, or browser automation.
- Treat all disabled skills as read-only reference material unless a human explicitly enables them.

## Disabled By Default

Disabled by default means the content is retained for traceability but must not be executed automatically.

Main disabled groups:

- `integrations/network-services/*`
- `integrations/platforms/composio/*`
- high-risk command/network integrations
- upstream MCP and plugin manifests in `integrations/mcp-clients/` and `integrations/platforms/*`

## Residual Risk

The repository contains many integration instructions for internal reference. A future model could still misuse them if it ignores `SKILL_METADATA.json`, `DISABLED.md`, or `security/SECURITY_POLICY.md`. The compact context files make these boundaries cheap to read first.
