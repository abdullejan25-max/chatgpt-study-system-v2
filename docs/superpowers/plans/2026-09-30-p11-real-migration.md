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
- [ ] Reuse private inventory; perform bounded final wrong-answer relation check.
- [ ] Verify Codex snapshot against the correct registry digest fields.
- [ ] Select the existing private AppData runtime convention for a new History target.

## Task 2: Restricted legacy source domain and retrieval

Files: new `adapters/legacy_sources.py`, Gateway/MCP read integration, synthetic tests.

- [ ] Test exact-byte preservation, distinct source types, deterministic IDs, transaction rollback, conflict refusal and retry.
- [ ] Implement domain validation and bounded source listing, search, metadata/range fetch.
- [ ] Store original source event times only when proven; acquisition/import times are separate.
- [ ] Persist `data_origin=legacy_import`, operator as importer, author/role unknown.
- [ ] Review implementation and run relevant existing transport/History regressions.

## Task 3: Snapshot, restore and internal apply

Files: new `migration/real_apply.py`, synthetic apply/snapshot tests; extend local CLI only if needed.

- [ ] Validate explicit source set, target and private journal isolation before writes.
- [ ] Reuse bounded verified DB/WAL snapshot helper; persist a self-contained target backup and verify SQLite integrity.
- [ ] Restore into an isolated target, reopen through Gateway/domain read methods and compare records.
- [ ] Invoke domain batch transactions; journal only after successful read-back. A crash between stores is recovered through deterministic IDs.
- [ ] Verify same source rerun creates no duplicates and preserves import timestamps and IDs.

## Task 4: Real migration and gates

- [ ] Strict public-history privacy audit before milestone push.
- [ ] Configure new private History target without replacing existing stores.
- [ ] Execute verified source batches; preserve legacy unknown relations as explicit unresolved archive evidence.
- [ ] Reconcile counts, all source bytes/hashes and provenance; verify restart persistence and MCP retrieval.
- [ ] Record V2 cutover and V1 retirement without deletion; publish deletion candidate categories.
- [ ] Review every P11 gate as PASS/BLOCKED/N/A with actual evidence.

## Task 5: Release only after gate PASS

- [ ] Update package/version, README, roadmap, current-state and release notes.
- [ ] Full verification and privacy audit; normal merge/push, annotated v0.2.0 tag and GitHub Release.
- [ ] Final report with Git/release state, migration counts, known limitations and deferred external expansion.
