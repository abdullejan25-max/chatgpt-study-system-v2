# P11 Real Migration Implementation Plan

> **For agentic workers:** Use `subagent-driven-development` or `executing-plans` to execute and review this plan.

**Goal:** Complete evidence-backed V1 to V2 migration, read-back, retry, retrieval, cutover and release gates from the existing P11 branch.

**Architecture:** Reuse existing inventory, snapshots, registry and domain repositories. Add a restricted legacy source/document representation beside raw History messages, preserving exact UTF-8 bytes and unknown identities. A local internal apply service validates explicit source sets, snapshots the target, proves isolated restore, invokes domain transactions and checkpoints a private journal. Public MCP exposes bounded read operations only.

**Tech Stack:** Python, SQLite, existing Gateway and MCP SDK, PowerShell 7.

## Global Constraints

- Agent thinks; Gateway executes. No arbitrary SQL import or Agent-facing migration writes.
- Preserve V1, original sources, backups, published history and v0.1.0.
- Study stays authoritative in place. Never infer wrong-answer evidence relationships.
- Private data, identifiers, paths, hashes, config and journals stay outside tracked Git files.
- v0.2.0 covers V1 migration and V2 cutover; external platform expansion is reported independently.
- Unknown author, role, message boundary and event times remain unknown.
- Current branch continuation and autonomous routine decisions are explicitly authorized by the user.

## Task 1: Recover and reconcile source evidence

- [x] Confirm branch, HEAD, clean status, remotes and full synthetic baseline.
- [x] Reuse private inventory; perform bounded final wrong-answer relation check.
- [x] Verify Codex snapshot against the correct registry digest fields.
- [x] Select the existing private AppData runtime convention for a new History target.

## Task 2: Restricted legacy source domain and retrieval

Files: new `adapters/legacy_sources.py`, Gateway/MCP read integration, synthetic tests.

- [x] Test exact-byte preservation, distinct source types, deterministic IDs, transaction rollback, conflict refusal and retry.
- [x] Implement domain validation and bounded source listing, search, metadata/range fetch.
- [x] Store original source event times only when proven; acquisition/import times are separate.
- [x] Persist `data_origin=legacy_import`, operator as importer, author/role unknown.
- [x] Review implementation and run relevant existing transport/History regressions.

## Task 3: Snapshot, restore and internal apply

Files: new `migration/real_apply.py`, synthetic apply/snapshot tests; extend local CLI only if needed.

- [x] Validate explicit source set, target and private journal isolation before writes.
- [x] Reuse bounded verified DB/WAL snapshot helper; persist a self-contained target backup and verify SQLite integrity.
- [x] Restore into an isolated target, reopen through Gateway/domain read methods and compare records.
- [x] Invoke domain batch transactions; journal only after successful read-back. A crash between stores is recovered through deterministic IDs.
- [x] Verify same source rerun creates no duplicates and preserves import timestamps and IDs.

## Task 4: Real migration and gates

- [x] Strict public-history privacy audit before milestone push.
- [x] Configure new private History target without replacing existing stores.
- [x] Execute verified source batches; preserve legacy unknown relations as explicit unresolved archive evidence.
- [x] Reconcile counts, all source bytes/hashes and provenance; verify restart persistence and MCP retrieval.
- [x] Record V2 cutover and V1 retirement without deletion; publish deletion candidate categories.
- [x] Review every P11 gate as PASS/BLOCKED/N/A with actual evidence.

## Task 5: Release only after gate PASS

- [x] Update package/version, README, roadmap, current-state and release notes.
- [x] Full verification and privacy audit before integration.
- Publication sequence: verify merged main, normal push, annotated v0.2.0 tag and GitHub Release.
- Final handoff verifies Git/release state and reports migration counts, known limitations and deferred external expansion.
