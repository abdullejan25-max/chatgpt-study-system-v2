# 当前状态

更新时间：2026-09-27。Phase 1–9 本地实现已完成，P10 Release Hardening 首次公开发布已完成。GitHub public repository 的 default branch 为 `main`；旧开发 history 仅保留在本地。真实 GitHub fresh clone 的默认与 dev 安装均不含 PyMuPDF，全量测试为 **308 passed、6 skipped**；MCP initialize 与只读 `health_report.ok = true` 通过。详细证据见 [P10 Release Gate](p10-release-gate.md)。

真实错题与 retrieval E2E 的既有结果已同步到 [Real Wrong Answer E2E checkpoint](real-wrong-answer-e2e-checkpoint.md)；该文档同步没有重新导入真实资料。

P10 release gates 已通过：项目使用 Apache-2.0，PyMuPDF 只在非默认 `pdf-ocr` extra 中提供。旧开发历史保留在本地开发仓库；公开 `main` 从无父 root `cc2ee4e9` 开始。GitHub fresh clone 的安装、测试、setup 与 MCP smoke 通过；项目所有者已确认 clean candidate Codex Desktop GUI gate 通过。GitHub 已于 2026-09-27 正式发布 `v0.1.0 — Initial Public Release`；tag 指向公开 `main` 的 `64d7849`，本次文档同步未改动该 tag。

阶段决策与限制记录在各 `phase-*-checkpoint.md`、[`phase-6-closeout.md`](phase-6-closeout.md)、架构文档和 ADR 中。

Phase 11 Legacy Migration 当前为 **BLOCKED**：权威 StudyVault 原地复用；55 个旧聊天 Markdown 只归档，7 个其它 Personal 项 skip；旧 Atomic Fact 因 History 未配置而 unresolved；28 条错题笔记和 70 张图片无法建立可信关系。新增 P11.3A 统一来源盘点已建立私有登记器（6 个来源条目）：ChatGPT 官方导出仍需登录，Gemini Takeout 导出已完成但下载再次要求 Google 登录，本地 Agent history 尚未验证；Gemini raw archive 尚未下载或检查，也没有统一 History 导入。只读 dry-run、私有 manifest 和 Study 检索验证已完成，当前续作增加的合成测试为 37 passed、2 skipped；未写入 V2 业务数据。详情与逐项 Gate 见 [Phase 11 Legacy Migration](phase-11-legacy-migration.md)。没有创建 v0.2.0 tag/Release，也未 push Phase 11 分支。

P12 preparation is in progress. A deterministic in-memory Obsidian renderer now accepts explicit Gateway DTOs; its synthetic suite is **19 passed**, and the full suite is **402 passed, 7 skipped**. It does not collect a complete snapshot or write a Vault. Official WorkBuddy and Hermes documents describe local stdio MCP clients, but this machine's connections and E2E remain unverified. Obsidian's real Vault view is also unverified. No P12 release gate is claimed PASS; see [P12 Host Compatibility Checkpoint](p12-host-compatibility.md) and [P12 Obsidian Reality Audit](p12-obsidian-reality-audit.md).

架构不变量：外部 Agent 是唯一智能层；Gateway 只执行确定性操作。Tunnel/Responses API 不属于 Core，也不是项目完成条件。真实私人 History、错题和教材不用于自动化测试。Phase 10 发布复验只使用合成 Study 配置，没有迁移或导入真实数据。

Phase 6 的 private document store 显式配置后可接收资产/文档；PDF 文字层由 `pypdf` 确定性提取，PDF 大文件只能通过显式配置的本地相对路径 ingest root 输入。授权的 269 页教材副本已通过 disposable MCP smoke 验证 search/page/原页 PNG/provenance；原始 23.5 MB 文件测试前后 SHA-256、size、mtime 一致。fresh smoke 显式禁用 OCR，记录 40 个 `pdf_text_layer`、3 个 `pdf_ocr_unavailable`、226 个 suspicious 页；同源第二次 ingestion 复用同一 document URI 且无需再次解析。此前受控 OCR continuation 的四个 16-page batch 完整提交，停止时为 40 个 `pdf_text_layer`、72 个 `pdf_ocr_derived`、157 个 suspicious 页、118 chunks；整本 eager OCR 不再是 Phase 6 条件。`unverified` 文字层不能证明公式/变量完整，原书数学符号和视觉页面应视为权威来源；Tesseract 参数告警仍是已知限制。大 PDF asset 支持受限分块读取；完整 PDF 超过 MCP 单次 binary-resource 上限。Phase 7 错题分析与来源分离保存；Phase 8 已加入 capability split、事务审计和 Windows reparse-point 检查。2026-09-26 已新增统一 append-only `write_provenance` ledger；History 源时间与导入时间分开，Agent/client identity 是 caller-reported。旧 OCR 页文本目前仍不做历史归档；本地 capability 也不是 Agent 身份认证。详情见 [`P1-P9 System Audit`](p1-p9-system-audit.md)。ChatGPT remote MCP / Tunnel 尚未实施，也不阻塞 Phase 4–9；Phase 10 GitHub Release Hardening 已通过首次公开发布。P10-B bootstrap 与 clean candidate Desktop 验证通过；History `not_configured` 是配置状态。
