# ADR-001: Greenfield V2

状态：Accepted
日期：2026-09-25

## Context

V1 跨 WorkBuddy 全局状态、StudyVault、Basic Memory、QMD、archive Hook 和独立 Python Router。Router 无真实主链路接入证据，并存在自动持久化、身份隔离、并发与幂等风险。真实价值集中在用户数据和已验证工作流，而非原型结构。

## Decision

创建全新的 V2 应用仓库。V1 代码不作为 V2 runtime dependency；StudyVault、Basic Memory、archive、教材和错题保持原位并作为只读外部源。任何迁移另立方案，必须有备份、manifest、小样本验证和回滚。

## Consequences

- 获得清晰模块边界、隐私规则和可重复测试。
- 初期需要重写少量 adapter 和 transport glue。
- V1 继续可用，直到 V2 逐项证明替代能力。
- Phase 3 不迁移或修改任何真实数据。

## Rejected

- 继续扩建 V1 Python Router：会保留错误边界和历史耦合。
- 直接重写 V1 数据目录：数据风险不可接受。
