# AGENTS.md — teach

Instructions for any coding or teaching agent working in `GCherry/teach` (Google Antigravity, Claude Code, Cursor, OpenAI Codex). `CLAUDE.md` imports this file; edit this one only.

## Workspace Role

`teach` is the dedicated repository for `/teach` learning courses, printable reference sheets, and the `$0` **Teach** GitHub Pages site (`https://gcherry.github.io/teach/`).

| Path | Purpose |
|---|---|
| `courses/<topic>/` | Self-contained `/teach` workspace (`MISSION.md`, `RESOURCES.md`, `NOTES.md`, `learning-records/*.md`, `lessons/*.html`, `reference/*.html`, `assets/*`). |
| `bin/` | Build and validation scripts (e.g., `bin/build-teach-site.py`, added in Wave 2). |
| `tests/` | Automated `unittest` suite verifying static site generation without mutating raw markdown sources. |
| `docs/agents/` | Agent-facing configuration (`issue-tracker.md`, `triage-labels.md`, `domain.md`). |
| `GLOSSARY.md` | Canonical domain vocabulary for `Teach`. |
| `.agents/skills`, `.claude/skills`, `.cursor/skills` | Git-ignored local NTFS junctions / symlinks pointing to `chill-hq/.agents/skills/`. **Never commit copies of shared skills here.** |

## Build & Verification Commands

```sh
python bin/build-teach-site.py --out dist
python -m unittest discover -s tests
```

## Course Conventions

- Preserve `/teach` workspace files (`MISSION.md`, `RESOURCES.md`, `NOTES.md`, `learning-records/*.md`, `lessons/*.html`, `reference/*.html`, `assets/*`) in raw agent-editable form inside `courses/<topic>/`.
- Use the **1A Atelier** design system (`Dark` + `Light` modes) and include both clipboard `/teach session-handback` and pre-filled GitHub Issue handback controls.
- Keep site builds strictly compatible with free `$0` GitHub Pages (`actions/deploy-pages`).

## Agent skills

### Shared skills

Shared skills (`coordinator`, `real-work`, `teach`, `triage`, `code-review`, `tdd`, etc.) live in `chill-hq/.agents/skills/` and are linked locally (not copied) per `chill-hq/docs/agents/repo-onboarding.md`.

### Issue tracker

GitHub Issues (`GCherry/teach`) via the `gh` CLI or GitHub MCP tools. See `docs/agents/issue-tracker.md`.

### Triage labels

Canonical labels (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`, `work-started`, `priority: now`, `priority: soon`, `priority: later`). See `docs/agents/triage-labels.md`.

### Domain docs

Single-context (`GLOSSARY.md` + `docs/adr/`). See `docs/agents/domain.md`.
