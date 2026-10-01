# P12 Step 3 — Hermes Integration checkpoint

日期：2026-10-01。状态：**WAITING_FOR_USER — model service authentication/connectivity**。
目标 v0.5.0 未发布，当前仍 0.4.0。没有以 transport/SDK 证据替代真实 Agent Gate。

## Reality audit

- 当前 worktree 干净 detached HEAD 起点为 a995e58b15f74165ae50c9cfc1ad18b9a0e5144d。
- 远端 main、v0.4.0 target 相同；annotated tag object 为 50a7fa0076197c5c36d5922b1c765c2553a4ac13。
- 已创建 codex/p12-step3-hermes-integration；没有改写旧版本或执行 force push。
- 本机 Hermes CLI reports v0.20.0 (2026.8.3)，安装为 Windows local app 下的
  hermes-agent source tree + Python 3.11.15 venv。安装源 remote 为 NousResearch/hermes-agent。
  未证明独立 Desktop shell 的版本等于 CLI version，不将二者混称。
- 实际 home 由 HERMES_HOME 指定，配置为该 home 下 config.yaml；原先 mcp_servers 为空。
- 本机源码与官方资料支持 stdio/StreamableHTTP/SSE；本集成使用 stdio。
  command/args/env 已真实验证，未依赖相对 cwd。
- user/profile home 与 managed overlay 是实际 loader 路径；当前 managed scope absent。
  native 同名定义优先于 portable plugin（后者跳过）。项目 AGENTS 是行为指导，
  未观察到单独 project MCP config 被自动读取，不套用 WorkBuddy precedence。
- 新 CLI 进程重读 config、发现工具已验证；Desktop live reload/restart 尚未验证。
  官方 reload/watch 描述不能代替本轮行为证据。

## Config and Memory

用户已授权配置。实际 user config 先在 Git 外备份，再合并独立 production
study_system 入口。Gateway 的只读配置保留原后端，仅 capabilities=["read"]。
原 production config 字节保持一致；未改 WorkBuddy config / Basic Memory 状态。
Gateway launcher 引用既有正式 checkout/venv，公开文档只含占位符。
sampling.enabled=false，无 business/transport adapter，无新增 Gateway 智能层。

memory.memory_enabled=false、user_profile_enabled=false 已由实际 config loader
确认生效；外部 memory provider 未配置，未创建新的 Knowledge Base。
这些为持久 user-level 设置，影响共享该 home 的后续 Hermes 会话；备份可恢复。
既有记忆未删除。Hermes 原生会话/runtime 元数据可保留，但不可作为 V2 权威数据，
不可用 session_search 补 Gateway 缺证据。尚未证明模型实际遵循此规则。

## Native transport evidence (not Agent E2E)

`hermes mcp test study_system` 真实产品 CLI 成功连接，发现 15 个只读 Gateway tools。
fresh process 经 Hermes 的 discover_mcp_tools 与原生注册 handler 调用 health：
ok=true、gateway_version=0.4.0、history.backend=sqlite。
注册列表含 4 个 resource/prompt utility，因此 19 个注册名称不代表 19 个 Gateway tools。

同一原生通道用唯一不存在标记查询 search_study/search_legacy_sources/search_wrong_answers：
全部 ok=true、results=[]；后两者 total=0，Study 未提供 total，不虚构计数。
原始 Gateway 回执仅存 Git 外。全程未打开 private DB/store。
未提取或输出真实学习正文，也未以文件系统验证学习数据。

## Model blocker

1. 现有默认 provider/model 的真实 `hermes -z` 重试三次后 Connection error。
2. 独立 HTTPS 请求复现 TLS UNEXPECTED_EOF，直连及现有本机代理均失败。
3. 既有备用 provider 的 HTTPS 可达；单次 Hermes override（未改默认模型）返回
   HTTP 403「无权访问 稳定组 分组」，尚未发生 Agent 工具调用。
4. 无 TLS 校验绕过，无新增密钥，无账号修改；已请求用户在 Hermes 恢复有权限的
   模型并确认普通对话可回复。用户无需通过聊天提供 credentials。

生产真实 Agent read-only 通过前不执行 controlled write。
没有建立 synthetic Wrong Answer、v1/v2 或隔离 Projection；没有发布/tag/push v0.5.0。
不执行 Step 4、不迁移会话、不重验 WorkBuddy。

## Final Gate (8 PASS / 14 WAITING; not release-ready)

| Item | Status | Evidence / remaining work |
| --- | --- | --- |
| Hermes Reality Audit | PASS | 安装、CLI version、本机源码、官方 transport/config 路径；Desktop 未验证限制明确 |
| Hermes Installation | PASS | executable/source/venv + CLI version |
| MCP / Integration Configuration | PASS | 持久 native stdio user config，原 production 未覆盖，read-only capability |
| Gateway Connection | PASS | 真实 Hermes native CLI discovery + handler health；尚非 Agent behavior |
| Canonical Workflow | WAITING | 真实 Agent 读取 canonical resource 并按其执行 |
| Study Retrieval | WAITING | Agent 存在/不存在检索 |
| History/Source Retrieval | WAITING | Agent source-only 检索与有界回读 |
| Wrong Answer Retrieval | WAITING | Agent active bundle/version |
| Asset/Document References | WAITING | Agent 实际 logical refs / bounded reads；缺引用不构造 |
| Gateway-only Boundary | WAITING | 规则已存在；未得到 Agent runtime 行为证据 |
| No-result Guard | WAITING | native 空结果已验证；Agent 无幻觉仍待验证 |
| Controlled Write | WAITING | 依赖 production Agent PASS，独立 server/target |
| Versioning | WAITING | 同一隔离 source 仅 v1/v2 |
| Idempotency | WAITING | exact request/key replay 不生成 v3 |
| Stale Conflict | WAITING | new key + stale expected_version=1 返回 conflict |
| Provenance | WAITING | Gateway timestamps/IDs + reported identity |
| Restart Persistence | WAITING | 真实 Host 退出后重启与 exact baseline comparison |
| Projection Interoperability | WAITING | scoped collector → renderer → writer，两次 byte-identical |
| Hermes Memory Conflict Audit | PASS | native Memory/profile disabled，外部 provider 未配置；runtime metadata 边界明确 |
| Privacy | PASS | 公开排除规则和针对性测试；本轮 tree/package/object 审计见后文，未来 release 必须重审 |
| Regression | PASS | targeted 62 passed；full 622 passed / 12 skipped |
| Documentation | PASS | design/plan/setup/current-state/compatibility/checkpoint 明确真实证据和剩余 Gate |

## Automated verification and privacy

先运行新增 5 个 Hermes private-tree 排除测试，全部失败；添加公共 .hermes/ 排除后通过。
targeted Projection/provenance/MCP/Wrong Answer/privacy：62 passed。
full default/dev：622 passed / 12 skipped；无失败。skip 为既有真实 Codex/QMD opt-in、
Windows symlink/junction/POSIX 权限能力与 optional PyMuPDF 缺失，不补称已执行。
git diff --check 通过；不将 CRLF 提示解释为错误。

包保持 version 0.4.0。曾在 checkout 放入明确 synthetic-only .hermes config sentinel
并构建 wheel/sdist，用于验证真实 packaging exclusion；随后删除该测试文件。
绝不复制实际 Hermes config。包及公开候选扫描的广义 Windows path 命中经人工检查
均为已有合成隐私测试中的 fictional/example/nora/x/a/private 路径或字符串断言，
不能误报为真实私人路径；新增文档不含真实本机绝对路径。
本轮最终 staged tree 为 164 个文件；wheel 42 files、sdist 165 files。
无受限 host/runtime artifacts、sentinel、credential pattern 或新增私人绝对路径。
5 个已有合成路径测试文件与 v0.4.0 内容一致（包内 CRLF 归一化后比较），已逐项复核。
全新 venv 从 wheel 安装成功；不带 checkout PYTHONPATH 的独立 stdio smoke 验证
version 0.4.0、15 read-only tools 与 canonical workflow resource；没有连接生产。
smoke 初次使用不支持的 synthetic collection 名称被配置校验拒绝，修正为约定的
studyvault 后通过，未改 Gateway 校验。
staged tree objects 在 commit 前审计；commit 后再检查 v0.4.0..HEAD 新增 reachable objects，
实际对象清单只存私有工程回执。没有新 tag，未 push 或创建 GitHub Release。
未来 v0.5.0 release 仍必须重新审计实际 v0.4.0→release object delta 和全部包。

## Resume

模型可回复后先真实 Hermes production Agent Gate，再独立 isolated controlled target。
保留 branch/配置/私有回执，继续现有任务，不从零重做，不复用 native evidence 冒充 Agent PASS。

### 从 b75c62d 继续的实际调用结果

用户报告模型已可用，授权继续剩余 14 项，不重跑 8 项 PASS。
本轮复用干净开发分支与持久配置，未重新验收原有 PASS 项。
直接启动 production read-only Agent 验收，但持久 CLI 默认 provider/model 仍为旧入口，
真实调用仍返回 Connection error，独立 HTTPS 复现 TLS EOF。
现有备用 provider 的两个已配置模型也均返回 HTTP 403「无权访问 稳定组 分组」。
单次 override 不修改用户默认模型；未替换凭证或关闭 TLS 校验。

这些失败调用的 CLI 退出码为 0，必须检查错误输出与实际 tool trace，不能仅用退出码
作为 E2E 成功证据。工具阶段尚未开始，Gate 仍为 8 PASS / 14 WAITING。
尚无法确认用户成功的 GUI 会话使用哪个 provider/model；已请求这两个非敏感名称
（或 profile），无需用户提供密钥或重复登录。
已在 Git 外准备下一阶段 synthetic canonical prompt，但未执行、未建立隔离 store。
未重复 regression/privacy Gate，未更新版本、tag、push 或 Release。
