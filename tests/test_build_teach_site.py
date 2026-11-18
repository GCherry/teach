"""Tests for bin/build-teach-site.py static site generation."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parent.parent / "bin" / "build-teach-site.py"
SPEC = importlib.util.spec_from_file_location("build_teach_site", MODULE_PATH)
assert SPEC and SPEC.loader
BUILD_MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILD_MOD)


class BuildTeachSiteTests(unittest.TestCase):
    def _seed_course(self, root: Path, slug: str, title: str) -> None:
        course = root / "courses" / slug
        (course / "assets").mkdir(parents=True)
        (course / "lessons").mkdir()
        (course / "reference").mkdir()
        (course / "learning-records").mkdir()

        (course / "assets" / "style.css").write_text("body { color: #fff; }", encoding="utf-8")
        (course / "assets" / "quiz.js").write_text("console.log('ok');", encoding="utf-8")
        (course / "MISSION.md").write_text(f"# Mission: {title}\n\n## Why\nLearn {title}.\n", encoding="utf-8")
        (course / "RESOURCES.md").write_text(
            "# Resources\n\n- [Primary Doc](https://example.com)\n", encoding="utf-8"
        )
        (course / "learning-records" / "0001-baseline.md").write_text(
            "# Baseline Established\n\nReady for lesson 1.\n", encoding="utf-8"
        )
        (course / "lessons" / "0001-intro.html").write_text(
            '<html><body><h1>Intro</h1><a href="../MISSION.md">Mission</a>'
            '<a href="../RESOURCES.md">Resources</a>'
            '<a href="https://example.com/spec.md">External</a></body></html>',
            encoding="utf-8",
        )
        (course / "reference" / "0001-sheet.html").write_text(
            '<html><body><h1>Sheet</h1><a href="../MISSION.md">Mission</a></body></html>',
            encoding="utf-8",
        )

    def test_multi_course_build_preserves_sources_and_rewrites_md_links(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            out = Path(tmp) / "dist"
            self._seed_course(root, "ai-software-factory", "AI Software Factory")
            self._seed_course(root, "systems-design", "Systems Design")

            mission_before = (root / "courses" / "ai-software-factory" / "MISSION.md").read_text(encoding="utf-8")
            summaries = BUILD_MOD.build_site(root, out)

            self.assertEqual(len(summaries), 2)
            self.assertTrue((out / "index.html").is_file())
            portal_html = (out / "index.html").read_text(encoding="utf-8")
            self.assertIn("AI Software Factory", portal_html)
            self.assertIn("Systems Design", portal_html)

            # Rendered markdown pages exist
            self.assertTrue((out / "courses" / "ai-software-factory" / "MISSION.html").is_file())
            self.assertTrue((out / "courses" / "ai-software-factory" / "RESOURCES.html").is_file())
            self.assertTrue(
                (out / "courses" / "ai-software-factory" / "learning-records" / "0001-baseline.html").is_file()
            )

            # Relative .md links rewritten to .html; external links untouched
            lesson_html = (out / "courses" / "ai-software-factory" / "lessons" / "0001-intro.html").read_text(
                encoding="utf-8"
            )
            self.assertIn('href="../MISSION.html"', lesson_html)
            self.assertIn('href="../RESOURCES.html"', lesson_html)
            self.assertIn('href="https://example.com/spec.md"', lesson_html)

            # Source markdown untouched
            mission_after = (root / "courses" / "ai-software-factory" / "MISSION.md").read_text(encoding="utf-8")
            self.assertEqual(mission_before, mission_after)


if __name__ == "__main__":
    unittest.main()
