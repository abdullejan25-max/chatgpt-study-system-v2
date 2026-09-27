# Private Codex JSONL Snapshot Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Preserve bounded Codex JSONL source candidates byte-for-byte in private per-user storage before parsing or import.

**Architecture:** Add a Codex-only snapshot store beside the official ZIP archive store. It copies an explicit JSONL tree into a private staging directory, hashes each file and a canonical manifest, verifies the source did not change, then atomically publishes a content-addressed snapshot. No parser or Gateway/database dependency is added.

**Tech Stack:** Python 3.12, pathlib/os/stat, hashlib, JSON, pytest, existing private-path and conversation-source registry helpers.

## Global Constraints

- Accept only an explicit absolute source directory; do not scan outside it.
- Hard limits: 10,000 files, 512 MiB per file, 2 GiB total, 16 directory levels.
- Never follow reparse points or symlinks; reject hard-linked candidate files.
- Preserve exact file bytes and relative paths; do not parse JSONL.
- Store private data only under `LOCALAPPDATA` or `XDG_STATE_HOME`, outside the repository.
- Keep conversation/message counts unknown and P11 `BLOCKED` until separate evidence proves otherwise.

---

### Task 1: Prove the synthetic snapshot contract

**Files:**
- Create: `tests/test_private_codex_jsonl_snapshot.py`
- Create: `src/chatgpt_study_system/migration/codex_snapshot.py`

**Interface:**
- `PrivateCodexJSONLSnapshotStore(root: Path | None = None, limits: CodexSnapshotLimits | None = None)`
- `snapshot_jsonl_tree(source_root: Path) -> CodexSnapshotResult`
- Fixed path-free `CodexSnapshotError.code`; `CodexSnapshotResult.stored_path` is excluded from `repr`.

- [ ] Add a synthetic nested JSONL tree test asserting byte-for-byte copied content, per-file SHA-256, a deterministic snapshot hash, and a private manifest that excludes the absolute source path and a sentinel string in file contents.
- [ ] Run `uv run --offline --extra dev pytest -q tests/test_private_codex_jsonl_snapshot.py -p no:cacheprovider`; verify the import/API failure is the expected RED result.
- [ ] Implement the minimum successful private copy, manifest, integrity verification, and atomic directory publication.
- [ ] Rerun the focused test and require GREEN.

### Task 2: Enforce bounds and source stability

**Files:**
- Modify: `src/chatgpt_study_system/migration/codex_snapshot.py`
- Modify: `tests/test_private_codex_jsonl_snapshot.py`

- [ ] Add tests for file-count, per-file bytes, total bytes, directory depth, empty tree, unsafe root, reparse point, hard link, and non-regular entries; assert fixed errors do not include paths.
- [ ] Add a source-mutation test that changes a synthetic source while copying and requires `source_changed` with no published snapshot.
- [ ] Implement bounded no-follow enumeration, source file identity/stat checks before and after copy, staged-file rehashing, and a second full metadata scan before publish.
- [ ] Run the focused suite and require all synthetic bounds and source-stability tests to pass.

### Task 3: Make completed captures idempotent and recoverable

**Files:**
- Modify: `src/chatgpt_study_system/migration/codex_snapshot.py`
- Modify: `tests/test_private_codex_jsonl_snapshot.py`

- [ ] Add tests for duplicate capture, corrupt existing target rejection, promotion of a fully manifested staging directory, and fail-closed preservation of incomplete staging.
- [ ] Implement exact manifest validation and target-file hash validation before returning `duplicate=True`; never replace an existing snapshot.
- [ ] Run the focused suite and verify no partial or final snapshot remains in temporary tests after handled errors.

### Task 4: Record the live inventory and checkpoint

**Files:**
- Modify: `src/chatgpt_study_system/migration/conversation_registry.py`
- Modify: `tests/test_conversation_source_registry.py`
- Modify: `docs/phase-11-legacy-migration.md`
- Modify: `docs/current-state.md`
- Modify: `docs/autonomous-run-status.md`
- Modify: `var/p11-p12-resume/checkpoint.json` (ignored/private)

- [ ] Add `jsonl` to the registry's fixed raw-format vocabulary and a synthetic test for round-trip/public-summary behavior.
- [ ] Re-enumerate only the existing explicit Codex sessions root, compare the result with the previously reported 70-file inventory, and capture only if the source set remains stable.
- [ ] Run the private snapshot store against that root; verify the stored manifest and all file hashes without printing paths, file names, content, or hashes.
- [ ] Update the private registry to the verified source-item count and digests while keeping conversation/message counts null and import status blocked.
- [ ] Update public docs with aggregate candidate count/bytes, explain the old-count discrepancy without claiming conversations/messages, and keep P11 `BLOCKED`.
- [ ] Run `git diff --check`, focused snapshot/registry tests, review the tracked diff for privacy, commit, then update the ignored checkpoint with the new HEAD and exact verification results.
