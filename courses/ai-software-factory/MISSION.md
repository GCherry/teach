# Mission: AI Software Factory Architecture, Observability & Governance

## Why
Upgrade `chill-hq` from a multi-agent workflow control plane into an observable, model-agnostic software factory, and build an executive-ready AI Software Factory & Governance architecture pitch for engineering leadership at work.

## Success looks like
- Architect a harness- and provider-agnostic **AI Gateway + Telemetry Control Plane** spanning Google Antigravity, Claude Code subscriptions, metered LLM APIs, and local models (Ollama / vLLM).
- Design a **Token-to-PR Observability Pipeline** joining usage telemetry (tokens, credits, cache hit rates, active users) with SDLC outcomes (PR throughput, Cost per Merged PR, review rounds, revert rate).
- Define concrete, agent-ready GitHub issues for `GCherry/chill-hq` to wire telemetry and gateway hooks into Coordinator v2 (`Planner`, `Engineering`, `Reviewer`, `Docs`, `Release`, `Retro`).
- Produce a **Leadership RFC / Pitch Blueprint** covering the 6 Factory Planes, per-user credit governance, and a phased rollout (`Crawl → Walk → Run → Fly`).

## Constraints
- Must remain **harness-agnostic** (Antigravity now, Claude Code subscription next, headless CI workers later) and **model-agnostic** (frontier APIs + local models).
- Must account for the architectural split between **subscription-authenticated harnesses** (flat-rate OAuth seats) and **API/local endpoints** (virtual-key metered routing).
- Keep all teaching state isolated in `learning/ai-software-factory/` until insights are ready to file as `chill-hq` GitHub issues or promote to `wiki/`.

## Out of scope
- Training or fine-tuning custom foundation models.
- Single-vendor lock-in architectures that exclude local models or multiple coding CLIs/IDEs.
