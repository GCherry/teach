# AI Software Factory Resources

## Knowledge

- [Article Series: "Minions: Stripe's one-shot, end-to-end coding agents" by Alistair Gray (Stripe Dev Blog)](https://stripe.dev/blog)
  Primary enterprise case study on running unattended coding agents at 1,300+ merged PRs/week using isolated cloud devboxes, an MCP "Toolshed", interleaved deterministic/LLM blueprints, and human merge gates. Use for: executive storytelling and designing Plane 2 (Execution) and Plane 5 (Verification).
- [Manifesto & Repo: StrongDM AI Team — "Software Factory" & Attractor](https://factory.strongdm.ai/) ([GitHub: strongdm/attractor](https://github.com/strongdm/attractor))
  Primary source on the "Dark Factory" model, specification-driven agent loops, holdout scenario validation, and Digital Twin test environments. Use for: contrasting human-reviewed factories against zero-human-review validation patterns.
- [Docs: LiteLLM Proxy — Virtual Keys & User/Team Budgets](https://docs.litellm.ai/docs/proxy/virtual_keys) ([Users & Budgets](https://docs.litellm.ai/docs/proxy/users))
  Open-source AI gateway reference for enforcing per-user `max_budget`, TPM/RPM limits, `User-Agent` coding-tool tracking, and unified routing across commercial APIs and local Ollama/vLLM models. Use for: designing Plane 4 (AI Gateway & FinOps).
- [Spec: OpenTelemetry — GenAI Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/)
  Vendor-neutral telemetry schema (`gen_ai.system`, `gen_ai.request.model`, `gen_ai.usage.input_tokens`, `gen_ai.usage.output_tokens`) for unifying spans and metrics across gateways and agent harnesses. Use for: defining a canonical cross-tool event schema.
- [Docs: Claude Code Monitoring & OpenTelemetry](https://claude-code.mintlify.site)
  Official configuration reference for exporting token, cost, and tool telemetry from Claude Code (`CLAUDE_CODE_ENABLE_TELEMETRY=1`) even on flat-rate subscription seats. Use for: Path 2 subscription observability.
- [Research: DORA — AI Capabilities & Software Delivery](https://dora.dev/research/ai/)
  Empirical research pairing PR throughput metrics with stability counter-metrics (change failure rate, rework/churn, review bottlenecks). Use for: designing leadership KPIs in Plane 6.

## Wisdom (Communities)

- [Latent Space / AI Engineer Community](https://www.latent.space/)
  High-signal practitioner discussions and conference talks on agent harnesses, context engineering, and enterprise AI gateways. Use for: real-world trade-offs when adopting coding agents across teams.
- [CNCF OpenTelemetry GenAI Working Group](https://opentelemetry.io/blog/2024/otel-generative-ai/)
  Practitioner community standardizing LLM and agent observability conventions. Use for: keeping custom telemetry aligned with emerging vendor-neutral standards.

## Gaps

- Standardized cross-harness correlation between local session transcripts (e.g., Google Antigravity `transcript.jsonl`, Claude Code OTel events) and GitHub PR webhooks without custom repo hooks or attribution headers.
