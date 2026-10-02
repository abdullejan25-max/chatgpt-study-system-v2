# P13 Canonical Normalization Implementation Plan

> Use executing-plans and test-driven-development in the existing worktree.
> Owner authorizes autonomous execution; review is an engineering check, not a pause.

**Goal:** Persist only deterministic canonical history, preserve every source and
explain every normalization outcome through formal Gateway operations.

**Architecture:** Pure adapters produce candidates/views; an additive SQLite derived
store persists immutable records/evidence/outcomes; Gateway validates source bytes,
attachments and pinned source sets. MCP is the Agent data boundary.

**Tech Stack:** Existing Python/SQLite/MCP and stdlib; no new DB engine or LLM.

## Constraints

- Source-only Gate already PASS; do not redo P11/P12/Gemini or unrelated audits.
- Real payloads/paths/receipts/ledgers/backups never enter Git.
- Production reads/writes, counts and recovery checks remain Gateway-owned.
- Only exact/derived-safe message candidates; unknown roles/boundaries/order stay source-only.
- Unknown time is nullable, never replaced by imported_at or normalized_at.
- Original source bytes and existing APIs remain unchanged.

## Task 1 — Pure deterministic adapters

Create `normalization/contracts.py`, `normalization/adapters.py` and source-specific
modules; tests `test_conversation_normalization.py` use invented bytes only.

- [ ] RED: linear messages, missing time, unknown role, malformed JSONL/duplicates,
  multiple session IDs, branch graph/cycles/hidden nodes, unsupported source,
  missing attachments and source-preserving candidate identities.
- [ ] GREEN: versioned candidate/view/outcome contracts, stable identities and exact
  source locators; inspect private schema signatures without exposing content.
- [ ] Targeted tests and independent adapter review; no production writes yet.

## Task 2 — Derived store and Gateway/MCP

Create `adapters/canonical_history.py`, `normalization/execution.py`,
`transports/canonical_tools.py`; extend Gateway/MCP narrowly.

- [ ] RED: source-set conflict, per-source atomicity, reopen/readback, duplicate
  canonical rerun, stable provenance/times, source view order, attachment mapping,
  permission boundaries, old API compatibility and literal no-result.
- [ ] GREEN: immutable canonical tables/evidence links/outcomes, bounded public
  searches/read APIs, deterministic execution and private batch receipts.
- [ ] Independent review, targeted regression and installed-package fresh Host discovery.

## Task 3 — Private normalization and reconciliation

- [ ] Formal Gateway normalizes acquired set, retaining unsupported/ambiguous evidence.
- [ ] Repeat all normalization; require zero new canonical records and stable proof.
- [ ] Source-by-source accounting and aggregate confidence/candidate/record counts.
- [ ] Gateway search/view/message/known sample/cross-source/no-result readback.
- [ ] Minimal real Codex/WorkBuddy/Hermes canonical history reads; no P12 rerun.

## Task 4 — Recovery, V1 and release preparation

- [ ] Add narrowly configured Gateway recovery operations with synthetic restore tests.
- [ ] Full private V2 backup/checksum/ledger and isolated restore smoke; fix/retry failures.
- [ ] V1 unique-data mapping and non-destructive logical retirement after recovery PASS.
- [ ] Final regression/package/privacy/Git-object audits, checkpoint/docs/release preparation.
- [ ] Stop only for final owner-confirmed V1 physical deletion or an allowed human blocker.
