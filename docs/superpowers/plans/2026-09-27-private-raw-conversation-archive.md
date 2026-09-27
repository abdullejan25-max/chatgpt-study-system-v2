# Private Raw Conversation Archive Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Preserve official ChatGPT and Gemini ZIP exports losslessly in a private per-user store and verify their bytes and ZIP CRCs before any parser or Gateway is involved.

**Architecture:** Add `migration/raw_archive.py` with a small `PrivateRawArchiveStore`. It writes source-scoped, content-addressed ZIPs and redacted sidecar manifests below the configured user state root; it never extracts entries or touches V2 business stores. Synthetic tests exercise limits, integrity, atomic publication, idempotency, and recovery after an interrupted manifest write.

**Tech Stack:** Python 3.11+, `pathlib`, `hashlib`, `zipfile`, `json`, existing migration path validation, pytest.

## Global Constraints

- Preserve exact input ZIP bytes; do not parse platform content or extract entries.
- Store only below the configured per-user state root and outside the repository.
- Support only `chatgpt` and `gemini` source systems.
- Enforce 512 MiB compressed bytes, 50,000 ZIP members, 2 GiB declared uncompressed bytes, and a 200:1 maximum per-member compression ratio.
- Reject encrypted, corrupt, changing, or unsafe source files with fixed path-free error codes.
- Never log paths, archive names, member names, hashes, account data, or conversation content.
- A successful archive ingest does not change P11 Gate status or write V2 business data.

---

### Task 1: Implement a verified happy-path archive ingest

**Files:**
- Create: `tests/test_private_raw_archive.py`
- Create: `src/chatgpt_study_system/migration/raw_archive.py`
- Modify: `docs/superpowers/specs/2026-09-27-private-raw-conversation-archive-design.md`

**Interfaces:**
- `PrivateRawArchiveStore(root: Path | None = None, limits: RawArchiveLimits | None = None)`
- `store.ingest_zip(source_path: Path, *, source_system: str) -> ArchiveIngestResult`
- `ArchiveIngestResult` returns `source_system`, `sha256`, `byte_count`, `member_count`, `uncompressed_byte_count`, `duplicate`, and a stored path hidden from `repr`.
- `RawArchiveError.code` is one fixed public code and its message contains no path or filename.

- [ ] **Step 1: Write the exact-byte preservation test**

Build a synthetic ZIP in a private test directory with one member named `private-sentinel.txt` and bytes `synthetic conversation payload`. Ingest it as `chatgpt`; assert the stored ZIP has identical bytes and SHA-256, the result reports one member, and the manifest contains no source path, original basename, member name, or sentinel payload.

- [ ] **Step 2: Run the test and verify the expected missing-interface failure**

Run: `uv run --offline --extra dev pytest -q tests/test_private_raw_archive.py::test_ingest_preserves_exact_zip_bytes_and_redacts_manifest -p no:cacheprovider`

Expected: FAIL because `chatgpt_study_system.migration.raw_archive` does not exist.

- [ ] **Step 3: Implement the minimal safe store and happy path**

Define immutable `RawArchiveLimits`, `ArchiveIngestResult`, and `RawArchiveError`. Add `default_raw_archive_root()` under the existing `LOCALAPPDATA`/`XDG_STATE_HOME` application tree; reject missing or non-absolute configured roots. Implement private staging, streaming SHA-256, ZIP CRC verification, redacted manifest creation, and atomic publication. Make the stored path `repr=False`.

- [ ] **Step 4: Run the focused test and verify the happy path passes**

Run: `uv run --offline --extra dev pytest -q tests/test_private_raw_archive.py::test_ingest_preserves_exact_zip_bytes_and_redacts_manifest -p no:cacheprovider`

Expected: PASS with byte-for-byte archive equality, matching SHA-256, and a manifest that excludes source paths, file/member names, and synthetic content.

- [ ] **Step 5: Commit the green happy-path implementation**

Run:

```powershell
git add tests/test_private_raw_archive.py src/chatgpt_study_system/migration/raw_archive.py docs/superpowers/specs/2026-09-27-private-raw-conversation-archive-design.md
git commit -m "feat: add private raw archive ingest"
```

### Task 2: Stream and verify a new private raw ZIP

**Files:**
- Modify: `tests/test_private_raw_archive.py`
- Modify: `src/chatgpt_study_system/migration/raw_archive.py`

**Interfaces:**
- New archives are stored as `<root>/<source_system>/<sha256>.zip` with a sibling `<sha256>.manifest.json`.
- Manifest fields are limited to source system, SHA-256, byte count, member count, declared uncompressed byte count, and UTC ingest time.
- `ingest_zip` streams in bounded chunks and creates its staging file exclusively below the private root.

- [ ] **Step 1: Add path, size, and source allowlist tests**

Assert `obsidian` is rejected with `unsupported_source`; a non-ZIP file and a `.zip` with corrupt central directory return `invalid_zip`; a source exceeding `max_archive_bytes` returns `archive_too_large`; and a symlink/reparse source returns `unsafe_path` without creating a target file.

- [ ] **Step 2: Run the new tests and confirm each fails for missing behavior**

Run: `uv run --offline --extra dev pytest -q tests/test_private_raw_archive.py -p no:cacheprovider`

Expected: failures are limited to absent ingest/path/ZIP validation behavior.

- [ ] **Step 3: Implement private root and safe source validation**

Use existing `validate_private_journal_path` and Windows user-state containment checks. Create source-specific storage directories with owner-only POSIX permissions; on Windows require the configured per-user state root. Reject repository overlap, reparse points, non-regular files, relative paths, and sources inside the destination root. Return only fixed `RawArchiveError` codes.

- [ ] **Step 4: Implement bounded stream-copy and source-stability checks**

Open the source once, capture `fstat` before copying, stream at most `max_archive_bytes + 1` into an exclusive `.partial` file while hashing, then compare size and high-resolution timestamps from the same source handle. Flush the destination and verify copied size and digest before ZIP checks. Remove only this call's partial file on failure.

- [ ] **Step 5: Implement ZIP metadata limits and CRC verification**

Open the staged ZIP without extraction. Reject encrypted members; enforce member count, declared total uncompressed bytes, and per-member compression ratio. Run `ZipFile.testzip()` only after these checks. Never include entry names in an exception or return value.

- [ ] **Step 6: Atomically publish the archive and redacted manifest**

Promote the verified partial file to `<source_system>/<sha256>.zip` without replacing an existing target. Write manifest bytes to an exclusive sibling partial, flush, and atomically rename to `<sha256>.manifest.json`. Ensure JSON contains only the specified fields.

- [ ] **Step 7: Run focused tests and commit the verified new-archive path**

Run: `uv run --offline --extra dev pytest -q tests/test_private_raw_archive.py -p no:cacheprovider`

Expected: all tests for exact bytes, path safety, source allowlist, size bound, ZIP structure, CRC, and redacted manifest pass.

```powershell
git add tests/test_private_raw_archive.py src/chatgpt_study_system/migration/raw_archive.py
git commit -m "feat: preserve verified private conversation archives"
```

### Task 3: Make retries idempotent and crash-recoverable

**Files:**
- Modify: `tests/test_private_raw_archive.py`
- Modify: `src/chatgpt_study_system/migration/raw_archive.py`

- [ ] **Step 1: Add idempotency and interrupted-publication tests**

Ingest the same synthetic ZIP twice and assert the second result is `duplicate=True` without changing archive or manifest bytes. Simulate an existing valid content-addressed ZIP without its manifest; assert retry validates it and creates the missing manifest. Create an invalid pre-existing manifest and assert a fixed `manifest_invalid` error with no overwrite.

- [ ] **Step 2: Run the tests and verify the crash-recovery cases fail first**

Run: `uv run --offline --extra dev pytest -q tests/test_private_raw_archive.py -p no:cacheprovider`

Expected: failures identify duplicate handling and incomplete-publication recovery only.

- [ ] **Step 3: Implement duplicate verification and missing-manifest recovery**

When the digest target exists, verify its size, digest, ZIP limits, and CRC. If its manifest exists, validate exact schema and values before returning duplicate. If absent, write the validated manifest atomically. Never replace an existing ZIP or invalid manifest.

- [ ] **Step 4: Run focused tests, inspect Git privacy, and checkpoint**

Run: `uv run --offline --extra dev pytest -q tests/test_private_raw_archive.py -p no:cacheprovider`

Expected: all synthetic archive tests pass; no archive data exists under the repository except synthetic temporary fixtures that pytest removes.

Run `git diff --check`, inspect the complete diff, confirm the default root is outside the repository, and confirm `git status --short` contains only intended source, test, spec, plan, and status-document changes.

- [ ] **Step 5: Update phase docs and commit the recovery behavior**

Document this as private raw archive preparation only, retain P11 `BLOCKED` and P12 `PREPARATION`, update the ignored resume checkpoint, then run:

```powershell
git add tests/test_private_raw_archive.py src/chatgpt_study_system/migration/raw_archive.py docs/phase-11-legacy-migration.md docs/current-state.md docs/autonomous-run-status.md
git commit -m "feat: recover private archive ingest after interruption"
```

## Review limits

- Do not run a real archive through the new component until the user completes the official export verification and downloads it.
- Do not change P11 or P12 Gate states based on synthetic tests.
- Do not add parser, History schema, or Gateway write paths in this plan.
