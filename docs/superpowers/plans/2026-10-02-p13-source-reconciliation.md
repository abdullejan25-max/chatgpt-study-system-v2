# P13 remaining source reconciliation implementation plan

Use executing-plans and TDD in the existing worktree. Owner authorization replaces optional
design-review pauses. Independent code review remains an engineering check.

## Constraints

- Real source bytes, locators, ledgers, receipts, Host traces and backups stay outside Git.
- Every production V2 read/write uses formal study_system Gateway/MCP operations.
- Preserve existing source-only evidence and already-PASS gates; no early normalization/deletion.

## Task 1 — Immutable source evidence backend

Create adapters/history_sources.py and tests/test_history_sources.py.

- [x] RED: exact bytes/digests, missing timestamp, renamed locator, runtime record kind,
  immutable conflict, malformed binary preservation, interrupted/rerun dedup and provenance.
- [x] GREEN: additive schema in configured History DB; BLOB dedup by byte digest;
  source-file deterministic identity; bounded reads/counts; existing legacy-reference linking.
- [x] Verify on isolated synthetic targets, never production files.

## Task 2 — Explicit private inbox and formal Gateway/MCP

Modify config.py, runtime.py, Gateway and MCP transport; add synthetic integration tests.

- [x] RED: unconfigured inbox/capability rejection, path aliases/overlap, digest mismatch,
  bounded batch/read/search, readback identity, reported provenance, backward config compatibility.
- [x] GREEN: relative manifest ingestion and existing-evidence registration; no absolute input
  paths returned. Preserve original backend contracts and non-History operations.
- [x] Fresh actual Codex Host loads new tools from this worktree's configuration;
  persist real native tool-call evidence rather than using a standalone direct client.

## Task 3 — Private input snapshots and reconciliation

- [x] Freeze existing ledger versions; recover append-only prefixes with exact hash proof.
- [x] Complete V1 locator/schema/source mapping audit from P11 evidence and known configs.
- [x] Import remaining explicit source inputs through formal Gateway, reuse existing records.
- [x] Repeat ingestion; record every disposition/ref/provenance/receipt digest durably.
- [x] Source search/readback/no-result and complete input-to-destination reconciliation.

## Task 4 — Checkpoint and next phase

- [x] Independent review; targeted checks and privacy-safe source checkpoint.
- [ ] Once acquired sources all have explained destinations, design deterministic canonical
  adapters/schema, then normalization, readback, full recovery and V1 logical retirement in order.
- [ ] Physical deletion remains one final owner-confirmed transaction.
