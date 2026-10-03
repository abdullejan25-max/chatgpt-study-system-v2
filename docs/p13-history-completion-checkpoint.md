# P13 — History Completion & Normalization checkpoint

日期：2026-10-03。起点：**v0.6.0 / 02d1ed2**。
当前状态：**已取得来源 Phase A/B PASS；Phase C normalization/reconciliation PASS；Phase D 两个真实 Host PASS，WorkBuddy History DEFERRED；真实 V2 backup/isolated restore PASS_NATIVE；Phase E unique-data audit PASS / logically retired / data retained**。
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
这是历史 source completion checkpoint；当前 V1/runtime/release 结果见末尾最终接续。Physical deletion 始终等待 owner。

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
| 12 | Canonical Schema | PASS | additive immutable conversation/message/source-specific view/evidence/outcome tables |
| 13 | Deterministic Normalization | PASS_REAL | Codex/WorkBuddy/Hermes deterministic adapters；ChatGPT synthetic tree adapter 为后续增量准备 |
| 14 | Ambiguity Guard | PASS | 32 ambiguous sources、237 ambiguous candidates 保留；不猜 role/time/order/boundary |
| 15 | Timestamp Semantics | PASS | occurred/imported/normalized 分离；不明单位保持 unknown；reparse 与 provenance 时间校验 |
| 16 | Ordering Semantics | PASS | source physical sequence / explicit tree；不按 import time 排序 |
| 17 | Attachment Mapping | PARTIAL | Gemini 149 个其它文件作为 opaque archive members 保留；实际附件数未知，不伪造 individual asset refs |
| 18 | Canonical Provenance | PASS | 所有 derived records 指向 immutable source；全量校验/reparse PASS |
| 19 | Normalization Idempotency | PASS_REAL | 56 native normalization calls，两轮完整处理；第二轮新增 conversation/message/view 均为 0 |
| 20 | Cross-source Reconciliation | PASS_ACQUIRED | 1,776 source outcomes 两轮稳定；每个 source 有持久 native receipts，未解释来源 0 |
| 21 | Production Gateway Readback | PASS_CODEX | initiating Desktop 原生 source search/verify、canonical category search/conversation/message read 均成功 |
| 22 | Cross-Agent History Read | PASS_TWO_HOSTS / WORKBUDDY_DEFERRED | Codex Desktop + Hermes native Agent 同一 history PASS；owner 明确将 WorkBuddy P13 History 延后，不阻塞 P13 |
| 23 | No-result | PASS_TWO_HOSTS | Codex Desktop 与 Hermes native Agent 专用 literal canonical query 均返回 total=0、empty list |
| 24 | Privacy | PASS_PUBLIC / PRIVATE_REFS_RETAINED | 当前 staged/wheel/sdist/current branch/main 无私人标记；旧 Codex private turn-diff refs 的配置命中单独记账，禁止发布这些 refs |
| 25 | Regression | PASS | final targeted380/1 skipped；full828/12 skipped；recovery53 passed，新增 supplemental scope 有 RED→GREEN |
| 26 | Recovery Backup | PASS_NATIVE | 3,778 files / 44,380,473,111 bytes；实际 native create verified、positive usage、manifest/provenance/logical digests/ledger Git 外保存 |
| 27 | Isolated Restore Smoke | PASS_NATIVE | 同一已验证 snapshot；各域 logical digests/manifest/ledger/counts 一致；Study read 与 Assets197/Documents29/WA sources5/analyses5 正式有界回读 PASS；native capacity sufficient |
| 28 | V1 Unique-data Audit | PASS | 442 个 bounded original inputs 精确映射；26 份增量已 source-only 导入并重放；producer freeze 后 V1-only unknown=0 |
| 29 | V1 Logical Retirement | PASS_DATA_RETAINED | 旧 router 无 active process/schedule；Basic Memory Host disabled；6 个 legacy writer hooks 可恢复停用；原始数据未删除 |
| 30 | Documentation | PARTIAL | 当前 checkpoint 与 Phase A design/plan 已写；最终报告待所有 Gate |

Physical deletion 独立于自动 Gate；必须等待 owner 明确确认。

## Canonical normalization real execution

Source-only completion 通过后才执行 normalization。真实 configured Codex Host 完成
28 批首轮与 28 批重跑；共 1,776 个 immutable sources，0 unresolved execution errors。
第二轮 new conversations/messages/views 均为 0；所有 sources 有两份 durable private
normalization receipts，结果逐 source 对账稳定。原字节 reparse 与全量 identity、
content digest、source/view/evidence/outcome/provenance 校验 PASS。

| 指标 | 数量 | 口径 |
| --- | ---: | --- |
| Canonical conversations | 487 | Codex 95、Hermes 42、WorkBuddy 350 |
| Canonical messages | 7,334 | distinct canonical identity，不等于原消息 appearances |
| Source-specific views | 494 | 每份 evidence 的原顺序/tree 独立保留 |
| Source outcomes | 1,776 | normalized 441、partial 12、ambiguous 32、unsupported 1,290、malformed 1 |
| Message candidates | 7,729 | adapter candidates，不作为成功 message 数 |
| Canonical appearances | 7,492 | exact 5,468、derived-safe 2,024；confidence 数量按 appearances 统计 |
| Reused canonical appearances | 158 | appearances 减 distinct messages，不是 source-file duplicates |
| Ambiguous candidates | 237 | 未生成 canonical message；原 evidence 保留 |
| Source-only retained | 1,323 | unsupported + ambiguous + malformed；partial 另行计数 |

Normalization 的 1 malformed source outcome 与 acquisition 的 2 malformed raw records
属于不同层级，不能相加成同一种错误。所有原 sources 保持不变。ChatGPT 仍为
acquisition_pending；Gemini activity/opaque members、legacy Markdown/DB 不猜成聊天。
附件原始 part metadata 保留 unresolved；本轮没有声称附件均已映射为 asset refs。

Initiating Codex Desktop 已使用加载后的原生 MCP 工具完成三类 category searches、
conversation/source-specific view 读取、bounded message byte read、源 checksum/provenance
校验及 canonical no-result。Hermes fresh native Agent 独立查询同一首条 Codex history，
完成 summary/search/conversation/message/source verify 六次实际 Gateway reads；正式
session export 和 token usage 在 Git 外保存。未传入来自 Codex 的 IDs 或 DTO。

WorkBuddy 原生配置已持久更新为当前代码、同一生产目标、read-only capabilities，
旧配置在 Git 外备份。但 Windows capture 返回 FrameArrived timeout，支持的 input
返回 coordinate input geometry unavailable；GUI read E2E 尚未独立执行，不能计 PASS。
Owner 明确将此 P13 canonical-history Desktop verification 记为 **DEFERRED — external
computer-use / desktop capture / input automation blocker**，不再阻塞 P13。既有
v0.4.0 WorkBuddy Host integration 与 v0.6.0 Cross-Agent integration PASS 保留；本轮
没有新的 Gateway/schema/product regression evidence。未来仅做一次最小增量补验。
一次后续 Codex CLI readback 遇 account usage limit；initiating Desktop 的真实读取
成功，account limit 不被误报为 Gateway failure。私有失败记录和成功读取证据均留存。

Full regression 774 passed / 12 skipped；针对 canonical 的 51 tests 覆盖 malformed/
ambiguous/branching/missing timestamp/attachment preservation/rerun/corruption detection。
这些真实迁移和 Host receipts 不在公开 fixtures 或 Git 中。

51 targeted tests 再次通过。wheel/sdist 构建成功；58 wheel members、207 sdist members、
206 staged candidates 的扫描未命中 3,567 个私有 identity/location markers 或受限内容。
新 wheel 在独立环境安装后，纯人工 synthetic normalization 两次结果一致，未访问生产。
全仓库 798 reachable blobs 扫描发现两份旧 Host config blob，仅由 Codex 私有
turn-diff refs 持有，不在当前 branch 或 main 历史中。完整 ref/object 明细 Git 外保存；
保留本地快照，不把全仓库扫描误称零命中。未来仅发布明确的公开 branch/tag，禁止
push --all、mirror 或发布 private turn-diff refs。本轮未 bump/tag/push/release。

V2 full backup 与 isolated restore 已通过真实 native Host 验证；V1 unique-data final audit、
logical retirement 尚未执行，不能声称 retirement ready，也未请求 physical deletion。
WorkBuddy History 按 owner 决定 DEFERRED，后续非破坏性工作自主推进。

## Recovery engineering 与真实执行状态

新增三个 opt-in、admin-only native MCP 工具：snapshot plan、immutable snapshot create、
snapshot verify/isolated restore。路径只来自私有配置，不接受任意路径或删除操作。
SQLite backup 捕获 committed WAL；大 BLOB 流式校验，Study、Assets、History、ledger、
原始 Gateway/QMD 配置和 migration evidence 纳入完整快照。公开说明见
[p13-recovery.md](p13-recovery.md)。

快照验证检查完整文件集合、字节 checksum、schema/row digest、source/canonical identity
和 provenance；manifest 另有独立 catalog checksum anchor。复制结束重新校验源文件，
防止同长度修改后恢复 mtime 掩盖变动。capacity 同时考虑 SQLite logical pages/WAL、
copy、temp 与独立 restore 空间，恢复前再次检查；显式 reserve 取 4 GiB 和 10% 计算值
中的较大者。真实 native plan 确认空间足够；未完成尝试保留，不覆盖或清理。

独立 review 发现的文件变动竞态、WAL capacity、manifest omission/forgery、publish
failure、restore capacity 与 legacy ambient QMD isolation 均有 synthetic 回归。
Windows 长路径曾使 normalization receipt 写入失败，已修复并通过深路径合成用例。
最新 full suite **816 passed / 12 skipped**；包含 partial-attempt aggregate 与慢速
recovery 期间 native ping 的回归。这些结果仅为公开工程证据，不能代替生产
backup/restore Gate。

真实 Gateway plan 返回 **3,778 files、44,380,473,022 required bytes**。上轮被中断的
create 尚未产生已发布目录，仅留下一个 **0-byte incomplete attempt**，原 Host 配置
已恢复。保留中断回执及未完成目录，真实 create 重试通过 configured native Hermes
Host 执行；没有 Agent-side snapshot/SQLite 检查。
首次中断/重连尝试不计 PASS。最终重试已取得 verified snapshot：**3,778 files、
44,380,473,111 bytes、1,776 sources、487 conversations、7,334 messages、494 views**。
官方 export 中实际 native call 与 positive usage 均已核验；原 Host 配置恢复。
Production → snapshot canonical/source proofs 一致。V1 未退役或删除。

随后复用该 immutable snapshot 完成真实 configured native isolated restore，
不是 direct SDK 或 Agent-side DB/store 验收。**Gate 26 / 27 均为 PASS_NATIVE**：
3,778 files / 44,380,473,111 bytes；全部 logical digests、manifest 与 ledger equality PASS。
恢复目标的 **1,776 sources、487 conversations、7,334 messages、494 views、
1,776 source outcomes、1,323 source-only retained** 与原目标一致，source/canonical
identity、provenance 与原始证据保持一致。

Isolated Study read verified。Assets **197**、Documents **29**、Wrong Answer
sources **5** / analyses **5** 的正式有界 native readback 与 whole logical digests
均 PASS。实际 native capacity 已纳入 copy/temp/WAL/显式 reserve 并确认足够。
恢复副本只用于隔离证明，不是第二 authority；生产目标未被覆盖。真实 tool trace、
positive usage、per-domain proofs 与 checksum 均 Git 外保存。V1 unique-data audit、
logical retirement 和 production writable ingress 验收仍待完成。

真实长调用暴露同步 recovery handler 阻塞 MCP event loop，导致 Host keepalive
重连。Synthetic regression 先复现 ping 延迟失败，再以 recovery-only worker thread
修复并通过；其余工具路径保持原样。独立 review 通过，新的真实 configured Host
create 重试已成功。取消请求不能证明 worker 已停止，必须通过 Gateway 核实结果。

最新 wheel 在独立环境完成 synthetic snapshot/reuse/restore 和慢速 native MCP ping
测试；深路径 receipt 回归通过。215 staged candidates、62 wheel members、216 sdist
members 的扫描仅在全 reachable Git 中保留两份已知历史 private config 命中；当前
候选、包、当前 branch/main 清洁。历史私有 refs 保留在本地并禁止发布。本轮保持
package 0.6.0，未 tag/push/release。

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
不替代 full V2 backup/isolated restore Gate；后续完整恢复已在 Gate 26/27 单独取得
PASS_NATIVE。V1 未进行逻辑退役或物理删除。

独立 code review 的 HTML 附件误识别、protected-output ancestor overlap 两项问题均有
synthetic RED→GREEN 回归；atomic replacement failure、raw-store reopen、不同包不覆盖旧
payload、相同分段同 title 及既有 text Document constraints 也已覆盖。targeted **56 passed**；
full **701 passed / 12 skipped**。46 wheel members / 185 sdist members 及公开 working/staged
candidate 隐私扫描通过；实际来源路径、指纹/member names 与真实活动文本 sentinels 无命中。
fresh installed wheel 的两次 synthetic CLI plan identity 相同，未访问生产。
没有 bump、tag、push 或 Release；工程改动仅提交本地 P13 branch。

## V1 audit incremental reconciliation (current)

P11 accepted accounting is reused. A bounded current audit found seven previously
skipped Personal files and 19 later archive files. All 26 are source-only imported
through native Gateway, exact rerun reuses all 26, errors=0. Only these new inputs
received deterministic unsupported outcomes; the earlier normalization was not
rerun. Current source index/outcomes=1,802; conversations=487/messages=7,334/views=494
remain unchanged. Unsupported outcomes=1,316 and wholly source-only retained=1,349.
Categories: basic_memory378/codex120/gemini1/hermes67/v1 93/workbuddy1,143.

V1-only unknown=0 after freezing the legacy Basic Memory archive writer. Exact
private mappings, both raw DB versions, config backups and producer/runtime
audit remain outside Git. Details: [V1 retirement](p13-v1-retirement.md).
The original full backup remains a valid point-in-time checkpoint. A new scoped
mutable-domain supplement captures the 26 later sources; its native create is
verified (237 files/1,048,793,838 bytes), isolated readback is PASS_NATIVE. It
explicitly excludes Study and accompanies the full Study backup/restore proof.
Production native synthetic smoke + fresh Hermes exact readback are PASS; final package/privacy/release verification is recorded below.

## Final non-destructive completion

V1 audit PASS; source-only increment26 exact rerun26 reused/errors0; no full
Gemini or existing normalization rerun. Current logical sources/outcomes1,802,
conversations487/messages7,334/source-only1,349. Two raw DBs are retained separately.
V1-only unknown=0 after producer freeze. V1 is logically retired/data retained:
6 legacy Basic Memory writer hooks disabled with exact private config rollback,
no Native Memory router process or scheduled dependency. Static StudyVault remains
authoritative and outside the physical transaction.

Supplemental native backup AND isolated restore PASS:237 files/1,048,793,838 bytes,
manifest/source/canonical/ledger proof equality; Assets197/Documents29/WA5/analysis5
formal readback. Study is explicitly excluded here; its full 3,778-file baseline
backup/restore remains PASS. This supplements, rather than replaces, that backup.

Persistent production ingress(read/ingest/write) and readonly(read) preserve all
P12 isolated aliases across Codex/WorkBuddy/Hermes. Codex native production smoke
passes source/v1/v2 exact replay/staleCONFLICT/bytes/provenance/onlyversions[1,2];
fresh Hermes from persisted Gateway0.7.0 returns the identical bundle and Asset
plus no-result. Marked synthetic1source/2versions are retained and are a known
post-backup test increment. WorkBuddy Desktop new-write verification is not claimed.

Engineering full828/12existing skips; targeted380/1; installed-wheel9PASS;
version/stdio38/1. Wheel/sdist and intended-public-ancestry privacy are verified
with real private markers kept solely in local audit inputs. Release: see
[v0.7.0](releases/v0.7.0.md). Physical deletion is an owner-confirmed transaction,
not an automatically passing Gate.
