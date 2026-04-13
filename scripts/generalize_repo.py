#!/usr/bin/env python3
"""Generalize the repository from model-specific import output to AI-ops layout.

This script performs mechanical moves/renames only. It does not try to erase
vendor names where they are functionally required for attribution, compatibility,
or an optional integration.
"""

from __future__ import annotations

import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


TEXT_SUFFIXES = {".md", ".txt", ".json", ".yaml", ".yml", ".toml", ".py", ".template"}

RENAMES: list[dict[str, str]] = []


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def move_path(src: Path, dst: Path, reason: str) -> None:
    if not src.exists():
        return
    if dst.exists():
        raise RuntimeError(f"Destination already exists: {dst}")
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(src), str(dst))
    RENAMES.append({"from": rel(src), "to": rel(dst), "reason": reason})


def rename_file(src: Path, new_name: str, reason: str) -> None:
    if not src.exists():
        return
    dst = src.with_name(new_name)
    if dst.exists():
        return
    src.rename(dst)
    RENAMES.append({"from": rel(src), "to": rel(dst), "reason": reason})


def read_text(path: Path) -> str:
    for encoding in ("utf-8", "utf-8-sig", "cp1252", "latin-1"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text(errors="replace")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def update_metadata_path(skill_dir: Path, new_category: str | None = None, new_status: str | None = None) -> None:
    metadata_path = skill_dir / "SKILL_METADATA.json"
    if not metadata_path.exists():
        return
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    if new_category:
        metadata["category"] = new_category
    if new_status:
        metadata["status"] = new_status
    metadata["generalized_at"] = datetime.now(timezone.utc).isoformat()
    metadata["location_type"] = "optional_integration" if "integrations" in skill_dir.parts else "core"
    write_text(metadata_path, json.dumps(metadata, indent=2, sort_keys=True) + "\n")


def structural_moves() -> None:
    move_path(ROOT / "skills" / "_templates", ROOT / "templates", "promote templates to neutral top-level core area")
    move_path(ROOT / "skills" / "_standards", ROOT / "standards", "promote standards to neutral top-level core area")
    move_path(ROOT / "templates" / "anthropic-skill-template", ROOT / "templates" / "skill-template", "rename upstream-branded core template to neutral name")
    move_path(ROOT / "templates" / "composio-template-skill", ROOT / "integrations" / "platforms" / "composio" / "template-skill", "move Composio-specific template to optional integration area")
    move_path(ROOT / "skills" / "automation" / "network-integrations", ROOT / "integrations" / "network-services", "isolate optional remote service integrations")
    move_path(ROOT / "skills" / "automation" / "connect", ROOT / "integrations" / "platforms" / "composio" / "connect", "isolate Composio connector surface")
    move_path(ROOT / "skills" / "automation" / "connect-apps", ROOT / "integrations" / "platforms" / "composio" / "connect-apps", "isolate Composio app actions")
    move_path(ROOT / "skills" / "engineering" / "claude-api", ROOT / "integrations" / "platforms" / "anthropic" / "claude-api", "isolate Anthropic Claude API materials")
    move_path(ROOT / "rules" / "CLAUDE.md", ROOT / "integrations" / "platforms" / "anthropic" / "legacy-claude-runtime-guide.md", "move platform-specific runtime guide out of core rules")
    move_path(ROOT / "rules" / "GEMINI.md", ROOT / "integrations" / "platforms" / "google" / "gemini-cli-guide.md", "move Gemini-specific runtime guide out of core rules")
    move_path(ROOT / "agents" / "CLAUDE.md", ROOT / "integrations" / "platforms" / "anthropic" / "agent-development-guide.md", "move Claude-specific agent authoring guide out of core agents")
    move_path(ROOT / "mcp" / "disabled-plugin-manifests" / "alirezarezvani.claude-marketplace.json.disabled", ROOT / "integrations" / "platforms" / "anthropic" / "claude-marketplace.json.disabled", "isolate Claude plugin metadata")
    move_path(ROOT / "mcp" / "disabled-plugin-manifests" / "alirezarezvani.codex-plugin.json.disabled", ROOT / "integrations" / "platforms" / "codex" / "codex-plugin.json.disabled", "isolate Codex plugin metadata")
    move_path(ROOT / "mcp" / "disabled-plugin-manifests" / "composio.connect-apps-plugin.json.disabled", ROOT / "integrations" / "platforms" / "composio" / "connect-apps-plugin.json.disabled", "isolate Composio plugin metadata")
    move_path(ROOT / "mcp" / "disabled-configs" / "tessl.mcp.json.disabled", ROOT / "integrations" / "mcp-clients" / "tessl.mcp.json.disabled", "isolate optional MCP client config")

    for folder in [ROOT / "mcp" / "disabled-plugin-manifests", ROOT / "mcp" / "disabled-configs"]:
        if folder.exists() and not any(folder.iterdir()):
            folder.rmdir()

    for codex_dir in list((ROOT / "skills").rglob(".codex")):
        parent = codex_dir.parent
        target = ROOT / "integrations" / "platforms" / "codex" / "skill-adapters" / parent.relative_to(ROOT)
        move_path(codex_dir, target / "codex-adapter", "move Codex adapter metadata out of core skills")


def rename_runtime_files() -> None:
    for path in list(ROOT.rglob("CLAUDE.md")):
        if ".git" in path.parts or ".venv" in path.parts or "integrations" in path.parts:
            continue
        rename_file(path, "AI_RUNTIME_GUIDE.md", "rename Claude-specific runtime file to neutral AI runtime guide")
    for path in list(ROOT.rglob("CLAUDE.md.template")):
        if ".git" in path.parts or ".venv" in path.parts:
            continue
        rename_file(path, "AI_RUNTIME_GUIDE.md.template", "rename Claude-specific template to neutral AI runtime guide template")


CORE_REPLACEMENTS = [
    (re.compile(r"\bClaude Code\b"), "an agent runtime"),
    (re.compile(r"\bClaude AI\b"), "an AI assistant"),
    (re.compile(r"\bClaude workflows\b"), "AI workflows"),
    (re.compile(r"\bClaude workflow\b"), "AI workflow"),
    (re.compile(r"\bClaude skills\b"), "AI skills"),
    (re.compile(r"\bClaude skill\b"), "AI skill"),
    (re.compile(r"\bGemini CLI\b"), "an agent runtime"),
    (re.compile(r"\bCodex CLI\b"), "an agent runtime"),
    (re.compile(r"\bChatGPT\b"), "an AI chat client"),
    (re.compile(r"\bclaude-code-skills\b"), "ai-ops-skills"),
    (re.compile(r"\bclaude-skills\b"), "ai-ops-skills"),
]


def neutralize_core_text() -> None:
    core_roots = [
        ROOT / "README.md",
        ROOT / "AI_README.md",
        ROOT / "agents",
        ROOT / "rules",
        ROOT / "skills",
        ROOT / "templates",
        ROOT / "standards",
        ROOT / "context",
        ROOT / "security",
    ]
    for root in core_roots:
        paths = [root] if root.is_file() else list(root.rglob("*"))
        for path in paths:
            if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
                continue
            if any(part in {".git", ".venv", "integrations", "docs", "licenses", "generated"} for part in path.parts):
                continue
            text = read_text(path)
            new_text = text
            for pattern, replacement in CORE_REPLACEMENTS:
                new_text = pattern.sub(replacement, new_text)
            if new_text != text:
                write_text(path, new_text)


def update_integration_metadata() -> None:
    for skill_file in (ROOT / "integrations").rglob("SKILL.md"):
        update_metadata_path(skill_file.parent, new_category="integration", new_status="disabled_by_default" if (skill_file.parent / "DISABLED.md").exists() else None)


def rewrite_generated_manifest() -> None:
    manifest = ROOT / "docs" / "generated" / "import_manifest.json"
    if not manifest.exists():
        return
    items = json.loads(manifest.read_text(encoding="utf-8"))
    moved = {entry["from"]: entry["to"] for entry in RENAMES}
    for item in items:
        path = item.get("path", "")
        if path in moved:
            item["path"] = moved[path]
            item["location_type"] = "optional_integration" if path.startswith("skills/automation") or "claude-api" in path else "core"
            if item["location_type"] == "optional_integration":
                item["category"] = "integration"
        elif path.startswith("skills/automation/network-integrations/"):
            item["path"] = path.replace("skills/automation/network-integrations/", "integrations/network-services/", 1)
            item["category"] = "integration"
            item["location_type"] = "optional_integration"
        elif path in {"skills/automation/connect", "skills/automation/connect-apps"}:
            item["path"] = path.replace("skills/automation/", "integrations/platforms/composio/", 1)
            item["category"] = "integration"
            item["location_type"] = "optional_integration"
        elif path == "skills/engineering/claude-api":
            item["path"] = "integrations/platforms/anthropic/claude-api"
            item["category"] = "integration"
            item["location_type"] = "optional_integration"
        else:
            item.setdefault("location_type", "core")
    write_text(manifest, json.dumps(items, indent=2, sort_keys=True) + "\n")


def write_renaming_map() -> None:
    write_text(ROOT / "docs" / "generated" / "generalization_renames.json", json.dumps(RENAMES, indent=2, sort_keys=True) + "\n")


def main() -> int:
    structural_moves()
    rename_runtime_files()
    neutralize_core_text()
    update_integration_metadata()
    rewrite_generated_manifest()
    write_renaming_map()
    print(json.dumps({"renames": len(RENAMES)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
