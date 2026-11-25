# Teaching Notes & User Preferences

- **Learner baseline:** Intermediate-to-senior Go and HTTP API developer. Skip introductory explanations of JSON, HTTP verbs, or CLI flags; focus on protocol boundaries, LLM-client ergonomics, and architectural trade-offs.
- **Concrete anchor:** Use `GCherry/ytmix` (`cmd/ytmix/` CLI, `internal/ui/` HTTP REST+SSE, `internal/mcp/` stdio JSON-RPC 2.0) as the running case study, unpacking `internal/mcp/` explicitly without assuming memorized internals.
- **Course format:** Two tightly scoped **Lessons** (`0001` Difference & Value; `0002` Cons, Costs & Decision Framework) paired with two printable **Reference Sheets** (`0001` Comparison Matrix + `ytmix` Primitives Map; `0002` Decision Scorecard & Failure Checklist).
- **Initial misconception to address:** "MCP feels like just another API." Lesson 0001 directly contrasts *API for deterministic software callers* vs. *standardized discovery/control contract for non-deterministic LLM hosts*, while Lesson 0002 validates where that intuition is *right* (when MCP adds unnecessary ceremony over a CLI or REST API).
