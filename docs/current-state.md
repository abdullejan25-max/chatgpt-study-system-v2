# 当前状态

更新时间：2026-09-30。P1–P10 已完成；**P11 V1 来源迁移与 V2 cutover Gate：PASS**。版本为 `0.2.0`；[正式 tag/Release](https://github.com/abdullejan25-max/chatgpt-study-system-v2/releases/tag/v0.2.0) 对应本次迁移范围。最终默认/dev 环境测试为 605 passed、12 skipped；完整验收见 [P11 Real Migration Completion](p11-real-migration-completion.md)。

V1 既有 1,209 项对账：150 项新增、1,052 项复用、7 项 skip、0 error。537 个 Study Markdown 与 511 个 Documents 原地复用。55 篇聊天档案、28 篇错题档案、1 条派生事实以明确类型保留原始字节；70 张图片中新增 66 个 Asset、复用 4 个内容重复。另有 82 个已验证 Codex JSONL 来源文件迁入，独立于 V1 对账。来源文档总数为 166，不能当作会话或消息数量。

全部来源/原图回读及同源重跑通过：166 个文档和 70 张图重跑新增均为零，ID 和原 imported_at 保持稳定。DB/WAL/原始 blobs 快照与隔离恢复通过；官方 MCP SDK 的两次全新 stdio 进程验证 History sqlite/ready、166 次按 ID 回读、跨来源检索、无结果 guard、97 个图引用及重启持久性。Study 检索返回 3 个结果；Study/Personal 原件的 root、大小和 mtime 前后保持一致，本次未重复 42GB 扫描。

旧错题有 97 个明确文档图片引用，覆盖 70 张图；完整业务语义仍有 28 篇 unresolved。未猜测题目、答案、图片角色或分析；现有 active Wrong Answer 为 5 个 Source、5 个 Analysis，未改变。Atomic Fact 是 derived source，Codex 是 source-only JSONL；canonical raw History message import 为 0。

私有配置选择 V2 为本项目权威运行系统。V1 未删除；[Deletion Candidate Report](v1-deletion-candidates.md) 将 Study 保留为权威来源，将原件和备份保留为档案。当前 Codex 对话已运行的 MCP 连接仍缓存旧 not_configured 配置与旧工具列表，需要重连；新进程验证不代表该旧连接已重载。

ChatGPT/Gemini 的私有 registry 保留 WAITING_FOR_USER；Hermes/WorkBuddy 后续来源规范化和客户端验证 deferred，不冒充迁移完成，也不作为本次 V1 迁移 blocker。P12 现有 Obsidian、WorkBuddy、Hermes 与合成跨客户端准备成果保留，未扩展新产品功能；见 [P12 Host Compatibility](p12-host-compatibility.md) 与 [P12 Obsidian Reality Audit](p12-obsidian-reality-audit.md)。

架构保持 Agent thinks; Gateway executes。新增 migration 是本机内部、受领域校验的确定性写路径；新增 MCP API 只有来源读取，未开放 arbitrary SQL 或通用 Agent import。真实配置、数据、journal、源 hash 和恢复材料均留在 Git 外。v0.1.0 与旧发布历史未修改。
