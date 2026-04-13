#!/usr/bin/env python3
"""Static security/privacy scanner for imported skills.

This is not a proof of safety. It is a deterministic guardrail scanner that
flags risky patterns so humans and future AI agents do not need to rediscover
the same hazards by reading the full repository.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


PATTERNS = {
    "data_exfiltration": [
        r"\bupload\b",
        r"\bsend\b.+\b(file|repository|code|context|document)",
        r"\bwebhook\b",
        r"https?://",
        r"\bshare\b.+\b(project|repo|context|file)",
    ],
    "secret_handling": [
        r"\.env\b",
        r"\bapi[_ -]?key\b",
        r"\btoken\b",
        r"\bsecret\b",
        r"\bcredential",
        r"\bssh\b",
        r"\bcertificate\b",
    ],
    "command_execution": [
        r"\brm\s+-rf\b",
        r"\bRemove-Item\b",
        r"\bsubprocess\b",
        r"shell\s*=\s*True",
        r"\beval\(",
        r"\bexec\(",
        r"\bnpm\s+install\b",
        r"\bpip\s+install\b",
        r"\bsudo\b",
    ],
    "network_integration": [
        r"\bcurl\b",
        r"\bwget\b",
        r"\bInvoke-WebRequest\b",
        r"\brequests\.",
        r"\bfetch\(",
        r"\bslack\b",
        r"\bgmail\b",
        r"\bdiscord\b",
        r"\blinkedin\b",
        r"\btwitter\b",
        r"\bcomposio\b",
        r"\bmcp\b",
    ],
    "prompt_risk": [
        r"\bentire\s+(repo|repository|codebase)\b",
        r"\bfull\s+(repo|repository|codebase)\b",
        r"\bpaste\s+all\b",
        r"\bcopy\s+all\b",
    ],
}


def read_text(path: Path) -> str:
    for encoding in ("utf-8", "utf-8-sig", "cp1252", "latin-1"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text(errors="replace")


def scan_file(path: Path, root: Path) -> list[dict]:
    text = read_text(path)
    findings: list[dict] = []
    for category, patterns in PATTERNS.items():
        for pattern in patterns:
            for match in re.finditer(pattern, text, flags=re.IGNORECASE):
                line = text.count("\n", 0, match.start()) + 1
                findings.append({
                    "category": category,
                    "path": str(path.relative_to(root)).replace("\\", "/"),
                    "line": line,
                    "pattern": pattern,
                    "excerpt": text[match.start():match.end()][:120],
                })
    return findings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    scan_roots = [
        root / name
        for name in ("skills", "integrations", "agents", "rules", "templates", "standards", "mcp", "security", "scripts")
        if (root / name).exists()
    ]
    files = []
    for scan_root in scan_roots:
        files.extend(
            p for p in scan_root.rglob("*")
            if p.is_file() and p.suffix.lower() in {".md", ".py", ".json", ".yaml", ".yml", ".toml", ".txt"}
        )
    findings = []
    for path in sorted(files):
        findings.extend(scan_file(path, root))
    summary = {
        "findings": findings,
        "finding_count": len(findings),
        "category_counts": {},
    }
    for finding in findings:
        category = finding["category"]
        summary["category_counts"][category] = summary["category_counts"].get(category, 0) + 1
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary["category_counts"], indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
