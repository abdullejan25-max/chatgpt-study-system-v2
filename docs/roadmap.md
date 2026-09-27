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
Phase 10：GitHub Release Hardening (in progress; clean release-candidate Desktop verification pending)
```

Phase 1–9 已完成本地实现与回归验证。Secure MCP Tunnel / ChatGPT remote MCP 是未来可选 transport，不属于项目本地完成条件。

P10 围绕 portable bootstrap、隐私边界、Apache-2.0 许可、PyMuPDF optional 隔离、clean checkout、文档和公开发布准备。旧开发历史会保留在本地，不改写；公开历史将从独立新 root commit 开始。开发 checkout 的 Desktop Host 已由项目所有者确认通过；最终 clean release candidate 的 GUI 验证仍需人工完成。详情见 [P10 Release Gate](p10-release-gate.md)。

```text
Phase 4：Architecture Rebaseline ✅
Phase 5：Personal History Read Layer ✅
Phase 6：Document & Asset Pipeline ✅ (PDF extraction implemented; native OCR has an external Tesseract gate)
Phase 7：Wrong Answer Pipeline ✅
Phase 8：Safe Write Layer ✅
Phase 9：Agent Interoperability ✅
Phase 10：GitHub Release Hardening (in progress; clean release-candidate Desktop verification pending)
```

Each phase is gated by synthetic tests and a coherent local commit. Phase 9 verified an independent stdio MCP client against the same server/Core used by Codex. ChatGPT remote MCP remains deferred as an external capability and is not an exit gate.
