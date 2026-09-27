# Codex JSONL Field-Presence Audit Plan

> **For agentic workers:** Use inline execution; all observations are aggregate-only.

**Goal:** Determine which allowlisted linkage, order, metadata, and attachment field names are present at each Codex rollout envelope layer without exposing any values.

**Architecture:** Extend the already bounded inspector with fixed category counts for record, payload, nested metadata, and content-block key presence. Run the verified private snapshot only after synthetic tests pass, and store counts in the ignored checkpoint.

**Tech Stack:** Existing Python inspector and pytest suite; no new dependencies.

## Global Constraints

- Count presence only for an explicit fixed key allowlist; ignore arbitrary keys and all values.
- Preserve existing line, record, identifier, image, and memory bounds.
- Verify the private snapshot before inspection; do not print IDs, values, file names, paths, or hashes.
- Do not infer linkage, order, role, branch semantics, or canonical counts from key presence.
- No History/Gateway/registry/Asset writes, no release, no push.

---

### Task 1: Aggregate schema-field presence

**Files:**
- Modify: `src/chatgpt_study_system/migration/codex_jsonl_inspector.py`
- Modify: `tests/test_codex_jsonl_inspector.py`
- Modify: `docs/superpowers/specs/2026-09-27-codex-jsonl-inspection-design.md`
- Modify: `var/p11-p12-resume/checkpoint.json` (ignored)

- [x] **Step 1: Add a failing synthetic test** proving fixed field names are counted by scope while sentinel values and arbitrary key names never appear in the result.
- [x] **Step 2: Run the focused test and confirm it fails because the result has no field-presence counts.**
- [x] **Step 3: Add bounded allowlisted field counters** for record, payload, `payload.meta`, and content-block scopes.
- [x] **Step 4: Run focused inspector/snapshot/registry/History tests and `git diff --check`.** Observed **58 passed, 4 skipped**.
- [x] **Step 5: Inspect the verified private snapshot with the updated inspector**; output contained only fixed scope/key categories and aggregate counts.
- [ ] **Step 6: Update public-safe status, private checkpoint, and commit the inspector/test/docs milestone.**

### Task 2: Compare candidate session IDs and ordinal continuity

- [x] **Step 1: Add a failing synthetic test** for matching/non-matching `session_meta.payload.id` versus `session_id`, plus equal/regressing top-level `ordinal` values.
- [x] **Step 2: Run the focused test and confirm the current result lacks these aggregate comparisons.**
- [x] **Step 3: Add only aggregate equality/regression counters**; retain no identifier or ordinal values in the result.
- [x] **Step 4: Run focused inspector/snapshot/registry/History tests.** Observed **59 passed, 4 skipped**.
- [x] **Step 5: Re-run the verified snapshot and save only comparison counts privately.** Observed 57 equal ID/session_id pairs and 43 non-matching; all 60,846 records have ordinals, with zero adjacent equalities/regressions.
- [ ] **Step 6: Update status/checkpoint and commit after `git diff --check`.**
