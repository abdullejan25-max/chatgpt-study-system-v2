# ADR-005: Memory Layers

状态：Accepted
日期：2026-09-25

## Context

V1 的 ChatGPT/WorkBuddy Native Memory、Basic Memory、StudyVault/QMD 和 Archive 职责重叠。Basic Memory 有真实数据价值，但 scope 和索引健康尚不适合作为永久承诺。

## Decision

- ChatGPT Memory：稳定偏好和协作方式。
- Personal History：可追溯的个人/学习历史，通过可替换 `HistoryBackend` 访问。
- Study Knowledge Base：StudyVault 中的教材、错题和学习笔记，通过 `StudyBackend` 访问。
- Archive：原始证据来源，不自动提升为 durable profile。

Basic Memory 是可能的 `HistoryBackend` adapter，不进入 Core contract。Phase 3 使用 `NotConfiguredHistoryBackend`，不迁移、不查询真实 history。

## Consequences

- 更换 Basic Memory 不影响 MCP tool contract。
- Study 资料不会混入 Personal History。
- 普通聊天不会由 Gateway 自动归档或提炼。
