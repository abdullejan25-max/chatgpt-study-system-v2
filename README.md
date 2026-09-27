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
- **Personal History**：读取显式登记的本地 History store；系统不会扫描聊天记录或自动导入历史。
- **Wrong Answers**：原始图片或文档作为证据，Agent 提供分析，Gateway 按权限保存来源和带版本的分析，并记录 provenance。不同 MCP Agent 使用同一套 `study-workflow://wrong-answer` 工作流。
- **Assets & Documents**：Gateway 对明确提交的来源做边界检查、哈希与登记；原始证据和派生文字保持可区分。

更完整的组件职责和安全约束见 [架构说明](docs/architecture.md)、[隐私边界](docs/privacy-boundary.md) 和 [ADR](docs/adr/)；已验证的错题链路证据见 [Real Wrong Answer E2E checkpoint](docs/real-wrong-answer-e2e-checkpoint.md)。

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

P1–P9 的本地功能已完成；P10 Release Hardening 的验收状态和当前测试基线见 [当前状态](docs/current-state.md) 与 [P10 Release Gate](docs/p10-release-gate.md)。项目运行和 MCP 调用不会自动推送代码或上传个人学习资料。
