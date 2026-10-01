# P13 — History Completion & Normalization checkpoint

日期：2026-10-01。起点：**v0.6.0 / 02d1ed2**。
当前状态：**Phase A PARTIAL；Phase B BLOCKED；Phase C–E NOT_STARTED**。
这是持续推进 checkpoint，不是 P13 完成报告，也不是 v0.7.0 release。

## 当前已取得的证据

在独立 worktree 上完成基线验证，没有重复 P11/P12 的 Host/E2E 验收。
有界 inventory 只访问已知历史输入根和官方导出位置；配置中的 V2 Study/History/Assets
目标根被显式保护。没有打开 V2 DB/store，也没有启动生产直接客户端作为 MCP 替代。

本轮 private acquisition manifest 包含 13 个 scope。登记 **1,323 个不同内容输入**，
合计 **486,424,742 bytes**；同类别相同字节以内容指纹识别，所有获取位置保留。
这些是文件级输入数量，不是 V2 sources、conversations 或 canonical messages。

| 来源类别 | 文件级输入 | 当前状态 |
| --- | ---: | --- |
| Codex 当前及 archived JSONL | 119 | 81 个输入与已有 Gateway source 的 SHA-256/byte count 完全相同；其余 38 个尚无 exact-byte mapping |
| WorkBuddy | 778 | 390 archive、368 session metadata、20 storage 文件；metadata 不冒充对话 |
| Hermes | 67 | 44 runtime/session dump、23 official export packets（含 export manifest） |
| Basic Memory 旧 archive | 359 | 已知两个 legacy 输入根，Markdown 先保留 source-only |
| ChatGPT | 未取得 | 已检查有界本地候选位置；等待官方导出或用户提供已有位置 |
| Gemini | 未取得 | 同上；不套用 ChatGPT parser |
| existing V2 source layer | 166 | 正式 Gateway 回读：82 Codex、55 legacy Markdown、28 legacy Wrong Answer document、1 derived fact |
| V1 原始/冷备份位置 | REVIEW_REQUIRED | 尚未核实精确位置；不能据历史 cutover 结论宣布 unique-data Gate PASS |

按格式：432 JSON、488 JSONL、403 Markdown。确定性结构 probe 的结果为
918 parsed、2 malformed、403 unsupported。这里 parsed 只代表有界结构检查；
unsupported 表示本轮未对 Markdown 做结构解析，不代表丢弃或无需 source-only 导入。
2 个 malformed 文件的原始指纹和获取位置仍在 ledger，没有修复或删除原文。

第一轮获取无 I/O error，未观察到同类别字节完全相同的不同位置副本。
不能据此声称不存在跨格式 semantic duplicate；本轮不做语义合并。
23 个固定 Hermes 官方获取文件重跑为 **0 new source / 0 new location**。
活跃 session 会继续增长；文件版本变化不能混称逻辑重复或完整静态快照。

## Private ledger 与恢复

ledger、原始 exports、获取位置、内容指纹、日志及 recovery receipts 全在 Git 外。
通用代码复用已有 verified file reader/private path 保护，并拒绝其它 Git checkout、
reparse/hardlink aliases、credential 输入及受保护 V2 target。

ledger schema v2 的首次发现和结构 disposition 原子提交；可补齐旧 discovered 中断点。
获取位置、原始文件内容指纹、probe version、结构质量与 nullable source time 保留。
错误与解决事件 append-only，当前未解决错误与历史失败分别计数。
导入/复用状态要求 Gateway receipt identity/digest 元数据；本轮没有登记 imported/reused，
也没有以 ledger 代替生产 V2 状态。recorded_at 是获取/记账时间，不能冒充 occurred_at。

私有 v1→v2 ledger upgrade 保留全部 1,323 项；固定输入重跑没有新增 source。
own-ledger backup checksum、独立 restore target 与聚合比较通过，原 snapshot 未改变。
**这是 migration ledger 恢复 smoke，不是 V2 backup/restore Gate。**

## 实际阻塞与顺序

初次会话直接读取已知 workflow URI 返回 `unknown MCP server 'study_system'`；本轮已不再复现。
当前 worktree 的 ignored local config 保留既有后端/权限，`enabled=true`、`required=true`，
cwd、project 与 local config 参数均指向当前 checkout。已自主增加此 worktree 的显式
`trusted` 记录，用户级其它配置和 MCP 定义未改变；重新读取配置未出现 untrusted warning。
此前主 checkout 已 trusted，linked worktree 也已能加载其项目配置，缺少独立 trust entry
不能单独证明项目未受信任。

当前 Desktop 日志有本会话的 `study_system status=ready`，实际 Host 子进程参数指向
当前 worktree。正式 workflow 读取、两次 native `health_report` 均成功：Gateway 0.6.0，
History `sqlite / ready`，Study configured/readable，QMD discoverable。MCP 已解除阻塞，
不要求用户中继、手工重载或另开直接客户端。

正式 `list_legacy_sources` 与 9 页 metadata snapshot 均取得 166 个不同 source record；
逐条 bounded fetch 仅取 1 byte，以获取 source hash/provenance 元数据，原内容未进入回执。
81 个 Codex input 与现存 source 的 hash/byte count 匹配；没有匹配的 38 个 input
**不等于 38 条漏导入对话**，仍需稳定 source identity 与版本对账，不能自动重复导入。
所有 destination metadata、映射及 Host 日志证据只保存 Git 外，本轮未修改 production。
`list_history_sources` 返回空 registered-source list，不能将其混同于 legacy source 数量。
source 与 History 的合成 no-result 查询均 `ok=true / total=0`；这是当前读取验证，
不是尚未实施的 canonical normalization 验收。

官方来源下载只需用户一次性获取整包，不要求逐条复制聊天，不上传到本项目/GitHub：

- [ChatGPT 官方导出](https://help.openai.com/en/articles/7260999-exporting-your-chatgpt-history-and-data)。
- [Gemini 官方导出](https://support.google.com/gemini/answer/16920332?hl=en)：
  My Activity → Gemini Apps 包含聊天/生成媒体/上传；只选 Gemini 主要是 Gems。
- [Hermes 官方 session export](https://hermes-agent.nousresearch.com/docs/user-guide/sessions/)：
  JSONL live context 与 Markdown full-display archive 分别获取，避免遗漏 compaction archives。

source-only completion 未通过前，不设计 canonical schema、不执行 normalization，
不审计/修改 V1 runtime，不执行物理删除。没有版本 bump、tag、push 或 Release。

## P13 Gate

| # | Gate | 状态 | 证据 / 尚需完成 |
| --- | --- | --- | --- |
| 1 | Legacy Inventory | PARTIAL | 13 scopes / 1,323 文件；官方导出、V2 对账及 V1 原始位置待核实 |
| 2 | Private Migration Ledger | PARTIAL | 获取/失败/恢复已实跑；import destination/provenance 待正式写入与回读 |
| 3 | ChatGPT Source Import | WAITING | 需要 official export 或已有本地位置 |
| 4 | Gemini Source Import | WAITING | 需要 official export 或已有本地位置 |
| 5 | WorkBuddy Source Import | NOT_STARTED | archive 与 runtime metadata 已区分；未写生产 |
| 6 | Hermes Source Import | NOT_STARTED | 官方获取文件已保存 Git 外；未写生产 |
| 7 | Codex Reconciliation | PARTIAL | 119 inputs；81 exact-byte mappings；其余 input 的稳定 identity/版本尚未完成对账 |
| 8 | V1 Legacy Reconciliation | PARTIAL | Gateway 已有 84 个 V1-derived source records；原始/冷备份位置与全集尚待核实 |
| 9 | Source Dedup | PARTIAL | inventory exact-byte identity；生产 reuse 与 semantic candidates 待 Phase B |
| 10 | Idempotent Import | NOT_STARTED | inventory 固定文件重跑 0 new；不能替代 import 幂等 |
| 11 | Source Preservation | PARTIAL | 获取输入未改写，原指纹/错误保留；V2 source persistence 待验收 |
| 12 | Canonical Schema | NOT_STARTED | source-only Gate 通过后才设计 |
| 13 | Deterministic Normalization | NOT_STARTED | 同上 |
| 14 | Ambiguity Guard | NOT_STARTED | probe 不猜角色/时间/边界；canonical guard 尚未实现 |
| 15 | Timestamp Semantics | PARTIAL | source time 与获取 recorded_at 分开，未知不填 mtime |
| 16 | Ordering Semantics | NOT_STARTED | 未生成 canonical 顺序 |
| 17 | Attachment Mapping | NOT_STARTED | 未 ingest/伪造任何历史 attachment |
| 18 | Canonical Provenance | NOT_STARTED | 尚无 canonical records |
| 19 | Normalization Idempotency | NOT_STARTED | 尚未 normalization |
| 20 | Cross-source Reconciliation | PARTIAL | 166 existing destination metadata 与私有输入已比较；完整 source-only 对账未完成 |
| 21 | Production Gateway Readback | PARTIAL | 当前 native health/list/snapshot/fetch 通过；迁移完成后的回读仍待 Phase B–D |
| 22 | Cross-Agent History Read | NOT_STARTED | normalization 后最小 read E2E，不重跑 P12 |
| 23 | No-result | PARTIAL | 当前 legacy source / History 合成查询均 total=0；canonical 与跨 Agent 读取尚未执行 |
| 24 | Privacy | PARTIAL | Phase A 排除测试/包扫描通过；P13 后续真实执行与发布仍须重新审计 |
| 25 | Regression | PARTIAL | Phase A targeted 50 passed；full 672 passed / 12 skipped；后续 normalization 未实现 |
| 26 | Recovery Backup | NOT_STARTED | own-ledger smoke 通过；V2 backup 未执行 |
| 27 | Isolated Restore Smoke | NOT_STARTED | V2 isolated restore 未执行 |
| 28 | V1 Unique-data Audit | NOT_STARTED | 前置 Gate 未通过，不能宣布无 unique data |
| 29 | V1 Logical Retirement | NOT_STARTED | P13 retirement 不提前执行 |
| 30 | Documentation | PARTIAL | 当前 checkpoint 与 Phase A design/plan 已写；最终报告待所有 Gate |

Physical deletion 独立于自动 Gate；必须等待 owner 明确确认。

## Phase A 工程验证

独立 code review 的问题均有合成回归：中断时发现/解析状态原子提交、JSON 与嵌套
messages 全局上限、固定公开错误枚举、失败/解决事件历史保留、完整 schema 校验、
同秒小数时间范围，以及并发旧 ledger upgrade 不重复 seed。最终审查认可 LOCAL
Phase A commit，不是 production Gate 或 P13 release。

targeted 新增 50 passed；full 672 passed / 12 skipped。skip 仍是既有 opt-in Host/QMD、
Windows/POSIX 文件能力及 optional PyMuPDF 边界，不称已执行。
wheel/sdist 构建通过；完全人工构造的 private sentinels 未进入包。
45 个 wheel members、181 个 sdist members 的隐私扫描无受限材料/真实私人路径。
fresh wheel 在独立环境两次 synthetic CLI inventory 为 0 new on rerun，未访问 production。
公开代码及最终 Git candidate/object 审计单独记录在 Git 外工程回执。

## 接续

Gateway 已恢复；先完成 source-only 对账与 importer/adapter 实现，复用已有 P11 验证管线。
已登记真实输入保留在当前 private ledger，不从零重新建立迁移，也不重复制造 V2 source。
官方导出或 V1 路径补齐时增加显式 scope，再执行同一 inventory 工具。
