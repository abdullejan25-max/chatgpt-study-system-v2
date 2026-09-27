# P12 Host Compatibility Checkpoint

Checked: 2026-09-27. This checkpoint combines official product documentation with a synthetic, host-neutral stdio process test; it does not inspect local host configuration or prove an active connection.

| Host | Officially documented MCP client capability | Evidence | Local P12 state |
|---|---|---|---|
| WorkBuddy | The official MCP guide documents a local stdio server using `command`, `args`, and `env`, and describes UI-based server configuration and status. | [WorkBuddy MCP guide](https://www.workbuddy.ai/docs/zh/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/MCP-Guide) | Application is installed, but no user MCP config was read or changed; no Gateway call or E2E is verified. |
| Hermes Agent | The official user guide documents local stdio MCP servers and the `mcp_servers` configuration with `command`, `args`, and `env`. | [Hermes MCP guide](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/mcp.md) | Application is installed, but no user MCP config was read or changed; no Gateway call or E2E is verified. |

## Interpretation

- Documentation establishes that both products describe a local stdio MCP client path. It does not establish compatibility with this repository's Gateway build, its Windows process launch, or private local settings.
- A synthetic repository test now starts the Gateway as a separate stdio subprocess and uses an independent MCP SDK client to verify that `projection_snapshot` is hidden with only `read`, then visible with the explicit `projection` capability and marked read-only while serving `begin` → `sources` → `records`; the focused process/History/Wrong Answer MCP set reports **24 passed**. This validates the host-neutral process boundary only, not either installed product's configuration, UI, or real-host E2E.
- A second synthetic test now runs three independent MCP client sessions against separate Gateway subprocess lifetimes sharing one temporary SQLite store: client A writes version 1, client B reads/searches and appends version 2 with `expected_version`, then client A reconnects and reads the persisted successor. Both clients discover the same canonical workflow and tool set; caller identities remain explicitly reported/unverified. The parity test plus existing Wrong Answer MCP and stdio process suites report **5 passed**. This is cross-client protocol preparation, not a WorkBuddy/Hermes host pass.
- Existing repository support remains Codex Desktop and a stdio MCP client. No product-specific adapter is required by the documented protocol, but each host still needs an explicit configuration and a real tool invocation to pass its local gate.
- Do not copy configuration or credentials from another host, create an ad hoc override, or claim a Host PASS from documentation alone.
- Next real-host gate: with the owner present, add the Gateway through each product's supported settings, confirm the actual server status, invoke `health_report`, and perform the approved read-only E2E. Keep write tools disabled until separately authorized and reviewed.
