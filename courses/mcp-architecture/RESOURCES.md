# MCP Architecture Resources

## Knowledge

- [Spec: Model Context Protocol (`2025-06-18`)](https://modelcontextprotocol.io/specification/2025-06-18) — [Architecture](https://modelcontextprotocol.io/specification/2025-06-18/architecture), [Tools](https://modelcontextprotocol.io/specification/2025-06-18/server/tools), [Resources](https://modelcontextprotocol.io/specification/2025-06-18/server/resources), [Prompts](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts)
  Primary normative specification for Host/Client/Server roles, capability negotiation, JSON-RPC 2.0 framing, and the three server primitives (`Tools`, `Resources`, `Prompts`). Use for: verifying protocol rules, `ToolAnnotations` semantics, and control-model boundaries.
- [Spec: JSON-RPC 2.0](https://www.jsonrpc.org/specification)
  Transport-agnostic RPC framing spec underlying MCP (`jsonrpc: "2.0"`, request `id`, notifications without `id`, and `-32700` to `-32603` error codes). Use for: understanding `ytmix/internal/mcp/registry.go` message dispatch and error semantics.
- [Article: "Introducing the Model Context Protocol" (Anthropic)](https://www.anthropic.com/news/model-context-protocol)
  Original design motivation ("M×N integration problem" vs. standardized client/server contract). Use for: why MCP exists beyond wrapping a single REST endpoint.
- [Engineering Post: "Code execution with MCP: Building more efficient agents" (Anthropic)](https://www.anthropic.com/engineering/code-execution-with-mcp)
  Empirical engineering breakdown of MCP's two biggest scaling cons—upfront tool-definition context bloat and intermediate payload round-trips—and when code/CLI execution outperforms chat-turn tool loops. Use for: Lesson 0002 context-budget trade-offs.
- [Codebase Anchor: `GCherry/ytmix` (`cmd/ytmix/`, `internal/ui/`, `internal/mcp/`)](https://github.com/GCherry/ytmix/blob/main/internal/mcp/registry.go) — [MCP Server](https://github.com/GCherry/ytmix/blob/main/internal/mcp/server.go), [HTTP UI Server](https://github.com/GCherry/ytmix/blob/main/internal/ui/server.go), [CLI Entry](https://github.com/GCherry/ytmix/blob/main/cmd/ytmix/main.go)
  Production Go implementation exposing one FFmpeg/FFprobe audio-mix engine simultaneously as a CLI, an HTTP REST+SSE web studio, and a zero-dependency stdio MCP server (9 tools, 3 static + dynamic job resources, 2 prompts). Use for: concrete side-by-side comparisons across both Lessons.

## Wisdom (Communities)

- [Model Context Protocol GitHub Discussions](https://github.com/modelcontextprotocol/modelcontextprotocol/discussions)
  Official maintainer and implementer forum debating spec evolutions (Streamable HTTP, Tasks, authorization, and real-world client quirks). Use for: checking how clients actually interpret optional spec features like `ToolAnnotations`.
- [Latent Space / AI Engineer Community](https://www.latent.space/)
  Practitioner engineering discussions on agent tool design, MCP vs. CLI trade-offs, and context-window economics. Use for: real-world patterns on when teams strip MCP back to CLIs or thin APIs.
