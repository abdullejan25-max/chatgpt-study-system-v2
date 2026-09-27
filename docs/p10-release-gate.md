# Phase 10 — GitHub Release Gate

更新时间：2026-09-27
状态：**自动门禁收尾中；clean release candidate 的 Codex Desktop GUI 验证尚未完成。** 未创建 GitHub repository、未添加 remote、未 push，也未发布 tag/Release。

## Repository snapshot

- 开发仓库分支：`phase-3-readonly-mcp-spike`；P10 开始时的基线 HEAD：`c413b4375de807e1ff2f39c6e3b3b1b402fd9940`。
- 旧开发 history 保留在本地，不做 rewrite。首次公开发布使用独立、只有新 root commit 的 `main`。
- 本机 `.codex/config.toml` 与根目录 `config.local.toml` 被忽略；本地 Desktop 配置没有被覆盖。P4–9 plan 已原样归档；ignored `docs/debug.log` 留在本机，不进入发布树。
- P1–P9 与 Wrong Answer / Retrieval E2E 均保持既有验证结果；P10 未重构 Gateway 或 Wrong Answer 主链路。

## Portable Codex Desktop bootstrap

- `.codex/config.example.toml` 仅有占位符；`.codex/setup_mcp.py` 从脚本位置定位 checkout，生成带显式 `cwd`、`uv --project`、`PYTHONPATH` 和私有 Gateway config 路径的本机配置。
- `required = true` 保留；未知的本机配置不会被 setup 覆盖。
- setup 测试覆盖空格/非 ASCII 路径、移动 checkout、未知配置保护和 Git 忽略边界。
- 项目所有者已报告开发 checkout 的真实 Desktop 新对话能加载 `study_system`、`health_report` 返回 `ok: true` 且 Study 可读；History `not_configured` 是配置状态。本轮仍需验证最终 clean release candidate 的 GUI Host。

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

## Security regression review

只读审计与合成回归未发现 path traversal、capability bypass、source refs、idempotency、transaction、provenance 或 versioning 的核心缺陷。图片 MIME 按文件签名判断，不保证完全可解码。当前 Windows 权限限制了 inbox symlink / junction 测试；对应 skip 会记录在测试结果中。

## Verification record

- 开发 checkout 完整测试：**308 passed, 5 skipped**。跳过项是 Codex CLI/真实 QMD opt-in，以及当前 host 的 NTFS junction / symlink 权限限制。
- Bootstrap + metadata 有专项测试；安全边界合成测试的既有审计结果为 **58 passed, 1 skipped**。
- clean release candidate 位于带空格和中文的临时路径；按 README 完成默认安装及 `dev` extra 后，PyMuPDF 模块和 distribution 均不存在。`pdf-ocr` extra 的 dry-run 解析成功，计划仅额外安装 PyMuPDF 1.28.2。
- clean candidate 全量测试：**307 passed, 6 skipped**。其中默认无 PyMuPDF 导致 OCR 专项用例跳过；Codex Host 与真实 QMD 是 opt-in；本机无法创建 NTFS junction / symlink。
- clean candidate 的 wheel 与 sdist 均构建成功；两种发行物都含 Apache-2.0 SPDX metadata 与 LICENSE，且 PyMuPDF 仅通过 `extra == 'pdf-ocr'` 声明。
- 使用生成配置启动实际 stdio server，MCP initialize 与 `health_report` 均通过；`ok: true`、合成 Study root 可读，History 为 `not_configured`，QMD 不可发现符合无 QMD 私有运行时的合成配置。
- `uv lock --check`、候选树 Git 初始化后的全量测试和发行物检查通过；最终 public object scan 在建立独立 root commit 后记录。
- 真实 Codex Desktop clean-candidate GUI 验证：待项目所有者完成；协议 smoke 不能替代此项。

## Release Gate

- [x] Apache-2.0 LICENSE 与 SPDX metadata 已添加；PyMuPDF 保持非默认 optional extra。
- [x] portable bootstrap、私有配置边界、E2E 证据同步与安全审计已记录。
- [x] 开发 checkout 当前完整测试通过。
- [x] clean release candidate 默认安装确认没有 PyMuPDF；`pdf-ocr` optional dependency 可解析。
- [x] clean release candidate 全量测试、package metadata/build 和 MCP initialize + `health_report` smoke 通过。
- [ ] public `main` 是独立无父 root，且 public tree / objects / history 复扫通过。
- [ ] 对该 clean release candidate 完成 Codex Desktop 新对话验证。
- [ ] Desktop gate 通过前不创建 GitHub repository、不添加 remote、不 push。
- [ ] Desktop gate 通过且发布后，fresh clone from GitHub 的最小复验。

## Clean candidate Desktop verification

打开本次提供的 clean release candidate 目录，在 Codex Desktop 信任该项目后新建对话。确认 `study_system` ready，调用只读 `health_report` 并确认 `ok: true`。合成配置不包含真实 Study/History/Asset 数据，也不启用写能力。
