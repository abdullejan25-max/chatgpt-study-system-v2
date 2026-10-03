# ChatGPT Study System V2

**Local-first、Agent-agnostic 的个人学习基础设施。** 让不同 Agent Host 通过同一个本地 Gateway 使用个人学习数据，同时由用户掌控数据位置和访问权限。

## What it is / 项目简介

ChatGPT Study System V2 将 Study 学习资料、Personal History、Wrong Answers 错题和原始文档接入兼容的 Agent Host。Agent 负责理解需求、推理和选择工具；Gateway 执行明确、可验证并受权限控制的数据操作。

系统不会自动扫描个人目录、导入聊天历史或上传 StudyVault。用户自行选择要配置的数据源，并明确发起导入。

## Architecture / 核心架构

```text
User → Agent Host → MCP (local stdio) → Gateway → Adapters → Local data
```

**Agent thinks; Gateway executes.** Gateway 校验请求、检查 capability 并记录 provenance。它不运行第二个 LLM，也不开放任意 Shell。

## Core data domains / 核心数据域

- **Study** — 通过明确配置的 QMD collection 检索学习资料；搜索使用隔离的临时副本，原始资料和索引仍由用户管理。
- **Personal History** — 保存原始来源证据，并以确定性方式生成派生的 canonical conversations 与 messages。
- **Wrong Answers** — 保留题目原始证据，Agent 分析另行保存并版本化。
- **Assets & Documents** — 显式登记原始文件及其派生文档文本。
- **Legacy / Source Evidence** — 保留有明确类型的历史输入；无法安全规范化的内容仍作为 source-only 证据。

## Key properties / 设计特点

- **Local-first：** 私有数据和配置保存在用户选择的本机位置。
- **保留来源：** 原始证据与规范化或分析后的数据分开保存。
- **确定性处理：** Gateway 不猜测缺失的角色、顺序、时间或会话边界。
- **可追溯：** 记录保留来源引用、provenance 和分析版本链。
- **Capability-controlled：** Gateway 执行 read、ingest、write、projection、admin 权限检查。
- **共享数据、各自对话：** 不同 Agent 可访问同一 Gateway 数据层，但不会因此共享对话上下文。

## Host validation records / Host 验证记录

| Host | 项目记录的状态 |
| --- | --- |
| Codex | Codex Desktop 原生 MCP History readback：**PASS**。 |
| Hermes | 原生 MCP History readback：**PASS**。 |
| WorkBuddy | P12 integration：**PASS**；P13 History 专项 GUI verification：**DEFERRED**。 |

ChatGPT hosted MCP 与 Secure MCP Tunnel 尚未实现；ChatGPT 官方 export 仍为 `acquisition_pending`。详情见[当前状态](docs/current-state.md)。

## Local data and privacy / 本地数据与隐私

StudyVault 是 Study 的唯一权威来源。History、Assets、Documents 和 Wrong Answers 只使用私有配置中明确选定的本机数据位置。原始证据与派生 History、文档文本和版本化分析保持区分。

- `config.local.toml`、`.codex/config.toml`、数据库、日志、导出文件及个人学习材料留在 Git 之外。
- 项目不会自动扫描或上传个人数据。
- 安装依赖时 `uv` 会从配置的软件源下载软件包；这不涉及上传个人学习数据。
- `.gitignore` 用于防止误提交，不构成安全边界；提交前仍需检查暂存内容。
- 数据读取和写入经由配置好的 Gateway 及其 capability 检查。

完整数据流和存储规则见[隐私边界](docs/privacy-boundary.md)。

## Installation / 安装

### Core prerequisites / 核心前置条件

项目核心运行时和 Gateway 不依赖 Codex Desktop。必需环境是 Python 3.11 或更高版本，以及 [`uv`](https://docs.astral.sh/uv/)；QMD、Node.js 和 OCR 组件按需安装：

- 若启用 Study 检索，需自行安装 Node.js 和 QMD，并在私有配置中指定运行时与索引位置。
- 若启用 OCR，运行 `uv sync --project . --extra pdf-ocr --no-editable` 安装 extra，并安装 Tesseract 和相应语言数据。默认安装不启用 OCR；PyMuPDF 有独立的 AGPL 或商业授权条件，见[许可证审计](docs/license-audit.md)。

### Install / configure Gateway / 安装与配置 Gateway

在仓库根目录创建私有 `config.local.toml` 并安装项目：

```powershell
Copy-Item config.example.toml config.local.toml
uv sync --project . --no-editable
```

只在 Git 外编辑 `config.local.toml`，填写准备启用的数据位置和权限；示例配置默认只读。Windows 下保留 `--no-editable`：它安装 wheel，可避开 Python 3.11 在非 ASCII 路径的 editable `.pth` 文件解码问题。

项目通过本机 stdio MCP transport 提供 Gateway；没有 HTTP listener 或 public endpoint。Host 启动 Gateway 时可使用以下命令形式：

```text
uv run --no-sync --project <repository-path> python -m chatgpt_study_system.transports.mcp_stdio --config <absolute-config.local.toml-path>
```

先完成 `uv sync`；`--no-sync` launcher 不会安装或更新依赖。依赖更新或 checkout 变更后重新运行 `uv sync`。各 Host 都可连接同一套 Gateway 实现和显式配置的数据层，具体 MCP 配置格式由 Host 决定。

### Connect Agent / Host / 连接 Agent / Host

#### Codex Desktop

`.codex/setup_mcp.py` 是 **Codex Desktop 专用的 Host setup helper**：它为该 Host 生成 Git 忽略的 `.codex/config.toml`，不是项目核心安装步骤。生成配置后，在 Codex Desktop 中信任此仓库并新建对话。Host 配置见 [Codex Host Setup](docs/codex-host-setup.md)，验收记录见[当前状态](docs/current-state.md)。

#### WorkBuddy

WorkBuddy 通过 local stdio MCP 连接同一 Gateway；配置与分阶段验收记录见 [WorkBuddy checkpoint](docs/p12-step2-workbuddy-checkpoint.md) 和[当前状态](docs/current-state.md)。

#### Hermes

Hermes 通过 local stdio MCP 连接同一 Gateway。Host 配置见 [Hermes Host Setup](docs/hermes-host-setup.md)，验收记录见[当前状态](docs/current-state.md)。

#### Other stdio MCP clients

支持启动本机 stdio MCP server 的其他 client，也可按上面的命令形式连接 Gateway；command、args、环境变量和路径字段按各自 client 的配置方式填写。协议上可接入不代表项目已逐个验证这些 Host；目前已有项目验证记录的是 Codex Desktop、WorkBuddy 和 Hermes。

## Current release / 当前版本

当前正式版本是 **[v0.7.0 — History Completion & Recovery](docs/releases/v0.7.0.md)**。后续 acquisition closure 对账为 1,804 sources/outcomes、487 个 canonical conversations、7,334 条 distinct messages 和 1,351 条 wholly source-only records。完整统计、Host 状态和恢复证据见[当前状态](docs/current-state.md)。

## Known limitations / 当前限制

- ChatGPT hosted MCP 和 Secure MCP Tunnel 尚未实现。
- ChatGPT 官方 export 尚未到达；到达后才会执行增量、幂等 acquisition。
- WorkBuddy 的 P13 History 专项 GUI verification 仍为 deferred；这不改变其 P12 integration PASS。
- Caller / Agent identity 是 `reported / unverified`，不代表已认证身份。
- QMD 搜索和 OCR 依赖用户在本机安装、配置可选软件。含糊的 History 来源保留为 source-only，不猜测生成 canonical messages。

## Documentation / 文档导航

- [Current State](docs/current-state.md) — 当前发布、Host、acquisition 和 recovery 状态。
- [Architecture](docs/architecture.md) — 稳定组件、数据边界和扩展点。
- [Privacy Boundary](docs/privacy-boundary.md) — 本地数据和 capability 规则。
- [History source ingestion](docs/history-source-ingestion.md) 与 [canonical normalization](docs/history-normalization.md)。
- [Recovery](docs/p13-recovery.md) 与 [v0.7.0 Release Notes](docs/releases/v0.7.0.md)。
- 历史检查点：[P11](docs/p11-real-migration-completion.md)、[P12 Step 1](docs/p12-step1-real-projection-checkpoint.md)、[P12 Step 2](docs/p12-step2-workbuddy-checkpoint.md)、[P12 Step 3](docs/p12-step3-hermes-checkpoint.md)、[P12 Step 4](docs/p12-step4-cross-agent-checkpoint.md) 和 [P13](docs/p13-history-completion-checkpoint.md)。
- Host 配置：[Codex](docs/codex-host-setup.md) 与 [Hermes](docs/hermes-host-setup.md)。
