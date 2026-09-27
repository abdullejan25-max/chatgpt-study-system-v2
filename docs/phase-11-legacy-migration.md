# Phase 11 — Legacy Migration

**状态：BLOCKED。** 已完成 Legacy Reality Audit、只读 dry-run 工具、私有 manifest 和 Study 检索验证；没有向 V2 History、Assets、Documents 或 Wrong Answer 业务存储写入旧数据。当前 Gate 被未配置的 History 后端和无法验证的旧错题来源关系阻断。

## Git 与发布基线

- 远端仓库为 `abdullejan25-max/chatgpt-study-system-v2`。开始工作前，`main` 与 `origin/main` 同为 `64d7849`，正式 `v0.1.0` tag 指向该公开版本。
- 在 Phase 11 分支先提交了最小 docs-only 发布状态同步，再开发迁移审计工具。`v0.1.0` 未修改；没有创建 `v0.2.0` tag/Release，没有 push。

## 架构和边界

- 新增本机命令 `study-migrate dry-run`。它只读取命令行显式指定的旧 Personal 根、旧项目根、可选 Native Memory 数据库、配置中的 V2 Study 根及 Asset 数据库。
- 命令没有 `apply` 模式，不注册 MCP 工具，也不写入 V2 业务库。它只将无正文、无绝对路径的清单写到仓库外的本机私有 SQLite journal。
- journal 在创建前以及每次 SQLite 连接前检查其主文件、`-wal`、`-shm`、`-journal` 与仓库、所有明确 source/target 根、数据库文件和数据库目录不存在重叠、reparse point 或硬链接；不安全路径会在写入前拒绝。
- SQLite 只读连接在 WAL 模式下可能更新 `-shm`。因此读取 Native Memory 和 V2 Asset 数据库前，命令会把明确选定的数据库和 WAL 复制到仓库及所有已配置 source/target 路径之外的临时目录，在临时副本上读取，并校验源文件复制前后 hash/大小一致；源 `-shm` 不复制、不打开。临时副本总量上限 512 MiB；发现活动 rollback journal、源变化或无法验证的文件句柄时会停止。正常结束后临时副本删除。
- Manifest 保存来源类别、稳定/不透明标识、内容 hash 或元数据 fingerprint、目标类型、动作、状态、源事件时间、导入时间、去重决定、验证状态和固定错误/跳过代码。路径形状的旧来源 ID 会哈希为不透明 ID。单根最多 250,000 个文件、源文件元数据总量最多 512 GiB；逐文件读取以盘点时的文件大小为上限，检测到文件变化就拒绝。Native Memory 单条内容最多读取 1 MiB，资产行最多 250,000 条。清单摘要按互斥结果分类并另列去重决定、reason/error code。每批最多 250 项；批记录与 checkpoint 在同一事务，WAL 写连接使用 `synchronous=FULL`。
- CLI 在开始读取前打印严格格式的随机 run token；成功时 JSON 也返回它，失败或中断后可用该 token 与同一 journal 恢复。任意调用者提供的路径形状或非随机令牌不会被回显。
- 没有通用任意数据库导入器。后续任何业务写入仍需明确的内部迁移接口、正式领域校验、前置快照和可回滚批次；本次不绕过 Gateway。

## Legacy Reality Audit 与 Migration Matrix

| 类别 | found | REUSE | planned import | content-hash 去重决定 | ARCHIVE-only | SKIP | unresolved | errors |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Study | 537 | 537 | 0 | 0 | 0 | 0 | 0 | 0 |
| Documents | 511 | 511 | 0 | 0 | 0 | 0 | 0 | 0 |
| Assets | 70 | 0 | 0 | 4 | 0 | 0 | 70 | 0 |
| Wrong Answers | 28 | 0 | 0 | 0 | 0 | 0 | 28 | 0 |
| Raw transcripts | 55 | 0 | 0 | 0 | 55 | 0 | 0 | 0 |
| Atomic Facts | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| Other / Unsupported | 7 | 0 | 0 | 0 | 0 | 7 | 0 | 0 |
| History | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

本次清单共 1,209 项，互斥结果对账为：1,048 项复用、55 项 ARCHIVE-only、7 项 SKIP、99 项 unresolved、0 项 planned import、0 项 committed、0 项已解决的去重结果、0 项 error；总计与 found 一致。另有 4 个 Asset 的 `content_hash` 决定表示字节已存在于 V2，但其错题关系仍 unresolved，因此不把它们误计为已解决迁移。源数据字节合计约 42.75 GB；候选导入估算为 33 B，可执行导入为 0 B。

### Study 与 QMD

- V2 的 Study root 与旧权威 StudyVault 是同一目录。没有复制 Markdown/PDF，也没有改写 Study 原文件。
- 没有把旧 QMD index 作为权威或复制为新数据。另在临时目录创建空 QMD index，仅从权威 Study root 重建 `studyvault` collection；临时 index 为 5,754,880 bytes，临时状态随验证结束清理。
- 新建索引后，`二次函数`、`三角形全等`、`机械能` 分别返回 3、1、1 条结果；虚构无结果查询返回 0。重建前后 Study 树、当前 V2 QMD config/index 的 hash、大小和修改时间均未变化。

### History、Assets 和 Wrong Answers

- 55 个聊天 Markdown 是 Basic Memory 已导入的文件，不是已验证的原始聊天导出。其 30 个文件大于当前 History 单条 100 KiB 上限，最大约 5.8 MiB；现有 History contract 还要求消息级 role 和会话 ID。为保持 lossless，不解析或改写这些内容。
- Legacy source hash 字段无法与受允许根目录中的现有 Markdown 文件 hash 对上；没有沿文件内的路径字段扩展扫描到其他目录。
- 旧 Native Memory fact 保留为 Atomic Fact/annotation 类型，绝不标成 user/assistant 原始消息。V2 History 配置为 `not_configured`，也没有能承载该 annotation 的迁移 contract，因此实际写入为零。
- 28 条错题笔记缺少稳定来源 ID、source ref、版本、可靠时间和 provenance。70 张图与笔记没有可证明配对关系；不猜题源、不创建 Wrong Answer。4 张图片的原始 SHA 与当前 4 个 V2 Asset blob 匹配，target stored bytes 的 SHA 校验通过；这 4 项仍保留关系 unresolved。其余 66 张没有目标 hash 命中，保持旧档案。
- 当前 V2 已有 5 个 Wrong Answer Source 与 5 个 Analysis、4 个唯一 Asset；既有 Gateway read-back 证据有效。本次没有重复注册或改写这些记录，旧笔记没有足够 legacy identity 可与它们合并。

## P11.3A — Unified AI / Agent Conversation History

**状态：BLOCKED，未导入。** 本次新增的统一来源盘点是 P11 正式范围；它不改变既有 1,209 项 Legacy inventory，也不把 app 安装记录当成聊天记录。

- 本地私有 conversation-source registry 已创建，当前有 7 个来源条目：ChatGPT 官方导出、Gemini 官方导出、Legacy Markdown archive，以及 Codex、WorkBuddy、Hermes 的安装/数据来源。POSIX 存储目录/数据库为 owner-only；Windows 默认落在用户状态目录。公共摘要只包含聚合数量与固定状态码，跨来源总数明确标为来源报告之和；账号、标识、私有路径和哈希留在本地。
- Legacy Basic Memory 中既有的 55 个聊天 Markdown 仍是 archive-only：它们不能证明平台会话 ID、message role/author、event time 或原始消息边界，因此不被计作 55 个已验证 conversation，也不转成 raw History messages。
- ChatGPT 官方导出尚未请求。Privacy Portal 打开后显示 Cloudflare 安全验证；没有输入账号、密码、验证码或提交请求，也没有绕过挑战。此项为 `WAITING_FOR_USER: CHATGPT_EXPORT_VERIFICATION`。
- Gemini 官方 Takeout 已只选择 `My Activity → Gemini Apps` 并提交一次性 ZIP 导出请求。官方详情页显示导出已完成（47.7 MB，页面列出的下载截止时间为 2026-10-04 16:06）；正常下载跳转到 Google 账号验证/reCAPTCHA。没有输入凭据或尝试解决验证，归档尚未落到本地，也未读取或检查。未选择其它 Google 产品或活动类别。此项为 `WAITING_FOR_USER: GEMINI_EXPORT_VERIFICATION_DOWNLOAD`。
- Codex 与 WorkBuddy 客户端已在有界主机盘点中发现。Codex 明确 sessions 目录仅盘点元数据，存在 **70 个 `.jsonl` 候选文件、306,937,852 bytes**；没有打开候选文件、创建原始副本或计算内容 hash，因此 conversation/message 数、文件完整性、role 与消息边界均未知，70 个候选 source items 保持 unresolved。WorkBuddy 安装元数据报告版本 **5.6.2**。官方 [Conversation Memory 文档](https://www.workbuddy.ai/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Memory)只说明从对话提取的摘要；其 [FAQ](https://www.workbuddy.ai/docs/workbuddy/From-Beginner-to-Expert-Guide/FQA)说明诊断日志可能含 conversation records。这不构成原始会话导出，本次未查看日志。本机没有通过 UI 确认 WorkBuddy 的日志目录或 MCP 设置。另有官方 [CodeBuddy Code CLI 文档](https://www.workbuddy.ai/docs/cli/headless)描述 CLI 会话恢复和 JSON 流；这些 CLI 文档不能证明本机安装的 WorkBuddy 桌面端使用同一数据源或暴露原始会话，因此仅作为待验证线索，不据此计数或导入。Hermes 官方 [Sessions 文档](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/sessions.md)说明 `state.db` 是会话存储，并支持 `HERMES_HOME`；在当前配置的数据根内发现该 SQLite 文件。通过迁移器的 DB+WAL 私有临时快照，检查了 schema、`quick_check` 和 `sessions`/`messages` 行数：**27 sessions、5,666 message rows**。未查询或输出会话/消息正文、标题、用户 ID、时间或附件；临时快照已清理。私有 registry 保存该快照的 manifest hash 和私有 locator，公共文档不保存。History target 未配置，尚未规范化、去重或导入，5,666 行均保持 unresolved。未读取浏览器凭据、cookie、token 或系统密钥库。
- History 后端仍为 `not_configured`，当前 capability 仅为 `read`。没有 V2 History、Assets、Documents 或 Wrong Answer 业务写入。新增了仅针对官方 ChatGPT/Gemini ZIP 的私有 raw archive 存储组件，并通过合成文件验证精确保留、上限、重复校验和中断恢复；当前没有任何真实归档落盘，也没有规范化记录或 retrieval E2E。
- 新增私有 registry 的合成测试在 Windows 为 **18 passed, 2 skipped**（两个 POSIX 权限位断言不适用）；与现有 migration journal 测试合并运行共 **37 passed, 2 skipped**。历史完整回归 **365 passed, 5 skipped** 属于先前 checkpoint，本次没有重复运行。

P11.3A subgates：Conversation Source Inventory、V1 Conversation Deduplication、Local Agent History Import（包括已发现的 Hermes store）、Gemini Export/Import（需用户完成账号验证并下载）、真实 Raw Archive Integrity、Normalization、Attachments、Cross-source Dedupe、Ordering、Retrieval E2E 与 Coverage Report 均为 **BLOCKED**；ChatGPT Export/Import 为 **WAITING_FOR_USER**（需用户完成 Privacy Portal 安全验证）。Raw archive 存储组件的合成验证通过不等于来源归档 Gate 通过。任何导出只有在官方 archive 可用并校验原始格式后才进入解析；未知时间、role、identity、分支或附件关系继续保持 unknown。

## Manifest、事务和回滚

- 真实 dry-run 的安全 run token 可用于恢复，私有 journal 不含原文和本机绝对路径。当前 run 有 5 个 manifest/checkpoint batch。相同真实 run 重放两次后 JSON 摘要及 checkpoint 数完全一致；合成测试还覆盖冲突来源 ID、相同 ID 的重复分类、重复 blob、planned→committed 单行状态更新、崩溃批次和 journal 恢复。
- 真实源文件未移动、删除或覆盖。Study/Personal 树元数据及 Native Memory、V2 Asset 数据库和 `-wal/-shm/-journal` sidecar 在 run 前后核对一致。SQLite 数据库和 WAL 只复制到临时私有 scratch 读取；合成 WAL 用例也验证源 DB/WAL/SHM 字节与元数据不变。无业务目标写入，因此不创建 target snapshot。
- 由于没有业务库写入，未创建 V2 target snapshot；业务数据 rollback 为 N/A。journal 本身每批事务化，冲突批次整个回滚，不影响已 checkpoint 批次。

## 验证

- 干跑状态为 **BLOCKED**，固定阻断代码：`history_target_not_configured`、`source_relation_unresolved`。
- 4 个与现有 V2 Asset 相同的旧图片通过 source bytes SHA-256 → target stored bytes SHA-256 校验；没有新 Asset 导入，所以新导入 hash 校验为 N/A。4 项关系仍 unresolved。
- 临时 QMD rebuild 与 Study 检索通过；History 无目标记录，History retrieval 为 BLOCKED。没有旧 Wrong Answer 写入，因此旧 Wrong Answer retrieval/read-back 为 N/A；当前 V2 的 5 条记录已有先前 Gateway read-back 证据。
- 完整回归：**365 passed, 5 skipped**。跳过项是受保护的真实 Codex/QMD smoke 未启用，以及当前主机不能创建 junction/symlink 的环境限制。
- Privacy/Git 检查未发现旧 StudyVault、聊天正文、照片、真实题目、数据库、私有 journal、绝对用户路径或源文件名进入 Git；本机 journal 存放在仓库外。

## Migration Gate

| Gate | 状态 | 说明 |
|---|---|---|
| Architecture | PASS | 单一 Agent 智能层；新增工具仅本机只读 dry-run |
| Legacy Inventory | PASS | 明确根目录完整盘点，摘要不含正文或路径 |
| Study Strategy | PASS | 同一权威根原地复用，临时 QMD 重建和检索通过 |
| History Migration | BLOCKED | History 未配置，旧 fact annotation contract 未实现；无业务写入 |
| Unified Conversation Source Inventory | BLOCKED | 私有登记器记录 7 个来源条目；Hermes 本地 DB 仅确认 27 sessions/5,666 message rows；Codex 有 70 个未解析 JSONL 候选文件（不等于会话数）；WorkBuddy 原始聊天来源未核实；ChatGPT/Gemini 仍有登录阻断 |
| Unified Conversation History | BLOCKED | 无 raw archive、规范化、跨源去重或检索证据；ChatGPT 子门槛为 WAITING_FOR_USER |
| Assets/Documents | BLOCKED | Study PDF 可原地复用；70 张旧错题图均未能与 source 建立可信关系，4 个现有目标 hash 命中也仍属 unresolved |
| Wrong Answers | BLOCKED | 28 条 note 与 70 张图的关系无法验证 |
| Idempotency | PASS | manifest identity、冲突检测、重跑和 checkpoint 合成测试通过 |
| Transactions | PASS | journal 分批原子写与冲突批次回滚测试通过；业务库没有提交 |
| Rollback | N/A | 业务目标未改动、未需要恢复；因此没有 target snapshot |
| Provenance | N/A | 没有真实迁移写入；源时间保留、未知时间保持 null |
| Privacy | PASS | 路径/正文/journal 未入仓库或摘要；源树与 DB sidecar 前后核对一致 |
| Automated Tests | PASS | 完整回归 365 passed, 5 skipped；跳过原因见上文 |
| Dry Run | BLOCKED | 完整清单有明确 History 和 source-relation 阻断项 |
| Real Migration | BLOCKED | 预检未通过，业务库写入为零 |
| Count Reconciliation | PASS | 1,209 项按互斥结果完整对账；4 个内容 hash 决定作为额外子计数 |
| Hash Validation | PASS | 4 个现有 Asset 的源/目标 bytes hash 相同；没有新 Asset 导入 |
| Retrieval E2E | BLOCKED | Study PASS；History target 缺失；旧 Wrong Answer 未导入 |
| Git Hygiene | PASS | 真实数据、private config、journal、备份均未跟踪 |
| Documentation | PASS | 本文、current-state、architecture/privacy 与 roadmap 已同步 |

## 后续技术条件

1. 用户在受信任的本地 V2 配置中显式配置 History SQLite store，并启用所需本地能力；当前干跑器不会替用户改该配置。
2. 为 legacy Atomic Fact 定义独立于 raw History message 的受限 annotation storage/validation 与 Gateway provenance 入口。
3. 只有获得可靠旧 source↔image 对照后，才评估错题迁移；否则保持旧档案只读。
4. 设计并测试仅适用于受限迁移适配器的业务写入、前置 snapshot/restore、正式 domain validation、逐批 read-back 和按 run ID 识别的 rollback。

满足这些条件并重新运行完整 dry-run、测试和目标快照之前，不进入真实迁移或 v0.2.0 release preparation。
