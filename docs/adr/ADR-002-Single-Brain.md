# ADR-002: Single Brain

状态：Accepted
日期：2026-09-25

## Context

V1 同时存在模型 Rule、Python Router、WorkBuddy Native Memory 与多个检索层。重复推理会增加不可观测行为、延迟和冲突。

## Decision

ChatGPT/Codex 是唯一理解、教学、规划和工具选择层。Local Gateway 不使用 LLM，不分类用户意图，不重新规划，也不自动把聊天写入 durable memory。

Gateway 只执行明确的 typed operation：验证、授权、调用 adapter、标准化、审计和错误处理。

## Consequences

- 工具选择质量由 host 模型和清晰 tool metadata 决定。
- 本地行为可以确定性测试。
- 不建立独立 Memory Router。
- 若工具选择错误，应先改 tool contract/description 与 eval，而非添加第二个 LLM。
