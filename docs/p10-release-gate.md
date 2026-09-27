# Phase 10 — GitHub Release Gate

更新时间：2026-09-27
状态：**Codex Desktop Host gate 已通过；GitHub 首次公开与真实 remote fresh-clone 复验待完成。** 尚未创建 GitHub repository、添加 remote 或 push，也未发布 tag/Release。

## Repository snapshot

- 开发仓库分支：`phase-3-readonly-mcp-spike`；P10 开始时的基线 HEAD：`c413b4375de807e1ff2f39c6e3b3b1b402fd9940`。
- 旧开发 history 保留在本地，不做 rewrite。首次公开发布使用独立、只有新 root commit 的 `main`。
- 本机 `.codex/config.toml` 与根目录 `config.local.toml` 被忽略；本地 Desktop 配置没有被覆盖。P4–9 plan 已原样归档；ignored `docs/debug.log` 留在本机，不进入发布树。
- P1–P9 与 Wrong Answer / Retrieval E2E 均保持既有验证结果；P10 未重构 Gateway 或 Wrong Answer 主链路。

## Portable Codex Desktop bootstrap

- `.codex/config.example.toml` 仅有占位符；`.codex/setup_mcp.py` 从脚本位置定位 checkout，生成带显式 `cwd`、`uv --project`、`PYTHONPATH` 和私有 Gateway config 路径的本机配置。
- `required = true` 保留；未知的本机配置不会被 setup 覆盖。
- setup 测试覆盖空格/非 ASCII 路径、移动 checkout、未知配置保护和 Git 忽略边界。
- 项目所有者已报告开发 checkout 的真实 Desktop 新对话能加载 `study_system`、`health_report` 返回 `ok: true` 且 Study 可读；History `not_configured` 是配置状态。
- 最终稳定 clean release candidate 的 Codex Desktop 新对话验证已通过：`study_system` 已加载，`health_report.ok = true`，`study.configured/root_exists/readable = true`，没有 MCP 启动、initialize 或 Study 配置错误。合成配置中的 `history.status = not_configured` 与 `qmd.discoverable = false` 是预期状态；验证未修改文件或数据，候选工作区保持干净。

## License 和 PyMuPDF

- 项目根目录 `LICENSE` 使用 Apache License 2.0 正文；`pyproject.toml` 的 SPDX metadata 为 `Apache-2.0`，并将 LICENSE 纳入发行包。
- Hatchling 最低版本为 1.27，以支持 PEP 639 的 `license` 与 `license-files`。
- PyMuPDF 仅属于非默认 `pdf-ocr` extra。项目 Apache-2.0 不改变 PyMuPDF 自身的 GNU AGPL v3 / Artifex 商业许可条件。
- wheel 与 sdist 的构建元数据均声明 `License-Expression: Apache-2.0`、包含 `LICENSE`，并将 PyMuPDF 标记为仅适用于 `pdf-ocr` extra。完整依赖范围与官方来源见 [Dependency License Audit](license-audit.md)。

## Private data boundary

- `.gitignore` 覆盖私有配置、数据库及 SQLite sidecar、StudyVault/History/Assets、inbox、staging、OCR/private indexes、日志、缓存、备份、PDF、图片和命名的聊天导出目录。
- `tests/fixtures/*.md` 与 `*.json` 仍可跟踪；二进制图片仍忽略。
- 发布候选扫描会覆盖所有 Git 候选文件及新 public Git objects；私有配置、真实学习数据和运行时状态不复制到 public history。当前 clean candidate 中本机合成 `config.local.toml`、生成的 `.codex/config.toml`、`.venv` 均被忽略。
- Real Wrong Answer / Retrieval 的既有证据见 [Real Wrong Answer E2E checkpoint](real-wrong-answer-e2e-checkpoint.md)，没有重新导入真实资料。

## History strategy

旧开发 history 的扫描曾发现历史开发提交包含机器账户安装路径；那些提交只保留在本地开发仓库，不会成为 public `main` 的祖先。发布采用单独的 release candidate Git repository，并从最终候选树创建无父提交的 root commit；不 rewrite、force-push 或上传旧 branches。public history 和所有 object 的复扫结果在下面的最终验证记录中更新。

当前独立 release candidate 的 public `main` root 为 `cc2ee4e9477a266a047d803822ba82de86e81024`，该提交没有 parent。candidate repository 没有 remote；GitHub repository 与 push 均尚未发生。

## Security regression review

只读审计与合成回归未发现 path traversal、capability bypass、source refs、idempotency、transaction、provenance 或 versioning 的核心缺陷。图片 MIME 按文件签名判断，不保证完全可解码。当前 Windows 权限限制了 inbox symlink / junction 测试；对应 skip 会记录在测试结果中。

## Verification record

- 开发 checkout 完整测试：**308 passed, 5 skipped**。跳过项是 Codex CLI/真实 QMD opt-in，以及当前 host 的 NTFS junction / symlink 权限限制。
- Bootstrap + metadata 有专项测试；安全边界合成测试的既有审计结果为 **58 passed, 1 skipped**。
- 先前一次性 clean release candidate 位于带空格和中文的路径；按 README 完成默认安装及 `dev` extra 后，PyMuPDF 模块和 distribution 均不存在。`pdf-ocr` extra 的 dry-run 解析成功，计划仅额外安装 PyMuPDF 1.28.2。
- clean candidate 全量测试：**307 passed, 6 skipped**。其中默认无 PyMuPDF 导致 OCR 专项用例跳过；Codex Host 与真实 QMD 是 opt-in；本机无法创建 NTFS junction / symlink。
- clean candidate 的 wheel 与 sdist 均构建成功；两种发行物都含 Apache-2.0 SPDX metadata 与 LICENSE，且 PyMuPDF 仅通过 `extra == 'pdf-ocr'` 声明。
- 使用生成配置启动实际 stdio server，MCP initialize 与 `health_report` 均通过；`ok: true`、合成 Study root 可读，History 为 `not_configured`，QMD 不可发现符合无 QMD 私有运行时的合成配置。稳定 clean candidate 上再次完成默认依赖安装、`setup_mcp.py` 和协议 smoke；生成配置针对该 checkout 且保留 `required = true`。
- 独立 public `main` 的 root commit 无 parent，旧开发 commit `c413b4375de807e1ff2f39c6e3b3b1b402fd9940` 不在 release candidate 的 Git objects 中；候选工作树与最终开发 HEAD 的 85 个文件 blob 一致。
- public tree 和所有 Git objects 的隐私复扫通过：无凭证、真实账户路径、数据库/教材/图片/日志扩展名、本机配置或旧开发祖先。路径脱敏测试中的用户目录样例均为合成夹具。最终 clean clone 的对象数据库与 public refs 一致，并通过 `git fsck` 检查。
- `uv lock --check`、候选树 Git 初始化后的全量测试和发行物检查通过。
- 真实 Codex Desktop clean-candidate GUI 验证：待项目所有者完成；协议 smoke 不能替代此项。

## Release Gate

- [x] Apache-2.0 LICENSE 与 SPDX metadata 已添加；PyMuPDF 保持非默认 optional extra。
- [x] portable bootstrap、私有配置边界、E2E 证据同步与安全审计已记录。
- [x] 开发 checkout 当前完整测试通过。
- [x] clean release candidate 默认安装确认没有 PyMuPDF；`pdf-ocr` optional dependency 可解析。
- [x] clean release candidate 全量测试、package metadata/build 和 MCP initialize + `health_report` smoke 通过。
- [x] public `main` 是独立无父 root，且 public tree / objects / history 复扫通过。
- [x] 对稳定 clean release candidate 完成 Codex Desktop 新对话验证；MCP 已加载，`health_report.ok = true`，合成 Study 可读。
- [ ] 在目标账号身份确认及全部发布前 gate 通过后，创建 public GitHub repository，仅 push clean public `main`。
- [ ] 从真实 GitHub remote fresh clone，并复验安装、setup、测试、MCP initialize 与 `health_report`。

## Clean candidate Desktop verification

**PASS。** 项目所有者已在最终稳定 clean release candidate 目录中信任项目并新建 Codex Desktop 对话。`study_system` 已加载；只读 `health_report` 返回 `ok = true`，Study 已配置且 root 存在、可读。`history.status = not_configured` 与 `qmd.discoverable = false` 符合不配置真实 History/QMD 的合成验证环境。没有修改文件或数据，候选工作区无未提交改动。该 GUI Host 验证不替代 push 后从 GitHub fresh clone 的复验。
