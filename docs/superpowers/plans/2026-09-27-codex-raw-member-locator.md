# Codex Raw Member Locator Plan

**Goal:** Resolve the physical JSONL record position and exact raw byte span independently from source-provided order fields.

**Boundary:** Synthetic byte streams only. This work does not traverse or parse the private snapshot, access History/Gateway, or change business storage.

## Contract

- Physical `record_ordinal` is zero-based per member and includes blank, malformed, non-object, and oversized LF-delimited spans.
- LF and CRLF terminators are included in the byte span. A final unterminated non-empty span counts; an empty file and a trailing LF do not create phantom spans.
- Each span has zero-based `byte_start` and exclusive `byte_end`; byte length is measured even when the span exceeds the parse limit.
- Normal-sized spans may carry their exact raw bytes. Oversized spans are drained in bounded chunks and retain locator/count metadata without retaining their content.
- Source JSON `ordinal`, `conversation_order`, and `message_order` remain separate and semantically unknown.
- Locator resolution must later verify snapshot/member identity and line alignment before returning bytes.

## Tasks

### Task 1: Pin locator semantics

- [x] Specify physical line indexing, byte boundaries, line-ending treatment, malformed/oversized handling, and separation from source-declared order in the lossless History design.
- [x] Assert in a synthetic adapter fixture that passed physical `record_ordinal` remains distinct from the source JSON `ordinal` field.
- [x] Run the focused adapter suite. Observed **8 passed**.

### Task 2: Add synthetic stream span index

- [x] Write synthetic tests for LF, CRLF, final unterminated lines, blank/malformed records, trailing LF, and oversized-line draining with exact start/end offsets.
- [x] Run the tests and confirm the span-index API is missing.
- [x] Implement a bounded binary-stream iterator that reports exact spans and omits oversized content.
- [x] Verify every emitted normal span round-trips to the exact original bytes; verify oversized spans preserve exact length without retaining data.
- [x] Run focused synthetic tests and `git diff --check`. Observed **12 passed** across span and adapter tests.
- [x] Update status/checkpoint and commit; keep private snapshot/Gateway/business data untouched. Commit: `52984e9`.

### Task 3: Bind physical spans to synthetic occurrences

**Files:**
- Modify: `src/chatgpt_study_system/migration/history_occurrence.py`
- Modify: `src/chatgpt_study_system/migration/codex_occurrence_adapter.py`
- Test: `tests/test_history_occurrence.py`
- Test: `tests/test_codex_occurrence_adapter.py`

**Interface:**
- Add optional paired `source_byte_start: int | None` and exclusive `source_byte_end: int | None` fields to `ImportedHistoryOccurrence`; hide them from `repr` and reject a partial pair, bools, negatives, and empty/reversed spans with the existing fixed validation error.
- Add `parse_codex_occurrence_span(span: JSONLRecordSpan, *, snapshot_sha256: str, source_member_ref: str) -> ImportedHistoryOccurrence`.
- The wrapper accepts only a normal span with retained raw bytes, passes its physical `record_ordinal` and byte boundaries to the existing line parser, and raises fixed `oversized_record` for over-limit spans. It does not verify a real snapshot or assign semantic order.

- [x] Write failing synthetic tests for paired offset validation, adapter preservation of ordinal/start/end when a malformed span precedes a valid line, source JSON `ordinal` remaining opaque, and fixed rejection of an oversized span.
- [x] Run the new tests and confirm the new fields/wrapper are missing.
- [x] Add the paired private locator fields and span wrapper with fixed errors; do not change direct line-parser behavior.
- [x] Run DTO, span, adapter, inspector, and History contract tests; run `git diff --check`. Observed **56 passed**.
- [ ] Update public-safe status and the ignored checkpoint, then commit this synthetic-only binding.
