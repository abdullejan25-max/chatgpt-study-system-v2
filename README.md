# ChatGPT Study System V2

一个 local-first、Agent-agnostic 的个人学习基础设施。它通过统一的本地 Gateway 连接 Study、Personal History、Wrong Answers 和原始学习材料；不会自动发现、导入或上传个人资料。

## 设计与架构

系统遵循 **Agent thinks; Gateway executes**：Agent 负责理解、推理和规划，Gateway 只执行明确、可验证且受权限控制的操作。Gateway 不运行第二个 LLM，也不提供任意 Shell。

```text
Agent
  ├─ Workflow：规定某类任务的操作步骤，例如错题工作流
  └─ MCP：为不同 Agent 提供同一套协议接口
         ↓ stdio
      Gateway：校验参数、权限、来源、事务、版本和 provenance
         ↓
      Adapters：Study / Personal History / Wrong Answers / Assets & Documents
         ↓
      明确配置的本机数据源
```

- **Study**：通过显式配置的 QMD collection 搜索学习资料。搜索使用隔离的临时副本；原始索引保持为用户管理的数据源。
- **Personal History**：读取显式登记的本地 History store；原始来源证据与确定性生成的 canonical conversations/messages 分开保存。规范化只接受可靠结构，不能确定的记录继续 source-only；系统不会扫描聊天记录或自动导入历史。
- **Legacy Sources**：读取经过显式迁移的旧来源文档，保留原始字节、类型与 provenance；聊天档案、旧错题笔记、派生事实和 Codex JSONL 与原始消息模型分开。`list_legacy_sources`、`search_legacy_sources`、`fetch_legacy_source` 提供只读检索和有界原文读取。
- **Wrong Answers**：原始图片或文档作为证据，Agent 提供分析，Gateway 按权限保存来源和带版本的分析，并记录 provenance。不同 MCP Agent 使用同一套 `study-workflow://wrong-answer` 工作流。
- **Assets & Documents**：Gateway 对明确提交的来源做边界检查、哈希与登记；原始证据和派生文字保持可区分。

更完整的组件职责和安全约束见 [架构说明](docs/architecture.md)、[隐私边界](docs/privacy-boundary.md) 和 [ADR](docs/adr/)；已验证的错题链路证据见 [Real Wrong Answer E2E checkpoint](docs/real-wrong-answer-e2e-checkpoint.md)。

`v0.2.0 — Legacy Migration` 的历史范围是 V1 来源迁移与 V2 cutover，证据见 [P11 completion](docs/p11-real-migration-completion.md)。P13 在正式 `v0.6.0` 基线上推进已取得来源的补齐与规范化，当前本地结果见 [P13 checkpoint](docs/p13-history-completion-checkpoint.md)、[source-only ingestion](docs/history-source-ingestion.md) 和 [canonical History](docs/history-normalization.md)。P13 尚未发布；旧错题的完整业务语义仍保留原有限制。

## 安装

### 前置条件

- Python 3.11 或更新版本。
- [`uv`](https://docs.astral.sh/uv/) 已安装并能从终端及 Codex Desktop 继承的 `PATH` 找到。
- 若要搜索 QMD Study collection，还需安装受支持版本的 Node.js 和 QMD，并在本机配置中填写可执行文件及索引路径。该外部运行时不会由本项目安装或捆绑。
- OCR 是可选能力，需要额外安装 `pdf-ocr` Python extra 和本机 Tesseract 语言数据；默认安装不启用 OCR。

### 一次性本机设置

在新 clone 的仓库根目录运行：

```powershell
Copy-Item config.example.toml config.local.toml
uv sync --project . --no-editable
```

该命令安装核心默认依赖，不安装 PyMuPDF。`--no-editable` 让 uv 安装项目 wheel，避免 Windows Python 3.11 在含中文路径的 editable `.pth` 文件上遇到系统代码页解码错误。Codex MCP 使用 `uv run --no-sync` 启动已安装环境；首次设置和依赖更新后都先完成 `uv sync`。核心测试另加 `--extra dev`；只有主动启用 PDF/OCR 时才加 `--extra pdf-ocr`，其中的 PyMuPDF 继续受其独立许可证约束。

macOS/Linux 可把第一条命令替换为 `cp config.example.toml config.local.toml`。编辑被 Git 忽略的 `config.local.toml`，填入自己本机的 Study/QMD 路径；只有确实要启用相应能力时，再配置 History、Asset store 和权限。默认配置示例仅启用 `read`，不会迁移现有数据，也不会选择个人数据目录。确认本机配置符合预期后，再运行：

```powershell
python .codex/setup_mcp.py
```

`.codex/setup_mcp.py` 会从自身位置定位仓库，并生成被忽略的 `.codex/config.toml`。生成配置使用本机 checkout 的显式绝对路径，并将 `PYTHONPATH` 指向该 checkout 的 `src`，避免 Codex Desktop 将 `cwd = "."` 解析到自身安装目录或依赖 editable install 的本机 locale 路径行为。模板中的 `required = true` 保证服务器启动失败会显式报错。运行脚本不会覆盖无法识别的现有本机配置。

在 Codex Desktop 打开并信任该仓库，然后**新建对话**，确认 `study_system` MCP 已加载。先调用只读 `health_report`。如果刚更改了 `PATH`，重启 Codex Desktop 后再新建对话。完整说明见 [Codex Host setup](docs/codex-host-setup.md)。

如不使用 Codex Desktop，可通过 stdio MCP client 启动同一 Gateway；本项目当前不启用 HTTP listener 或公开服务端点。

### 后续 v0.7.0 升级流程

当前正式版本仍为 `v0.6.0`。待 `v0.7.0` 正式发布后，按以下顺序升级：

1. 通过已配置 Gateway 创建并验证私有备份，保留现有配置；恢复步骤见 [private recovery](docs/p13-recovery.md)。
2. 切换到正式发布的 checkout，在仓库根目录运行 `uv sync --project . --frozen --no-editable`；需要的 optional extras 按既有配置保留。
3. 在被忽略的私有 Gateway 配置中同步 `[gateway].version`，保留原有数据位置和 capability 设置。
4. 重载各 Host 的 MCP，在新会话用原生 `study_system` 验证 `health_report`、来源检索、canonical History 读取与 no-result。

隔离恢复副本只用于恢复验收，不能配置成第二份权威数据层。升级不会自动导入或删除历史来源。

## 测试

```powershell
uv sync --project . --extra dev --no-editable
uv run --no-sync --project . --extra dev pytest -q
```

测试使用人工编写的合成数据。Codex Host smoke、真实 QMD smoke 和受 Windows 文件系统权限限制的测试是 opt-in 或可能跳过；synthetic 测试不等于真实 Codex Desktop 新会话验证。

## 数据与安全边界

- `config.local.toml`、`.codex/config.toml`、数据库及 SQLite sidecar、日志、缓存、真实图片和 PDF 都属于本机数据，不应提交。
- Gateway 只访问本机配置显式指定的来源；Capability 控制 `read`、`write`、`ingest`、`projection` 和 `admin` 操作。批量投影导出需要单独显式启用 `projection`，普通 `read` 不包含该权限。写入错题记录必须经 Gateway，不直接写数据库。
- 项目运行时不会自动上传学习资料。首次安装 Python 依赖时，`uv` 会从配置的软件源下载软件包；这不是上传个人学习数据。
- `.gitignore` 是防误提交措施，不是安全边界；提交前仍须检查 `git status` 和提交内容。
- 不要把真实 StudyVault、History、教材、错题图片、聊天记录或数据库复制到仓库或测试夹具。

## 当前限制

- ChatGPT hosted MCP / Secure MCP Tunnel 尚未实现；当前 MCP 运行方式是本机 stdio。
- QMD、Node 和 Study 索引需要用户自行安装并在私有配置中显式指定。
- OCR 是可选本机能力，依赖 Tesseract 与语言数据；识别文字不能取代原始页面证据。
- 本项目源代码按 Apache License 2.0 许可，SPDX 标识为 `Apache-2.0`。`pdf-ocr` extra 中的 PyMuPDF 使用其自身的 GNU AGPL v3 或 Artifex commercial license；项目 Apache-2.0 声明不会改变 PyMuPDF 的许可证，安装该 extra 前请确认适用条件。详见 [P10 License audit](docs/license-audit.md)。

## 状态

当前正式基线为 **`v0.6.0 — Cross-Agent Integration`**，P12 已完成，既有 Codex、WorkBuddy、Hermes Host PASS 保留。P13 是尚未发布的本地工程与私有迁移：已验证 1,776 个来源、487 个 canonical conversations、7,334 条 distinct messages、494 个 source-specific views；1,323 个来源完全保留 source-only。

ChatGPT 官方导出为 `acquisition_pending`，到达后做增量幂等补录。WorkBuddy 的 P13 History Host 验收为 `DEFERRED`，不阻塞后续工作。真实 V2 backup 已获 `PASS_NATIVE`；isolated restore、V1 unique-data audit 和 logical retirement 待执行。生产 writable ingress 将复用 Gateway，验收尚未完成。V1 physical deletion 必须另获 owner 明确确认。当前证据与限制见 [当前状态](docs/current-state.md) 和 [P13 checkpoint](docs/p13-history-completion-checkpoint.md)；项目运行和 MCP 调用不会自动推送代码或上传个人学习资料。

P11 与 P12 Step 1 的历史迁移、投影和人工 GUI 证据分别见 [P11 completion](docs/p11-real-migration-completion.md) 和 [P12 Step 1](docs/p12-step1-real-projection-checkpoint.md)。

## Hermes Integration（v0.5.0）

Hermes Agent v0.20.0 经原生 stdio MCP 接入同一 Gateway，22/22 Gate 已通过。
真实 CLI Agent 的生产只读、三类 no-result、隔离 v1/v2、幂等/冲突、reported/unverified
provenance、Host 退出/重启与 isolated Projection 证据见 [Hermes checkpoint](docs/p12-step3-hermes-checkpoint.md)。
生产与隔离服务器不同名；Hermes Memory/profile disabled，session/runtime metadata 不作为 V2 权威层。
配置和已验证 DeepSeek 会话入口见 [Host setup](docs/hermes-host-setup.md)，
范围与发布检查见 [v0.5.0 notes](docs/releases/v0.5.0.md)。Desktop shell live reload/GUI restart
未单独验收；Step 4 跨 Agent 矩阵与会话迁移不属于该 v0.5.0 发布范围，后续状态见上文。

## WorkBuddy Integration（v0.4.0）

P12 Step 2 的真实 WorkBuddy 验收与隔离 Projection 证据见
[WorkBuddy Integration checkpoint](docs/p12-step2-workbuddy-checkpoint.md)。
WorkBuddy 5.6.2 经正式 MCP 使用同一 Gateway；读、计数、存在性判断与写入均经过 Gateway。
隔离 controlled-write、版本/幂等/冲突、reported/unverified provenance、真实重启和隔离 Projection Gate 全部 PASS。
Basic Memory disabled；production 入口与隔离测试入口分开。WorkBuddy 聊天历史迁移不属于该 v0.4.0 发布范围；P13 本地来源与 Host 验收状态见上文。
发布范围、验证与限制见 [v0.4.0 release notes](docs/releases/v0.4.0.md)。

## Obsidian Visualization（v0.3.0 起）

既有 Gateway → collector → renderer → writer 将真实数据投影到私有 Vault 的 `V2Projection`，通过 manifest 管理所有权与安全重建。Dashboard 提供四类 Sources、Wrong Answers、Knowledge Points、Error Types、Study 相对引用以及 Asset/Document logical refs。来源页面是元数据视图，不复制聊天正文、不推断消息角色或会话边界；P12 Step 1 验收时 canonical messages 为 0，后续 P13 canonical History 保持独立 derived layer。Study 保持单一权威来源，不复制或重写原文件。

批量读取需在忽略的私有配置中显式启用 `projection`。在仓库根目录执行：

```powershell
$env:PYTHONPATH = Join-Path (Get-Location) "src"
uv run --no-sync python -m chatgpt_study_system.obsidian_build --config config.local.toml --vault <existing-private-vault>
```

构建命令要求现有 Vault 包含配置的 Study root，且 Study 与 `V2Projection` 互不重叠。它验证文件回读、相对链接、第二次独立构建与 manifest 稳定性；未登记为 generated 的用户笔记不属于删除范围。普通写入失败可回滚，突然断电或进程终止不保证整个目录原子替换。发布范围与限制见 [v0.3.0 release notes](docs/releases/v0.3.0.md)。
