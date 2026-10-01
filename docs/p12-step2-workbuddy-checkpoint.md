# P12 Step 2 — WorkBuddy Integration

验收日期：2026-10-01。发布版本：v0.4.0；真实 Host 验收基线版本为 0.3.0。
**最终 Gate：21/21 PASS。发布验证见文末及 v0.4.0 release notes。**

## 基线与范围

从干净 main / v0.3.0 的 `c30b353b9db9596fa65a789f9112828351b147e1` 开始。
P11、P12 Step 1 保持 PASS；不重做迁移、Obsidian 设计或架构。
未执行 Hermes、Cross-Agent 最终阶段、WorkBuddy 历史迁移、消息规范化或 V1 删除。

## 真实 WorkBuddy 与证据层级

Windows 安装登记、executable metadata 和真实界面确认 WorkBuddy 5.6.2。
正式 stdio MCP 可用；用户截图确认服务器连接和工具发现，用户回传确认真实
WorkBuddy 的工具调用及 Agent 行为。SDK 检查是独立补充证据，不能替代真实 Host。

官方 [MCP 指南](https://www.workbuddy.ai/docs/zh/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/MCP-Guide)
说明用户级、项目级配置及 command/args/env。Desktop 5.6.2 的同名覆盖优先级
和 reload 保证未明确建立，不能套用 CodeBuddy CLI/IDE 规则。
GUI 添加页截图确认用户级 mcp.json 是实际配置编辑入口。
现有 GUI study_system 被用户报告为不可编辑/托管，保留为 production 入口。
同名配置曾出现重启后目标解析不一致，属于 Host config persistence / resolution
precedence 问题，不是 Gateway 数据持久性失败。

采用不同名称的临时 `study_system_p12_isolated`，明确指向现有 controlled target；
所有私有定义与备份在 Git 外。Basic Memory 保持 disabled，既有 production 定义
在最终检查中未改动。临时服务器及测试数据保留，后续由用户决定是否移除；
没有正式记录删除接口，未通过 SQL 清理。

## 只读 E2E 与边界修正

真实 WorkBuddy 起初直接以 mode=ro 查询 SQLite 并错误解释 source-only 状态，
该轮不通过。新增薄项目规则 `.codebuddy/rules/study-system-gateway-only.md`，
AGENTS 明确读、计数、存在性判断也必须走 Gateway；不复制领域逻辑、不增加 adapter。

用户回传后续 Gateway-only 验收：health 0.3.0 / sqlite-ready、Study 存在/不存在
检索、source 搜索/有界读取、active Wrong Answer bundle/version、Asset logical refs
及有界读取均正常。来源 166 = 82 Codex + 55 legacy chat + 28 legacy wrong + 1 fact。
canonical messages=0 是既定 source-only 边界，不能报告为未迁移。
检索命中数不冒充表计数；未提供的计数报告缺少 Gateway 证据。
Study/source/Wrong Answer 三类不存在查询如实无结果，不包装模型知识为用户记录。
Source 总字节数与本次读取字节数必须区分。生产 bundle 缺 Document ref 不构造 URI；
Document 逻辑引用通过隔离合成文档及 Gateway 回读补充。

## Controlled write 与 restart

用户明确验收真实 WorkBuddy controlled-write E2E PASS：canonical workflow、
合成文档、Source、v1 保存/回读、expected_version 更新至 v2、相同请求幂等重试、
新 key 的 stale conflict。无生产学习记录写入，没有重做测试或创建 v3。
SDK/Gateway 补充确认既有 document 可读、bundle total=2 / versions=[1,2]、
v2 supersedes v1、测试关键词只命中一个 Source。
身份是 caller-reported/unverified，不是强认证身份；Gateway 负责时间、版本和 provenance。

旧私有 restart-gateway-baseline.json 收据确实存在，来自早先 SDK Gateway 回读。
它与用户后来指定的 10 个 timestamp/provenance 字段完全一致。
“未找到重启前快照”的结论已纠正；收据存在本身不是 Host restart 证据。
用户给出的正式 baseline 已另行私有保存，并在再次真实 WorkBuddy 完全退出/重启后
由用户明确确认 **Restart Persistence=PASS**。接着进入 Projection，未再执行写入。

## Isolated Projection

正式 writer 拒绝 repository overlap，因此放弃先前位于仓库 var 下的测试输出位置，
使用仓库外的独立测试 Vault；controlled target / MCP 参数 / stores 保持不变。
不访问真实 StudyVault。Vault 没有 authoritative Study，不生成虚假 Study 关系。

默认 collector 会要求 History；隔离 target 明确 History not_configured，曾真实返回
HISTORY_UNAVAILABLE，未把错误伪装成空数据。新增 `collect_wrong_answer_projection`，
显式只收集 Wrong Answers，复用既有 projection capability、水位分页和完整性校验。
默认三域 collector 保持原行为；无新 Gateway schema、业务逻辑或 Host adapter。

正式 Gateway → collector → renderer → writer 两次独立构建验证：

- 1 个测试 Wrong Answer，2 个 analysis，latest v2，无 v3。
- v2→v1 supersession、实际 document logical URI、study_relations=[] 正确。
- provenance summary 与 Gateway 返回一致，身份显示 reported (unverified)。
- 14 个 generated Markdown；manifest 与所有输出逐项对账。
- 两次 manifest 和全部 Markdown byte-identical，无重复页面/随机 ID 漂移。
- 无绝对私人路径、无原始 Asset bytes，仅 Markdown 与 manifest。
- 构建前后 Gateway bundle 完全一致，MCP 配置未改变，Basic Memory disabled。
- 未访问 production 或真实 StudyVault；不能用未读生产文件的哈希声称已检查其全量完整性。

Projection 的程序验收 PASS；独立 Vault 的人工 GUI 外观验收尚未执行。
本阶段只复用已通过 Step 1 的渲染/GUI设计，不重开 Step 1；若用户需要额外外观验收，
可在隔离 Vault 检查 Dashboard、Wrong Answer v2 和关系链接，不涉及生产 Vault。

## Final Gate

PASS 为本项证据满足；真实 Host 的用户验收与 SDK/Gateway 补充证据明确区分。

| Item | Status | Evidence |
| --- | --- | --- |
| WorkBuddy Reality Audit | PASS | 5.6.2 安装/UI、实际配置入口、真实 stdio 工具行为；Host 同名解析限制已记录 |
| WorkBuddy Installation | PASS | 安装登记/executable/UI 一致 |
| MCP Configuration | PASS | 独立隔离 server 持久配置，用户确认真实重启验收 |
| Gateway Connection | PASS | 用户真实 health 调用，SDK 补充 |
| Canonical Workflow | PASS | 用户 controlled-write 流程验收；SDK canonical resource/prompt 校验 |
| Study Retrieval | PASS | 用户 production 只读存在/不存在检索；本轮未切回 |
| History/Source Retrieval | PASS | 用户 source 查询/有界读取、source-only 语义修正 |
| Wrong Answer Retrieval | PASS | active bundle/version 和无结果查询 |
| Asset/Document References | PASS | real Host Asset reads，隔离 Document 创建/回读验收及 Gateway corroboration |
| Capability Boundary | PASS | Gateway-only 项目规则、后续用户只读/写入/重启验收；早先违规不计为 PASS |
| No-result Guard | PASS | real Host Study/source/Wrong Answer 三类无结果 |
| Controlled Write | PASS | 用户真实 Host 隔离 E2E 验收，既有对象 Gateway 回读 |
| Versioning | PASS | versions=[1,2]，无 v3 |
| Idempotency | PASS | 用户 controlled-write 验收，未额外重放写入 |
| Stale Conflict | PASS | 用户 controlled-write 验收，未额外冲突写入 |
| Provenance | PASS | caller-reported/unverified、时间/ID exact baseline 与用户重启验收 |
| Restart Persistence | PASS | 用户明确确认第二次真实 isolated Host 重启 exact diff 通过 |
| Obsidian Refresh | PASS | 两次正式链路构建，14 Markdown，manifest/内容字节稳定 |
| Privacy | PASS | tracked tree + intended new files、secret/private-path scan、wheel/sdist 审计；发布后实际新增 objects 另行审计 |
| Regression | PASS | targeted 65 passed / 1 skipped；full 617 passed / 12 skipped |
| Documentation | PASS | README/current-state/architecture/host compatibility/checkpoint 更新，历史失败与证据限制明确 |

验收完成时版本仍 0.3.0，未 commit/merge/push/tag/Release；后续用户已授权 v0.4.0 发布。
已知 Host 同名优先级限制、旧 Codex resources/list
兼容问题和 WorkBuddy 历史迁移保持独立 deferred。

## 发布前验收验证与审计（0.3.0 基线）

- Targeted Projection/Writer/Collector/Build/Provenance/stdio parity：65 passed，1 skipped。
- Full default/dev：617 passed，12 skipped。新增 3 个 collector tests 经先失败后通过验证。
- git diff --check：PASS；Windows LF/CRLF 提示不是 whitespace error。
- Tracked tree 156 files 加拟新增 rule/checkpoint：无 private path、credential 或敏感文件命中。
- origin/main..HEAD 新增 reachable objects 为 0；未 commit/add 新对象，所以对象增量检查无目标。
  后续 commit/release 必须重新审计实际新增 objects，不能沿用本轮零对象结论。
- 包审计发现仅依赖 .git/info/exclude 不足：初次 sdist 含本地 WorkBuddy config/log。
  添加 .workbuddy/ 到公共 .gitignore 后重建并复验：wheel/sdist 均无私人配置、日志、
  DB、图像或导出；这些失败产物仅在本机，未上传。
- Wheel 42 files；sdist 168 files；0.3.0 metadata、Apache-2.0/LICENSE、canonical workflow
  和 optional-only PyMuPDF 均正确。无 secrets/absolute private paths 命中。

无需重开 Step 1 GUI Gate。隔离 Projection 程序验收完整；未声明已经完成独立 Vault
的人工外观观察。用户可选做该观察，当前 Step 2 证据 Gate 不依赖新增人工设计验收。
验收变更包含 .gitignore 的打包隐私修复、Gateway-only 指导、14 行 collector 入口、
3 个 meaningful tests 和公开脱敏文档。此处零对象/0.3.0 包数字仅指验收时点；
不能代替后续 v0.4.0 commit、package 与 remote 审计。

## v0.4.0 发布验证（2026-10-01）

用户明确授权 autonomous release；不重复已 PASS 的人工 WorkBuddy/GUI、controlled-write、
restart 或 isolated Projection。package、example 与三个 ignored runtime config 的版本
同步为 0.4.0；私有 runtime config 仅版本字段变化，其余 TOML 值相等并保留私有备份。
WorkBuddy MCP 定义仍包含 production 与独立 isolated 入口，Basic Memory disabled。

- 发布 targeted：65 passed / 1 skipped；full：617 passed / 12 skipped。
- git diff --check：PASS。源码差异只含已验收 collector、对应测试、规则、打包排除与版本/文档。
- Wheel 42 files、sdist 169 files；version 0.4.0、Apache-2.0/LICENSE、canonical workflow、optional-only PyMuPDF 审计通过。
- 公开候选树 159 files：无私人路径、credentials 或受限文件命中；staged tree 单独复验。
- 独立 installed-package stdio smoke：package/MCP/Gateway 0.4.0、15 read tools、canonical resource/workflow 通过；全程零持久化操作，不连接生产数据。
- 实际 v0.3.0..HEAD 新增 reachable objects 在 commit 后、push 前审计；不复用验收时零对象结论。
- main、annotated tag、GitHub Release、remote tree/metadata/notes 与 fresh clone install 按正式发布流程核验。

发布内容与兼容限制见 [v0.4.0 notes](releases/v0.4.0.md)。无新的人工 GUI Gate 要求。
