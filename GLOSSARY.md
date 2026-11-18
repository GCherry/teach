# Teach

Domain glossary for `GCherry/teach` — interactive multi-session learning courses, printable reference sheets, and static GitHub Pages publishing built around `/teach`.

## Language

**Course**:
A self-contained topic directory under `courses/<slug>/` holding a `MISSION.md`, `RESOURCES.md`, `NOTES.md`, `learning-records/`, `lessons/`, `reference/`, and `assets/`.
_Avoid_: Module, Track, Folder, Workspace

**Mission**:
The concrete real-world goal in `MISSION.md` that grounds every lesson, citation, and retrieval exercise for a Course.
_Avoid_: Goal doc, Objective file, Syllabus

**Lesson**:
A short, interactive HTML unit (`lessons/NNNN-<slug>.html`) teaching one tightly scoped concept inside the learner's Zone of Proximal Development with immediate retrieval feedback.
_Avoid_: Chapter, Page, Tutorial, Post

**Reference Sheet**:
A print-ready, compressed HTML quick-reference (`reference/NNNN-<slug>.html`) capturing reusable schemas, formulas, tables, or glossaries across lessons.
_Avoid_: Cheat sheet doc, Appendix, Summary page

**Learning Record**:
A sequential Markdown decision record (`learning-records/NNNN-<slug>.md`) capturing verified understanding, prior knowledge, corrected misconceptions, or Mission shifts.
_Avoid_: Journal entry, Note, Log

**Session Handback**:
The structured `/teach session-handback` summary copied or logged from the browser UI (scores, missed checks, follow-up notes) so an agent can compute the next Lesson and Learning Record.
_Avoid_: Export dump, Progress sync, Telemetry ping

**Zone of Proximal Development**:
The target challenge window between what the learner already proved in `learning-records/` and what stretches them just enough without overloading working memory.
_Avoid_: Difficulty level, Skill tier
