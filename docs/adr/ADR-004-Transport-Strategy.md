# ADR-004: Transport Strategy

状态：Accepted with capability gate
日期：2026-09-25

## Context

Codex local MCP、ChatGPT Plugin 和 Secure MCP Tunnel 是不同连接能力。官方文档对 Plus/Pro 的完整 MCP entitlement 描述不完全一致，不能把账号权限写入业务架构假设。

## Decision

Core/Services 与 Local Gateway 使用 transport-neutral Python contracts，不导入 MCP SDK 或具体 transport。Phase 3 已通过 Codex host 直接启动 stdio MCP；当前运行时继续使用该 transport。

远程 MCP transport 与 Secure MCP Tunnel 属于未来 non-Core 集成，不在当前运行时或 Phase 4–9 Core 实施范围。若未来为 ChatGPT 接入私有本机 MCP，必须单独验证账号能力与部署方式；任何 transport 都不能改变 Gateway 授权规则，也不能让 Core 依赖网络连接。

Plus 账号的 Developer Mode、custom Plugin、完整读写 MCP 与 tunnel 权限全部标记为账号实测项。不可用时不判定 Gateway 失败。

## Consequences

- stdio 与直接测试共用同一 Gateway；未来 transport 也必须复用该边界。
- Phase 3 不建公网 endpoint，不开放入站端口。
- ChatGPT capability report 与代码验收分开保存。

## Official sources

- [Codex 与本地 MCP](https://learn.chatgpt.com/docs/extend/mcp)
- [ChatGPT Plugin 连接](https://developers.openai.com/plugins/deploy/connect-chatgpt)
- [Secure MCP Tunnel](https://developers.openai.com/api/docs/guides/secure-mcp-tunnels)
