#!/usr/bin/env python3
"""Find duplicate or near-duplicate skill names in the normalized repository."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from difflib import SequenceMatcher
from pathlib import Path


def read_name(skill_file: Path) -> str:
    for line in skill_file.read_text(encoding="utf-8", errors="replace").splitlines()[:20]:
        if line.lower().startswith("name:"):
            return line.split(":", 1)[1].strip().strip("\"'").lower().replace("_", "-")
    return skill_file.parent.name.lower()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    search_roots = [root / name for name in ("skills", "integrations") if (root / name).exists()]
    skills = sorted(
        path
        for search_root in search_roots
        for path in search_root.rglob("SKILL.md")
        if (path.parent / "SKILL_METADATA.json").exists()
    )
    by_name = defaultdict(list)
    for skill in skills:
        by_name[read_name(skill)].append(str(skill.parent.relative_to(root)).replace("\\", "/"))
    exact = {name: paths for name, paths in by_name.items() if len(paths) > 1}
    names = sorted(by_name)
    near = []
    for index, left in enumerate(names):
        for right in names[index + 1:]:
            ratio = SequenceMatcher(None, left, right).ratio()
            if ratio >= 0.88:
                near.append({"left": left, "right": right, "similarity": round(ratio, 3)})
    report = {"exact_duplicates": exact, "near_duplicates": near, "skill_count": len(skills)}
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"skill_count": len(skills), "exact_duplicate_names": len(exact), "near_duplicate_pairs": len(near)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
