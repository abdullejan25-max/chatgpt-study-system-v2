# ADR-009：统一写入 Provenance

状态：Accepted

日期：2026-09-26

## 背景

Phase 7 的错题分析已有追加版本，但调用者信息仅有宽泛的 `agent_supplied` 标记。History 的 `created_at` 表示源记录发生时间，缺少 Gateway 实际导入时间和导入批次。资产、文档、OCR 派生页和 History 使用不同 SQLite 数据库或表，原有 audit 只描述操作结果，无法统一查询来源与版本。

## 决策

- 每个本地 SQLite 数据库使用同一逻辑结构的 append-only `write_provenance` 表；记录与所在数据库的领域数据在同一事务提交。
- 领域表继续承担自己的语义：原始 Asset/History source 不与派生页或 Agent 分析合并；Wrong Answer Analysis 继续以版本行追加保存。
- `data_origin` 区分 `source`、`deterministic_derived`、`agent_generated`、`imported`、`system_generated`。`actor_type` 描述写入通道为 `external_client`、`importer`、`system` 或 `unknown`，不声称完成了个人身份认证。迁移数据没有可靠 actor 信息时标记为 `unknown`。
- Gateway/runtime 生成 UTC `recorded_at`。History 的原始事件时间保留在 `original_created_at` / `created_at`；实际导入时间、报告的来源系统和 batch ID 独立记录。
- MCP 可选接受 `reported_agent`、`reported_client`、`run_id`。存储层将其标记为 `reported`；没有提供时标记 `unavailable`。不接受调用方自报时间、origin、actor type 或版本。
- 每个新错题分析版本记录前一版本的分析 ID 和 provenance ID；乐观并发检查与幂等请求仍有效。每次 OCR 页更新追加页 provenance 版本并引用文档及原始 Asset。
- 旧数据不重写。迁移以 `pre_provenance` 标记既有记录，能安全识别的源时间保留为原始时间，不补造历史 Agent/client 身份。
- Provenance 只存逻辑 ID 和元数据，不存题目正文、原始图像、绝对路径或凭证。已有 `operation_audit` 继续记录事务成功操作，不与 provenance 混为一张表。

## 后果和限制

- History 与 Asset/Document 数据库位于不同本地 SQLite 文件，无法提供跨库原子事务；每个数据库内部原子提交。
- 当前 MCP 本地 capability 是 Gateway 进程级配置，不是按 Agent 身份隔离的认证授权。报告身份用于审计上下文，不用于授予权限。
- OCR 页的旧版文本尚未归档为可经 Gateway 读取的历史内容；provenance 链能显示更新时间、版本与来源，但不恢复被 OCR 替换的派生文本。此限制不影响 Wrong Answer Analysis 的旧版本正文，后者是 append-only。
- History `source_system` 是导入程序提供的标签，不是经过验证的来源系统凭据。
- 迁移在各库首次执行写路径时幂等升级；纯只读启动不会悄悄改数据库。

## 验证

合成测试覆盖 schema 升级、重复迁移、append-only 约束、可信 UTC 时间、source refs、身份信任状态、History 原始时间与导入时间、错题版本链、MCP tool/resource metadata、权限、回滚和 idempotency。完整结果记录在 [`P1-P9 System Audit`](../p1-p9-system-audit.md)。
