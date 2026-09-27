# Codex Occurrence Adapter Implementation Plan

> **For agentic workers:** Use inline execution. Keep every step test-first and synthetic-only.

**Goal:** Convert one already-decoded Codex rollout JSONL line into a private `ImportedHistoryOccurrence` value without assigning conversation identity, semantic order, or attachment completeness.

**Architecture:** Add a pure line parser that accepts bounded JSON bytes and explicit verified-snapshot provenance, recognizes only documented envelope and content shapes, and returns the existing DTO. Unknown record/content shapes remain opaque references to the source line. The adapter is not connected to snapshot traversal, source registry, Gateway, or database.

**Tech Stack:** Python standard library JSON parser, existing DTO, pytest; no new dependencies.

## Global Constraints

- Synthetic fixtures only; do not invoke the adapter on the private snapshot.
- Require caller-supplied verified snapshot digest, private member locator, and non-negative record ordinal.
- Preserve source timestamps verbatim as strings; do not parse, sort, or normalize.
- Keep conversation reference, conversation/message order, title, model, and branches unknown unless this exact parser contract gains reviewed evidence.
- Do not extract image/audio bytes, create Assets, flatten events/tools into messages, or map unknown roles.
- Fixed path-free errors; no logging or serialization of source values.
- No Gateway, History SQLite, registry, MCP, business-store write, push, or release.

---

### Task 1: Bounded synthetic line parser

**Files:**
- Create: `src/chatgpt_study_system/migration/codex_occurrence_adapter.py`
- Test: `tests/test_codex_occurrence_adapter.py`
- Modify: `docs/superpowers/specs/2026-09-27-lossless-history-envelope-design.md`

**Interface:**

```python
parse_codex_occurrence_line(
    raw_line: bytes,
    *,
    snapshot_sha256: str,
    source_member_ref: str,
    record_ordinal: int,
) -> ImportedHistoryOccurrence
```

- Response message records may map an explicit `payload.id` to `source_item_id`, preserve an explicit open-string role, and map typed text blocks.
- Inline images, audio, tool/event records, and unknown block shapes become source references such as `record:4/content:1`; raw values remain available only from the caller-owned snapshot.
- Every other record value is left unmapped; `conversation_ref`, title, model, source-declared ordering, and branch refs stay unknown.
- Malformed JSON, oversized lines, unsupported top-level values, and invalid provenance fail with a fixed `Codex occurrence parse failed (<code>)` error.

- [x] **Step 1: Add failing synthetic tests** for a developer message with text/image blocks, an event record, an unknown record/content block, raw timestamp preservation, and fixed redacted errors for malformed/oversized inputs.
- [x] **Step 2: Run the focused tests and confirm the expected failure.** The initial run failed at collection because the module did not yet exist.
- [x] **Step 3: Implement the bounded pure parser** with a 16 MiB line cap and only the mappings listed above.
- [x] **Step 4: Run adapter, DTO, inspector, and History contract tests.** Observed **42 passed** in 5.63s.
- [x] **Step 5: Run `git diff --check` and commit the synthetic-only adapter, tests, spec, and plan** (`bcb76d6`). Follow-up to preserve unmapped `ordinal` / `phase` values is `8644406`.
