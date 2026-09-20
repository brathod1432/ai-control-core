#!/usr/bin/env python3
"""Static checks for local LaTeX report projects.

This script reads local .tex and .bib files only. It does not compile LaTeX,
install packages, contact the network, or execute document content.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


LABEL_RE = re.compile(r"\\label\{([^}]+)\}")
CREF_RE = re.compile(r"\\(?:cref|Cref|ref|autoref)\{([^}]+)\}")
CITE_RE = re.compile(r"\\(?:cite|parencite|textcite|autocite|footcite|citep|citet)(?:\[[^\]]*\])*\{([^}]+)\}")
BIB_RESOURCE_RE = re.compile(r"\\addbibresource\{([^}]+)\}")
BIBTEX_RE = re.compile(r"\\bibliography\{([^}]+)\}")
BIB_KEY_RE = re.compile(r"@\w+\s*\{\s*([^,\s]+)")


def strip_comments(text: str) -> str:
    lines = []
    for line in text.splitlines():
        escaped = False
        kept = []
        for char in line:
            if char == "%" and not escaped:
                break
            kept.append(char)
            escaped = char == "\\" and not escaped
            if char != "\\":
                escaped = False
        lines.append("".join(kept))
    return "\n".join(lines)


def split_keys(raw: str) -> list[str]:
    keys = []
    for group in raw:
        keys.extend(key.strip() for key in group.split(",") if key.strip())
    return keys


def find_bib_files(tex_path: Path, tex: str) -> list[Path]:
    files: list[Path] = []
    for name in BIB_RESOURCE_RE.findall(tex):
        files.append((tex_path.parent / name).resolve())
    for name_group in BIBTEX_RE.findall(tex):
        for name in name_group.split(","):
            candidate = name.strip()
            if candidate:
                if not candidate.endswith(".bib"):
                    candidate += ".bib"
                files.append((tex_path.parent / candidate).resolve())
    return files


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: check_latex_project.py path/to/main.tex")
        return 2

    tex_path = Path(sys.argv[1]).resolve()
    if not tex_path.exists():
        print(f"ERROR: file not found: {tex_path}")
        return 2

    raw_tex = tex_path.read_text(encoding="utf-8-sig", errors="replace")
    tex = strip_comments(raw_tex)
    findings: list[str] = []

    required_markers = {
        "documentclass": r"\\documentclass",
        "begin document": r"\\begin\{document\}",
        "title matter or title page": r"\\begin\{titlepage\}|\\maketitle",
        "table of contents": r"\\tableofcontents",
        "bibliography output": r"\\printbibliography|\\bibliography\{",
    }
    for label, pattern in required_markers.items():
        if not re.search(pattern, tex):
            findings.append(f"Missing {label}.")

    if "--shell-escape" in raw_tex or "minted" in tex:
        findings.append("Potential shell-escape dependency found. Require explicit user approval before building with shell escape.")

    labels = LABEL_RE.findall(tex)
    duplicate_labels = sorted({label for label in labels if labels.count(label) > 1})
    for label in duplicate_labels:
        findings.append(f"Duplicate label: {label}")

    label_set = set(labels)
    referenced_labels = split_keys(CREF_RE.findall(tex))
    for key in sorted(set(referenced_labels) - label_set):
        findings.append(f"Reference target has no matching label: {key}")

    cite_keys = split_keys(CITE_RE.findall(tex))
    bib_files = find_bib_files(tex_path, tex)
    bib_keys: set[str] = set()
    for bib_file in bib_files:
        if bib_file.exists():
            bib_text = bib_file.read_text(encoding="utf-8-sig", errors="replace")
            bib_keys.update(BIB_KEY_RE.findall(bib_text))
        else:
            findings.append(f"Bibliography file not found: {bib_file}")

    if cite_keys and not bib_files:
        findings.append("Citations are present but no bibliography resource was found.")
    for key in sorted(set(cite_keys) - bib_keys):
        findings.append(f"Citation key has no matching bibliography entry: {key}")

    draft_markers = ["TODO", "FIXME", "TBD", "Source needed", "\\todo{"]
    for marker in draft_markers:
        if marker in raw_tex:
            findings.append(f"Draft marker remains: {marker}")

    if findings:
        print("NEEDS REVIEW")
        for finding in findings:
            print(f"- {finding}")
        return 1

    print("PASS: static LaTeX checks found no common structural issues.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

