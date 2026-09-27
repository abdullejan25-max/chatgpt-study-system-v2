# Codex JSONL Structural Inspection Plan

**Goal:** Reproducibly inspect a verified private Codex JSONL snapshot without exposing content or claiming unsupported conversation/message semantics.

**Architecture:** A bounded read-only inspector verifies the content-addressed snapshot first, parses one JSONL record at a time, and returns fixed categorical counts. It does not normalize or persist History items.

## Tasks

### Task 1: Synthetic inspector contract

- [x] Add synthetic tests for valid records, metadata IDs, message roles/timestamps, duplicate IDs, and image data URIs.
- [x] Add tests for malformed/non-object records, line/record limits, snapshot mismatch, and redacted errors/results.
- [x] Implement a path-free aggregate result with fixed allowlisted categories.
- [x] Bound retained message-ID and image-deduplication state; fail closed when those bounds are exceeded.
- [x] Run focused synthetic tests and review that no values from input records escape.

### Task 2: Inspect existing private snapshot

- [x] Run only after the inspector verifies the manifest and all file hashes.
- [x] Compare observed structural counts with the prior bounded audit without publishing identifiers/content.
- [x] Store semantic uncertainties and aggregate evidence in the ignored checkpoint; leave canonical conversation/message counts unknown.
- [x] Update P11 docs to distinguish observed event/message-shaped records from canonical History counts.
- [x] Use the structural evidence to write a separate design-only proposal for a lossless History envelope; no schema or Gateway implementation in this plan.

### Task 3: Checkpoint and next design gate

- [x] Run `git diff --check`, focused tests, and adjacent History contract tests.
- [ ] Commit code, tests, plan, and public-safe docs.
- [ ] Update the ignored resume checkpoint to the verified HEAD.
- [ ] Use the evidence to design a separate lossless normalized History model; do not write V2 business data until target configuration and gates pass.
