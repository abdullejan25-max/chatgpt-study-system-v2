# 72-Hour Autonomous Continuation Status

更新时间：2026-09-27

## 当前状态

- 当前分支：`phase-11-legacy-migration`
- 最近功能提交：`bcb76d6`（新增仅经合成 fixture 验证的 Codex occurrence adapter，不接真实快照或数据库）。
- 当前阶段：P11，步骤 P11.3A Unified AI / Agent Conversation History
- P11 状态：**BLOCKED**。没有官方导出 ZIP、规范化、真实迁移、V2 业务写入或发布；Codex 候选完成私有原始快照和 aggregate-only 结构检查，不代表 canonical 计数或迁移。
- P12：仅做安全准备；没有真实 Obsidian、WorkBuddy、Hermes 或 Cross-Agent Gate PASS。

## 已完成的安全工作

- 保留既有 P11 dry-run/journal 与 1,209 项 inventory；没有重扫约 42.75 GB 的旧来源。
- 新增私有 conversation-source registry，校验固定状态词、计数、UTC 时间、哈希和覆盖说明；POSIX 存储目录/数据库为 owner-only，Windows 默认落在用户状态目录；公共摘要仅输出汇总计数与固定状态码，跨来源总数明确标为来源报告之和。
- 根据只读代码审查修复目录权限问题：默认数据库改放专用目录；若 POSIX 上该目录已存在但权限对 group/other 开放，则初始化失败且不改原权限。6 条旧 registry 记录已复制并逐条回读验证，摘要一致；旧 registry 哈希未变，作为恢复副本保留。复审未发现新问题。
- 运行新增 registry 与现有 migration journal 的定向测试：**37 passed, 2 skipped**（两个 POSIX 权限位断言不适用于 Windows）。先前完整回归记录为 **365 passed, 5 skipped**；本次未重跑。
- 用只读主机盘点发现 Obsidian、WorkBuddy、Hermes 已安装；安装事实不代表聊天数据可访问或 MCP 集成通过。
- 官方 Google Takeout 的 Gemini Apps 导出已完成；详情页显示 47.7 MB，下载截止时间为 2026-10-04 16:06。下载跳转到 Google 账号验证/reCAPTCHA；没有尝试求解或输入凭据，归档未落盘。私有 registry 状态为 `WAITING_FOR_USER`，conversation/message 数仍未知。
- 根据 Hermes 官方 Sessions 文档定位 `HERMES_HOME/state.db`；仅对 DB+WAL 私有临时快照做 SQLite schema / `quick_check` 与表行数查询，确认 **27 sessions、5,666 message rows**，未查询会话/消息文本、title、用户 ID 或时间。私有 registry 保存 snapshot manifest hash 与 locator；临时副本已清理，V2 没有写入。
- Codex sessions 目录的最新元数据盘点及字节快照复验为 82 个 `.jsonl` 候选文件、322,967,757 bytes；仅做有界结构检查，没有输出正文或推断 canonical 会话/消息数。之前 checkpoint 的 70 个文件、306,937,852 bytes 与本次差异未解释。私有 registry 已记录 `raw_format=jsonl`、82 个 unresolved source items 及私有摘要；conversation/message counts 仍未知。
- 新增显式 `projection` capability 与只读 `projection_snapshot` MCP/Gateway 接口。History 与 Wrong Answer 分别使用独立 SQLite 高水位 token；支持来源/记录分页、每域 10,000 条与 32 MiB 上限、固定错误、逻辑 URI 校验和 provenance 分类字段白名单。普通 `read` 不显示也不能调用该工具。没有访问任何真实 History/Wrong Answer 数据库。
- 新增 projection collector：按独立 store 水位完整读取所有来源及记录页，核对来源数、来源记录数与 domain 总数，检测重复/不前进 cursor，并且只在完整核对后返回 renderer snapshot。没有跨 store 原子性保证。
- 合成验证：projection/collector/writer suite **36 passed, 1 skipped**；全量测试 **433 passed, 8 skipped**。端到端覆盖 Gateway collection → renderer → manifest writer，并验证读取不新增 DB audit。流水线测试发现嵌套完整 SHA 路径在 Windows 临时根下超长；现已改为单一组合身份 SHA-256 路径。
- 整分支只读复审（`64d7849..3a9339b`）未发现 P0/P1；发现的 Obsidian writer 风险均已修复并复审：拒绝写入仓库重叠目录；更新失败时恢复旧文件与 manifest；若恢复失败保留带映射的恢复目录；manifest 列出的缺失文件也能正确回滚；备份/空目录/staging 清理失败会明确设置状态。相关 renderer/writer/collector 模块定向验证 **44 passed, 1 skipped**；没有真实 Vault 或个人投影。
- Codex JSONL snapshot 与 registry 定向测试 **33 passed, 4 skipped**；与 raw ZIP 和 migration manifest 回归合并运行 **62 passed, 4 skipped**。全量回归未重跑。
- 独立 Codex JSONL 结构检查器、私有 snapshot/registry 与 History 合约回归 **57 passed, 4 skipped**；没有运行全量套件。检查器兼容已观察到的外层与嵌套 session metadata ID 字段，并在两者冲突时失败关闭。基于结构观察新增 lossless History envelope 设计提案；仅为文档，不改 schema、Gateway 或业务数据。
- 合成-only History occurrence DTO 已加入：保留 typed block 边界、open role/kind、原始时间字符串、record ordinal 与可选 source-declared ordering，敏感字段从 `repr()` 隐藏。与 inspector 和 History 合约回归 **36 passed**；DTO 未接入真实 importer、Gateway 或数据库。
- 合成-only Codex line adapter 已加入：仅映射明确 role、ID、原始 timestamp 和 text block；图片、音频、工具/事件及未知结构通过 snapshot locator 保留。未知 conversation/order/title/model/branch 不补猜。adapter/DTO/inspector/History 定向回归 **42 passed**；没有运行个人快照或真实数据库。

## P11.3A 来源覆盖

私有登记器有 7 个来源条目（本次以只读行数核对）；跨来源 conversation/message 总数仍未知（来源间可能重叠）。Hermes 当前可访问 SQLite snapshot 报告 27 sessions、5,666 message rows。

| 来源 | 当前证据与状态 |
|---|---|
| ChatGPT | 官方 Privacy Portal 显示 Cloudflare 安全验证，未提交导出请求或尝试绕过验证。`WAITING_FOR_USER: CHATGPT_EXPORT_VERIFICATION` |
| Gemini | 官方导出已完成，详情页为 47.7 MB，截止 2026-10-04 16:06；下载跳转到 Google 账号验证/reCAPTCHA。没有输入凭据或解决挑战，归档未本地下载或检查。`WAITING_FOR_USER: GEMINI_EXPORT_VERIFICATION_DOWNLOAD` |
| Legacy Markdown | 既有 55 项保持 archive-only；文件数不等于已验证的 conversation/message 数。 |
| Hermes | 官方文档确认会话存入 `state.db`；当前配置位置的副本 integrity 为 `ok`，27 sessions、5,666 message rows。仅查 SQLite 结构、完整性与行数，没有查正文或时间。History target 未配置，仍 `BLOCKED`，全部 message rows 未导入。 |
| Codex | 最新元数据盘点和已复验的私有字节快照包含 82 个 `.jsonl` 候选文件、322,967,757 bytes；此前记录的 70 个文件、306,937,852 bytes 差异未解释。结构统计观察到 60,846 条有效 JSON 记录、1,988 条 message-shaped records、100 条 metadata IDs 全位于外层 `payload.id`（77 个 distinct 值）、11 组时间戳冲突的重复 message ID，以及 21 个内嵌图片 data URI（14 个唯一）。这些不是 canonical conversation/message counts；正文未输出，尚未规范化或导入。 |
| WorkBuddy | 安装元数据报告版本 5.6.2；本地聊天存储和可访问的原始导出仍未验证。官方 [Conversation Memory 文档](https://www.workbuddy.ai/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Memory)说明记忆是从对话提取的摘要；[FAQ](https://www.workbuddy.ai/docs/workbuddy/From-Beginner-to-Expert-Guide/FQA)说诊断日志可能含对话记录；[跨设备任务文档](https://www.workbuddy.ai/document/cross-device-tasks)描述已授权连接设备可查看桌面任务对话历史。这只确认了文档所述的应用内查看路径，没有确认原始导出或本地存储格式。 |

History 仍未配置，当前 capability 仅为 `read`。官方 ChatGPT/Gemini ZIP ingest 组件只用合成归档验证；没有真实官方 ZIP 导出落盘。Codex 原始 JSONL 候选已做私有字节快照，并经独立只读检查器做有界结构计数；未输出正文，也未规范化。真实会话 identity、canonical 会话/消息数、跨源去重、附件处理、History 导入、read-back 和 retrieval E2E 仍未完成。未知 role、author、时间语义、thread、message boundary、分支或附件关系保持 unknown。

## P12 状态

- **Step 1 — Obsidian**：纯内存 renderer、History 时间线、独立 manifest-bounded writer、opt-in per-store Gateway 枚举接口及 reconciliation collector 均已实现并通过合成测试。原 synthetic end-to-end **36 passed, 1 skipped**；本次 writer 安全修复后的三个相关模块 **44 passed, 1 skipped**。先前全量回归 **433 passed, 8 skipped**，本次未重跑。无个人 snapshot。writer 仅经 synthetic 目录验证。真实 Vault/GUI 未检查，O1–O13 和 P12 Step 1 release gate 仍未通过，详见 [Obsidian Reality Audit](p12-obsidian-reality-audit.md)。
- 新增的 Host-neutral process smoke 通过独立 MCP SDK 验证真实 stdio 子进程在仅有 `read` 时隐藏 `projection_snapshot`，在显式 `projection` 时展示只读工具并分页读取合成 History projection；与 History/Wrong Answer MCP capability 测试合计 **24 passed**。这不是 WorkBuddy/Hermes Host E2E。
- **Step 2 — WorkBuddy**：官方文档确认提供本地 stdio MCP 配置；本机 Gateway 配置和真实 E2E 未验证，仍需用户启用/配置。
- **Step 3 — Hermes**：官方文档确认支持本地 stdio MCP；本机 Gateway 配置和真实 E2E 未验证，仍需用户启用/配置。
- **Step 4 — Cross-Agent**：被前置真实 Host gate 阻断；无跨 Host 写读、版本或投影验证。

## WAITING_FOR_USER

1. **ChatGPT 导出**：在官方 Privacy Portal 标签页由用户本人完成 Cloudflare 安全验证；随后再提交官方数据导出请求。没有读取或输入凭据、验证码、cookie 或 token。
2. **History 目标**：在受信任的本机私有配置中配置 History store，并启用所需写能力。当前工作不会修改私有配置。
3. **Obsidian GUI**：打开目标 Vault，确认可用于只读人类视图；工具当前未完成真实 GUI 检查。
4. **WorkBuddy / Hermes**：按各 Host 的正式设置启用 MCP/Gateway 连接，并提供相应本机授权；未用临时配置或伪造 host PASS。
5. **WorkBuddy 历史来源**：在桌面端确认任务/对话历史是否提供正式原始导出或明确的本地来源。官方文档仅证明已授权连接设备可查看历史；没有访问本机 UI 或诊断日志。
6. **Gemini 导出下载**：官方归档已完成，但下载跳转到 Google 账号验证/reCAPTCHA。请在官方 Takeout 页面由用户本人完成验证并下载；当前没有本地 raw archive，下载截止时间页面显示为 2026-10-04 16:06。

## 独立工程前置

- **Projection snapshot consistency**：Gateway API 与 collector 已实现，并通过合成数据核对 per-source/per-domain counts。History 与 Wrong Answer 位于不同 SQLite 数据库，不能声称存在跨库原子快照；真实私有配置未启用 projection，因此个人快照与 Vault Gate 仍需等待用户配置/授权及 GUI。
- **Private raw snapshots**：ChatGPT/Gemini ZIP ingest 仍只通过合成归档验证，限制最大 512 MiB、50,000 entries、2 GiB 展开量和 200:1 单成员压缩比。新增 Codex JSONL-only 私有快照器，执行有界枚举、精确字节复制、清单/逐文件 SHA-256 复验和幂等校验；Windows 长路径复验已覆盖。独立只读 inspector 对已验证快照观察到 82 个文件、60,846 条有效 JSON 记录、1,988 条 message-shaped records、77 个 distinct session metadata IDs；这些不是规范化或 canonical conversation/message counts。检查未输出正文；登记器中 conversation/message counts 仍未知，History 无写入。P11 仍为 BLOCKED。

## 发布与隐私

- `v0.1.0` 未改；没有创建 `v0.2.0` tag/Release，也没有 push。
- 原始对话、导出、账号数据、真实路径、源哈希和私有 source registry 均未进入 Git。
- WorkBuddy 与 Hermes 的 stdio 客户端能力已按官方文档确认；本机连接、工具调用和跨 Host E2E 仍未验证，详见 [P12 Host Compatibility Checkpoint](p12-host-compatibility.md)。
- Obsidian O1 contracts and missing facets are documented in [P12 Obsidian Reality Audit](p12-obsidian-reality-audit.md); private Vault selection and GUI remain user gates.
- 应用内已安排本地线程每 6 小时续作一次，覆盖 72 小时；状态无变化时保持安静。
- 下一安全步骤：WorkBuddy 需用户在桌面端核实官方文档提到的历史入口及是否有原始导出；同时可继续 Host-neutral P12 准备。Codex 候选文件在取得受限格式证据前不解析。保持 V2 私有 History/错题读取禁用，直到受信任配置明确启用。维护 WAITING_FOR_USER 清单，不重复提交 Gemini 导出；不执行真实业务写入或发布。
