# Bounded Projection Enumeration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add explicitly authorized, bounded, per-store Gateway enumeration for future P12 projection collection.

**Architecture:** Add a separate `projection` capability and a three-operation snapshot protocol (`begin`, `sources`, `records`). Each SQLite store captures its own high-water token and validates later pages against it. The Gateway exposes safe DTOs; the renderer and writer remain separate.

**Tech Stack:** Python, SQLite, existing Gateway/MCP contracts, pytest.

## Global Constraints

- Bulk export requires the explicit `projection` capability; plain `read` does not grant it.
- Keep History and Wrong Answer watermarks independent; never claim cross-store atomicity.
- Use only synthetic SQLite databases in tests.
- No filesystem output, private database reads, or real Vault integration.
- Enforce page size 20, per-domain source/record caps of 10,000, History source-plus-item cap 10,000, and per-domain stored-payload cap 32 MiB.
- Use fixed public errors without paths, record content, or backend diagnostics.

---

### Task 1: Implement per-store snapshot adapters

**Files:**
- Modify: `src/chatgpt_study_system/adapters/history.py`
- Modify: `src/chatgpt_study_system/adapters/wrong_answers.py`
- Test: `tests/test_history.py`
- Test: `tests/test_wrong_answers.py`

- [x] Add failing tests for `begin`, `sources`, and `records` operations; include inserts after `begin` and verify they are excluded by the captured watermark.
- [x] Add failing tests for page/cursor validation, total count and byte bounds, and stable deterministic ordering.
- [x] Implement read-only SQLite snapshot token capture and keyset pagination for each store; never create a database during export.
- [x] Ensure Wrong Answer analysis pages preserve version and `supersedes_analysis_id` ordering.
- [x] Verify existing store tests plus new focused adapter tests.

### Task 2: Add Gateway capability and DTO operations

**Files:**
- Modify: `src/chatgpt_study_system/contracts.py`
- Modify: `src/chatgpt_study_system/gateway.py`
- Modify: `src/chatgpt_study_system/runtime.py`
- Test: `tests/test_history.py`
- Test: `tests/test_wrong_answers.py`
- Test: `tests/test_runtime.py`

- [x] Write failing tests proving plain `read` is denied and `projection` permits only read-only projection operations.
- [x] Add a `projection` capability without changing the meaning of existing capabilities; validate it in config and Gateway construction.
- [x] Validate and serialize each page through Gateway safe DTO handling, including local-path redaction, logical source references, categorical provenance, and payload bounds.
- [x] Verify the new Gateway methods do not write to either store by checking audit counts and read-only adapter connections.

### Task 3: Expose a gated MCP tool

**Files:**
- Modify: `src/chatgpt_study_system/transports/mcp_stdio.py`
- Test: `tests/test_mcp_stdio.py`
- Test: `tests/test_history_mcp.py`
- Test: `tests/test_wrong_answer_mcp.py`

- [x] Add one strict `projection_snapshot` tool schema for `begin`, `sources`, and `records`; mark it read-only.
- [x] Filter it from tool listings unless `projection` or `admin` is enabled and enforce capability again at call time.
- [x] Test schema limits, invalid arguments, `read` denial, and synthetic paging through the MCP transport.
- [x] Run focused tests, full suite, and `git diff --check`; update public/private checkpoints with exact evidence.
- [x] Commit the implementation and checkpoint separately.

## Task 4: Collect and reconcile complete renderer snapshots

**Files:**
- Add: `src/chatgpt_study_system/projection_collector.py`
- Test: `tests/test_projection_collector.py`

- [x] Verify 21-source synthetic snapshots cross domain page boundaries and a 21-analysis source crosses the records page boundary.
- [x] Reconcile per-source and domain totals; reject mismatched counts and nonadvancing cursors without returning a partial snapshot.
- [x] Construct the existing pure `ProjectionSnapshot` input and render it in a synthetic end-to-end test.

This does not claim cross-store atomicity or a real Host/Vault gate.
