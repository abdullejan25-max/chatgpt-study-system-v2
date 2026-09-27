# Project Agent Guidance

When handling a wrong-answer request in this repository, use the `study_system` MCP server and its canonical `study-workflow://wrong-answer` workflow. Do not duplicate the workflow rules here.

If the MCP server is unavailable, first verify that this exact repository is open in Codex and that Codex has trusted the project so its `.codex/config.toml` is loaded. Do not replace the unavailable Gateway with direct database writes or temporary inline MCP overrides.

Use the formal Gateway/MCP tools for persisted changes. Explain clearly when a requested action cannot proceed because the local private Gateway configuration or capabilities are not enabled.
