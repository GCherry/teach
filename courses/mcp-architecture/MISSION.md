# Mission: MCP Architecture & Trade-Offs (vs. APIs and CLIs)

## Why
You have already shipped an MCP server in `GCherry/ytmix` (`internal/mcp/`), yet MCP can still feel like "just another API" wrapped in JSON. Understanding the exact architectural boundary between MCP, REST/HTTP APIs, and CLIs lets you decide cleanly when MCP earns its complexity—and when a plain HTTP endpoint or CLI flag is simpler, cheaper, and safer.

## Success looks like
- Explain the runtime, discovery, and control-model differences between an MCP server (`ytmix mcp`), an HTTP REST+SSE server (`ytmix ui`), and a CLI (`ytmix`).
- Map `ytmix`'s 3 MCP primitives—**Tools** (`plan_mix`, `start_render`), **Resources** (`ytmix://presets`, `ytmix://jobs/{id}`), and **Prompts** (`create-sleep-mix`)—to real agent orchestration value.
- Diagnose MCP's concrete failure modes and costs (upfront `tools/list` context tax, stateful stdio lifecycle, polling vs. SSE push, prompt injection via untrusted tool/ID3 outputs, and advisory `ToolAnnotations`).
- Score any new feature against a repeatable decision checklist before choosing MCP vs. REST API vs. CLI.

## Constraints
- Ground every concept in real code from `GCherry/ytmix` (`cmd/ytmix/`, `internal/ui/`, `internal/mcp/`) rather than abstract toy examples.
- Teach at an intermediate-to-senior Go/API developer pace while unpacking `ytmix/internal/mcp/` internals explicitly.
- Keep Lessons short, self-contained, and retrieval-focused with printable Reference Sheets.

## Out of scope
- Writing a new MCP client/host runtime from scratch or deploying remote OAuth-authenticated Streamable HTTP MCP clusters in production.
- Deep FFmpeg audio/video rendering mechanics inside `ytmix` (covered only where they shape `plan_mix`, `start_render`, or streaming trade-offs).
