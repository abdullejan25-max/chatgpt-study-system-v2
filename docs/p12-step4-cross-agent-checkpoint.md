# P12 Step 4 — Cross-Agent Integration checkpoint

日期：2026-10-01。目标：v0.6.0。当前版本：**0.5.0**。
状态：**Stage A REAL VALIDATED / WAITING_FOR_WORKBUDDY_TRUST**。
最终 Gate：**7 PASS / 6 PARTIAL / 12 WAITING**。尚未完成 A → B → C，不得发布。

## Reality delta audit

干净 linked worktree 从 v0.5.0 的 33570d69516d8e1f61653d200696204f82c697bc
创建 `codex/p12-step4-cross-agent-final-e2e`。远端 main/tag target 相等；annotated
tag object 为 af192cd4c6cec1f84b537de7669da69f6a95e2e6。
WorkBuddy executable/UI 仍为 5.6.2，Hermes CLI 仍为 v0.20.0 (2026.8.3)，
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
`Tool ... not found in the deferred tools index`，未到达 canonical Gateway，也未提交更新，
不能计 cross-agent discovery/update PASS。

只调查版本变化造成的配置 delta。当前安装 loader 源码明确将用户 MCP transport
config hash 与 trust approval 绑定，未批准项为 `trust-pending`，不会提供给 Agent。
新 alias 的持久 config 存在，但实际 approval snapshot 无对应记录；旧 study entry
有记录。工具 cache 不含 server name 本身不足以证明连接失败；本轮结论依据
实际 Agent trace、有效配置、trust 状态和 loader 的 blocked condition。

需要 owner 在 WorkBuddy MCP 列表完成该 alias 的信任确认。未写 approval file、
未伪造 trust、未借已批准旧名称覆盖 production，也未使用 CodeBuddy SDK 替代
WorkBuddy。canonical target/v1 不变，原始 Host trace/诊断留在 Git 外。
5.6.2 单 Host PASS 是历史 evidence，不将其冒充 5.7.3 cross-agent PASS。

## Gateway/SDK corroboration

共享配置、能力和 workflow 已经 Gateway stdio 验证。后续必须通过 Gateway
建立正式 baseline、验证 historical provenance、v2/idempotency/conflict/no-v3、
exact restart comparison 和 final scoped Projection。不能用 SDK 补称真实 Host 行为。

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
| 4 | WorkBuddy Real Host Connection | WAITING | 5.7.3 新 alias trust-pending，需 owner GUI 确认 |
| 5 | Hermes Real Host Connection | PASS | canonical target 真实新 CLI Agent 会话及官方 export |
| 6 | Natural-Language Auto Routing | PARTIAL | 两 Host 已观察；WorkBuddy 待验 |
| 7 | Agent A Create | PASS | canonical Document/source/v1 + 完整 readback，首轮 FAIL 保留 |
| 8 | Agent B Cross-Agent Discovery | WAITING | fresh WorkBuddy marker-only prompt |
| 9 | Agent B Update | WAITING | append v2、readback |
| 10 | Agent C Cross-Agent Discovery | WAITING | fresh Codex latest=v2 |
| 11 | Version Graph | WAITING | real cross-Host [1,2] / supersession |
| 12 | Cross-Agent Provenance | WAITING | Hermes v1 / WorkBuddy v2；历史字段不变 |
| 13 | Idempotency | WAITING | exact real Host request/key replay |
| 14 | Stale Conflict | WAITING | Gateway CONFLICT with new key/stale version |
| 15 | No v3 | WAITING | final total=2 / unique versions and IDs |
| 16 | Cross-Agent No-result | PARTIAL | Codex real no-result；其他覆盖待验 |
| 17 | Gateway-only Boundary | PARTIAL | 已执行两 Host 经 Gateway；WorkBuddy 待验 |
| 18 | No Human Data Relay | PARTIAL | 已执行步骤无 DTO 中继；final chain 待验 |
| 19 | No Session/Memory Shortcut | PARTIAL | 新会话、最小 prompt；final traces 待验 |
| 20 | Cross-Agent Persistence | WAITING | A/B 退出后 C exact comparison |
| 21 | Projection Final E2E | WAITING | 最终 shared target 两次正式 build |
| 22 | Memory Authority Boundary | PASS | disabled configs、Gateway-only guidance、无新 Memory |
| 23 | Privacy | WAITING | 原始 configs/traces/stores/Vault 均 Git 外；final audit 待验 |
| 24 | Regression | PASS | targeted 32；full 622/12；review focused 1 |
| 25 | Documentation | PASS | spec/plan/checkpoint、证据层级及等待状态明确 |

## Resume and release boundary

继续同一 branch、shared canonical target 和私有 receipts，不能从头重新验收。
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
