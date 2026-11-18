# User Has Already Built the Workflow & Agent Control Plane in chill-hq

The user has already designed and implemented a multi-agent workflow control plane in `chill-hq` (`Coordinator v2` with `Planner`, `Engineering`, `Reviewer`, `Docs`, `Release`, and `Retro` roles, plus `Risk Tier`, `Ask-First Gate`, `Narrowing Gate`, `Acceptance Check`, and `Merge Bar` gates). Future lessons must skip introductory role-taxonomy explanations and focus on the missing infrastructure planes: **AI Gateway & Model Routing**, **Cross-Harness Telemetry (Subscription vs. Metered API vs. Local)**, **Token-to-PR Attribution**, and **Enterprise Governance**.

## Evidence
- Inspected `README.md`, `GLOSSARY.md`, and `AGENTS.md` in `chill-hq`, confirming existing Role contracts, CI validation (`bin/validate.py`), and dual-mode repo onboarding.
- User stated concrete goals: upgrading `chill-hq` with observability + AI gateway capabilities and pitching an agnostic governance architecture to leadership.

## Implications
- Treat `chill-hq`'s Coordinator v2 as the anchor example for **Plane 1 (Intake)** and **Plane 5 (Verification & Release)** in every lesson.
- Emphasize the architectural split between flat-rate subscription harnesses (Google Antigravity, Claude Code subscription) and gateway-routed API/local endpoints.
