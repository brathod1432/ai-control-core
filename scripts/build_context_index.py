#!/usr/bin/env python3
"""Build compact machine-readable context indexes from normalized skills."""

from __future__ import annotations

import argparse
from pathlib import Path
import json


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    root = args.root.resolve()
    metadata_roots = [root / name for name in ("skills", "integrations") if (root / name).exists()]
    skills = []
    for metadata_root in metadata_roots:
        for metadata_path in metadata_root.rglob("SKILL_METADATA.json"):
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            skill_dir = metadata_path.parent
            location_type = "optional_integration" if "integrations" in skill_dir.parts else "core"
            skills.append({
                "name": metadata.get("name", skill_dir.name),
                "category": metadata.get("category", "uncategorized"),
                "status": metadata.get("status", "unknown"),
                "path": str(skill_dir.relative_to(root)).replace("\\", "/"),
                "location_type": location_type,
            })
    skills = sorted(skills, key=lambda item: (item["location_type"], item["category"], item["name"]))

    grouped: dict[str, list[dict]] = {}
    for item in skills:
        group = f"{item['location_type']}:{item['category']}"
        grouped.setdefault(group, []).append(item)

    lines = [
        "# Skills Index",
        "",
        "START HERE: choose by category, then read only the target `SKILL.md` and its `SKILL_METADATA.json`.",
        "",
        f"Total normalized skill-like assets: {len(skills)}",
        f"Core skills: {sum(1 for item in skills if item['location_type'] == 'core')}",
        f"Optional integrations: {sum(1 for item in skills if item['location_type'] == 'optional_integration')}",
        "",
    ]
    for group, items in grouped.items():
        location_type, category = group.split(":", 1)
        title = "Core" if location_type == "core" else "Optional Integrations"
        lines.append(f"## {title}: {category}")
        for item in items:
            status = item["status"]
            lines.append(f"- `{item['name']}` - `{item['path']}` - `{status}`")
        lines.append("")
    (root / "context").mkdir(exist_ok=True)
    (root / "context" / "SKILLS_INDEX.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    summary = {
        "skills_indexed": len(skills),
        "core_skills": sum(1 for item in skills if item["location_type"] == "core"),
        "optional_integrations": sum(1 for item in skills if item["location_type"] == "optional_integration"),
        "groups": len(grouped),
    }
    generated_dir = root / "docs" / "generated"
    generated_dir.mkdir(exist_ok=True)
    (generated_dir / "current_inventory_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
