# Hermes Integration Implementation Plan

执行方式：当前工作树顺序执行；用户已明确自主工程授权。

**Goal:** 真实 Hermes 安全接入现有 Gateway，全部 Gate 通过后发布 v0.5.0。
**Architecture:** 原生 stdio，独立 production/read-only 与 isolated server，复用 Gateway。
**Tech Stack:** Hermes native MCP、Python MCP SDK、现有 pytest/Projection、Hatch。

## Global Constraints

- Agent thinks; Gateway executes；V2 数据不直接通过文件/SQLite 读取。
- 不覆盖 production、不写生产 synthetic 数据；身份 reported/unverified。
- 版本仅在真实 Host Gate 全 PASS 后更新；无需反复审批。

## Tasks

- [x] 核实根目录、状态、HEAD、远端 main/tag；核对 Hermes executable/version/source。
- [x] 查标准 transport、user/profile/managed config、Memory、reload/restart 模型。
- [ ] 配置持久 native stdio production read-only；私有备份和参数仅存 Git 外。
- [ ] 验证 native discovery/health；修复可证实的模型连接问题。
- [ ] 真正 Agent production retrieval、bounded refs、三类 no-result、Gateway-only。
- [ ] 通过上项后建立独立 target，真实 Agent canonical v1/v2/idempotency/conflict。
- [ ] 保存 baseline，退出/重启 Host，exact comparison；两次 scoped Projection。
- [ ] targeted/full tests，增加有意义的 integration/privacy 测试（先失败后修复）。
- [ ] docs/checkpoint 明确证据层级及 blocker；package/privacy/object audit。
- [ ] 全 Gate PASS 后 version/release notes/build/commit/main/tag/push/Release。
- [ ] remote verification、fresh clone clean install、stdio smoke。
