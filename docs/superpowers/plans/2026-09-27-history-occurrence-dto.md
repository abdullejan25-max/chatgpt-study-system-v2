# Imported History Occurrence DTO Implementation Plan

> **For agentic workers:** Use the inline execution flow for this plan. Every step uses checkbox syntax and must be completed with synthetic tests.

**Goal:** Add an immutable, versioned, privacy-conscious domain DTO for one source-record occurrence without connecting it to the Gateway or any database.

**Architecture:** Add two frozen dataclasses in a dedicated migration module: one typed content block and one imported occurrence. Keep source IDs, content, and private locators out of `repr`; distinguish source record order from source-declared conversation/message order; preserve unknown source fields through references to the immutable snapshot rather than flattening them into text.

**Tech Stack:** Python dataclasses and existing pytest suite; no new runtime dependencies.

## Global Constraints

- Use synthetic fixtures only; do not read private conversation body content.
- Do not integrate with `HistoryImportItem`, Gateway, SQLite, MCP, Assets, or Documents in this change.
- Do not infer conversation IDs, roles, timestamps, model names, or ordering.
- Preserve source order locator separately from optional source-declared ordering.
- Keep private source paths, IDs, text, branch refs, and metadata out of dataclass representations.
- Keep P11 `BLOCKED`; make no business-store writes, pushes, tags, or releases.

---

### Task 1: Immutable occurrence types

**Files:**
- Create: `src/chatgpt_study_system/migration/history_occurrence.py`
- Test: `tests/test_history_occurrence.py`
- Modify: `docs/superpowers/specs/2026-09-27-lossless-history-envelope-design.md`

**Interfaces:**
- `HistoryOccurrenceBlock(kind: str, text: str | None = None, source_ref: str | None = None)`
- `ImportedHistoryOccurrence(schema_version: int, source_system: str, snapshot_sha256: str, source_member_ref: str, record_ordinal: int, kind: str, role: str | None, content_blocks: tuple[HistoryOccurrenceBlock, ...], source_item_id: str | None = None, conversation_ref: str | None = None, conversation_title: str | None = None, author: str | None = None, model_name: str | None = None, source_created_at: str | None = None, source_updated_at: str | None = None, imported_at: str | None = None, import_batch_id: str | None = None, conversation_order: int | None = None, message_order: int | None = None, branch_refs: tuple[str, ...] = (), unknown_field_refs: tuple[str, ...] = (), conflict_codes: tuple[str, ...] = ())`
- Values are frozen; source order uses `record_ordinal`, and source-declared order is separate and optional.
- All validation errors use fixed text and never echo caller data.

- [x] **Step 1: Write the failing synthetic tests**
  - Assert fields preserve open role/kind strings, typed block boundaries, optional source metadata, branch/unknown refs, conflicts, and distinct locator/order values.
  - Assert frozen instances reject mutation.
  - Assert `repr()` omits source IDs, snapshot/member references, text, title, author, model, branch refs, and unknown-field refs.
  - Assert invalid digest/version/order/type values raise fixed messages without echoing a supplied path or private sentinel.

- [x] **Step 2: Run the focused tests and confirm the expected failure**

Run: `uv run --offline --extra dev pytest -q tests/test_history_occurrence.py -p no:cacheprovider`

Expected: FAIL because the new module/types do not exist yet.

- [x] **Step 3: Implement the minimum immutable DTOs and fixed validation**
  - Use `@dataclass(frozen=True)`.
  - Keep sensitive fields `repr=False` and prevent nested block text from appearing in the parent representation.
  - Validate SHA-256 with the lowercase 64-hex form, non-negative exact-integer ordinals, schema version `1`, and exact tuple inputs.
  - Bound `source_system`, `kind`, and `role` to non-empty strings of at most 80 characters; bound private references/identifiers and title/author/model strings to 4,096 characters; bound text blocks to 1 MiB; reject control characters in identifiers, labels, and references while allowing them in content.
  - Keep timestamps as source strings without parsing or normalization. Require all order values to be non-negative exact integers when present.
  - Do not add parsing, serialization, persistence, or importer functions.

- [x] **Step 4: Run focused tests and adjacent History tests**

Run: `uv run --offline --extra dev pytest -q tests/test_history_occurrence.py tests/test_codex_jsonl_inspector.py tests/test_history.py -p no:cacheprovider`

Expected: PASS with no Gateway/database integration.

Observed: **36 passed** in 5.74s.

- [x] **Step 5: Commit the synthetic-only DTO**
  - State that the DTO is an in-memory proposal and is not yet accepted by the current History write contract.
  - Run `git diff --check`; stage only the named files and plan.
  - Commit as `feat: add lossless history occurrence DTO` (`8442e18`).
