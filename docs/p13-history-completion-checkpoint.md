# P13 — History Completion & Normalization checkpoint

日期：2026-10-02。起点：**v0.6.0 / 02d1ed2**。
当前状态：**已取得来源 Phase A/B PASS；Phase C 进入设计；Phase D/E NOT_STARTED**。
这是持续推进 checkpoint，不是 P13 完成报告，也不是 v0.7.0 release。

## 当前已取得的证据

在独立 worktree 上完成基线验证，没有重复 P11/P12 的 Host/E2E 验收。
有界 inventory 只访问已知历史输入根和官方导出位置；配置中的 V2 Study/History/Assets
目标根被显式保护。没有打开 V2 DB/store，也没有启动生产直接客户端作为 MCP 替代。

既有 Gemini/inventory/MCP/Gateway Gate 保留。沿明确 WorkBuddy transcript refs
增量取得 366 个实际 JSONL 文件，不重扫无关目录。V1 通过 P11 descriptor 与已知旧
项目定位：冷备份和旧项目 DB 的唯一 Memory 行全部字段相同，raw bytes 不同，分别保存。

私有 ledger 共 **1,692 unique fingerprints、1,694 acquisition locations、663,156,921 bytes**。
正式 Gateway source index **1,776 records**；包含对 166 既有 legacy records 的引用，
不复制旧 BLOB，Gemini 同样只引用原 bundle，不重新导入。全部 inputs 有 destination
和 native receipt digest；每条 evidence 至少两次成功校验，identity/provenance 稳定。

| 来源类别 | 唯一获取输入 | Gateway source index | 状态 |
| --- | ---: | ---: | --- |
| Codex | 119 | 120 | 既有历史版本全部对账；活跃文件旧前缀通过 byte count/hash proof |
| WorkBuddy | 1,143 | 1,143 | 既有 778 加 365 distinct referenced transcripts；366 路径含一个 exact copy |
| Hermes | 67 | 67 | runtime、official exports 与 manifest 分别保留 |
| Basic Memory legacy | 359 | 359 | Markdown source-only，结构不猜测 |
| V1 | 3 | 86 | 两份 raw DB、一个 staged fact；既有 V1 sources 引用复用 |
| Gemini | 1 | 1 | 150 members / 336 activities，不等于 canonical counts |
| ChatGPT | 未到达 | 0 | acquisition_pending；后续增量幂等补录 |

唯一输入格式：432 JSON、853 JSONL、403 Markdown、1 plain text、2 SQLite、1 ZIP。
2 个 acquired exact copies 复用；Gemini 包内 9 个相同字节 copies 仍原样保存。
一个 V1 DB pair 只登记 duplicate candidate，不作 semantic merge。
2 个 malformed records 原字节完整保存；source import errors=0，未解释 missing set=0。
没有无法恢复的旧登记版本。一个增长日志的 inventory cutoff 之后的活跃尾部明确延期，
旧前缀已恢复，原文件未截断；未来增量补录。ChatGPT pending 不阻止已取得来源推进。

## Private ledger 与恢复

ledger、原始 exports、获取位置、内容指纹、日志及 recovery receipts 全在 Git 外。
通用代码复用已有 verified file reader/private path 保护，并拒绝其它 Git checkout、
reparse/hardlink aliases、credential 输入及受保护 V2 target。

ledger schema v2 的首次发现和结构 disposition 原子提交；可补齐旧 discovered 中断点。
获取位置、原始文件内容指纹、probe version、结构质量与 nullable source time 保留。
错误与解决事件 append-only，当前未解决错误与历史失败分别计数。
导入/复用状态要求 Gateway receipt identity/digest 元数据；Gemini 已登记 imported/reused，
receipt 关联正式 Gateway 回读证据，不以 ledger 代替生产状态。公开 ledger 摘要仍保留
`gateway_current_state=unverified`，因为 ledger 本身不能验证 Gateway。
recorded_at 是获取/记账时间，不能冒充 occurred_at。

私有 v1→v2 ledger upgrade 保留全部 1,323 项；固定输入重跑没有新增 source。
own-ledger backup checksum、独立 restore target 与聚合比较通过，原 snapshot 未改变。
**这是 migration ledger 恢复 smoke，不是 V2 backup/restore Gate。**
Gemini 导入后另建 own-ledger snapshot，1,324 source counts/全部聚合字段的 isolated
restore 比较再次 PASS，backup checksum 未改变。

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
所有 destination metadata、映射及 Host 日志证据只保存 Git 外；此处记录的是既有
Gateway 恢复 Gate。后续 Gemini production writes 及回读另列如下。
`list_history_sources` 返回空 registered-source list，不能将其混同于 legacy source 数量。
source 与 History 的合成 no-result 查询均 `ok=true / total=0`；这是当前读取验证，
不是尚未实施的 canonical normalization 验收。

官方来源下载只需获取整包，不要求逐条复制聊天，不上传到本项目/GitHub：

- [ChatGPT 官方导出](https://help.openai.com/en/articles/7260999-exporting-your-chatgpt-history-and-data)。
- [Gemini 官方导出](https://support.google.com/gemini/answer/16920332?hl=en)：
  My Activity → Gemini Apps 包含聊天/生成媒体/上传；只选 Gemini 主要是 Gems。
- [Hermes 官方 session export](https://hermes-agent.nousresearch.com/docs/user-guide/sessions/)：
  JSONL live context 与 Markdown full-display archive 分别获取，避免遗漏 compaction archives。

ChatGPT 请求已提交，等待数据到达，不需重复申请；Gemini 包已取得并完成本轮处理。
已取得来源 source-only completion PASS，自动进入 deterministic normalization 设计。
V1 runtime/physical deletion 仍在 normalization、backup/restore Gate 之后。未 bump/tag/push/release。

## P13 Gate

| # | Gate | 状态 | 证据 / 尚需完成 |
| --- | --- | --- | --- |
| 1 | Legacy Inventory | PASS_ACQUIRED | 14 scopes；已取得输入全集有解释；pending/deferred 明确记账 |
| 2 | Private Migration Ledger | PASS | 所有 source destination/native receipt/digest/stable signatures Git 外保存 |
| 3 | ChatGPT Source Import | ACQUISITION_PENDING | 请求已提交，数据未到达；非当前 blocker |
| 4 | Gemini Source Import | PASS | 完整官方包通过 native Gateway 保存；150 members 全部字节对账 |
| 5 | WorkBuddy Source Import | PASS | 1,143 records；referenced transcripts 两轮 0 error / rerun 0 new |
| 6 | Hermes Source Import | PASS | 67 原始 inputs 完整校验、重跑稳定 |
| 7 | Codex Reconciliation | PASS | 119 acquired inputs / 120 source versions；精确旧前缀与引用复用 |
| 8 | V1 Legacy Reconciliation | PASS_SOURCE | 84 existing V1-derived records 加两份 raw DB；原始证据分别保留 |
| 9 | Source Dedup | PASS | 2 acquired exact copies；9 Gemini member copies 保留；1 candidate 不合并 |
| 10 | Idempotent Import | PASS | 1,776 identity/byte/provenance signatures 跨重跑稳定 |
| 11 | Source Preservation | PASS | 全部原字节 Gateway 校验；immutable evidence；无 source 覆盖 |
| 12 | Canonical Schema | IN_PROGRESS | source-only Gate 已通过，进入设计 |
| 13 | Deterministic Normalization | NOT_STARTED | 同上 |
| 14 | Ambiguity Guard | NOT_STARTED | probe 不猜角色/时间/边界；canonical guard 尚未实现 |
| 15 | Timestamp Semantics | PARTIAL | source time 与获取 recorded_at 分开，未知不填 mtime |
| 16 | Ordering Semantics | NOT_STARTED | 未生成 canonical 顺序 |
| 17 | Attachment Mapping | PARTIAL | Gemini 149 个其它文件作为 opaque archive members 保留；实际附件数未知，不伪造 individual asset refs |
| 18 | Canonical Provenance | NOT_STARTED | 尚无 canonical records |
| 19 | Normalization Idempotency | NOT_STARTED | 尚未 normalization |
| 20 | Cross-source Reconciliation | PASS_SOURCE | 1,692 acquired fingerprints 加84 existing-source indexes全部有解释 |
| 21 | Production Gateway Readback | PARTIAL | source byte/provenance/counts/search native PASS；canonical 待完成 |
| 22 | Cross-Agent History Read | NOT_STARTED | normalization 后最小 read E2E，不重跑 P12 |
| 23 | No-result | PARTIAL | 既有 legacy/History 与本轮 Gemini document synthetic no-result 均成功；canonical/跨 Agent 尚未执行 |
| 24 | Privacy | PARTIAL | Phase A 排除测试/包扫描通过；P13 后续真实执行与发布仍须重新审计 |
| 25 | Regression | PARTIAL | source targeted21 passed；full723 passed/12 skipped；normalization 待完成 |
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

Source framework 经独立 review 修复并复核：64–90 KiB root 分段读取、SQL 有界查询、
等价 UTC 时刻幂等、大 BLOB 单连接流式校验。新工具通过持久 worktree 配置加载到
真实 Codex Host，无 inline override、直接 client 或 Agent-side DB read/write。
首次工具审批配置拒绝与 3 次 60-second transport timeout 全部留存；限定工具授权、
600-second timeout 后续跑成功，超时批次 128 条均 reuse，未重复建 source。
每批完整 receipt Git 外持久化，compact 仅减少返回体。

新增 source tests21 passed；full723 passed/12 skipped；公共包与 staged candidates 隐私
检查无真实数据。所有指纹、路径、内容、Host traces、ledger、receipts 均 Git 外。
source-only Gate已通过，继续 canonical design/normalization，不中途暂停或提前 retirement。

## Gemini source-only real execution

一个官方包为 **1 logical source bundle**，不混入既有 166 legacy-source record 统计。
包大小 **49,923,269 bytes**；150 个 file members 全部保留，其中一个是经私有格式审计
确认的 My Activity HTML，包含 **336 explicit activity blocks**，其余 **149 个文件保持 opaque**。
上传的 HTML/JSON/TXT 可能本身包含其它聊天，未解析为 Gemini conversations/messages。
actual attachment count、conversation count、message count 均未知；本轮 canonical writes 为 0。

完整 ZIP 保存为 96 个固定 binary Asset ranges；原活动 HTML 保存为 28 个 UTF-8
Document/Asset ranges；一个 deterministic derived manifest Document 关联全部 ranges、
member order/digests 与 source type。Manifest 不含私人 absolute locator 或导入时间，
source evidence 不被 Document normalization 替换。Native provenance 保留
source/external-client 与 deterministic-derived 区分，reported identity 不冒充 authenticated。

在发布 root 前，正式 Gateway 回读全部 ZIP/HTML 原字节，在私有 isolated target
重建官方包，完整 SHA-256、每个 member SHA-256 与 ZIP CRC 均 PASS。Root 随后保存并
完成原字节 checksum、Document provenance/source-ref、marker search 与 no-result。
全文 search 使用既有 1,000-character chunks，完整长 digest 可能跨 chunk 无命中；
digest prefix 命中同一 root，完整 identity 以 native Asset byte readback 校验，未修改搜索 contract。

生产重跑两轮各 125 次 artifact operations，**0 logical source 新增、0 ref changes、
0 provenance changes**，root marker search 始终仅一个结果。9 个 member-byte duplicate
copies 仍保留在原 ZIP 中；不同格式/packaging 不作 semantic merge。

执行校验曾发现 **2 次 native byte-identity mismatch**，重试后都与计划一致，原因未确定。
失败返回产物保持未被 manifest 引用，正式 refs、私有失败回执和恢复结果全部留存审计，
没有静默清理。当前 Gemini 未解决错误为 0；不将异常产物计为 Gemini logical sources。

原始输入、raw copy、payloads、native write/readback receipts、ledger destination mapping
及 isolated reconstructed ZIP 均 Git 外。这是 **Gemini archive recovery proof**，
不替代尚未执行的 full V2 backup/isolated restore Gate。V1 未进行逻辑退役或物理删除。

独立 code review 的 HTML 附件误识别、protected-output ancestor overlap 两项问题均有
synthetic RED→GREEN 回归；atomic replacement failure、raw-store reopen、不同包不覆盖旧
payload、相同分段同 title 及既有 text Document constraints 也已覆盖。targeted **56 passed**；
full **701 passed / 12 skipped**。46 wheel members / 185 sdist members 及公开 working/staged
candidate 隐私扫描通过；实际来源路径、指纹/member names 与真实活动文本 sentinels 无命中。
fresh installed wheel 的两次 synthetic CLI plan identity 相同，未访问生产。
没有 bump、tag、push 或 Release；工程改动仅提交本地 P13 branch。
