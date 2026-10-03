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

## Supported and verified Hosts / 已验收的 Host

| Host | 已验收状态 |
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

需要 Python 3.11 或更高版本，以及 [`uv`](https://docs.astral.sh/uv/)。在仓库根目录创建本机配置并安装项目：

```powershell
Copy-Item config.example.toml config.local.toml
uv sync --project . --no-editable
```

编辑 `config.local.toml`，只填写准备启用的数据位置和权限。示例配置默认只读。Windows 下保留 `--no-editable`：它安装 wheel，可避开 Python 3.11 在非 ASCII 路径的 editable `.pth` 文件解码问题。

若使用 Codex Desktop，生成本机忽略配置：

```powershell
python .codex/setup_mcp.py
```

在信任该仓库的 Codex Desktop 窗口中新建对话，并调用 `health_report`。配置细节见 [Codex Host Setup](docs/codex-host-setup.md)。其他 MCP client 可通过本机 stdio 启动同一 Gateway；项目不开放公网服务端点。

Codex launcher 使用 `uv run --no-sync`；首次安装及更新依赖后，先重新运行 `uv sync`。

Study 检索可选用外部安装的 QMD 和 Node.js；项目不安装或捆绑它们。OCR 需要额外安装 Tesseract 和语言数据。启用 `pdf-ocr` extra 的命令为 `uv sync --project . --extra pdf-ocr --no-editable`；其中 PyMuPDF 有独立的 AGPL 或商业授权条件，见 [许可证审计](docs/license-audit.md)。

## Current release / 当前版本

当前正式版本是 **[v0.7.0 — History Completion & Recovery](docs/releases/v0.7.0.md)**。后续 acquisition closure 对账为 1,804 sources/outcomes、487 个 canonical conversations、7,334 条 distinct messages 和 1,351 条 wholly source-only records。完整统计、Host 状态和恢复证据见[当前状态](docs/current-state.md)。

## Known limitations / 当前限制

- 当前 transport 为本机 stdio MCP；ChatGPT hosted MCP 和 Secure MCP Tunnel 尚未实现。
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
