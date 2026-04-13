#!/usr/bin/env python3
"""Validate simple local markdown links and stale core path references."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


STALE_PATTERNS = [
    "skills/automation/network-integrations",
    "skills/_templates",
    "skills/_standards",
    "rules/CLAUDE.md",
    "rules/GEMINI.md",
    "agents/CLAUDE.md",
    "mcp/disabled-configs",
    "mcp/disabled-plugin-manifests",
]

LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    broken_links = []
    stale_references = []
    skip_parts = {".git", ".venv"}
    for path in root.rglob("*.md"):
        if skip_parts & set(path.parts):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        rel_path = str(path.relative_to(root)).replace("\\", "/")
        if not rel_path.startswith("docs/generated/") and not rel_path.startswith("integrations/"):
            for stale in STALE_PATTERNS:
                if stale in text and rel_path not in {"docs/GENERALIZATION_REPORT.md", "docs/RENAMING_MAP.md"}:
                    stale_references.append({"path": rel_path, "pattern": stale})
        for match in LINK_RE.finditer(text):
            target = match.group(1).split("#", 1)[0]
            if not target or re.match(r"^[a-z]+://", target) or target.startswith("mailto:"):
                continue
            if target.startswith("/"):
                candidate = root / target.lstrip("/")
            else:
                candidate = (path.parent / target).resolve()
            if not candidate.exists():
                broken_links.append({"path": rel_path, "target": match.group(1)})
    report = {
        "broken_links": broken_links,
        "broken_link_count": len(broken_links),
        "stale_references": stale_references,
        "stale_reference_count": len(stale_references),
    }
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"broken_link_count": len(broken_links), "stale_reference_count": len(stale_references)}, indent=2))
    return 0 if not broken_links and not stale_references else 1


if __name__ == "__main__":
    raise SystemExit(main())
