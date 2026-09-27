# 72-Hour Autonomous Continuation Status

更新时间：2026-09-27

## 当前状态

- 当前分支：`phase-11-legacy-migration`
- Last safe implementation commit：`4a826d6` (`fix: keep history projection paths Windows-safe`)
- 当前阶段：P11，步骤 P11.3A Unified AI / Agent Conversation History
- P11 状态：**BLOCKED**。没有真实迁移、V2 业务写入或发布。
- P12：仅做安全准备；没有真实 Obsidian、WorkBuddy、Hermes 或 Cross-Agent Gate PASS。

## 已完成的安全工作

- 保留既有 P11 dry-run/journal 与 1,209 项 inventory；没有重扫约 42.75 GB 的旧来源。
- 新增私有 conversation-source registry，校验固定状态词、计数、UTC 时间、哈希和覆盖说明；POSIX 存储目录/数据库为 owner-only，Windows 默认落在用户状态目录；公共摘要仅输出汇总计数与固定状态码，跨来源总数明确标为来源报告之和。
- 根据只读代码审查修复目录权限问题：默认数据库改放专用目录；若 POSIX 上该目录已存在但权限对 group/other 开放，则初始化失败且不改原权限。6 条旧 registry 记录已复制并逐条回读验证，摘要一致；旧 registry 哈希未变，作为恢复副本保留。复审未发现新问题。
- 运行新增 registry 与现有 migration journal 的定向测试：**37 passed, 2 skipped**（两个 POSIX 权限位断言不适用于 Windows）。先前完整回归记录为 **365 passed, 5 skipped**；本次未重跑。
- 用只读主机盘点发现 Obsidian、WorkBuddy、Hermes 已安装；安装事实不代表聊天数据可访问或 MCP 集成通过。
- 官方 Google Takeout 的 Gemini Apps 导出已完成；页面显示 47.7 MB，下载截止时间为 2026-10-04 16:06。尝试下载时跳转到 Google 登录；未输入凭据或验证码，未下载本地归档。相应 registry 状态已更新为 `available`，conversation/message 数仍未知。
- 根据 Hermes 官方 Sessions 文档定位 `HERMES_HOME/state.db`；仅对 DB+WAL 私有临时快照做 SQLite schema / `quick_check` 与表行数查询，确认 **27 sessions、5,666 message rows**，未查询会话/消息文本、title、用户 ID 或时间。私有 registry 保存 snapshot manifest hash 与 locator；临时副本已清理，V2 没有写入。
- 在明确的 Codex sessions 数据目录仅盘点文件元数据：70 个 `.jsonl` 候选文件，合计约 307 MB；没有打开文件或推断会话/消息数。私有 registry 将 70 个候选文件记为未解析 source items，conversation/message counts 仍未知。
- 新增显式 `projection` capability 与只读 `projection_snapshot` MCP/Gateway 接口。History 与 Wrong Answer 分别使用独立 SQLite 高水位 token；支持来源/记录分页、每域 10,000 条与 32 MiB 上限、固定错误、逻辑 URI 校验和 provenance 分类字段白名单。普通 `read` 不显示也不能调用该工具。没有访问任何真实 History/Wrong Answer 数据库。
- 新增 projection collector：按独立 store 水位完整读取所有来源及记录页，核对来源数、来源记录数与 domain 总数，检测重复/不前进 cursor，并且只在完整核对后返回 renderer snapshot。没有跨 store 原子性保证。
- 合成验证：projection/collector/writer suite **36 passed, 1 skipped**；全量测试 **433 passed, 8 skipped**。端到端覆盖 Gateway collection → renderer → manifest writer，并验证读取不新增 DB audit。流水线测试发现嵌套完整 SHA 路径在 Windows 临时根下超长；现已改为单一组合身份 SHA-256 路径。

## P11.3A 来源覆盖

私有登记器有 6 个来源条目；跨来源 conversation/message 总数仍未知（来源间可能重叠）。Hermes 当前可访问 SQLite snapshot 报告 27 sessions、5,666 message rows。

| 来源 | 当前证据与状态 |
|---|---|
| ChatGPT | 官方 Privacy Portal 的“下载我的数据”流程要求账户登录；未提交导出请求。`WAITING_FOR_USER: CHATGPT_EXPORT` |
| Gemini | 官方导出已完成，可下载 47.7 MB，截止 2026-10-04 16:06；下载跳转到 Google 登录。归档未本地下载或检查，`WAITING_FOR_USER: GEMINI_EXPORT_SIGN_IN_DOWNLOAD`。 |
| Legacy Markdown | 既有 55 项保持 archive-only；文件数不等于已验证的 conversation/message 数。 |
| Hermes | 官方文档确认会话存入 `state.db`；当前配置位置的副本 integrity 为 `ok`，27 sessions、5,666 message rows。仅查 SQLite 结构、完整性与行数，没有查正文或时间。History target 未配置，仍 `BLOCKED`，全部 message rows 未导入。 |
| Codex | 已发现 70 个 `.jsonl` 候选文件（不是已验证的 conversation 数）；没有读取内容，conversation/message counts 与 role、边界、身份仍未知，导入未开始。 |
| WorkBuddy | 已发现客户端安装；本地聊天存储和可访问的原始导出仍未验证。官方 [Conversation Memory 文档](https://www.workbuddy.ai/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Memory)说明记忆是从对话提取的摘要；[FAQ](https://www.workbuddy.ai/docs/workbuddy/From-Beginner-to-Expert-Guide/FQA)说诊断日志可能含对话记录。这些资料没有证明存在可用的原始聊天导出。 |

History 仍未配置，当前 capability 仅为 `read`。Raw archive、规范化、跨源去重、附件处理、History 导入、read-back 和 retrieval E2E 均未完成。未知 role、author、时间、thread、message boundary、分支或附件关系保持 unknown。

## P12 状态

- **Step 1 — Obsidian**：纯内存 renderer、History 时间线、独立 manifest-bounded writer、opt-in per-store Gateway 枚举接口及 reconciliation collector 均已实现并通过合成测试。synthetic end-to-end **36 passed, 1 skipped**，全量回归 **433 passed, 8 skipped**。无个人 snapshot。writer 仅经 synthetic 目录验证。真实 Vault/GUI 未检查，O1–O13 和 P12 Step 1 release gate 仍未通过，详见 [Obsidian Reality Audit](p12-obsidian-reality-audit.md)。
- **Step 2 — WorkBuddy**：官方文档确认提供本地 stdio MCP 配置；本机 Gateway 配置和真实 E2E 未验证，仍需用户启用/配置。
- **Step 3 — Hermes**：官方文档确认支持本地 stdio MCP；本机 Gateway 配置和真实 E2E 未验证，仍需用户启用/配置。
- **Step 4 — Cross-Agent**：被前置真实 Host gate 阻断；无跨 Host 写读、版本或投影验证。

## WAITING_FOR_USER

1. **ChatGPT 导出**：在保留的官方 Privacy Portal 标签页完成账户登录及平台要求的验证；之后才能继续提交官方数据导出请求。没有读取或输入凭据、验证码、cookie 或 token。
2. **History 目标**：在受信任的本机私有配置中配置 History store，并启用所需写能力。当前工作不会修改私有配置。
3. **Obsidian GUI**：打开目标 Vault，确认可用于只读人类视图；工具当前未完成真实 GUI 检查。
4. **WorkBuddy / Hermes**：按各 Host 的正式设置启用 MCP/Gateway 连接，并提供相应本机授权；未用临时配置或伪造 host PASS。
5. **Gemini 导出下载**：官方归档已完成，但下载页要求 Google 登录。请在官方 Takeout 页面完成账户登录/验证后再下载；当前没有本地 raw archive，下载截止时间页面显示为 2026-10-04 16:06。

## 独立工程前置

- **Projection snapshot consistency**：Gateway API 与 collector 已实现，并通过合成数据核对 per-source/per-domain counts。History 与 Wrong Answer 位于不同 SQLite 数据库，不能声称存在跨库原子快照；真实私有配置未启用 projection，因此个人快照与 Vault Gate 仍需等待用户配置/授权及 GUI。

## 发布与隐私

- `v0.1.0` 未改；没有创建 `v0.2.0` tag/Release，也没有 push。
- 原始对话、导出、账号数据、真实路径、源哈希和私有 source registry 均未进入 Git。
- WorkBuddy 与 Hermes 的 stdio 客户端能力已按官方文档确认；本机连接、工具调用和跨 Host E2E 仍未验证，详见 [P12 Host Compatibility Checkpoint](p12-host-compatibility.md)。
- Obsidian O1 contracts and missing facets are documented in [P12 Obsidian Reality Audit](p12-obsidian-reality-audit.md); private Vault selection and GUI remain user gates.
- 应用内已安排本地线程每 6 小时续作一次，覆盖 72 小时；状态无变化时保持安静。
- 下一安全步骤：继续核实 WorkBuddy 的正式聊天来源，或推进其它 Host-neutral P12 合成兼容工作；Codex 候选文件在取得受限格式证据前不解析。保持 V2 私有 History/错题读取禁用，直到受信任配置明确启用。维护 WAITING_FOR_USER 清单，不重复提交 Gemini 导出；不执行真实业务写入或发布。
