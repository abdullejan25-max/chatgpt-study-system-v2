# Provenance & P1–P9 System Audit Report

日期：2026-09-26

## 审查基线

- Checkout：本轮指定的 `chatgpt-study-system-v2` 项目目录（报告不保存本机绝对路径）。
- 初始 HEAD：`928fdf1479c41d1088ae846001573cf9b0ceffd0`，分支 `phase-3-readonly-mcp-spike`。Phase 7–9 代码、测试与 checkpoint 已存在于该提交所含的仓库状态中；没有发现被遗漏的后续提交或其他本地分支。
- 初始工作区有一个已有未跟踪目录 `docs/superpowers/plans/2026-09-25-phase-4-9.md`，本轮保留未改。
- 初始完整回归：`280 passed, 5 skipped`。

## 统一 provenance 设计

各本地 SQLite 库使用同一 schema 的 append-only `write_provenance` ledger；领域表继续保留 History、Asset/Document、Wrong Answer 各自的语义。每个领域迁移用 scoped `schema_migrations` 版本标记幂等回填旧数据，不重写旧内容，也不伪造历史身份。provenance 和对应记录在同一个本地 SQLite 事务内提交，独立的 `operation_audit` 仍记录操作结果。

Ledger 记录 `record_type`、逻辑 `record_id`、`version`、`data_origin`、`actor_type`、`identity_trust`、报告身份/session、逻辑 `source_refs`、Gateway UTC `recorded_at`、前一 provenance ID，以及导入系统、原始时间、导入时间和 batch ID。新 provenance 行由 SQLite triggers 禁止 UPDATE/DELETE。

| 数据 | 来源类型 | 写入时间与来源 |
|---|---|---|
| 原始 Asset / Wrong Answer source | `source` | Gateway 写入 UTC 时间；引用原始 `asset://` 或 `document://`；原始 Source 记录不因分析而改写 |
| 文档及文本/OCR 页 | `deterministic_derived` | 引用原始 Asset；OCR 对同一页追加 provenance 版本，链接上一版 |
| Wrong Answer Analysis | `agent_generated` | Gateway UTC 时间、已校验的 Asset/Document refs；每个分析正文保留为 append-only 行并链接前一版本 |
| History 导入记录 | `imported` | 保留源 `created_at`，另存 Gateway `imported_at`、`source_system` 标签、batch ID 和 History source ref |
| 旧数据库行 | 依领域类型 | 迁移状态 `pre_provenance`；历史 Agent/client 与不明导入字段留空 |

`reported_agent`、`reported_client`、`run_id` 是可选 MCP 写入 envelope。它们只标为 `reported`，不作为认证，也不决定 capability。没有报告身份时标为 `unavailable`。Gateway/runtime 生成写入时间；caller 不得提交任意时间、origin 或版本号。

## P1–P9 跨阶段审查范围

审查了架构和 ADR、Phase 1–9 checkpoints、运行时依赖和模型扫描、Gateway 与 stdio MCP schemas/handlers/resources、SQLite schema 和 migration、权限 capability、History/Asset/Document/Wrong Answer adapters、事务与回滚、audit、logical URI/dedupe、path/privacy 边界、独立 MCP client 和 Host E2E 测试边界。

Single-Brain 仍成立：runtime 只有确定性操作，没有 model/provider SDK 或生成 API；OCR/PDF/QMD/SQLite 是本地或确定性处理。学习分析只由 Agent 提供。Study、History、原始 Documents/Assets、派生页和错题源/分析仍分离。Gateway read/write/ingest 权限在 tool discovery 和 Gateway operation 两处执行。路径输入仍在显式 root 内验证，外部输出进行本地路径清理；Asset/Document 批次、History 导入、Wrong Answer 写入与 audit 使用本地事务。重复导入保留 content-addressed ID；错题来源不可变，分析以 optimistic version 和 idempotency key 追加。

## 本轮发现和处理

1. Wrong Answer 版本号存在，但没有显式前一版本标识；报告身份、session/client 字段缺失。已在分析响应、MCP envelope 和 ledger 中加入明确的 `supersedes_analysis_id` / provenance 链与报告身份字段，保留旧分析正文和幂等重放。
2. History `created_at` 是来源事件时间，未表示实际导入时间。已新增原始时间与导入时间分离、导入系统标签、batch ID、History source 逻辑引用和导入状态；未添加 Agent-facing History import MCP capability。
3. Documents 的原始 Asset、确定性文档页和 OCR continuation 在领域字段中虽可区分，但无共同持久化 provenance。已加入资产/文档/派生页 provenance；OCR 页每次更新追加一版并 supersede 前版 provenance，原始 Asset 保持 source 类型。
4. MCP typed tools 与 resources 的来源元数据不一致。已将 provenance 回传到 page/image/asset resource metadata 与相应 typed tool 结果。
5. 旧数据库需要兼容迁移。已加按领域 scope 的 idempotent migration；未知旧身份保持空，老记录明确标记 `pre_provenance`。
6. History backend 可替换，但新增加的 provenance/import 字段原先没有经过 Gateway 结构校验。已加入 logical ID、时间、origin、引用和 identity trust 检查，避免替代 backend 将伪造的路径或身份元数据泄漏到 MCP 响应。

## 未解决限制 / 后续 gate

- OCR 派生页旧文本仍会被当前页表替换；provenance 保留时间、source 和 supersedes 链，但没有历史文本归档读取 API。旧错题分析正文不受此限制，仍完整保留。
- 本地 capability 是进程级权限，不是多 Agent 身份认证/授权。外部身份是 caller-reported；不应将本地 stdio capability 配置用于不受信任的共享 remote transport。
- 各 SQLite 数据库各自原子提交，History 与 Asset/Document 之间没有分布式事务。
- Tesseract/PyMuPDF 可选 OCR 环境和授权边界仍是 Phase 6 已记录限制；本轮没有重新运行整本教材 OCR。
- 不做真实 JPG E2E，所以 readiness 只说明本地 Gateway/MCP/DB 合同具备进入受控真实 JPG E2E 的条件，不表示已验证真实图片质量、识别准确度或真实数据迁移。

## 真实 JPG Wrong Answer E2E 条件评估

核心链路已具备：MCP 可读取原始 Asset bytes；Gateway 可存储 JPG/PNG 原件并保留 source 标记；Agent 可自行查看图像、提交用户确认的问题/答案；分析写入要求实际存在的 Asset/Document refs 和 Study 逻辑引用；版本、可信时间 provenance、audit、权限和回滚均有合成覆盖。教材检索仍可选参考材料，未要求整本 OCR。

因此，在下一轮单独授权真实 JPG E2E、继续使用本地私有 store 且不迁移整库的前提下，判定：

**READY FOR REAL WRONG-ANSWER E2E**

此判定不授权本轮执行真实 JPG 测试，也不代表多 Agent 的 reported identity 已通过认证。

## 测试

- Baseline full regression（实现前）：`280 passed, 5 skipped`。
- Provenance/History/Documents/Wrong Answers/MCP/capability targeted regression：`148 passed, 1 skipped`。
- Full regression：`293 passed, 5 skipped`。Skips 为 Codex Host opt-in、Windows junction/symlink host restrictions、受保护真实 QMD smoke opt-in。
