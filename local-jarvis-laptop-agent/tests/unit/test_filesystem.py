from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from jarvis.filesystem import (
    FileInspectionConfig,
    FileInspectionError,
    ReadOnlyFilesystemInspector,
    extract_explicit_path,
)


class ReadOnlyFilesystemInspectorTests(unittest.TestCase):
    def test_extract_explicit_windows_path_from_user_text(self) -> None:
        text = (
            r"go through each files on this project path: "
            r"C:\Users\kbrat\PycharmProjects\PremiumPros and provide summary"
        )

        self.assertEqual(
            extract_explicit_path(text),
            r"C:\Users\kbrat\PycharmProjects\PremiumPros",
        )

    def test_inspector_lists_files_reads_text_and_skips_noise(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "README.md").write_text("# Demo\nA small app.", encoding="utf-8")
            (root / "src").mkdir()
            (root / "src" / "app.py").write_text("print('hello')", encoding="utf-8")
            (root / ".env").write_text("TOKEN=super-secret", encoding="utf-8")
            (root / "image.png").write_bytes(b"\x00\x01binary")
            (root / "node_modules").mkdir()
            (root / "node_modules" / "ignored.js").write_text("ignored", encoding="utf-8")
            inspector = self._inspector(root)

            result = inspector.inspect(root)
            evidence = result.evidence_summary()

            paths = {item.path for item in result.files}
            self.assertIn("README.md", paths)
            self.assertIn(str(Path("src") / "app.py"), paths)
            self.assertIn(".env", paths)
            self.assertIn("image.png", paths)
            self.assertNotIn(str(Path("node_modules") / "ignored.js"), paths)
            self.assertIn("A small app", evidence)
            self.assertNotIn("super-secret", evidence)
            self.assertIn("secret_path", evidence)
            self.assertIn("binary_or_unsupported", evidence)

    def test_inspector_enforces_bounds_and_allowed_roots(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            for index in range(5):
                (root / f"file{index}.txt").write_text(str(index), encoding="utf-8")
            inspector = ReadOnlyFilesystemInspector(
                FileInspectionConfig(allowed_roots=(root,), max_files=2)
            )

            result = inspector.inspect(root)

            self.assertEqual(len(result.files), 2)
            self.assertTrue(result.truncated)
            with self.assertRaises(FileInspectionError):
                inspector.inspect(root.parent)

    def test_inspection_does_not_create_or_modify_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            file_path = root / "README.md"
            file_path.write_text("content", encoding="utf-8")
            before = {
                path.relative_to(root): (path.stat().st_size, path.stat().st_mtime_ns)
                for path in root.rglob("*")
            }
            inspector = self._inspector(root)

            inspector.inspect(root)

            after = {
                path.relative_to(root): (path.stat().st_size, path.stat().st_mtime_ns)
                for path in root.rglob("*")
            }
            self.assertEqual(before, after)

    def _inspector(self, root: Path) -> ReadOnlyFilesystemInspector:
        return ReadOnlyFilesystemInspector(FileInspectionConfig(allowed_roots=(root,)))


if __name__ == "__main__":
    unittest.main()
