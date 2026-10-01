# 当前状态

## P12 Step 4 — Cross-Agent Integration（v0.6.0，25/25 Gate PASS）

从 live v0.5.0 main/tag 继续，真实 Hermes 0.20.0 → WorkBuddy 5.7.3 → Codex CLI
0.159.2 fresh sessions 通过同一 shared isolated Gateway 完成 Document/source/v1、
独立发现并追加 v2、exact replay、实际 stale CONFLICT、末读无 v3 和 no-result。
A/B 退出后 C 原始 Asset/document/page/source/v1/v2 全 DTO exact-equal；历史
provenance/timestamps/refs/supersession 未改变，identity 仍 caller-reported/unverified。

最终三 Host 数据访问只用 native MCP；不共享上下文或人工转贴 DTO。旧失败尝试
保留且不计 PASS：Hermes 首轮文档/marker 不完整；WorkBuddy trust 前 script fallback
与 Memory 副本；Codex 初轮把 list 失败误当 workflow 不可读。仅补最小 Host 路由
指引，不重构 Gateway；生产配置与旧已验收 server definitions 保留。

现有 scoped Projection 两次生成14 Markdown，Markdown/manifest byte-identical。
版本同步为 0.6.0；targeted144 passed/4 skipped，full622 passed/12 skipped。
实际 public169/wheel42/sdist170 privacy、独立 clean install/stdio、diff 已通过。
最终 commit/tag push前审计与正常发布/远端核验按已授权流程执行，最终远端回执
记录于正式 GitHub Release。完整证据和已知 Host 展示限制见
[Step 4 checkpoint](p12-step4-cross-agent-checkpoint.md)。不重验既有单 Host Gate。

## P12 Step 3 — Hermes Integration（v0.5.0，22/22 Gate PASS）

从 v0.4.0/b75c62d checkpoint 继续，不重复已有 8 项 PASS。真实 Hermes Agent
v0.20.0 (2026.8.3) 使用内置 deepseek / deepseek-v4-pro / high 入口，原生 stdio
执行 production read-only 与独立 isolated controlled-write。官方 Host trace 证明
仅 Gateway 数据访问、三类 no-result，隔离对象仅 v1/v2，exact idempotency replay
与 stale CONFLICT 正常；身份仍 reported/unverified，Memory/profile disabled。
当前 22/22 Gate PASS，restart 与 scoped Projection 已通过。初次 restart 因 Agent
抄错 source ID 返回 INVALID_ARGUMENT，该轮不计 PASS，后续已用 Gateway search 回收实际 ID，并通过完整 DTO exact comparison。
发布版本为 0.5.0。针对性回归 89 passed / 2 skipped，全量 622 passed / 12 skipped；
完整历史与发布验证见 [Hermes checkpoint](p12-step3-hermes-checkpoint.md) 和
[v0.5.0 release notes](releases/v0.5.0.md)。远端验收回执在正式 Release 中记录。

## P12 Step 2 — WorkBuddy Integration（v0.4.0，21/21 Gate PASS）

真实 WorkBuddy 5.6.2 只读、隔离 controlled-write 及重启持久性由用户验收；
Gateway 补充回读确认同一测试 Source 和 versions 1/2，未创建 v3。
独立临时 MCP 名称避免托管 production 入口的同名解析问题，Basic Memory disabled。
所有读/计数/存在性/写入均要求 Gateway-only；最初 direct SQLite 验收作废。

隔离 Projection 经 Gateway → collector → renderer → writer 生成 14 个 Markdown，
latest v2、supersession、document refs、空 Study relations 和 provenance 正确；
两次 Markdown/manifest 字节稳定，未访问 production 或真实 StudyVault。
发布回归 targeted 65 passed / 1 skipped，full 617 passed / 12 skipped；
package、Gateway 配置与 MCP metadata 同步到 0.4.0，独立 installed-package stdio smoke 通过。
公开候选树 159 files、wheel 42 files、sdist 169 files 的隐私/metadata 审计通过；
实际新增 Git objects 在 commit 后、push 前按 v0.3.0..HEAD 审计。
完整证据以 [Step 2 checkpoint](p12-step2-workbuddy-checkpoint.md) 与
[v0.4.0 release notes](releases/v0.4.0.md) 为准。
下文 P11 / Step 1 版本与验证数字是历史基线，不代表当前 package 版本。

更新时间：2026-10-01。P1–P10 已完成；**P11 V1 来源迁移与 V2 cutover Gate：PASS**。P11 发布版本为 `0.2.0`；[正式 tag/Release](https://github.com/abdullejan25-max/chatgpt-study-system-v2/releases/tag/v0.2.0) 对应本次迁移范围。最终默认/dev 环境测试为 605 passed、12 skipped；完整验收见 [P11 Real Migration Completion](p11-real-migration-completion.md)。

V1 既有 1,209 项对账：150 项新增、1,052 项复用、7 项 skip、0 error。537 个 Study Markdown 与 511 个 Documents 原地复用。55 篇聊天档案、28 篇错题档案、1 条派生事实以明确类型保留原始字节；70 张图片中新增 66 个 Asset、复用 4 个内容重复。另有 82 个已验证 Codex JSONL 来源文件迁入，独立于 V1 对账。来源文档总数为 166，不能当作会话或消息数量。

全部来源/原图回读及同源重跑通过：166 个文档和 70 张图重跑新增均为零，ID 和原 imported_at 保持稳定。DB/WAL/原始 blobs 快照与隔离恢复通过；官方 MCP SDK 的两次全新 stdio 进程验证 History sqlite/ready、166 次按 ID 回读、跨来源检索、无结果 guard、97 个图引用及重启持久性。Study 检索返回 3 个结果；Study/Personal 原件的 root、大小和 mtime 前后保持一致，本次未重复 42GB 扫描。

旧错题有 97 个明确文档图片引用，覆盖 70 张图；完整业务语义仍有 28 篇 unresolved。未猜测题目、答案、图片角色或分析；现有 active Wrong Answer 为 5 个 Source、5 个 Analysis，未改变。Atomic Fact 是 derived source，Codex 是 source-only JSONL；canonical raw History message import 为 0。

私有配置选择 V2 为本项目权威运行系统。V1 未删除；[Deletion Candidate Report](v1-deletion-candidates.md) 将 Study 保留为权威来源，将原件和备份保留为档案。当前 Codex 对话已运行的 MCP 连接仍缓存旧 not_configured 配置与旧工具列表，需要重连；新进程验证不代表该旧连接已重载。

ChatGPT/Gemini 的私有 registry 保留 WAITING_FOR_USER；Hermes/WorkBuddy 后续来源规范化和客户端验证 deferred，不冒充迁移完成，也不作为本次 V1 迁移 blocker。P11 完成时，P12 Obsidian、WorkBuddy、Hermes 与合成跨客户端成果仅为准备状态；见 [P12 Host Compatibility](p12-host-compatibility.md) 与 [P12 Obsidian Reality Audit](p12-obsidian-reality-audit.md)。

架构保持 Agent thinks; Gateway executes。新增 migration 是本机内部、受领域校验的确定性写路径；新增 MCP API 只有来源读取，未开放 arbitrary SQL 或通用 Agent import。真实配置、数据、journal、源 hash 和恢复材料均留在 Git 外。v0.1.0 与旧发布历史未修改。

## P12 Step 1 — Obsidian Visualization

**Gate：PASS；目标发布版本 `0.3.0`。** 复用既有 collector、renderer 和 manifest-owned writer，新增 opt-in `legacy_sources` metadata 分页与现有 Vault 构建入口。166 个来源按 82 / 55 / 28 / 1 分类；canonical messages 保持 0；5 个 Wrong Answer Source 与 5 个 Analysis 未改变。

真实私有 Vault 生成 184 个 Markdown 文件及 manifest；逐文件 UTF-8 回读、相对链接和第二次独立构建字节一致。当前 Study root 为 1,146 files / 564 Markdown，索引引用原文件，大小/mtime 前后不变，不复制 Study。2026-10-01 用户人工确认 Dashboard、Sources、Wrong Answers、Knowledge Points、Error Types、Study 和关系图谱正常，V1/V2 共存边界清楚，无明显乱码、断链、重复页、私人路径泄露或原文异常。

Fresh official MCP stdio 正常；Codex Host resources/list 的兼容问题独立 deferred，不阻塞投影。旧 P12 preparation 文档是历史快照；本次 Step 1 证据以 [真实投影检查点](p12-step1-real-projection-checkpoint.md) 与 [v0.3.0 notes](releases/v0.3.0.md) 为准。WorkBuddy/Hermes/Cross-Agent、消息规范化、V1 删除及增量重设计均未纳入本次范围。

## Final release verification (2026-10-01)

The default/dev full suite passed **614 tests, 12 skipped**. Skips cover existing platform/symlink, opt-in Host/QMD and optional PDF/OCR conditions; actual fresh official MCP and real-Vault checks were run separately. Wheel and source distribution build passed. Package audits confirm version `0.3.0`, Apache-2.0 license metadata/LICENSE, canonical workflow data and optional-only PyMuPDF; no private config, Vault, images, databases or raw exports are included. The public tree and new Git objects are audited before push. Real 0.3.0 Gateway health and stable 166-source/184-file projection were revalidated after installation.
