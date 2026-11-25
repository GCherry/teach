# MCP Architecture & Trade-Offs Course (`courses/mcp-architecture/`) + Issue #1

**Origin:** Nov 25, 2026 09:58:00 AM EST — User request via `/coordinator` + `/teach`, bundled with [`GCherry/teach#1`](https://github.com/GCherry/teach/issues/1).

Create a new `/teach` **Course** (`courses/mcp-architecture/`) teaching how the Model Context Protocol (MCP) differs from REST/HTTP APIs and CLIs, where MCP delivers genuine value, and its real-world cons/failure modes — anchored directly in `GCherry/ytmix`'s three interfaces (`cmd/ytmix/` CLI, `internal/ui/` HTTP REST+SSE, `internal/mcp/` JSON-RPC 2.0 stdio) — while closing Issue #1 (`AGENTS.md` cleanup, `plans/` scaffolding, and PR CI checks in `.github/workflows/deploy-pages.yml`).

## For Future Agents

The plan file is the source of truth — a chat summary is not a handoff. Last
step of every agent, including subagents: mark checkboxes `- [x]`; set phase
status; write **Phase Summary**; record **Verification Plan** results. When all
phases are done, fill **Final Recap** and **Deployment Plan**, then archive this
file per the `real-work` skill (Section 3).

**Repo:** `GCherry/teach` (`D:\CodingWorkspace\teach\teach`) — read [`AGENTS.md`](../AGENTS.md) before building or testing. (Reference example repo: `GCherry/ytmix` at `D:\CodingWorkspace\ytmix\ytmix`, public on GitHub.)

**Branch:** `feature/mcp-architecture-course` off `main` (`45383d2`).

**Domain docs:** [`GLOSSARY.md`](../GLOSSARY.md), [`docs/agents/issue-tracker.md`](../docs/agents/issue-tracker.md), [`docs/agents/triage-labels.md`](../docs/agents/triage-labels.md), [`docs/agents/domain.md`](../docs/agents/domain.md).

**Related skills:** `coordinator`, `real-work`, `teach`, `code-review`, `tdd`.

## Open Questions

| # | Question | Owner | Resolve by | Blocking? |
|---|---|---|---|---|

### Resolved

| # | Question | Resolution |
|---|---|---|
| 1 | Which exact live URLs and line-anchored `GCherry/ytmix` links pass live verification (`search_web` / URL check) for `RESOURCES.md` and Lesson citations? | Resolved Nov 25, 2026 10:04:00 AM EST — Verified HTTP 200 across `modelcontextprotocol.io/specification/2025-06-18/{,architecture,server/tools,server/resources,server/prompts}`, `jsonrpc.org/specification`, `anthropic.com/{news/model-context-protocol,engineering/code-execution-with-mcp}`, `github.com/modelcontextprotocol/modelcontextprotocol/discussions`, `latent.space`, and `GCherry/ytmix/blob/main/{cmd/ytmix/main.go,internal/ui/server.go,internal/mcp/{server,registry}.go}` — see Phase 1B Summary. |

## Decisions (confirmed)

| Topic | Decision |
|---|---|
| Course placement | Dedicated new **Course** under `courses/mcp-architecture/` (separate `MISSION.md`, `RESOURCES.md`, `NOTES.md`, `learning-records/`, `lessons/`, `reference/`, `assets/`), leaving `courses/ai-software-factory/` focused on its gateway/telemetry Mission. |
| Mission outcome | Architectural decision judgment: knowing when MCP beats a REST/HTTP API or CLI, where its real value lies, and what its cons/costs are across `ytmix` and future systems. |
| Deliverable structure | Two-Lesson sequence (`0001` Difference & Value in `ytmix`; `0002` Cons, Context/Security Costs & When Not to Use MCP) paired with two printable **Reference Sheets** (`0001` MCP vs API vs CLI Matrix + `ytmix` Primitives Map; `0002` Decision Scorecard & Failure/Mitigation Checklist). |
| ZPD baseline | Senior-developer pace on Go/HTTP APIs, while explicitly unpacking `ytmix/internal/mcp/` (`Tools`, `Resources`, `Prompts`, JSON-RPC 2.0 stdio) without assuming memorized internals. |
| `RESOURCES.md` scope | Include primary specs (MCP `2025-06-18`, JSON-RPC 2.0, Anthropic MCP docs, `GCherry/ytmix` source pointers) plus 1–2 moderated practitioner communities. |
| Issue #1 bundling | Bundle [`GCherry/teach#1`](https://github.com/GCherry/teach/issues/1) into this branch/PR (`Closes #1`): scaffold `plans/README.md` + `plans/archive/README.md`, remove stale Wave 2 line from `AGENTS.md`, and add `pull_request` CI validation (skipping Pages upload/deploy) to `.github/workflows/deploy-pages.yml`. |
| Design system & assets | Reuse the **1A Atelier** (`Dark` + `Light`) design system (`style.css`, `quiz.js`) inside `courses/mcp-architecture/assets/`, including both clipboard `/teach session-handback` and pre-filled GitHub Issue handback controls. |
| Glossary discipline | Strictly honor `teach/GLOSSARY.md` (`Course`, `Mission`, `Lesson`, `Reference Sheet`, `Learning Record`, `Session Handback`, `Zone of Proximal Development`). Distinguish `ytmix` domain terms explicitly (`ytmix audio Track`, `YouTube Chapter Timestamps`) so `_Avoid_` terms never leak into `teach` concepts. |
| Frozen cross-file contract | `lessons/0001-why-mcp-is-not-just-an-api.html`, `lessons/0002-the-hidden-costs-of-mcp.html`, `reference/0001-mcp-vs-api-vs-cli-matrix.html`, `reference/0002-mcp-decision-and-failure-checklist.html`, `learning-records/0001-api-and-ytmix-baseline.md`. |

## Grill

**Recorded:** Nov 25, 2026 09:58:00 AM EST

### Design tree

```text
Teach MCP Course + Issue #1
├── Course Placement → Dedicated courses/mcp-architecture/ (Confirmed)
├── Mission & Scope → Architectural judgment; 2 Lessons + 2 Reference Sheets (Confirmed)
├── ZPD Baseline → Senior dev on APIs/Go; unpack ytmix/internal/mcp/ explicitly (Confirmed)
├── Issue #1 Integration → Bundled on feature/mcp-architecture-course with Closes #1 (Confirmed)
│   ├── AGENTS.md cleanup → Engineering (Wave 1A), Risk: High
│   ├── plans/ scaffolding → Planner (Wave 0)
│   └── deploy-pages.yml PR trigger → Must isolate concurrency group from live main deploys (G1)
├── Static Site & Assets → bin/build-teach-site.py copies first-course assets to dist/assets & per-course assets (G2)
├── Pedagogical & Quiz Rules → Uniform option word/char counts, varied answer slots, verified primary URLs (G3, G4)
└── Domain Vocabulary & ADRs → Honor teach/GLOSSARY.md; no new ADR or glossary edits needed (G5)
```

### Auto-taken (Critical / Low-risk)

| # | Class | Rec | Where applied |
|---|---|---|---|
| G1 | Critical | In `.github/workflows/deploy-pages.yml`, scope `concurrency.group` per PR vs `'pages'` (`${{ github.event_name == 'pull_request' && format('pr-{0}', github.event.pull_request.number) || 'pages' }}`) so opening a PR never cancels an active `main` GitHub Pages deployment, and gate `configure-pages`, `upload-pages-artifact`, and `deploy` with `if: github.event_name != 'pull_request'`. | Phase 1A |
| G2 | Low-risk | Copy `courses/ai-software-factory/assets/{style.css,quiz.js}` into `courses/mcp-architecture/assets/` and keep relative `.md` links (`../MISSION.md`, `../RESOURCES.md`) so `bin/build-teach-site.py` renders and rewrites both raw and `dist/` pages cleanly. | Phase 1B, Phase 2A, Phase 2B |
| G3 | Critical | Enforce `teach/SKILL.md` quiz parity rules (equal/near-equal option word and character counts, varied correct-answer positions, zero formatting hints) and `teach/GLOSSARY.md` naming discipline across all Lessons and Reference Sheets. | Phase 2A, Phase 2B, Phase 3 |
| G4 | Critical | Verify all external primary-source URLs (`modelcontextprotocol.io`, JSON-RPC 2.0, Anthropic MCP docs, community links, and `GCherry/ytmix` blob links) before writing `RESOURCES.md` and Lesson citations (`teach/SKILL.md`: never trust parametric knowledge). | Phase 1B |
| G5 | Low-risk | No `GLOSSARY.md` edits or ADRs needed (`domain-modeling` 3-criteria bar not met for adding a standard `Course`); Risk Tier is **High** due to `AGENTS.md` and `.github/workflows/deploy-pages.yml`, so halt at Wave 0 for explicit user approval before `Engineering` starts and require Human Merge Approval at `Release`. | Wave 0, Wave 3 |

### Remaining (Other → Open Questions)

_(None remaining — all decidable product, scope, and bundling choices were confirmed with the user during Wave 0 grilling; Phase 1B's live URL verification is an irreducible execution lookup tracked in Open Questions #1.)_

## Parallel Execution

| Wave | Phases | Parallel? | Agent count | Gate |
|---|---|---|---|---|
| **0** | 0 | No | 1 | User approves Wave 0 (`plans/mcp-architecture-course.md`, Issue #1 CI/AGENTS scope, and user-facing Course scope) |
| **1** | 1A, 1B | **Yes** | 2 | After Wave 0 approved |
| **2** | 2A, 2B | **Yes** | 2 | After Wave 1 complete (frozen file paths & `assets/` locked) |
| **3** | 3 | No | 1 | After Wave 2 complete (`Reviewer` → `Planner Acceptance Check` → `Release` PR for Human Merge Approval) |

## Wave 0: Planning, Scaffolding & Issue Claim <!-- serial -->

**Triggered by:** User — Nov 25, 2026 09:58:00 AM EST

### Phase 0: Plan Authoring, `plans/` Scaffolding & Issue #1 Claim

Status: Complete <!-- Not Started | In Progress | Complete | Abandoned -->
**Triggered by:** User — Nov 25, 2026 09:58:00 AM EST

- [x] Create branch `feature/mcp-architecture-course` off `main` in `D:\CodingWorkspace\teach\teach`.
- [x] Scaffold `plans/README.md` and `plans/archive/README.md` in `GCherry/teach` (partial Issue #1 criterion).
- [x] Author `plans/mcp-architecture-course.md` with post-write `## Grill` pass recorded.
- [x] Claim [`GCherry/teach#1`](https://github.com/GCherry/teach/issues/1): assign `@me`, apply `work-started` (remove `needs-triage`), and post kickoff comment linking `plans/mcp-architecture-course.md` and `feature/mcp-architecture-course`.
- [x] **Wave 0 Gate (`Ask-First Gate`):** Present the plan and summary to the user and obtain explicit approval before dispatching `Engineering`.

#### Verification Plan

- Confirmed `plans/README.md`, `plans/archive/README.md`, and `plans/mcp-architecture-course.md` exist on `feature/mcp-architecture-course` (`git status -sb` showed only `?? plans/`).
- Confirmed `gh issue edit 1` + `gh issue comment 1` succeeded (`https://github.com/GCherry/teach/issues/1#issuecomment-7166150933`).

#### Phase Summary

Completed Wave 0 planning, scaffolded `plans/` indexes, claimed `GCherry/teach#1`, and received explicit user approval (`"aproved build it all"`) at Nov 25, 2026 10:02:43 AM EST to proceed with Waves 1–3.

## Wave 1: Repo Hygiene (Issue #1) & Course Foundation <!-- parallel: up to 2 tracks -->

**Triggered by:** Coordinator (User approval) — Nov 25, 2026 10:04:00 AM EST

### Phase 1A: Close Out Issue #1 (`AGENTS.md` + CI PR Build Guard)

Status: Complete <!-- Not Started | In Progress | Complete | Abandoned -->
**Triggered by:** Coordinator (User approval) — Nov 25, 2026 10:04:00 AM EST

**Owned files:** `AGENTS.md`, `.github/workflows/deploy-pages.yml`

- [x] Remove the stale `*(Wave 2 adds bin/build-teach-site.py and tests/.)*` line from `AGENTS.md` (`Build & Verification Commands` section).
- [x] Update `.github/workflows/deploy-pages.yml` to trigger on `pull_request: branches: [main]` in addition to `push: branches: [main]` and `workflow_dispatch`.
- [x] Isolate `concurrency.group` in `.github/workflows/deploy-pages.yml` so PR runs use `pr-<number>` while `main` deploys use `pages`, and gate `Configure Pages`, `Upload Pages artifact`, and the `deploy` job with `if: github.event_name != 'pull_request'`.
- [x] Validate `.github/workflows/deploy-pages.yml` structure and run `python -m unittest discover -s tests -v`.

#### Verification Plan

- `python -m unittest discover -s D:\CodingWorkspace\teach\teach\tests -v` → `exit code 0` (`Ran 1 test in 0.125s`, `OK`).
- Direct file inspection of `AGENTS.md:1-35` and `.github/workflows/deploy-pages.yml:1-58` confirmed stale Wave 2 line removed, `pull_request: branches: [main]` added, per-PR `concurrency.group` isolated, and `if: github.event_name != 'pull_request'` applied to `Configure Pages`, `Upload Pages artifact`, and `deploy`. (`PyYAML` is not installed in local Python; CI runner will parse workflow natively.)

#### Phase Summary

Closed Issue #1's `AGENTS.md` and `.github/workflows/deploy-pages.yml` deliverables cleanly. Ready for Wave 2 Lessons and Reference Sheets.

### Phase 1B: Course Foundation (`courses/mcp-architecture/`)

Status: Complete <!-- Not Started | In Progress | Complete | Abandoned -->
**Triggered by:** Coordinator (User approval) — Nov 25, 2026 10:04:00 AM EST

**Owned files:** `courses/mcp-architecture/MISSION.md`, `courses/mcp-architecture/RESOURCES.md`, `courses/mcp-architecture/NOTES.md`, `courses/mcp-architecture/learning-records/0001-api-and-ytmix-baseline.md`, `courses/mcp-architecture/assets/style.css`, `courses/mcp-architecture/assets/quiz.js`

- [x] Copy `courses/ai-software-factory/assets/style.css` and `courses/ai-software-factory/assets/quiz.js` into `courses/mcp-architecture/assets/`.
- [x] Verify live primary-source URLs via `search_web` and HTTP `HEAD` (`200 OK`) for Model Context Protocol spec (`2025-06-18`), JSON-RPC 2.0 specification, Anthropic MCP engineering docs, 2 practitioner communities, and `GCherry/ytmix` GitHub `blob/main` URLs (resolving Open Question #1).
- [x] Author `courses/mcp-architecture/MISSION.md` per `teach/MISSION-FORMAT.md`.
- [x] Author `courses/mcp-architecture/RESOURCES.md` per `teach/RESOURCES-FORMAT.md` (annotated Knowledge + Wisdom sections with verified URLs).
- [x] Author `courses/mcp-architecture/NOTES.md` capturing learner preferences and ZPD notes.
- [x] Author `courses/mcp-architecture/learning-records/0001-api-and-ytmix-baseline.md` per `teach/LEARNING-RECORD-FORMAT.md`.

#### Verification Plan

- `python D:\CodingWorkspace\teach\teach\bin\build-teach-site.py --root D:\CodingWorkspace\teach\teach --out D:\CodingWorkspace\teach\teach\dist` → `exit code 0` (`Built Teach portal with 2 course(s) into D:\CodingWorkspace\teach\teach\dist`).
- External URL `HEAD` check (outside sandbox) returned `200` on all 14 URLs in `RESOURCES.md`.

#### Phase Summary

Created `courses/mcp-architecture/` foundation (`MISSION.md`, `RESOURCES.md`, `NOTES.md`, `learning-records/0001-api-and-ytmix-baseline.md`, `assets/{style.css,quiz.js}`) and verified static portal build with 2 courses. Ready for Wave 2.

## Wave 2: Lessons & Printable Reference Sheets <!-- parallel: up to 2 tracks -->

**Triggered by:** Engineering — Nov 25, 2026 10:05:25 AM EST

### Phase 2A: Lesson 0001 & Reference Sheet 0001 (Difference & Value via `ytmix`)

Status: Complete <!-- Not Started | In Progress | Complete | Abandoned -->
**Triggered by:** Engineering — Nov 25, 2026 10:05:25 AM EST

**Owned files:** `courses/mcp-architecture/lessons/0001-why-mcp-is-not-just-an-api.html`, `courses/mcp-architecture/reference/0001-mcp-vs-api-vs-cli-matrix.html`

- [x] Author `courses/mcp-architecture/lessons/0001-why-mcp-is-not-just-an-api.html` using `1A Atelier` layout (`style.css`, `quiz.js`, `data-lesson-id="mcp-architecture/0001-why-mcp-is-not-just-an-api"`):
  - Contrasts `ytmix`'s 3 interfaces (`cmd/ytmix/main.go` CLI vs. `internal/ui/server.go` HTTP REST+SSE vs. `internal/mcp/` JSON-RPC 2.0 stdio) with inline SVG diagram.
  - Unpacks `initialize`, Tools (`plan_mix` dry-run + `ToolAnnotations`), Resources (`ytmix://presets`, `ytmix://themes`, `ytmix://resolutions`, `ytmix://jobs/{id}`), and Prompts (`create-sleep-mix`, `clean-youtube-release`).
  - Includes `[data-router-exercise]` (4 scenarios), `[data-quiz]` (4 questions, exact word-count parity, varied answer slots), Reference Drawer, follow-up reminder, and `/teach session-handback` bar.
- [x] Author `courses/mcp-architecture/reference/0001-mcp-vs-api-vs-cli-matrix.html` (`class="no-handback"`, `Print Sheet` button) with comparison matrix, complete `ytmix` MCP inventory (9 tools, 3 static + 2 dynamic resources, 2 prompts), and JSON-RPC 2.0 lifecycle sequence.

#### Verification Plan

- `python -m unittest discover -s D:\CodingWorkspace\teach\teach\tests -v` → `exit code 0` (`Ran 1 test in 0.062s`, `OK`).
- `python D:\CodingWorkspace\teach\teach\bin\build-teach-site.py --root D:\CodingWorkspace\teach\teach --out D:\CodingWorkspace\teach\teach\dist` → `exit code 0` (`Built Teach portal with 2 course(s)`).
- Link check across `dist/courses/mcp-architecture/**/*.html` and `dist/index.html`: `Checked 112 local links, missing: []`.
- Glossary check across `courses/mcp-architecture/`: `0` `_Avoid_` terms found.
- Quiz parity check for `0001-why-mcp-is-not-just-an-api.html`: Q1 `[13, 13, 13, 13]` (`pos 2`), Q2 `[12, 12, 12, 12]` (`pos 4`), Q3 `[12, 12, 12, 12]` (`pos 1`), Q4 `[12, 12, 12, 12]` (`pos 3`).

#### Phase Summary

Authored Lesson 0001 and printable Reference Sheet 0001 anchored in `ytmix`, verified all relative links and exact quiz option parity, and built `dist/` cleanly.

### Phase 2B: Lesson 0002 & Reference Sheet 0002 (Cons, Costs & Decision Framework)

Status: Complete <!-- Not Started | In Progress | Complete | Abandoned -->
**Triggered by:** Engineering — Nov 25, 2026 10:05:25 AM EST

**Owned files:** `courses/mcp-architecture/lessons/0002-the-hidden-costs-of-mcp.html`, `courses/mcp-architecture/reference/0002-mcp-decision-and-failure-checklist.html`

- [x] Author `courses/mcp-architecture/lessons/0002-the-hidden-costs-of-mcp.html` using `1A Atelier` layout (`style.css`, `quiz.js`, `data-lesson-id="mcp-architecture/0002-the-hidden-costs-of-mcp"`):
  - Covers 5 concrete cons grounded in `ytmix/internal/mcp/` (upfront `tools/list` context-window tax, stateful stdio lifecycle & stdout fragility with 16 MiB cap, polling `get_render_status` vs. SSE, indirect prompt injection via `rawId3Title` + advisory `ToolAnnotations` vs. `DisallowUnknownFields`, and CLI maintenance duplication) with inline SVG decision diagram.
  - Includes `[data-router-exercise]` (4 scenarios), `[data-quiz]` (4 questions, exact word-count parity, varied answer slots), Reference Drawer, follow-up reminder, and `/teach session-handback` bar.
- [x] Author `courses/mcp-architecture/reference/0002-mcp-decision-and-failure-checklist.html` (`class="no-handback"`, `Print Sheet` button) with the 5-gate Decision Scorecard (REST vs. CLI vs. MCP) and `ytmix`-grounded hardening checklist.

#### Verification Plan

- `python -m unittest discover -s D:\CodingWorkspace\teach\teach\tests -v` → `exit code 0` (`Ran 1 test in 0.062s`, `OK`).
- `python D:\CodingWorkspace\teach\teach\bin\build-teach-site.py --root D:\CodingWorkspace\teach\teach --out D:\CodingWorkspace\teach\teach\dist` → `exit code 0`.
- Link check: `Checked 112 local links, missing: []`; Glossary check: `0` `_Avoid_` terms.
- Quiz parity check for `0002-the-hidden-costs-of-mcp.html`: Q1 `[12, 12, 12, 12]` (`pos 2`), Q2 `[12, 12, 12, 12]` (`pos 4`), Q3 `[11, 11, 11, 11]` (`pos 1`), Q4 `[12, 12, 12, 12]` (`pos 3`).

#### Phase Summary

Authored Lesson 0002 and printable Reference Sheet 0002 covering MCP cons, security/context trade-offs, and exit criteria, verified all local links and exact quiz parity, and built `dist/` cleanly.

## Wave 3: Full Verification, Review, Acceptance Check & PR Release <!-- serial -->

**Triggered by:** Planner — Nov 25, 2026 09:58:00 AM EST

### Phase 3: End-to-End Verification, `Reviewer`, `Acceptance Check`, Plan Archival & PR Prep

Status: Not Started <!-- Not Started | In Progress | Complete | Abandoned -->
**Triggered by:** Planner — Nov 25, 2026 09:58:00 AM EST

- [ ] Run `python -m unittest discover -s tests -v` and `python bin/build-teach-site.py --root . --out dist`.
- [ ] Verify generated `dist/index.html` lists both `AI Software Factory` and the new MCP Course, and verify zero broken internal links across `dist/courses/mcp-architecture/` (HTML + rendered Markdown).
- [ ] Run read-only `Reviewer` (`code-review` Standards + Spec) against `HEAD` SHA and resolve any blocking findings.
- [ ] Run read-only `Planner` `Acceptance Check` grading all plan checkboxes and Issue #1 criteria.
- [ ] Update [`GCherry/teach#1`](https://github.com/GCherry/teach/issues/1) checkboxes (`- [x]`) and fill **Final Recap** and **Deployment Plan** below.
- [ ] Archive `plans/mcp-architecture-course.md` → `plans/archive/mcp-architecture-course.md` (updating `plans/README.md`, `plans/archive/README.md`, and relative links `../` → `../../`) in the final commit on `feature/mcp-architecture-course` before PR merge per `real-work` Section 3.
- [ ] Run `Release` (`pre-merge`): push `feature/mcp-architecture-course`, open PR targeting `main` with `Closes #1` and `## Code Review Summary`, verify PR CI workflow runs `unittest` + `build-teach-site.py` without deploying Pages, and pause for **Human Merge Approval** (`Risk: High` PR targeting `main`).

#### Verification Plan

- `python -m unittest discover -s tests -v` passes all tests.
- `python bin/build-teach-site.py --root . --out dist` exits `0` and leaves raw Markdown sources unchanged (`git status` clean of unintended diffs).
- `gh pr checks` green on `pull_request` trigger (build/test pass, Pages deploy skipped), **Merge Bar** satisfied, awaiting human merge.

#### Phase Summary

_(write when phase completes)_

## Final Recap

_(write when all phases complete)_

## Deployment Plan

_(write when all phases complete)_
