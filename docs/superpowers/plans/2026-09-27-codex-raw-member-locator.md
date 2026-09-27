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

- [ ] Write synthetic tests for LF, CRLF, final unterminated lines, blank/malformed records, trailing LF, and oversized-line draining with exact start/end offsets.
- [ ] Run the tests and confirm the span-index API is missing.
- [ ] Implement a bounded binary-stream iterator that reports exact spans and omits oversized content.
- [ ] Verify every emitted normal span round-trips to the exact original bytes; verify oversized spans preserve exact length without retaining data.
- [ ] Run focused synthetic tests and `git diff --check`.
- [ ] Update status/checkpoint and commit; keep private snapshot/Gateway/business data untouched.
