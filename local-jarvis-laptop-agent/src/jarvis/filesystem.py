"""Read-only local filesystem inspection for explicitly scoped paths."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
import os

from .safety import redact_text


DEFAULT_EXCLUDED_DIRS = frozenset(
    {
        ".git",
        ".hg",
        ".svn",
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        ".venv",
        "venv",
        "env",
        "node_modules",
        "dist",
        "build",
        ".idea",
        ".vscode",
    }
)
TEXT_EXTENSIONS = frozenset(
    {
        ".bat",
        ".cfg",
        ".conf",
        ".css",
        ".csv",
        ".env.example",
        ".gitignore",
        ".html",
        ".ini",
        ".js",
        ".json",
        ".jsx",
        ".md",
        ".ps1",
        ".py",
        ".rst",
        ".toml",
        ".ts",
        ".tsx",
        ".txt",
        ".yaml",
        ".yml",
    }
)
SECRET_NAME_PARTS = (
    ".env",
    "id_rsa",
    "id_dsa",
    "id_ecdsa",
    "id_ed25519",
    "private",
    "secret",
    "secrets",
    "token",
    "credential",
    "credentials",
    "password",
)
SECRET_EXTENSIONS = frozenset({".key", ".pem", ".p12", ".pfx"})


@dataclass(frozen=True)
class FileInspectionConfig:
    allowed_roots: tuple[Path, ...] = field(default_factory=lambda: default_allowed_roots())
    excluded_dirs: frozenset[str] = DEFAULT_EXCLUDED_DIRS
    max_depth: int = 6
    max_files: int = 300
    max_snippet_files: int = 40
    max_read_bytes_per_file: int = 4096
    max_total_read_bytes: int = 65536


@dataclass(frozen=True)
class InspectedFile:
    path: str
    kind: str
    size_bytes: int | None
    snippet: str | None = None
    skipped_reason: str | None = None


@dataclass(frozen=True)
class FileInspectionResult:
    root: Path
    files: list[InspectedFile]
    directories_seen: int
    truncated: bool
    skipped: dict[str, int]

    def evidence_summary(self) -> str:
        ext_counts = Counter(
            Path(item.path).suffix.lower() or "[no extension]"
            for item in self.files
            if item.kind == "file"
        )
        top_extensions = ", ".join(
            f"{extension}={count}" for extension, count in ext_counts.most_common(12)
        )
        lines = [
            f"Read-only local filesystem inspection completed for: {self.root}",
            f"Files listed: {len([item for item in self.files if item.kind == 'file'])}",
            f"Directories seen: {self.directories_seen}",
            f"Truncated: {self.truncated}",
            f"Top file types: {top_extensions or 'none'}",
        ]
        if self.skipped:
            skipped_text = ", ".join(
                f"{reason}={count}" for reason, count in sorted(self.skipped.items())
            )
            lines.append(f"Skipped: {skipped_text}")

        lines.append("")
        lines.append("File inventory:")
        for item in self.files[:120]:
            size = "" if item.size_bytes is None else f" ({item.size_bytes} bytes)"
            reason = "" if item.skipped_reason is None else f" [{item.skipped_reason}]"
            lines.append(f"- {item.path}{size}{reason}")

        snippets = [item for item in self.files if item.snippet]
        if snippets:
            lines.append("")
            lines.append("Bounded text snippets:")
            for item in snippets[:20]:
                lines.append(f"### {item.path}")
                lines.append(item.snippet or "")
        return "\n".join(lines)


class FileInspectionError(ValueError):
    """Raised when a read-only inspection request is not safely scoped."""


class ReadOnlyFilesystemInspector:
    """Inspect local files without creating, modifying, or deleting anything."""

    def __init__(self, config: FileInspectionConfig | None = None) -> None:
        self.config = config or FileInspectionConfig()
        self.allowed_roots = tuple(root.resolve() for root in self.config.allowed_roots)

    def inspect(self, requested_path: str | Path) -> FileInspectionResult:
        root = Path(os.path.expandvars(str(requested_path))).expanduser().resolve()
        if not self._is_allowed(root):
            allowed = ", ".join(str(path) for path in self.allowed_roots)
            raise FileInspectionError(
                f"Path is outside the approved read-only roots. Approved roots: {allowed}"
            )
        if not root.exists():
            raise FileInspectionError(f"Path does not exist: {root}")

        files: list[InspectedFile] = []
        skipped: Counter[str] = Counter()
        directories_seen = 0
        truncated = False
        total_read_bytes = 0
        snippet_count = 0

        if root.is_file():
            item, read_bytes = self._inspect_file(root, root.parent, total_read_bytes, snippet_count)
            return FileInspectionResult(
                root=root,
                files=[item],
                directories_seen=0,
                truncated=False,
                skipped={item.skipped_reason: 1} if item.skipped_reason else {},
            )

        stack: list[tuple[Path, int]] = [(root, 0)]
        while stack:
            current, depth = stack.pop()
            directories_seen += 1
            if depth > self.config.max_depth:
                skipped["max_depth"] += 1
                continue

            try:
                children = sorted(current.iterdir(), key=lambda path: (path.is_file(), path.name.lower()))
            except OSError:
                skipped["unreadable_directory"] += 1
                continue

            for child in children:
                if len([item for item in files if item.kind == "file"]) >= self.config.max_files:
                    truncated = True
                    break
                if child.is_dir():
                    if child.name in self.config.excluded_dirs:
                        skipped["excluded_directory"] += 1
                        continue
                    stack.append((child, depth + 1))
                    continue
                if child.is_file():
                    item, read_bytes = self._inspect_file(child, root, total_read_bytes, snippet_count)
                    files.append(item)
                    if item.snippet:
                        snippet_count += 1
                        total_read_bytes += read_bytes
                    if item.skipped_reason:
                        skipped[item.skipped_reason] += 1
            if truncated:
                break

        files.sort(key=lambda item: item.path.lower())
        return FileInspectionResult(
            root=root,
            files=files,
            directories_seen=directories_seen,
            truncated=truncated,
            skipped=dict(skipped),
        )

    def _inspect_file(
        self,
        path: Path,
        root: Path,
        total_read_bytes: int,
        snippet_count: int,
    ) -> tuple[InspectedFile, int]:
        try:
            size = path.stat().st_size
        except OSError:
            return InspectedFile(
                path=_relative_or_name(path, root),
                kind="file",
                size_bytes=None,
                skipped_reason="unreadable_file",
            ), 0

        if _looks_secret_path(path):
            return InspectedFile(
                path=_relative_or_name(path, root),
                kind="file",
                size_bytes=size,
                skipped_reason="secret_path",
            ), 0
        if snippet_count >= self.config.max_snippet_files:
            return InspectedFile(
                path=_relative_or_name(path, root),
                kind="file",
                size_bytes=size,
                skipped_reason="snippet_file_limit",
            ), 0
        if total_read_bytes >= self.config.max_total_read_bytes:
            return InspectedFile(
                path=_relative_or_name(path, root),
                kind="file",
                size_bytes=size,
                skipped_reason="total_read_limit",
            ), 0
        if not _is_probably_text_file(path):
            return InspectedFile(
                path=_relative_or_name(path, root),
                kind="file",
                size_bytes=size,
                skipped_reason="binary_or_unsupported",
            ), 0

        read_limit = min(
            self.config.max_read_bytes_per_file,
            self.config.max_total_read_bytes - total_read_bytes,
        )
        try:
            raw = path.read_bytes()[:read_limit]
        except OSError:
            return InspectedFile(
                path=_relative_or_name(path, root),
                kind="file",
                size_bytes=size,
                skipped_reason="unreadable_file",
            ), 0
        if b"\x00" in raw:
            return InspectedFile(
                path=_relative_or_name(path, root),
                kind="file",
                size_bytes=size,
                skipped_reason="binary_or_unsupported",
            ), 0

        text = raw.decode("utf-8", errors="replace")
        snippet = redact_text(_clean_snippet(text))
        return InspectedFile(
            path=_relative_or_name(path, root),
            kind="file",
            size_bytes=size,
            snippet=snippet,
        ), len(raw)

    def _is_allowed(self, path: Path) -> bool:
        return any(path == root or root in path.parents for root in self.allowed_roots)


def default_allowed_roots() -> tuple[Path, ...]:
    home = Path.home()
    return (home / "PycharmProjects",)


def extract_explicit_path(text: str) -> str | None:
    """Extract an explicit absolute local path from user text."""

    quoted = _extract_quoted_path(text)
    if quoted:
        return quoted

    normalized = text.strip()
    marker_match = None
    for marker in ("project path:", "path:", "folder:", "directory:"):
        index = normalized.casefold().find(marker)
        if index >= 0:
            marker_match = normalized[index + len(marker) :].strip()
            break
    candidate_source = marker_match or normalized

    drive_index = _find_drive_path_start(candidate_source)
    if drive_index is None:
        return None

    candidate = candidate_source[drive_index:].strip()
    for separator in (" and ", " please", " to summarize", " to analyse", " to analyze"):
        index = candidate.casefold().find(separator)
        if index > 0:
            candidate = candidate[:index]
    return candidate.strip().rstrip(".,;")


def _extract_quoted_path(text: str) -> str | None:
    for quote in ('"', "'"):
        parts = text.split(quote)
        for part in parts[1::2]:
            if _find_drive_path_start(part) is not None:
                return part.strip()
    return None


def _find_drive_path_start(text: str) -> int | None:
    for index in range(max(0, len(text) - 2)):
        if text[index].isalpha() and text[index + 1 : index + 3] == ":\\":
            return index
    return None


def _relative_or_name(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return path.name


def _looks_secret_path(path: Path) -> bool:
    name = path.name.casefold()
    if path.suffix.casefold() in SECRET_EXTENSIONS:
        return True
    return any(part in name for part in SECRET_NAME_PARTS)


def _is_probably_text_file(path: Path) -> bool:
    name = path.name.casefold()
    suffix = path.suffix.casefold()
    return suffix in TEXT_EXTENSIONS or name in TEXT_EXTENSIONS


def _clean_snippet(text: str) -> str:
    lines = [line.rstrip() for line in text.splitlines()]
    compact = "\n".join(line for line in lines if line.strip())
    return compact[:3000]
