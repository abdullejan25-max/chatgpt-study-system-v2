# Phase 11 Legacy Migration Implementation Plan

> **For agentic workers:** Use this plan task-by-task with checkpoints. Steps use checkbox syntax for tracking.

**Goal:** Produce a privacy-safe, repeatable legacy inventory and migration manifest, and migrate only records that can be represented losslessly by configured V2 domain contracts.

**Architecture:** Keep Study as an explicitly configured external authority and keep the migration journal local and private. Build a deterministic planner that fingerprints records without storing their text, absolute paths, or private filenames; any eventual domain write must call an existing Gateway contract or a narrowly scoped internal adapter. The current History target is not configured, so real History writes remain gated until the operator explicitly configures that private target.

**Tech Stack:** Python 3.11+, SQLite, pytest, existing Gateway adapters, PowerShell for local read-only inventory.

## Global Constraints

- The legacy source remains read-only; do not delete, replace, move, or normalize old files.
- Do not add an LLM or VLM to the runtime and do not generate summaries or facts.
- Do not write real private data, absolute paths, database files, or migration journals to Git.
- Do not use direct SQL writes against formal V2 databases.
- StudyVault is reused in place; do not copy its Markdown or PDFs or its QMD index.
- Wrong-answer source/analysis writes must follow `study-workflow://wrong-answer` and use Gateway tools.
- Do not modify tag `v0.1.0`, push, force-push, or create a `v0.2.0` release.
- Use synthetic-only automated fixtures; real migration requires dry-run, tests, snapshot, explicit targets, and privacy checks.

---

### Task 1: Add a privacy-safe migration manifest model

**Files:**
- Create: `src/chatgpt_study_system/migration/__init__.py`
- Create: `src/chatgpt_study_system/migration/manifest.py`
- Create: `tests/test_legacy_migration_manifest.py`

**Interfaces:**
- `MigrationItem` contains `legacy_source_type`, opaque `legacy_identity`, `source_fingerprint`, `target_type`, optional `target_logical_id`, `action`, `status`, optional `imported_at`, optional `source_event_time`, `dedup_decision`, `validation_state`, and safe reason/error codes.
- `stable_migration_key(system, legacy_id, content_hash)` returns a deterministic opaque key; when the legacy identifier is absent, the planner uses a content fingerprint plus a source-scope identity.
- `MigrationJournal(path)` stores run metadata, items, and checkpoints in a private SQLite file, rejects path-shaped public fields, and commits each journal batch atomically.
- `summarize(items)` returns only category counts and fixed reason codes; it never returns item content, source paths, or filenames.

- [ ] Add synthetic tests for deterministic keys, duplicate-key/content conflict, required manifest fields, path redaction, category summaries, and an interrupted journal batch rollback.
- [ ] Run `uv run --extra dev pytest -q tests/test_legacy_migration_manifest.py -p no:cacheprovider`; confirm the intended missing-module/API failures.
- [ ] Implement the model and journal with parameterized SQL, bounded strings, WAL checkpointing, and transactions scoped to one batch.
- [ ] Rerun the focused tests and verify the journal can reopen and resume without duplicating manifest rows.

### Task 2: Add deterministic dry-run classification

**Files:**
- Create: `src/chatgpt_study_system/migration/planner.py`
- Create: `tests/test_legacy_migration_planner.py`
- Modify: `src/chatgpt_study_system/migration/manifest.py`

**Interfaces:**
- `SourceRecord` supplies a source class, stable ID when available, content fingerprint, optional event time, target type, and only privacy-safe validation facts.
- `plan_records(records, existing_targets, target_health)` yields `reuse`, `import`, `archive`, or `skip` actions with explicit dedup and validation states.
- Existing target fingerprints win as deduplications; conflicting reuse of one legacy ID with different content is unresolved and never overwritten.
- An unconfigured History backend blocks History imports and reports the fixed reason `history_target_not_configured` without writing to the target.

- [ ] Add synthetic tests for dry-run target immutability, same-content/different-path dedupe, duplicate legacy ID conflicts, unknown timestamps, malformed/unsupported records, current-target dedupe, and Study reuse without copy actions.
- [ ] Run the focused planner test file and confirm expected failures.
- [ ] Implement only deterministic classification; do not add a generic database importer or a real-data write path.
- [ ] Rerun focused planner tests and check that summaries remain path- and content-free.

### Task 3: Add a source-specific, read-only inventory command

**Files:**
- Create: `src/chatgpt_study_system/migration/inventory.py`
- Create: `src/chatgpt_study_system/migration/cli.py`
- Create: `tests/test_legacy_migration_inventory.py`
- Modify: `pyproject.toml`

**Interfaces:**
- `study-migrate dry-run` accepts only explicit Study, Personal History, and legacy project roots, validates that roots exist and contain no reparse-point escapes, and writes the private journal only to an explicit local path.
- Scanners report counts, byte sizes, file-class metadata, stable ID/hash fingerprints, and parseability; they never print raw content or absolute paths.
- The command defaults to dry-run. It refuses any target write because this phase’s discovered History target is not configured and the existing message-level importer cannot represent whole legacy conversation archives losslessly.
- The command reports archive-only/unresolved files as such; it does not infer chat roles, missing source identities, or image-to-note relations.

- [ ] Add synthetic temporary-directory tests for source containment, symlink/reparse refusal, counts and hashes, hidden path handling, and malformed Markdown/archive classification.
- [ ] Run the focused inventory tests and confirm expected failures.
- [ ] Implement the explicit-root scanners and a CLI summary with no path-bearing errors.
- [ ] Run the CLI only on synthetic fixtures first, then run one real dry-run against the already authorized legacy roots and the read-only V2 target.
- [ ] Confirm source file hashes/metadata remain unchanged and the journal is outside tracked files.

### Task 4: Record the audit, gates, and technical boundary

**Files:**
- Create: `docs/phase-11-legacy-migration.md`
- Modify: `docs/current-state.md`
- Modify: `docs/architecture.md` only if the private migration boundary changes materially.

- [ ] Record the matrix, aggregate counts, design, test results, dry-run result, target configuration gate, and known limitations without paths, filenames, hashes, or personal text.
- [ ] Run the full synthetic test suite requested by the Phase 11 task, `git diff --check`, `git status`, `git diff`, and `git ls-files` privacy scans.
- [ ] Stop real writes while History is unconfigured or source semantics remain unresolved; document the precise enablement and data-resolution prerequisites.
- [ ] Leave the branch unpushed, preserve `v0.1.0`, and do not start release preparation.

## Review coverage

- Items 1–8 of the Phase 11 specification are covered by the baseline sync, bounded inventory, classification, and private manifest.
- Dry-run, resumability, batch journal transactions, and privacy checks are covered by Tasks 1–3.
- A business-data apply mechanism, snapshot restore, History readback, and real Wrong Answer migration are gated because the configured History store is absent and legacy image/note semantics cannot be resolved safely from the source metadata.
- The dry-run can finish with a documented `BLOCKED` result; it must not fabricate an import-ready state or enable private configuration on the user's behalf.
