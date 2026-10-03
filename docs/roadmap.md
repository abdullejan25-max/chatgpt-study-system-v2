# 项目路线图

> 历史路线图快照，内容截至 2026-09-30。此页中的 P12 `PREPARATION` 表示当时的阶段状态，之后的发布和验收已继续推进。当前正式版本、状态和限制以 [Current State](current-state.md) 为准。

```text
Phase 1：V1 审计 ✅
Phase 2：ChatGPT-first V2 架构 ✅
Phase 3：只读 MCP Spike ✅
Phase 4–9：Local Study Infrastructure ✅
Phase 10：GitHub Release Hardening ✅（v0.1.0）
Phase 11：V1 来源迁移与 V2 cutover ✅ PASS（v0.2.0）
Phase 12：Agent Projection & Interoperability ⏸ PREPARATION
```

P11 的版本范围是 V1→V2 来源迁移与 V2 cutover；全平台 canonical conversation/message History 统一属于后续扩展。该范围明确区分 V1 已有数据与尚未进入 V1 的外部平台数据，不能用未取得的 ChatGPT/Gemini 导出来声称 V1 数据已迁移，也不能让它们阻断独立完成的 V1 无损来源迁移。

P11 已执行真实领域写入、DB/WAL/blob snapshot、隔离 restore、hash/read-back、同源重跑、MCP retrieval E2E 和 restart persistence。Study 原地复用；旧聊天和错题保留为 typed source documents，Atomic Fact 保留为 derived fact，Codex 82 个来源文件保留为 source-only JSONL。完整错题语义及 canonical conversation normalization 的已知限制保持明确。逐项验收见 [P11 completion](p11-real-migration-completion.md)，V1 保留分类见 [Deletion candidates](v1-deletion-candidates.md)。

P12 保留现有 Obsidian renderer/writer/collector、投影能力、WorkBuddy/Hermes preparation 和跨客户端合成 harness；本任务未增加 P12 产品功能，也未声称其 Gate PASS。下一独立任务是在明确私有投影目标后完成真实 Obsidian GUI 与 WorkBuddy/Hermes 客户端 E2E。外部官方导出、canonical source normalization 和更高效 source index 分别以真实状态推进。

P1–P10 的历史验收见各阶段 checkpoint 与 [P10 Release Gate](p10-release-gate.md)。Secure MCP Tunnel / ChatGPT remote MCP 仍是非 Core 的可选 transport，不属于本地 P11 迁移条件。旧 tag、公开历史和 V1 原件均保持。
