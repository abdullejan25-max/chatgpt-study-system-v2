# ADR-003: Local Gateway Boundary

状态：Accepted
日期：2026-09-25

## Context

Gateway 接触本机私有资料，必须成为安全边界，但不能发展成第二个 Agent。

## Decision

Gateway 提供稳定 contract、schema validation、路径 allowlist、permission policy、adapter 调用、结果裁剪、审计和错误码。业务 core 不依赖 MCP、QMD 或 Basic Memory 的具体协议。

Gateway 不提供任意 Shell、任意路径、动态 executable、自动持久化、自动 reindex/reset、学习规划或 LLM routing。

`health_report` 必须是纯读探测：不创建文件/目录/数据库/日志，不启动子进程。`search_study` 只能运行固定 `qmd search`，固定 collection，`shell=False`。

## Consequences

- 所有 host 共用同一安全策略。
- adapter 可以替换而不改 tool contract。
- 少量显式工具优先于通用“执行命令”工具。
