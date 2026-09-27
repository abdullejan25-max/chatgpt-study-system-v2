# 项目路线图

```text
Phase 1：V1 审计 ✅
↓
Phase 2：ChatGPT-first V2 架构 ✅
↓
Phase 3：只读 MCP Spike ✅
↓
Phase 4–9：Local Study Infrastructure ✅
  ├─ Architecture / Single-Brain ✅
  ├─ StudyVault / QMD read path ✅
  ├─ Personal History read path ✅
  ├─ Documents / Assets / PDF extraction ✅
  ├─ Wrong Answer pipeline ✅
  ├─ Safe write policy / audit ✅
  └─ Codex + independent MCP client ✅
↓
Phase 10：GitHub Release Hardening ✅ (`v0.1.0` published)
↓
Phase 11：Legacy Migration ⏸ BLOCKED（只读 audit/dry-run 完成；History 与错题关系 gate 未通过）
↓
Phase 12：Agent Projection & Interoperability ⏸ PREPARATION（Obsidian 纯内存 renderer 已实现；全量枚举、Vault GUI 与多 Host Gate 未通过）
```

Phase 1–9 已完成本地实现与回归验证。Secure MCP Tunnel / ChatGPT remote MCP 是未来可选 transport，不属于项目本地完成条件。

P10 围绕 portable bootstrap、隐私边界、Apache-2.0 许可、PyMuPDF optional 隔离、clean checkout、文档和公开发布准备。旧开发历史保留在本地；公开历史从独立新 root commit 开始。真实 GitHub fresh clone 与 clean release candidate 的 Desktop Host 验证均通过，`v0.1.0 — Initial Public Release` 已发布。详情见 [P10 Release Gate](p10-release-gate.md)。

Phase 11 已完成旧数据盘点、StudyVault 原地复用验证及本机只读 dry-run；没有向 V2 业务库写入。History 后端未配置，旧错题图文关系无法验证，因此真实迁移与 v0.2.0 release preparation 均未通过 Gate。详细分类、计数和技术条件见 [Phase 11 Legacy Migration](phase-11-legacy-migration.md)。

```text
Phase 4：Architecture Rebaseline ✅
Phase 5：Personal History Read Layer ✅
Phase 6：Document & Asset Pipeline ✅ (PDF extraction implemented; native OCR has an external Tesseract gate)
Phase 7：Wrong Answer Pipeline ✅
Phase 8：Safe Write Layer ✅
Phase 9：Agent Interoperability ✅
Phase 10：GitHub Release Hardening ✅ (`v0.1.0` published)
Phase 11：Legacy Migration ⏸ BLOCKED
```

Each phase is gated by synthetic tests and a coherent local commit. Phase 9 verified an independent stdio MCP client against the same server/Core used by Codex. ChatGPT remote MCP remains deferred as an external capability and is not an exit gate.

Phase 12 preparation includes a deterministic in-memory Obsidian renderer and a synthetic cross-client stdio parity test that exercises shared Gateway versioned writes/read-back across process restarts. The renderer does not query a complete corpus or write a Vault; the parity test does not configure WorkBuddy/Hermes. Full History and wrong-answer enumeration, a confirmed private Vault target, GUI review, and real Host checks remain prerequisites; no Phase 12 gate or release is claimed PASS.
