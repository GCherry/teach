# User Knows HTTP APIs & CLIs, Questions Where MCP Differs From Plain APIs

The user builds Go services, CLIs, and HTTP REST+SSE endpoints (`GCherry/ytmix` `cmd/ytmix/` and `internal/ui/`) and has an MCP server in `ytmix/internal/mcp/`, but currently perceives MCP as redundant with a standard API. Lessons should skip basic HTTP/JSON-RPC syntax drills and focus on the host/client/server split, the three control models (`Tools`, `Resources`, `Prompts`), and the concrete architectural cons of MCP relative to REST APIs and CLIs.

## Evidence
- User stated: "I think I understand them but I feel like they are just API's. Where is the difference, where is the value, and what are the cons of using MCP."
- Inspected `GCherry/ytmix` (`cmd/ytmix/main.go`, `internal/ui/server.go`, `internal/mcp/{server,registry,capabilities,inspect,plan,render_jobs,resources_prompts}.go`), confirming all three interfaces wrap the same `internal/mixer` engine.

## Implications
- Anchor **Lesson 0001** in a three-way `ytmix` comparison (CLI vs. `internal/ui/` HTTP REST+SSE vs. `internal/mcp/` stdio MCP) to make discovery, schemas, and `Tools`/`Resources`/`Prompts` tangible.
- Anchor **Lesson 0002** in `ytmix/internal/mcp/` engineering constraints (context-window tax of 9 schemas, stdio process lifecycle, polling `get_render_status` vs. SSE `/api/render/{id}/events`, ID3 prompt injection, and advisory `ToolAnnotations`).
