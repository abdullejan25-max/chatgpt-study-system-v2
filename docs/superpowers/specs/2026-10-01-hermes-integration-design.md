# P12 Step 3 Hermes Integration design

用户已授权自主完成调查、实现、验收和有条件发布；无需重复设计审批。
基线为 v0.4.0 / a995e58b15f74165ae50c9cfc1ad18b9a0e5144d。

## Architecture

优先 Hermes 原生 MCP stdio → study_system → Gateway。安装版本已确认
v0.20.0 (2026.8.3)，其 native client 支持 command/args/env。
无需业务 adapter。只有正式 transport 不兼容时才考虑纯 transport adapter。
生产只读配置引用原有 stores；隔离服务器使用不同名称、独立配置和 stores。
生产只读真实 Agent 验收通过前不执行隔离 controlled write。

## Boundaries

所有 V2 读写（包括计数）通过 Gateway；不读取或打开 private stores。
禁用 Hermes 自动 Memory、用户 profile 和外部 memory provider 对本集成的使用；
必要的 session/runtime metadata 可保留，不能成为 V2 权威数据或替代检索。
身份仍 caller-reported/unverified。Projection 复用已有 scoped collector、renderer、writer。
不执行 Step 4、迁移或重新验收 WorkBuddy。

## Evidence and errors

区分真实 Agent 行为、Hermes native MCP client transport、SDK corroboration、自动测试。
模型连接失败不能解释为 MCP 失败；native discovery 不能代替 Agent E2E。
缺失 logical ref 不构造 URI；no-result 如实为空；unavailable 不等于 empty。

## Release

22 项 Gate 全部有证据通过后才改版本、tag、push 和 Release。
发布前检查 tree/staged/untracked、wheel/sdist 和 v0.4.0 之后 reachable objects。
受模型服务/login/信任阻塞时记录真实 blocker，继续所有独立工程工作，保留 0.4.0。
