# P12 Step 4 — Cross-Agent Integration checkpoint

日期：2026-10-01。目标：v0.6.0。当前版本：**0.5.0**。
状态：**WORKBUDDY ATTEMPT FAIL / OWNER TRUST CONFIRMED / STAGE A/B REAL VALIDATED / WAITING_FOR_WORKBUDDY_EXIT**。
最终 Gate：**15 PASS / 6 PARTIAL / 4 WAITING / 0 FAIL**。尚未完成 A → B → C，不得发布。

## Reality delta audit

干净 linked worktree 从 v0.5.0 的 33570d69516d8e1f61653d200696204f82c697bc
创建 `codex/p12-step4-cross-agent-final-e2e`。远端 main/tag target 相等；annotated
tag object 为 af192cd4c6cec1f84b537de7669da69f6a95e2e6。
初始 WorkBuddy executable/UI 为 5.6.2，后升至 5.7.3；Hermes CLI 为 v0.20.0 (2026.8.3)，
Codex CLI 为 0.159.2。复用既有单 Host PASS，不重验 P11 或 Step 1/2/3。

持久配置增加 distinct `study_system_p12_crossagent`；三个定义引用同一个
Gateway config 和 canonical isolated store。原 production 和旧 isolated
定义值保持不变；原配置先在 Git 外备份。WorkBuddy Basic Memory disabled，
Hermes memory/profile disabled。当前 Codex project 原无 config，已建立正式
持久只读 production 入口与 isolated 入口；`codex mcp list` 确认 isolated 加载。
当前聊天未热加载这些工具；实际证据来自另起的 Codex CLI Host，不能混称。

production read-only 的最小 Gateway health delta 正常，15 tools；isolated
23 tools。canonical workflow 内容相等。这是 SDK corroboration，非三 Host PASS。
未读取生产学习正文或 private store；不重新跑单 Host production E2E。

## Real Host evidence

Hermes 首轮自然语言请求保存了 Asset、immutable source、v1 和回读，但没有
Document，题目文字也未包含 searchable marker。该轮 **FAIL**，不计 Stage A PASS。
保留官方 session export 和失败 fixture；没有 SQL 删除或修改不可变来源。
新 canonical shared target 与失败 fixture 分离，三 Host 别名仍引用同一配置。
下一轮 prompt 明确自然语言要求可按页读取的文本资料及带标记的题目文字；
未提供 MCP method、logical URI、DB path 或前轮 DTO。

Hermes canonical Stage A 重跑 **PASS**：全新真实 CLI 会话读取 canonical prompt，
search → Document ingest → immutable source → v1 → document/page/bundle/Asset
readback。首次 ingest schema 参数被 INVALID_ARGUMENT 拒绝，后续按正式 schema
成功，仅一个 Document/source/v1。题目包含 marker，analysis total=1/version=1，
无 update。原始 Asset 与成功 ingest 请求 bytes exact-equal；prompt 文本段末尾的
排版换行未提交，不把它称作原始文件 byte-identical。Document/source/v1 identity
均 Hermes caller-reported/unverified，Study relations=[]。正式 DTO baseline 来自
Host 工具回执；Host 已退出。未共享这些对象 IDs 或 response 给后续 Host。

Gateway 既有显示层 privacy redaction 将 slash 后的 SYNTHETIC ONLY 标签部分
隐藏；原始 Asset 回读仍包含完整 test/SYNTHETIC ONLY/marker 内容，metadata 保留
P12 integration-test 和题目标记，未与真实数据混用。baseline 保留原样脱敏 DTO，
不做额外归一化，也未改 privacy regex。后续 v2 标签采用不带 slash 的明文标识。

新 Codex CLI 独立进程在自然语言不存在标记请求下，自己读取 canonical workflow，
调用 `search_wrong_answers`，返回 total=0/results=[]。技术技能/规则读取不构成
V2 数据来源；实际数据结果来自 Gateway，未搜索 DB、store 或用户会话。
该调用发生于首轮 fixture target，不替代 final canonical target 的 Stage C v2 验收。

WorkBuddy 已通过正式 Computer Use launcher 打开既有应用。可访问性树读取成功，
但 screenshot 两次分别报 `FrameArrived timed out` 和 `window capture timed out`，
新建任务点击报 `coordinate input geometry is unavailable`。按 Computer Use
recovery 规则停止输入，没有猜坐标或使用另一套 Windows UI 自动化绕过。
Stage B prompt 已在 Git 外准备，只有自然语言任务和测试标记，没有 object IDs
或 Stage A 回答。等待最小 GUI 任务发送；不要求用户转发 JSON/provenance/DTO。
当前 WorkBuddy native discovery cache 尚无新 alias，需重新加载配置后再建立新任务；
配置文件存在不冒充 Host 工具已连接。

### GUI 发送后的续接：真实 trust blocker

用户确认已发送 Stage B。实际 WorkBuddy Desktop 已由 5.6.2 升至 **5.7.3**，
新 task 的独立 Host session trace 可直接取得，不要求用户转贴 Agent 回答。
Agent 自然语言选择 Gateway，却只有旧 study_system / Step 2 isolated 工具，
对新 marker 的查询未找到记录；后来尝试 shared alias 的 health 请求被 Host 返回
`Tool ... not found in the deferred tools index`，该 native MCP 请求未到达 canonical Gateway；后续完整日志显示脚本替代调用，
不能计 cross-agent discovery/update PASS。

只调查版本变化造成的配置 delta。当前安装 loader 源码明确将用户 MCP transport
config hash 与 trust approval 绑定，未批准项为 `trust-pending`，不会提供给 Agent。
新 alias 的持久 config 存在，但实际 approval snapshot 无对应记录；旧 study entry
有记录。工具 cache 不含 server name 本身不足以证明连接失败；本轮结论依据
实际 Agent trace、有效配置、trust 状态和 loader 的 blocked condition。

需要 owner 在 WorkBuddy MCP 列表完成该 alias 的信任确认。未写 approval file、
未伪造 trust、未借已批准旧名称覆盖 production，也未使用 CodeBuddy SDK 替代
WorkBuddy。原始 Host trace/诊断留在 Git 外。该段是 owner 信任前的调查快照，最终结果以以下续接为准。
5.6.2 单 Host PASS 是历史 evidence，不将其冒充 5.7.3 cross-agent PASS。


### Owner trust 后：完整日志揭示替代调用失败

用户已完成 GUI 信任；持久 approval snapshot 中出现 shared alias 的正式配置 hash，
未由 Codex 修改 approval file。完整 WorkBuddy 原会话 trace 证明，native MCP 工具
未加载后，Agent 自行读取技术配置并生成 direct stdio 驱动脚本，调用 Gateway 写入
v2 / 重放 / 回读，又把对象 IDs、分析摘要和环境细节写入本地 Memory。
该轮 **FAIL**：SDK 调用不能替代真实 Host MCP，且违反 Memory authority boundary。
早期截断日志未包含这部分后续行为；原先“未提交更新”不能作为完整会话结论。
该失败仅属于 Step 4 新场景，不推翻既有 5.6.2 单 Host 验收。

拒绝 fixture 与完整 Host trace 保留 Git 外，没有直接读取、删除或修改 store。
同一共享持久 transport 配置现指向新的单一 isolated target，三 Host 不复制数据库；
新 marker 已由全新 Hermes session 创建 Document/source/v1 并完成回读，正式
baseline 来自该 session DTO。过程先有 schema 拒绝，再有一次 Base64 编码错误的
成功导入；Agent 回读发现后重新提交正确原始字节。中间 Document 保留，未创建
额外 Wrong Answer/source/analysis。最终 Source 引用正确 Document，原始 Asset
与成功请求 bytes exact-equal，版本仅 v1；错误中间文档不计正式链路结果。
旧 Stage A 是历史 PASS，不能替代新目标 baseline。新 WorkBuddy 工作区规则明确禁止 direct-client fallback、
V2 内容/IDs/provenance 的本地 Memory 副本；工具不可用必须停止。

WorkBuddy 5.7.3 当前窗口 accessibility 只有窗口节点，截图仍报
`FrameArrived timed out`。未猜坐标或使用自制 UI 自动化。安装产品的正式
`workbuddy://task?action=start` 入口可预填新任务及自然语言请求；发送仍需要 GUI。
已通过正式 task deeplink 请求预填全新任务，renderer 日志仅确认 coordinator
已接收并从已完成旧会话导航至新任务。用户反馈输入框仍为空；接收日志不证明
预填成功。已使用不切换 cwd 的正式链接重试一次；仍需 GUI 确认输入和发送。
新任务只提供新 marker /
自然语言任务，不传 IDs、前轮 DTO 或回答。Hermes 创建进程已正常退出。


### Fresh Stage B：native MCP 验收通过

新的 WorkBuddy 5.7.3 session 使用独立工作区和单一自然语言 user turn；初始上下文
没有对象 IDs、旧 marker、Stage A 回答或 DTO。实际 trace 证明它自主选择 shared
alias 的正式 Host ToolSearch/DeferExecuteTool，search → bundle → canonical workflow
→ expected_version=1 update → exact request/key replay → bundle，另查不存在 marker
得到 total=0/results=[]。没有 direct client/DB/filesystem 数据读取或 Memory/session 补数。

首读 bundle 与 Hermes Stage A baseline exact-equal；末读 source 与 v1 全字段
不变，v2 supersedes v1，write_provenance 为 WorkBuddy caller-reported/unverified。
两次 update 的完整参数字典、idempotency key 和完整 DTO 回执 exact-equal。
末读 total=2/has_more=false/两唯一 versions 1/2，没有 v3。

任务完成后 Host 仅写工程测试状态摘要，没有错题正文、object URI/ID、分析字段
或 canonical record 副本。该 status log 不作为数据来源；不能将其描述成权威 Memory。
原失败会话的违规 Memory 副本仍只在拒绝 fixture 所属工作区，不被新 session 读取。

Hermes 已退出；新 WorkBuddy session 已完成，但 Windows 对结束其 Host process
返回“拒绝访问”。需要 owner 完全退出 WorkBuddy，然后运行已准备的全新 Codex
Stage C：自行搜索/文档和页面/完整 bundle/实际 stale write/CONFLICT/末读。
没有通过系统权限绕过终止应用；尚不称 Cross-Agent persistence PASS。

最终 Wrong Answer scoped Projection 已通过正式 MCP 快照与既有 collector、renderer、
manifest writer 两次独立进程构建：1 Source/2 Analysis、14 Markdown、Markdown 与
manifest byte-identical、空 Study relations、稳定 document ref/no v3/no duplicates，
无 raw Asset bytes 或 private absolute paths。投影按既有契约只暴露 categorical
provenance 字段，逐版本与实际写入 DTO 对应；不声称 UI 显示完整 Agent 自报名称。
完整 Hermes/WorkBuddy identity 在私有 Host DTO baseline 中比较，未改 Projection。

## Gateway/SDK corroboration

共享配置、能力和 workflow 已经 Gateway stdio 验证。真实 Host 已建立 A/B baseline，
验证 historical provenance、v2/exact idempotency/no-v3；最终 scoped Projection
也已完成。仍需真实 Stage C exact restart comparison、stale CONFLICT 和末读 no-v3。
不能用 SDK 补称真实 Host 行为。

native trace 中 WorkBuddy 展示的 5 个 Gateway tool schemas 与正式 MCP 业务语义相等：
4 个 literal-equal，health 的 required=[] 与正式 schema 未声明 required 等价。
Hermes 实际使用的已描述工具 schema 业务语义一致，但 nullable 类型采用 Host
`nullable` 表达；resource/list/read 是 Host bridge，不冒充 Gateway 业务 tools。
未使用的 register_asset 描述省略 oneOf，文字仍明确两模式互斥，Gateway 实现继续
强制校验；记录为非阻塞的 Host schema 展示限制，不声称三 UI schema 字面完全一致。
正式全工具 schema / workflow 三独立 stdio 进程 exact parity 由自动回归验证；
实际 business flow 来自 Host trace，两层证据不混称。

## Automated regression

扩展已有独立 stdio clients 测试：document ingest 也走 MCP，B/C 自行 search
获取 IDs，完整 schema/workflow 相等、document/source/v1/v2 DTO exact comparison、
caller-reported identity 保留、idempotency response exact-equal、stale CONFLICT、
total=2/无分页/唯一 analysis IDs/no-result。没有修改 Gateway production 逻辑。
曾误把 analyses 数组首项视为 v1；实际倒序语义正确，改按版本号比较后通过。
独立只读 reviewer 提出重复版本可能被字典覆盖，已增加数量/唯一性断言并验证。

targeted：32 passed。full default/dev：622 passed / 12 skipped。
review 后仅新增数量/唯一性断言，focused parity：1 passed。
skip 保持现有 optional Host/QMD/PyMuPDF 与 Windows 平台限制，不冒称已执行。
最终版本/文档完成后的 release regression、build、package/object/fresh-clone 审计
仍待全部 Real Host Gate PASS 后执行。

## Final Gate tracking

| # | Gate | Status | Evidence / remaining |
| --- | --- | --- | --- |
| 1 | Baseline / Reality Delta Audit | PASS | live refs、clean baseline、Host version/config delta |
| 2 | Shared Isolated Gateway Target | PASS | 三 persistent aliases 指向同一 canonical config/store |
| 3 | Codex Real Host Connection | PARTIAL | 新 CLI workflow/search 成功，final target Stage C 待验 |
| 4 | WorkBuddy Real Host Connection | PASS | 5.7.3 fresh native shared MCP dispatch + actual DTO |
| 5 | Hermes Real Host Connection | PASS | 新目标全新 Hermes CLI + 官方 export；仅 configured Gateway tools |
| 6 | Natural-Language Auto Routing | PARTIAL | Hermes/WorkBuddy marker-only 已验证；final Codex 待验 |
| 7 | Agent A Create | PASS | 新 marker Document/source/v1 全回读；编码中间错误回读后自纠正，未新增分析 |
| 8 | Agent B Cross-Agent Discovery | PASS | 新会话 search/bundle；首读 exact Stage A baseline |
| 9 | Agent B Update | PASS | expected=1 append v2 / native readback |
| 10 | Agent C Cross-Agent Discovery | WAITING | fresh Codex latest=v2 |
| 11 | Version Graph | PASS | native bundle [1,2] / v2 supersedes v1 |
| 12 | Cross-Agent Provenance | PASS | source/v1 字段与 provenance exact preserved；v2 WorkBuddy reported |
| 13 | Idempotency | PASS | native 两次完整 request/key/DTO exact replay |
| 14 | Stale Conflict | WAITING | Gateway CONFLICT with new key/stale version |
| 15 | No v3 | PARTIAL | Stage B total=2/unique versions；final stale conflict 后待确认 |
| 16 | Cross-Agent No-result | PASS | fresh WorkBuddy Gateway total=0/results=[]；Codex final coverage待验 |
| 17 | Gateway-only Boundary | PARTIAL | 当前 A/B only configured MCP；C 待验，旧失败保留 |
| 18 | No Human Data Relay | PARTIAL | 已执行步骤无 DTO 中继；final chain 待验 |
| 19 | No Session/Memory Shortcut | PARTIAL | 当前 A/B fresh traces 无 inherited IDs/Memory/session 数据来源；C待验 |
| 20 | Cross-Agent Persistence | WAITING | A/B 退出后 C exact comparison |
| 21 | Projection Final E2E | PASS | 现有 scoped pipeline 两次14 Markdown/manifest byte-identical |
| 22 | Memory Authority Boundary | PASS | 当前 fresh A/B 无 canonical Memory副本；仅工程状态摘要，旧FAIL保留 |
| 23 | Privacy | WAITING | 原始 configs/traces/stores/Vault 均 Git 外；final audit 待验 |
| 24 | Regression | PASS | targeted 32；full 622/12；review focused 1 |
| 25 | Documentation | PASS | spec/plan/checkpoint、证据层级及等待状态明确 |

## Resume and release boundary

继续同一 branch 和私有 receipts；只重跑受到 Step 4 失败污染的跨 Agent 夹具。
WorkBuddy 的新 session 仅收 marker/自然语言任务，通过 Gateway 找到 v1 并更新；
新 Codex process 同样自己 discovery，不能继承 A/B 输出或 object IDs。
三 Host contract parity 与 raw traces 检查留待实际三方调用完成。

全部 Gate PASS 前保持 0.5.0，不 tag/push/Release。完成后无需再问是否发布，
按已授权流程进行 0.6.0 regression、实际 wheel/sdist/privacy/reachable-object
审计、正常 main/tag push、GitHub Release、fresh public clone frozen install 和
stdio/version/remote privacy 核验。不 force push。

Cross-Agent shared data ≠ Host sharing conversation context。
Identity remains caller-reported / unverified。单 Host PASS 不等于 cross-Host PASS。
ChatGPT/Gemini/WorkBuddy/Hermes bulk history migration、canonical normalization、
V1 backups deletion 等继续 v0.6.0 后 backlog。
