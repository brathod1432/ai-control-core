#!/usr/bin/env python3
"""Normalize external skill repositories into this internal repository.

The script is intentionally conservative:
- copies plain files only, never upstream .git data
- skips generated Gemini/Codex wrapper skills from the alirezarezvani tree
- disables network/action integrations by default
- writes per-skill metadata and duplicate/import reports
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


IGNORE_DIRS = {
    ".git",
    ".github",
    ".claude-plugin",
    ".codex-plugin",
    ".venv",
    "__pycache__",
    "node_modules",
}

SKIP_SKILL_PARTS = {
    "assets",
    "expected_outputs",
    "test-project",
    "eval-workspace",
    "tests",
}

ALIREZA_PRIMARY_DIRS = {
    "business-growth",
    "c-level-advisor",
    "engineering",
    "engineering-team",
    "finance",
    "marketing-skill",
    "product-team",
    "project-management",
    "ra-qm-team",
}

RISK_KEYWORDS = {
    "network": [
        "api",
        "webhook",
        "http://",
        "https://",
        "curl",
        "wget",
        "requests.",
        "fetch(",
        "invoke-webrequest",
        "slack",
        "email",
        "gmail",
        "discord",
        "twitter",
        "x.com",
        "linkedin",
        "dropbox",
        "google drive",
        "composio",
        "browser",
        "upload",
        "download",
        "post ",
        "send ",
        "share",
        "sync",
    ],
    "secrets": [
        ".env",
        "token",
        "secret",
        "credential",
        "api key",
        "apikey",
        "ssh",
        "certificate",
        "auth",
        "vault",
    ],
    "command": [
        "rm -rf",
        "remove-item",
        "subprocess",
        "shell=True",
        "exec(",
        "eval(",
        "npm install",
        "pip install",
        "docker run",
        "sudo ",
    ],
    "exfiltration": [
        "send files",
        "upload files",
        "project context",
        "entire codebase",
        "full repository",
        "copy repository",
        "paste all",
    ],
}

FORCE_DISABLED_PATTERNS = [
    "composio-skills",
    "connect",
    "connect-apps",
    "connect-apps-plugin",
]

OPT_IN_KEYWORDS = [
    "slack",
    "email",
    "gmail",
    "twitter",
    "linkedin",
    "browser",
    "download",
    "upload",
    "fetch",
    "langsmith",
    "lead",
    "ads",
    "mcp",
    "claude-api",
    "api",
]

ALIASES = {
    "artifacts-builder": "web-artifacts-builder",
    "mcp-server-builder": "mcp-builder",
    "template-skill": "skill-template",
    "template": "skill-template",
    "changelog": "changelog-generator",
    "docker_hub-automation": "docker-hub-automation",
    "anthropic_administrator-automation": "anthropic-administrator-automation",
}

CATEGORY_KEYWORDS = [
    ("mcp", ["mcp"]),
    ("security", ["security", "secops", "ciso", "threat", "audit", "secrets", "vault", "iso27001"]),
    ("data", ["data", "database", "sql", "analytics", "xlsx", "docx", "pdf", "pptx", "finance"]),
    ("media", ["image", "video", "gif", "art", "theme", "canvas", "deck"]),
    ("writing", ["writer", "copy", "content", "resume", "comms", "documentation", "changelog"]),
    ("research", ["research", "intel", "competitive", "summarizer"]),
    ("business", ["business", "growth", "sales", "revenue", "advisor", "cfo", "ceo", "coo", "cro", "chro", "cpo"]),
    ("productivity", ["project", "scrum", "meeting", "organizer", "atlassian", "jira", "confluence"]),
    ("automation", ["automation", "browser", "ci-cd", "pipeline", "workflow", "sync", "connect"]),
    ("engineering", ["code", "developer", "frontend", "backend", "devops", "architect", "testing", "qa", "playwright", "api"]),
]


@dataclass(frozen=True)
class Source:
    key: str
    root: Path
    priority: int


def slugify(value: str) -> str:
    value = value.strip().lower().replace("_", "-")
    value = re.sub(r"[^a-z0-9-]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return ALIASES.get(value, value)


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


def skill_dirs_for_source(source: Source) -> list[Path]:
    if source.key == "anthropic":
        roots = [source.root / "skills"]
    elif source.key == "composio":
        roots = [source.root]
    elif source.key == "alirezarezvani":
        roots = [source.root / name for name in sorted(ALIREZA_PRIMARY_DIRS)]
    else:
        roots = [source.root]

    dirs: list[Path] = []
    for root in roots:
        if not root.exists():
            continue
        for skill_file in root.rglob("SKILL.md"):
            directory = skill_file.parent
            rel_parts = set(directory.relative_to(source.root).parts)
            if rel_parts & SKIP_SKILL_PARTS:
                continue
            if source.key == "alirezarezvani" and "skills" in rel_parts:
                continue
            if any(part in IGNORE_DIRS for part in directory.parts):
                continue
            dirs.append(directory)
    return sorted(dirs)


def classify_category(slug: str, source: Source, rel_path: Path) -> str:
    rel_first = rel_path.parts[0] if rel_path.parts else ""
    if source.key == "composio" and "composio-skills" in rel_path.parts:
        return "automation/network-integrations"
    if source.key == "alirezarezvani":
        mapping = {
            "business-growth": "business",
            "c-level-advisor": "business",
            "engineering": "engineering",
            "engineering-team": "engineering",
            "finance": "data",
            "marketing-skill": "business",
            "product-team": "productivity",
            "project-management": "productivity",
            "ra-qm-team": "security",
        }
        return mapping.get(rel_first, "engineering")
    for category, words in CATEGORY_KEYWORDS:
        if any(word in slug for word in words):
            return category
    return "productivity"


def detect_risks(text: str, slug: str, source: Source, rel_path: Path) -> dict[str, list[str]]:
    lower = text.lower()
    risks: dict[str, list[str]] = {}
    for risk, terms in RISK_KEYWORDS.items():
        hits = sorted({term for term in terms if term in lower or term in slug})
        if hits:
            risks[risk] = hits[:8]
    if source.key == "composio" and "composio-skills" in rel_path.parts:
        risks.setdefault("network", []).append("composio integration catalog")
    return risks


def status_for(slug: str, source: Source, rel_path: Path, risks: dict[str, list[str]]) -> str:
    rel_text = "/".join(rel_path.parts).lower()
    if any(pattern in rel_text for pattern in FORCE_DISABLED_PATTERNS):
        return "disabled_by_default"
    if source.key == "composio" and "composio-skills" in rel_path.parts:
        return "disabled_by_default"
    if "command" in risks and ("network" in risks or "secrets" in risks):
        return "disabled_by_default"
    if any(keyword in slug for keyword in OPT_IN_KEYWORDS) or "network" in risks:
        return "opt_in_external"
    return "active_local"


def safety_block(status: str, risks: dict[str, list[str]]) -> str:
    risk_names = ", ".join(sorted(risks)) if risks else "none detected"
    if status == "disabled_by_default":
        return (
            "## Internal Safety Override\n\n"
            "- Status: disabled by default.\n"
            "- Do not execute commands, connect accounts, call remote APIs, upload files, "
            "or transmit repository content unless a human explicitly enables this skill for a bounded task.\n"
            "- Never read `.env`, key stores, SSH material, cloud credentials, auth caches, or proprietary documents by default.\n"
            f"- Audit categories: {risk_names}.\n\n"
        )
    if status == "opt_in_external":
        return (
            "## Internal Safety Override\n\n"
            "- Status: local-only unless explicitly opted into external access.\n"
            "- Before using network tools, account connectors, browser automation, or APIs, state the destination, data scope, and credential source.\n"
            "- Do not transmit repository files, secrets, credentials, or private documents by default.\n"
            f"- Audit categories: {risk_names}.\n\n"
        )
    return (
        "## Internal Safety Override\n\n"
        "- Status: active for local use.\n"
        "- Keep operation local by default. Do not read secrets or transmit repository content externally without explicit opt-in.\n"
        f"- Audit categories: {risk_names}.\n\n"
    )


def inject_safety(content: str, status: str, risks: dict[str, list[str]]) -> str:
    block = safety_block(status, risks)
    if content.startswith("---\n"):
        end = content.find("\n---\n", 4)
        if end != -1:
            insert_at = end + len("\n---\n")
            return content[:insert_at] + "\n" + block + content[insert_at:].lstrip("\n")
    return block + content.lstrip("\n")


def copy_tree(src: Path, dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    def ignore(_directory: str, names: list[str]) -> set[str]:
        return {name for name in names if name in IGNORE_DIRS or name.endswith(".zip")}
    shutil.copytree(src, dst, ignore=ignore)
    for bad in dst.rglob(".git"):
        if bad.is_dir():
            shutil.rmtree(bad)


def load_skill_name(skill_dir: Path) -> str:
    text = read_text(skill_dir / "SKILL.md")
    match = re.search(r"^name:\s*[\"']?([^\"'\n]+)", text, flags=re.MULTILINE)
    if match:
        return slugify(match.group(1))
    return slugify(skill_dir.name)


def collect_skills(sources: list[Source]) -> tuple[list[dict], list[dict]]:
    candidates: list[dict] = []
    for source in sources:
        for directory in skill_dirs_for_source(source):
            rel = directory.relative_to(source.root)
            slug = load_skill_name(directory)
            text = read_text(directory / "SKILL.md")
            risks = detect_risks(text, slug, source, rel)
            candidates.append({
                "slug": slug,
                "source": source.key,
                "source_path": str(directory),
                "relative_path": str(rel).replace("\\", "/"),
                "priority": source.priority,
                "category": classify_category(slug, source, rel),
                "status": status_for(slug, source, rel, risks),
                "risks": risks,
                "size": len(text),
            })

    chosen: dict[str, dict] = {}
    duplicates: list[dict] = []
    for item in sorted(candidates, key=lambda x: (-x["priority"], x["source"], x["relative_path"])):
        slug = item["slug"]
        if slug not in chosen:
            chosen[slug] = item
            continue
        duplicates.append({
            "slug": slug,
            "kept": chosen[slug],
            "merged_from": item,
            "reason": "same canonical slug or known alias; higher-priority safer source retained",
        })
    return list(chosen.values()), duplicates


def copy_skills(skills: list[dict], repo: Path) -> list[dict]:
    imported: list[dict] = []
    for item in sorted(skills, key=lambda x: (x["category"], x["slug"])):
        src = Path(item["source_path"])
        location_type = "core"
        category = item["category"]
        if item["category"] == "automation/network-integrations":
            dst = repo / "integrations" / "network-services" / item["slug"]
            location_type = "optional_integration"
            category = "integration"
        elif item["slug"] in {"connect", "connect-apps"}:
            dst = repo / "integrations" / "platforms" / "composio" / item["slug"]
            location_type = "optional_integration"
            category = "integration"
        elif item["slug"] == "claude-api":
            dst = repo / "integrations" / "platforms" / "anthropic" / item["slug"]
            location_type = "optional_integration"
            category = "integration"
        else:
            dst = repo / "skills" / item["category"] / item["slug"]
        copy_tree(src, dst)
        skill_file = dst / "SKILL.md"
        content = read_text(skill_file)
        write_text(skill_file, inject_safety(content, item["status"], item["risks"]))
        metadata = {
            "name": item["slug"],
            "category": category,
            "status": item["status"],
            "location_type": location_type,
            "source_repository": item["source"],
            "source_relative_path": item["relative_path"],
            "risk_categories": sorted(item["risks"]),
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }
        write_text(dst / "SKILL_METADATA.json", json.dumps(metadata, indent=2, sort_keys=True) + "\n")
        if item["status"] == "disabled_by_default":
            write_text(
                dst / "DISABLED.md",
                "# Disabled By Default\n\n"
                "This skill was imported for traceability but contains integration, network, secret, or command-execution risk. "
                "It must not be run automatically. Enable only for a bounded task after reviewing the skill, destination services, "
                "credential source, and data scope.\n",
            )
        imported.append({
            "name": item["slug"],
            "path": str(dst.relative_to(repo)).replace("\\", "/"),
            "category": category,
            "location_type": location_type,
            "status": item["status"],
            "source": item["source"],
            "risk_categories": sorted(item["risks"]),
        })
    return imported


def copy_supporting_content(sources: dict[str, Path], repo: Path) -> list[dict]:
    copied: list[dict] = []

    def copy_file(src: Path, dst: Path, note: str) -> None:
        if src.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            copied.append({"path": str(dst.relative_to(repo)).replace("\\", "/"), "source": str(src), "note": note})

    def copy_dir(src: Path, dst: Path, note: str) -> None:
        if src.exists():
            copy_tree(src, dst)
            copied.append({"path": str(dst.relative_to(repo)).replace("\\", "/"), "source": str(src), "note": note})

    anthropic = sources["anthropic"]
    composio = sources["composio"]
    alireza = sources["alirezarezvani"]

    copy_file(anthropic / "spec" / "agent-skills-spec.md", repo / "standards" / "agent-skills-spec.md", "canonical skill specification")
    copy_dir(anthropic / "template", repo / "templates" / "skill-template", "canonical skill template")
    copy_dir(composio / "template-skill", repo / "integrations" / "platforms" / "composio" / "template-skill", "secondary platform-specific template source")
    copy_dir(alireza / "templates", repo / "templates" / "operational-templates", "operational templates")
    copy_dir(alireza / "standards", repo / "standards" / "operational-standards", "team standards")
    copy_file(alireza / "SKILL-AUTHORING-STANDARD.md", repo / "standards" / "skill-authoring-standard.md", "authoring standard")
    copy_file(alireza / "CONVENTIONS.md", repo / "rules" / "CONVENTIONS.md", "cross-tool conventions")
    copy_file(alireza / "CLAUDE.md", repo / "integrations" / "platforms" / "anthropic" / "legacy-claude-runtime-guide.md", "Claude instruction source, retained as compatibility reference")
    copy_file(alireza / "GEMINI.md", repo / "integrations" / "platforms" / "google" / "gemini-cli-guide.md", "Gemini instruction source, retained as compatibility reference")
    copy_dir(alireza / ".claude" / "commands", repo / "rules" / "commands", "command templates, inert markdown")
    copy_dir(alireza / "agents", repo / "agents", "agent persona instructions")
    copy_dir(anthropic / "skills" / "mcp-builder" / "reference", repo / "mcp" / "reference", "MCP builder references")
    copy_file(alireza / ".mcp.json", repo / "integrations" / "mcp-clients" / "tessl.mcp.json.disabled", "disabled upstream MCP config")
    copy_file(alireza / ".codex-plugin" / "plugin.json", repo / "integrations" / "platforms" / "codex" / "codex-plugin.json.disabled", "disabled plugin manifest")
    copy_file(alireza / ".claude-plugin" / "marketplace.json", repo / "integrations" / "platforms" / "anthropic" / "claude-marketplace.json.disabled", "disabled plugin marketplace metadata")
    copy_file(composio / "connect-apps-plugin" / ".claude-plugin" / "plugin.json", repo / "integrations" / "platforms" / "composio" / "connect-apps-plugin.json.disabled", "disabled plugin manifest")
    copy_file(alireza / "LICENSE", repo / "docs" / "licenses" / "alirezarezvani-claude-skills-MIT-LICENSE.txt", "upstream MIT license")
    copy_file(anthropic / "THIRD_PARTY_NOTICES.md", repo / "docs" / "licenses" / "anthropic-THIRD_PARTY_NOTICES.md", "upstream third-party notices")
    return copied


def demote_nested_skill_markers(repo: Path) -> list[str]:
    """Rename nested non-canonical SKILL.md files so scanners see one skill layer.

    Canonical imported skill directories always get SKILL_METADATA.json beside
    SKILL.md. Templates intentionally keep their SKILL.md names.
    """
    demoted: list[str] = []
    roots = [repo / name for name in ("skills", "integrations") if (repo / name).exists()]
    for root in roots:
        for skill_file in root.rglob("SKILL.md"):
            if "templates" in skill_file.parts:
                continue
            if (skill_file.parent / "SKILL_METADATA.json").exists():
                continue
            target = skill_file.with_name("SKILL_REFERENCE.md")
            if target.exists():
                target.unlink()
            skill_file.rename(target)
            demoted.append(str(target.relative_to(repo)).replace("\\", "/"))
    return demoted


def clean_top_level(repo: Path) -> None:
    for name in ["agents", "rules", "skills", "mcp", "integrations", "templates", "standards"]:
        path = repo / name
        if path.exists():
            shutil.rmtree(path)
        path.mkdir(parents=True, exist_ok=True)
    for name in ["security", "docs", "context", "scripts"]:
        (repo / name).mkdir(exist_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--composio", required=True, type=Path)
    parser.add_argument("--anthropic", required=True, type=Path)
    parser.add_argument("--alirezarezvani", required=True, type=Path)
    args = parser.parse_args()

    repo = args.repo.resolve()
    sources = [
        Source("anthropic", args.anthropic.resolve(), 100),
        Source("alirezarezvani", args.alirezarezvani.resolve(), 80),
        Source("composio", args.composio.resolve(), 70),
    ]

    clean_top_level(repo)
    skills, duplicates = collect_skills(sources)
    imported = copy_skills(skills, repo)
    supporting = copy_supporting_content({s.key: s.root for s in sources}, repo)
    demoted = demote_nested_skill_markers(repo)

    report_dir = repo / "docs" / "generated"
    report_dir.mkdir(parents=True, exist_ok=True)
    write_text(report_dir / "import_manifest.json", json.dumps(imported, indent=2, sort_keys=True) + "\n")
    write_text(report_dir / "duplicate_report.json", json.dumps(duplicates, indent=2, sort_keys=True) + "\n")
    write_text(report_dir / "supporting_content.json", json.dumps(supporting, indent=2, sort_keys=True) + "\n")
    write_text(report_dir / "demoted_nested_skill_references.json", json.dumps(demoted, indent=2, sort_keys=True) + "\n")

    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "skills_imported": len(imported),
        "duplicates_consolidated": len(duplicates),
        "status_counts": {},
        "category_counts": {},
    }
    for item in imported:
        summary["status_counts"][item["status"]] = summary["status_counts"].get(item["status"], 0) + 1
        summary["category_counts"][item["category"]] = summary["category_counts"].get(item["category"], 0) + 1
    write_text(report_dir / "import_summary.json", json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
