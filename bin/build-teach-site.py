#!/usr/bin/env python3
"""Build static HTML output for a Teach multi-course repository."""

from __future__ import annotations

import argparse
import html
import re
import shutil
import sys
from pathlib import Path

MD_LINK_RE = re.compile(r'((?:href|src)=["\'])([^"\']+?)\.md((?:#[^"\']*)?["\'])', re.IGNORECASE)
EXTERNAL_PREFIXES = ("http://", "https://", "mailto:", "#")


def _inline_format(text: str) -> str:
    """Convert inline markdown (links, code, bold, italic) to safe HTML."""
    escaped = html.escape(text, quote=False)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)

    def _link_repl(match: re.Match[str]) -> str:
        label, target = match.group(1), match.group(2)
        if not target.startswith(EXTERNAL_PREFIXES) and target.endswith(".md"):
            target = target[:-3] + ".html"
        elif not target.startswith(EXTERNAL_PREFIXES) and ".md#" in target:
            target = target.replace(".md#", ".html#", 1)
        return f'<a href="{html.escape(target, quote=True)}">{label}</a>'

    escaped = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", _link_repl, escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", escaped)
    return escaped


def markdown_to_html(md_text: str) -> tuple[str, str]:
    """Render simple Markdown into HTML body and return (title, body_html)."""
    lines = md_text.splitlines()
    title = "Teach Document"
    out: list[str] = []
    in_code = False
    in_list = False
    para_buf: list[str] = []

    def flush_para() -> None:
        if para_buf:
            out.append(f"<p>{_inline_format(' '.join(para_buf))}</p>")
            para_buf.clear()

    def close_list() -> None:
        nonlocal in_list
        if in_list:
            out.append("</ul>")
            in_list = False

    for raw in lines:
        stripped = raw.strip()
        if stripped.startswith("```"):
            flush_para()
            close_list()
            if not in_code:
                out.append("<pre><code>")
                in_code = True
            else:
                out.append("</code></pre>")
                in_code = False
            continue

        if in_code:
            out.append(html.escape(raw))
            continue

        if not stripped:
            flush_para()
            close_list()
            continue

        heading_match = re.match(r"^(#{1,4})\s+(.*)$", stripped)
        if heading_match:
            flush_para()
            close_list()
            level = len(heading_match.group(1))
            heading_text = heading_match.group(2).strip()
            if level == 1 and title == "Teach Document":
                title = heading_text
            out.append(f"<h{level}>{_inline_format(heading_text)}</h{level}>")
            continue

        if stripped.startswith("- ") or stripped.startswith("* "):
            flush_para()
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li>{_inline_format(stripped[2:].strip())}</li>")
            continue

        close_list()
        para_buf.append(stripped)

    flush_para()
    close_list()
    if in_code:
        out.append("</code></pre>")
    return title, "\n".join(out)


def rewrite_md_links(html_text: str) -> str:
    """Rewrite local relative .md links inside HTML attributes to .html."""
    def _repl(match: re.Match[str]) -> str:
        prefix, path_part, suffix = match.group(1), match.group(2), match.group(3)
        if path_part.startswith(("http://", "https://")):
            return match.group(0)
        return f"{prefix}{path_part}.html{suffix}"

    return MD_LINK_RE.sub(_repl, html_text)


def wrap_atelier_page(
    *,
    title: str,
    kicker: str,
    body_html: str,
    css_href: str,
    js_href: str,
    nav_links: list[tuple[str, str, bool]],
    brand_href: str,
    subtitle: str,
) -> str:
    """Wrap content in the 1A Atelier Dark/Light shell."""
    nav_items = "\n        ".join(
        f'<a class="nav-link{" active" if active else ""}" href="{html.escape(href, quote=True)}">{html.escape(label)}</a>'
        for label, href, active in nav_links
    )
    return f"""<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Teach · {html.escape(title)}</title>
  <link rel="stylesheet" href="{html.escape(css_href, quote=True)}" />
  <script>
    (function () {{
      var m = new URLSearchParams(window.location.search).get("mode") || localStorage.getItem("teach_theme") || "dark";
      document.documentElement.setAttribute("data-theme", m === "light" ? "light" : "dark");
    }})();
  </script>
</head>
<body class="no-handback" data-lesson-id="teach-portal">
  <nav class="site-nav">
    <div class="site-nav-inner">
      <a class="site-brand" href="{html.escape(brand_href, quote=True)}">
        <span class="brand-mark">T</span>
        <span class="brand-text">
          <strong>Teach</strong>
          <span class="brand-sub">{html.escape(subtitle)} · <span data-mode-badge>Dark Mode</span></span>
        </span>
      </a>
      <div class="site-links">
        {nav_items}
        <button class="btn" type="button" data-theme-toggle>Light Mode</button>
      </div>
    </div>
  </nav>
  <main class="page-wide prose-wide">
    <p class="kicker">{html.escape(kicker)}</p>
    {body_html}
  </main>
  <script src="{html.escape(js_href, quote=True)}"></script>
</body>
</html>
"""


def _extract_html_title(html_path: Path) -> str:
    text = html_path.read_text(encoding="utf-8")
    m = re.search(r"<h1[^>]*>(.*?)</h1>", text, re.IGNORECASE | re.DOTALL)
    if m:
        return re.sub(r"<[^>]+>", "", m.group(1)).strip()
    return html_path.stem


def build_site(root: Path, out: Path) -> list[dict[str, object]]:
    """Compile all courses/<slug> directories under root into static HTML in out."""
    courses_dir = root / "courses"
    if not courses_dir.is_dir():
        raise FileNotFoundError(f"Missing courses directory: {courses_dir}")

    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True, exist_ok=True)

    course_dirs = sorted([p for p in courses_dir.iterdir() if p.is_dir()], key=lambda p: p.name)
    summaries: list[dict[str, object]] = []
    shared_assets_copied = False

    for cdir in course_dirs:
        slug = cdir.name
        dest = out / "courses" / slug
        shutil.copytree(cdir, dest)

        assets_dir = cdir / "assets"
        if not shared_assets_copied and assets_dir.is_dir():
            shutil.copytree(assets_dir, out / "assets", dirs_exist_ok=True)
            shared_assets_copied = True

        # Render root markdown docs inside course
        mission_title = slug.replace("-", " ").title()
        for md_name in ("MISSION.md", "RESOURCES.md", "NOTES.md"):
            md_path = cdir / md_name
            if md_path.is_file():
                doc_title, doc_body = markdown_to_html(md_path.read_text(encoding="utf-8"))
                if md_name == "MISSION.md":
                    mission_title = doc_title.removeprefix("Mission:").strip() or mission_title
                rendered = wrap_atelier_page(
                    title=doc_title,
                    kicker=f"Course · {slug} · {md_name}",
                    body_html=doc_body,
                    css_href="assets/style.css",
                    js_href="assets/quiz.js",
                    nav_links=[
                        ("All Courses", "../../index.html", False),
                        ("Course Home", "index.html", False),
                        ("Mission", "MISSION.html", md_name == "MISSION.md"),
                        ("Resources", "RESOURCES.html", md_name == "RESOURCES.md"),
                    ],
                    brand_href="../../index.html",
                    subtitle=mission_title,
                )
                (dest / f"{md_path.stem}.html").write_text(rendered, encoding="utf-8")

        # Render learning-records/*.md
        records_out: list[tuple[str, str]] = []
        lr_dir = cdir / "learning-records"
        if lr_dir.is_dir():
            for lr_md in sorted(lr_dir.glob("*.md")):
                lr_title, lr_body = markdown_to_html(lr_md.read_text(encoding="utf-8"))
                rendered_lr = wrap_atelier_page(
                    title=lr_title,
                    kicker=f"Learning Record · {lr_md.stem}",
                    body_html=lr_body,
                    css_href="../assets/style.css",
                    js_href="../assets/quiz.js",
                    nav_links=[
                        ("All Courses", "../../../index.html", False),
                        ("Course Home", "../index.html", False),
                        ("Mission", "../MISSION.html", False),
                    ],
                    brand_href="../../../index.html",
                    subtitle=mission_title,
                )
                (dest / "learning-records" / f"{lr_md.stem}.html").write_text(rendered_lr, encoding="utf-8")
                records_out.append((lr_title, f"learning-records/{lr_md.stem}.html"))

        # Rewrite .md links inside copied lessons and references
        lessons_out: list[tuple[str, str]] = []
        refs_out: list[tuple[str, str]] = []
        for sub, target_list in (("lessons", lessons_out), ("reference", refs_out)):
            sub_dir = dest / sub
            if sub_dir.is_dir():
                for html_file in sorted(sub_dir.glob("*.html")):
                    rewritten = rewrite_md_links(html_file.read_text(encoding="utf-8"))
                    html_file.write_text(rewritten, encoding="utf-8")
                    target_list.append((_extract_html_title(html_file), f"{sub}/{html_file.name}"))

        # Build per-course index.html
        def _render_list(items: list[tuple[str, str]], empty_msg: str) -> str:
            if not items:
                return f"<p><em>{html.escape(empty_msg)}</em></p>"
            lis = "".join(f'<li><a href="{html.escape(h, quote=True)}">{html.escape(t)}</a></li>' for t, h in items)
            return f"<ul>{lis}</ul>"

        course_body = f"""<h1>{html.escape(mission_title)}</h1>
<p class="lead">Course workspace: <code>courses/{html.escape(slug)}/</code></p>
<div class="grid-2">
  <div class="card">
    <span class="card-tag">Lessons</span>
    <h3>Interactive Modules</h3>
    {_render_list(lessons_out, "No lessons yet.")}
  </div>
  <div class="card">
    <span class="card-tag">Reference</span>
    <h3>Printable Sheets</h3>
    {_render_list(refs_out, "No reference sheets yet.")}
  </div>
</div>
<div class="grid-2">
  <div class="card">
    <span class="card-tag amber">Context</span>
    <h3>Mission &amp; Resources</h3>
    <ul>
      <li><a href="MISSION.html">Mission (MISSION.md)</a></li>
      <li><a href="RESOURCES.html">Curated Resources (RESOURCES.md)</a></li>
    </ul>
  </div>
  <div class="card">
    <span class="card-tag amber">ZPD State</span>
    <h3>Learning Records</h3>
    {_render_list(records_out, "No learning records yet.")}
  </div>
</div>"""

        course_html = wrap_atelier_page(
            title=mission_title,
            kicker=f"Teach · Course Hub · {slug}",
            body_html=course_body,
            css_href="assets/style.css",
            js_href="assets/quiz.js",
            nav_links=[
                ("All Courses", "../../index.html", False),
                ("Course Home", "index.html", True),
                ("Mission", "MISSION.html", False),
                ("Resources", "RESOURCES.html", False),
            ],
            brand_href="../../index.html",
            subtitle=mission_title,
        )
        (dest / "index.html").write_text(course_html, encoding="utf-8")

        summaries.append({
            "slug": slug,
            "title": mission_title,
            "lessons": lessons_out,
            "references": refs_out,
            "records": records_out,
        })

    # Build root Teach portal index.html
    cards_html = []
    for item in summaries:
        slug = str(item["slug"])
        title = str(item["title"])
        lessons = item["lessons"]
        refs = item["references"]
        records = item["records"]
        first_lesson = lessons[0][1] if lessons else "index.html"
        cards_html.append(f"""  <div class="card">
    <span class="card-tag">{len(lessons)} Lesson(s) · {len(refs)} Reference(s)</span>
    <h3><a href="courses/{html.escape(slug)}/index.html">{html.escape(title)}</a></h3>
    <p><code>courses/{html.escape(slug)}/</code> · {len(records)} learning record(s)</p>
    <p>
      <a class="btn btn-primary" href="courses/{html.escape(slug)}/{html.escape(first_lesson)}">Start / Resume</a>
      <a class="btn" href="courses/{html.escape(slug)}/index.html">Course Hub</a>
    </p>
  </div>""")

    portal_body = f"""<h1>Teach</h1>
<p class="lead">
  Interactive multi-session courses, printable reference sheets, and retrieval practice built via <code>/teach</code>.
</p>
<div class="grid-2">
{chr(10).join(cards_html)}
</div>"""

    portal_html = wrap_atelier_page(
        title="Course Portal",
        kicker="Teach · Course Catalog",
        body_html=portal_body,
        css_href="assets/style.css",
        js_href="assets/quiz.js",
        nav_links=[("Course Catalog", "index.html", True)],
        brand_href="index.html",
        subtitle="Learning Portal",
    )
    (out / "index.html").write_text(portal_html, encoding="utf-8")
    return summaries


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build static Teach site for GitHub Pages.")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--out", type=Path, default=Path(__file__).resolve().parent.parent / "dist")
    args = parser.parse_args(argv)

    summaries = build_site(args.root.resolve(), args.out.resolve())
    print(f"Built Teach portal with {len(summaries)} course(s) into {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
