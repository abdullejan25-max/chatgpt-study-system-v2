# P12 Step 3 — Hermes Integration checkpoint

日期：2026-10-01。状态：**REAL VALIDATED — 22/22 Gate PASS; v0.5.0 release candidate verified**。
全部真实 Host Gate 通过后，发布版本更新为 0.5.0；真实 E2E 基线为 0.4.0。
没有以 transport/SDK 证据替代真实 Agent Gate。

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
不可用 session_search 补 Gateway 缺证据。初始 checkpoint 尚无 Agent 行为证据；后续真实 trace 验证遵循边界，见下文。

## Native transport evidence (not Agent E2E)

`hermes mcp test study_system` 真实产品 CLI 成功连接，发现 15 个只读 Gateway tools。
fresh process 经 Hermes 的 discover_mcp_tools 与原生注册 handler 调用 health：
ok=true、gateway_version=0.4.0、history.backend=sqlite。
注册列表含 4 个 resource/prompt utility，因此 19 个注册名称不代表 19 个 Gateway tools。

同一原生通道用唯一不存在标记查询 search_study/search_legacy_sources/search_wrong_answers：
全部 ok=true、results=[]；后两者 total=0，Study 未提供 total，不虚构计数。
原始 Gateway 回执仅存 Git 外。全程未打开 private DB/store。
未提取或输出真实学习正文，也未以文件系统验证学习数据。

## Historical model blocker (resolved)

1. 现有默认 provider/model 的真实 `hermes -z` 重试三次后 Connection error。
2. 独立 HTTPS 请求复现 TLS UNEXPECTED_EOF，直连及现有本机代理均失败。
3. 既有备用 provider 的 HTTPS 可达；单次 Hermes override（未改默认模型）返回
   HTTP 403「无权访问 稳定组 分组」，尚未发生 Agent 工具调用。
4. 无 TLS 校验绕过，无新增密钥，无账号修改；已请求用户在 Hermes 恢复有权限的
   模型并确认普通对话可回复。用户无需通过聊天提供 credentials。

以下为初始阻塞时点的状态：生产真实 Agent read-only 通过前不执行 controlled write；
当时未建立 synthetic Wrong Answer、v1/v2 或隔离 Projection，未发布/tag/push v0.5.0。
不执行 Step 4、不迁移会话、不重验 WorkBuddy。

## Final Gate (22 PASS / 0 WAITING)

| Item | Status | Evidence / remaining work |
| --- | --- | --- |
| Hermes Reality Audit | PASS | 安装、CLI version、本机源码、官方 transport/config 路径；Desktop 未验证限制明确 |
| Hermes Installation | PASS | executable/source/venv + CLI version |
| MCP / Integration Configuration | PASS | 持久 native stdio user config，原 production 未覆盖，read-only capability |
| Gateway Connection | PASS | 真实 Hermes native CLI discovery + handler health；尚非 Agent behavior |
| Canonical Workflow | PASS | 真实 Agent resource discovery/read + retrieval-only canonical workflow |
| Study Retrieval | PASS | 真实 Agent QMD 查询 2 命中与唯一不存在查询 0 命中 |
| History/Source Retrieval | PASS | 真实 Agent source search 与 128 bytes bounded fetch；source-only 语义保持 |
| Wrong Answer Retrieval | PASS | 真实 Agent active bundle，实际 analysis_versions=[1] |
| Asset/Document References | PASS | production real Asset bounded read + isolated real Agent document/page/original Asset refs |
| Gateway-only Boundary | PASS | 官方 session export trace，仅 tool_describe/tool_call 桥接到生产 Gateway read tools |
| No-result Guard | PASS | 真实 Agent 三类不存在检索均 ok=true/results=[]，回答明确无结果 |
| Controlled Write | PASS | 真实 Hermes Agent 15 isolated Gateway calls；document/source/v1/v2/readback |
| Versioning | PASS | final bundle total=2，versions=[1,2]，v2 supersedes v1 |
| Idempotency | PASS | 两次 update 的完整 request args 与 response exact-equal，均返回 v2 |
| Stale Conflict | PASS | new key + expected_version=1；实际 Gateway CONFLICT，无 v3 |
| Provenance | PASS | Gateway timestamps/IDs/data_origin/source_refs 与 reported/unverified caller；provenance supersession |
| Restart Persistence | PASS | actual CLI Host exited → new PID，Gateway search 回收实际 ID；document/page/full bundle exact-equal，无额外归一化 |
| Projection Interoperability | PASS | 两次正式 isolated MCP → scoped collector → renderer → manifest-owned writer；14 Markdown 与 manifest byte-identical |
| Hermes Memory Conflict Audit | PASS | native Memory/profile disabled，外部 provider 未配置；runtime metadata 边界明确 |
| Privacy | PASS | 公开排除规则和针对性测试；本轮 tree/package/object 审计见后文，未来 release 必须重审 |
| Regression | PASS | 原 checkpoint targeted 62 passed；发布 targeted 89 passed / 2 skipped，full 622 passed / 12 skipped |
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

### DeepSeek model resolution and production Agent acceptance

界面名称 Deepseek V4 Pro High 经本机 picker/display source 与 provider resolver
确认对应内置 provider=deepseek、model=deepseek-v4-pro、reasoning=high。
profile 为既有 default；resolver 使用官方 DeepSeek API endpoint 与已配置凭证，
没有修改持久旧默认模型、复制密钥或关闭 TLS 校验。真实 probe 回复成功。

随后真实 Hermes CLI Agent 完成 production read-only E2E；官方 sessions export 的
完整 trace 共 16 次 Gateway 工具调用，另有 tool_describe schema bridge。
所有 bridge target 均为 study_system；没有 shell/filesystem/SQL/session_search/Memory
或写入调用。官方 export 是 Host 调用证据，不是直接解析 V2/Hermes SQLite。
Study 有 2 个实际命中、source 查询实际命中后读取 128 bytes、active Wrong Answer
bundle 版本列表为 [1]，实际原始 Asset 读取 64 bytes。三类唯一不存在查询均为空，
不提供 total 的 Study 仅报告结果数。production bundle 没有 Document URI，未伪造。
最终 Agent 回答只输出有界结果元数据，原始 receipt/export 保存在 Git 外。

已在真实 production PASS 后建立独立 isolated target/config/assets/store/inbox/Vault，
server=study_system_p12_hermes_isolated，不同名覆盖 production。History 明确
not_configured；Study 为独立空目录，QMD 未配置可用，不生成假 Study relations。
production MCP definition 保持值相等；该时点 controlled write 正在真实 Agent 中执行。

### Controlled write / provenance — REAL VALIDATED

真实 Hermes CLI Agent 只调用 isolated server，官方 trace 记录 15 次 Gateway operations。
canonical resource → exact synthetic text document ingest → document/page/original Asset reads
→ immutable Wrong Answer source → v1 save/readback → expected_version=1 update v2/readback
→ exact request/key replay → new key stale expected_version=1 conflict → final bundle。
其 question/analysis 明确标注 P12 Hermes integration-test / SYNTHETIC ONLY，study_relations=[]。

机器对账确认两次幂等更新所有 argument 值完全一致，response 完全一致；stale 请求
仅 key 改变，仍 expected_version=1，实际 Gateway code=CONFLICT。Hermes bridge 将错误
包装为 error JSON 字符串，校验时进一步解析，而非凭 Agent 口头声明。
final bundle total=2、版本 [1,2]，v2 supersedes v1，未创建 v3。
Document/source/v1/v2 的 write_provenance 身份均 reported、agent=Hermes；
recorded_at、created_at、data_origin、logical refs、provenance IDs 与 supersession 由 Gateway 提供。

完整 document/page/final bundle baseline 来自该 Host 退出前的真实工具回执，
没有从 private DB/store 取数。第一 Host 已正常退出，随后启动不同 PID 的全新 Hermes
CLI Host 做只读重连；不退出用户其他 Desktop/messaging 会话。restart exact comparison
在该时点正在执行；本 Gate 范围是实际 CLI Agent Host，不冒称 Desktop shell 重启。

### Restart / Projection — REAL VALIDATED

首次 restart 的 source_id 被 Agent 抄为 65 hex chars，Gateway INVALID_ARGUMENT；
该轮 FAIL，不作为通过证据，Document/page 已能正常读取。无需改 Gateway 或读取 DB。
后续完全退出该 Host 并启动新 CLI Host，经 search_wrong_answers 实际返回的 ID 回读：
完整 document、page、bundle 与首次写入 Host 退出前 trace 中 DTO 原样 exact-equal。
比对未追加文本/时间/路径归一化；Gateway DTO 自身的既有隐私脱敏保留，不声称读取 raw store。
所有 identities/timestamps/provenance/version graph 均一致，仅 v1/v2，无 v3。
CLI Host PID/退出时序有私有工程回执；未将用户其他 Desktop 会话重启冒充该测试。

Projection 通过持久 isolated server 的 native MCP client 调用 projection_snapshot，
既有 collect_wrong_answer_projection 做两次独立完整采集；纯 renderer 与正式
manifest-owned writer 在项目运行环境处理 Gateway 采集 DTO。没有私有 store 直读。
History not_configured 明确 omitted，不断言为空。MCP optional None 参数按 schema 省略；
初次脚本误传 null 被拒绝，修正 client 参数组装，不改变 Gateway 或增加业务 adapter。
既有 Projection provenance 为四字段隐私摘要，与完整 readback provenance 对应字段相等，
不把摘要称为全 provenance IDs。纯 renderer 的依赖使用项目 venv，未向 Hermes 安装新依赖。

1 Source / 2 analyses，latest=v2，v2 supersedes v1；document ref 正确，Study relations=[]。
两次产生 14 个 Markdown；每一文件及 manifest 回读相等，连续构建 byte-identical。
无重复页面、私人绝对路径或 raw Asset bytes；bundle 构建前后 exact-equal；未访问生产。
前期 helper 的宽松 drive regex 误匹配 logical URI，已改用既有 build 的边界 regex，
不是放宽真实私人路径检查。未重开 Step 1 GUI 或执行 Step 4 cross-agent matrix。

全部 22 项通过后进入已授权发布；原有 8 项不重新执行 Host Gate。
版本变更后的 regression/package/privacy/object/clean-install 属发布验证，会独立执行。

### v0.5.0 release verification

独立最终复核确认 restart 三项正式 DTO exact comparison 与 scoped Projection 证据，
并修正 architecture 中过时的 Hermes deferred 文字。无新增 business adapter 或 Gateway 行为变化。
版本同步 pyproject、lock、config example 到 0.5.0；私有 production 原配置、Hermes
read-only 配置与 isolated 配置仅 gateway.version 改为 0.5.0，其余 TOML 值完全一致，
均在 Git 外备份。未修改学习内容或 WorkBuddy Host 配置。

发布 targeted：89 passed / 2 skipped；full：622 passed / 12 skipped。
skip 为现有可选 Codex/QMD/PyMuPDF 和 Windows symlink/junction/POSIX/FIFO 限制。
git diff check 通过。公开候选 165 files；wheel 42 files；sdist 166 files。
tracked/staged/untracked 和包扫描无 Host config/log/session/memory/credential、学习原件或
新增私人路径。六个已有合成路径/检查代码文件与 v0.4.0 内容一致，逐文件复核，
不是将宽泛排除规则当作隐私通过。

独立新 venv 从 0.5.0 wheel clean install，通过未带 checkout PYTHONPATH 的真实 stdio：
package/MCP/Gateway version 0.5.0、15 read-only tools、canonical resource、health PASS。
只连接独立无数据配置，不访问生产。Apache-2.0 LICENSE 与 metadata 正常，PyMuPDF 仍为可选 extra。

v0.4.0 之后的已有 commit/tree/blob 在提交前审计；实际 release commit 后、push 前
再审计完整新增 reachable objects 及 annotated tag，回执留在 Git 外。
正常 fast-forward main / annotated v0.5.0 / push / GitHub Release 后，远端 refs、
公开 fresh-clone clean install / stdio 结果记录于正式 Release 的 Remote verification 段，
不以本地轮子或历史 0.4.0 验证替代远端验收。
