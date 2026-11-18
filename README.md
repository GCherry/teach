# Teach

Interactive multi-session learning courses, printable reference sheets, and retrieval practice exercises authored via `/teach` and published to GitHub Pages (`1A Atelier` Dark & Light design system).

## Structure

- `courses/<topic>/` — Self-contained `/teach` workspaces (`MISSION.md`, `RESOURCES.md`, `NOTES.md`, `learning-records/`, `lessons/`, `reference/`, `assets/`).
- `bin/` — Static site generator (`build-teach-site.py`, added in Wave 2) compiling raw markdown + HTML courses into `dist/` for `$0` GitHub Pages deployment.
- `docs/agents/` — Agent tracker, triage labels, and domain doc contracts linked to [`chill-hq`](https://github.com/GCherry/chill-hq).

## Local Commands (Wave 2+)

```sh
python bin/build-teach-site.py --out dist
python -m unittest discover -s tests
```
