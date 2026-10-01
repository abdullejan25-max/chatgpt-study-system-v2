# P12 Host Compatibility Checkpoint

Checked: 2026-09-27. This checkpoint combines official product documentation with a synthetic, host-neutral stdio process test; it does not inspect local host configuration or prove an active connection.

| Host | Officially documented MCP client capability | Evidence | Local P12 state |
|---|---|---|---|
| WorkBuddy | The official MCP guide documents a local stdio server using `command`, `args`, and `env`, and describes UI-based server configuration and status. | [WorkBuddy MCP guide](https://www.workbuddy.ai/docs/zh/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/MCP-Guide) | Application is installed, but no user MCP config was read or changed; no Gateway call or E2E is verified. |
| Hermes Agent | The official user guide documents local stdio MCP servers and the `mcp_servers` configuration with `command`, `args`, and `env`. | [Hermes MCP guide](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/mcp.md) | Application is installed, but no user MCP config was read or changed; no Gateway call or E2E is verified. |

## Interpretation

2026-10-01 Hermes Step 3 已开始：v0.20.0 (2026.8.3) native stdio discovery/health
可用，生产只读 config 已持久保存；模型服务 TLS/403 故障阻塞真实 Agent E2E。
下列早期调查表是历史快照，当前证据见 [Hermes checkpoint](p12-step3-hermes-checkpoint.md)
与 [Host setup](hermes-host-setup.md)。尚无 Hermes v0.5.0 release。

- Documentation establishes that both products describe a local stdio MCP client path. It does not establish compatibility with this repository's Gateway build, its Windows process launch, or private local settings.
- A synthetic repository test now starts the Gateway as a separate stdio subprocess and uses an independent MCP SDK client to verify that `projection_snapshot` is hidden with only `read`, then visible with the explicit `projection` capability and marked read-only while serving `begin` → `sources` → `records`; the focused process/History/Wrong Answer MCP set reports **24 passed**. This validates the host-neutral process boundary only, not either installed product's configuration, UI, or real-host E2E.
- A second synthetic test now runs three independent MCP client sessions against separate Gateway subprocess lifetimes sharing one temporary SQLite store: client A writes version 1, client B reads/searches and appends version 2 with `expected_version`, an identical idempotency replay returns version 2, and a new stale-version write conflicts; client A reconnects and reads exactly versions 1 and 2. Both clients discover the same canonical workflow and tool set; caller identities remain explicitly reported/unverified. The parity test plus existing Wrong Answer MCP and stdio process suites report **5 passed**. This is cross-client protocol preparation, not a WorkBuddy/Hermes host pass.
- Existing repository support remains Codex Desktop and a stdio MCP client. No product-specific adapter is required by the documented protocol, but each host still needs an explicit configuration and a real tool invocation to pass its local gate.
- Do not copy configuration or credentials from another host, create an ad hoc override, or claim a Host PASS from documentation alone.
- Next real-host gate: with the owner present, add the Gateway through each product's supported settings, confirm the actual server status, invoke `health_report`, and perform the approved read-only E2E. Keep write tools disabled until separately authorized and reviewed.

## WorkBuddy Step 2 superseding checkpoint (2026-10-01)

The WorkBuddy preparation-only row above is historical. Real WorkBuddy 5.6.2
read-only/write/restart acceptance is now owner-verified, with Gateway and
isolated Projection corroboration. Gate PASS, included in v0.4.0. No Hermes
acceptance is implied. See [Step 2](p12-step2-workbuddy-checkpoint.md) for
Gateway-only rule correction, same-name Host resolution limits, distinct
isolated server, evidence levels and final package/privacy audits.
