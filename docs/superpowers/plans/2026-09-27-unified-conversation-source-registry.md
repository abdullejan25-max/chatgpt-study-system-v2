# Unified Conversation Source Registry Implementation Plan

> **For agentic workers:** Use the existing Phase 11 checkout and execute this plan task-by-task with checkpoints. The user's 72-hour master prompt authorizes autonomous inline execution and requires a recoverable status record.

**Goal:** Record the discovered AI/Agent conversation sources and their export/import coverage in a private local registry without exposing chat content, account identifiers, or local paths in tracked files.

**Architecture:** Add a typed registry beside the existing Phase 11 migration code, with transactional local persistence outside the repository and aggregate-only public summaries. The registry records evidence and status; it does not read credentials, download from unofficial endpoints, configure History, or write V2 business data.

**Tech Stack:** Python 3.11+, standard-library JSON/SQLite/path handling, pytest, existing migration path-safety helpers.

## Global Constraints

- The master prompt's source inventory scope is limited to installed app data/config/history locations, user project directories, known Agent data directories, authorized Legacy roots, and official export/UI flows.
- Do not recursively scan the system drive, browser password stores, cookie databases, credential vaults, auth token storage, or unrelated private directories.
- Preserve original exports losslessly; private raw archives stay outside Git and retain verifiable hashes.
- Unknown role, author, time, conversation, message boundary, branch, or attachment relation remains unknown; do not infer it.
- Keep `Agent thinks; Gateway executes`; use formal Gateway/domain contracts for any future persisted V2 change.
- Do not configure private History or write to V2 stores without the required explicit local configuration and capabilities.
- Do not publish a release, modify `v0.1.0`, delete Legacy/V1 data, or push this branch.
- Use synthetic-only automated fixtures; never place real chat content, account identifiers, or private exports in Git.

---

## File Structure

- `src/chatgpt_study_system/migration/conversation_registry.py`: source metadata record validation, safe aggregate summary, private registry path, transactional load/upsert.
- `tests/test_conversation_source_registry.py`: synthetic registry validation, persistence, aggregate redaction, and unsafe-path coverage.
- `docs/phase-11-legacy-migration.md`: add the P11.3A inventory/export/import gate and its observed status.
- `docs/current-state.md`: summarize the new P11.3A scope and current blockers.
- `docs/autonomous-run-status.md`: public-safe continuation checkpoint, updated at each milestone.
- Private local state under the configured per-user application state directory: source registry and raw exports; never tracked.

## Interfaces

```python
@dataclass(frozen=True)
class ConversationSourceRecord:
    source_id: str
    source_system: str
    source_type: str
    acquisition_method: str
    discovered: bool
    accessible: bool
    export_status: str
    import_status: str
    raw_format: str | None
    stable_identity: str | None
    conversation_count: int | None
    message_count: int | None
    earliest_known_time: str | None
    latest_known_time: str | None
    source_hash: str | None
    manifest_hash: str | None
    imported_count: int
    deduplicated_count: int
    unresolved_count: int
    coverage_notes: tuple[str, ...]
    private_locator: str | None
```

- `ConversationSourceRegistry(path).upsert(record)` atomically replaces one record by its opaque `source_id` and rejects malformed metadata or a path overlapping the repository.
- `ConversationSourceRegistry(path).list_sources()` returns validated typed records only to local code.
- `ConversationSourceRegistry(path).public_summary()` returns aggregate counts and fixed status codes only; it never returns source IDs, locators, hashes, account labels, titles, or conversation content.
- `default_conversation_registry_path()` resolves only to the configured per-user application state root and fails closed if no such root exists.

### Task 1: Define and validate registry records

**Files:**
- Create: `src/chatgpt_study_system/migration/conversation_registry.py`
- Create: `tests/test_conversation_source_registry.py`

- [x] Write synthetic tests for valid source records, invalid status vocabulary, invalid counts, invalid UTC timestamps, invalid hashes, and disallowed coverage-note text.
- [x] Run `uv run --extra dev pytest -q tests/test_conversation_source_registry.py -p no:cacheprovider`; confirm the tests fail because the registry API is absent.
- [x] Implement `ConversationSourceRecord`, fixed status vocabularies, field validation, and `public_summary()` with only aggregate values.
- [x] Rerun the focused file and confirm invalid or path-shaped values fail without printing their contents.

### Task 2: Persist the registry privately and atomically

**Files:**
- Modify: `src/chatgpt_study_system/migration/conversation_registry.py`
- Modify: `tests/test_conversation_source_registry.py`

- [x] Add a `tmp_path` test that upserts two synthetic sources, reopens the registry, and verifies exact metadata round-trip.
- [x] Add tests that an upsert replaces only the same opaque `source_id`, and that public summaries contain counts but not locators, IDs, hashes, or labels.
- [x] Add tests that the default registry path uses only `LOCALAPPDATA` or `XDG_STATE_HOME`, and that absent configuration fails closed.
- [x] Run the focused file and confirm the persistence tests fail before implementation.
- [x] Implement bounded JSON payloads in transactional SQLite persistence and private path validation using the existing migration safety helper.
- [x] Rerun the focused file and verify reopen, replacement, unsafe-path rejection, and summary redaction.

### Task 3: Record the real source inventory and P11.3A gate

**Files:**
- Modify: `docs/phase-11-legacy-migration.md`
- Modify: `docs/current-state.md`
- Create or update: `docs/autonomous-run-status.md`
- Private only: the per-user conversation source registry

- [ ] Add source records only from bounded, named app-data roots or official export evidence; do not scan broadly or read browser credentials.
- [ ] Record ChatGPT/Gemini request state, local Agent source discovery, raw-archive status, counts when reliable, and fixed coverage gaps.
- [ ] Update public docs with aggregate counts, status, blockers, and the next safe action; omit absolute paths, account identifiers, titles, filenames, source hashes, and chat text.
- [ ] Run `git diff --check`, inspect the complete documentation diff, confirm the registry and raw archives are ignored, and verify no private names or absolute paths entered tracked files.

## Deferred Gate Work

- Platform-specific normalization starts only after an official raw archive is available and its exact schema has been inspected locally.
- History import, attachments, deterministic chunking, deduplication, retrieval E2E, snapshot/restore, and real apply remain separate work. They require exact source fields, a configured History target, and the appropriate capability; this registry plan does not claim those gates PASS.
- Any format that cannot preserve source-proven roles, ordering, times, identities, and message boundaries remains raw-archive-only until a truthful representation is proven.

## Review Coverage

- Covers source discovery/status fields and a private, resumable registry without changing V2 History or migration business data.
- Does not claim complete source coverage, normalized import, P11 PASS, or any P12 release gate.
