# ADR-006: Permission Model

状态：Accepted
日期：2026-09-25

## Context

模型提示和客户端确认不能作为本地数据授权边界。未来能力包括读取、草稿、提交和管理操作，风险差异很大。

## Decision

采用四级能力模型：

- R0 Read：最小只读返回、路径 allowlist、输入校验和审计。
- R1 Draft：只能写 V2 staging；不写权威数据根。
- R2 Commit：展示目标/diff/备份，使用与内容 hash 绑定且有时效的确认 token。
- R3 Admin：删除、覆盖、迁移、reset/reindex 等不进入普通 MCP tool list；默认关闭，仅限预定义 operator action。

任意 Shell 永远不作为通用工具。Phase 3 只实现 R0 的 `health_report` 和 `search_study`。

## Consequences

- 权限检查在 Gateway 服务端执行。
- tool annotations 只描述行为，不能替代授权。
- 后续新增工具必须先确定风险级别、审计字段和回滚方式。
