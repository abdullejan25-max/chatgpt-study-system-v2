# P12 Step 1 — Obsidian Projection Preparation Plan

> This plan advances the P12 projection implementation while its real GUI and user-vault gates remain pending. It does not claim a release gate PASS.

## Goal

Build a deterministic, one-way renderer from explicitly supplied V2 Gateway read DTOs to an in-memory map of generated Markdown paths and contents. Keep V2 as the only authoritative store. Do not read SQLite directly, inspect private user content, or write to a real Obsidian vault in this milestone.

## Evidence and design decision

- The current live `health_report` reports History as `not_configured`; `list_history_sources` is unavailable in this Host.
- `HistoryBackend` supports source listing, query-based search, and fetch by known item ID. Search is not a complete corpus enumeration API.
- Wrong-answer Gateway reads support query-based search and bundle-by-known-source-ID. They do not enumerate all source IDs.
- Therefore this milestone implements the pure rendering boundary only. A future complete collector requires bounded, consistent Gateway enumeration APIs and a configured History target; real file output also requires a confirmed private Vault/output root.

## Invariants

- Input is a caller-provided snapshot of Gateway read DTOs; renderer code has no Gateway, database, filesystem, or network dependency.
- Output is a deterministic mapping of safe relative POSIX paths to UTF-8 Markdown strings. IDs are hashed for paths; source IDs remain in frontmatter where the projection contract requires them.
- The dashboard reports counts only for DTOs actually supplied and labels that scope explicitly; it never implies a complete V2 inventory.
- History content is preserved as provided by the Gateway. Ordering uses parsed UTC instants; equal timestamps use a deterministic ID tie-break and are marked as not proving original event order.
- Wrong-answer source, analysis versions, source refs, Study relations, and provenance summaries come only from the supplied Gateway DTOs. Assets remain references; bytes are never copied or embedded.
- Study source files are not rewritten or duplicated. Generated content is never committed from a real user snapshot.
- Enforce record and total-output bounds; validation errors use fixed messages without echoing private values.

## Tasks

### Task 1 — Synthetic contract tests

- [x] Test deterministic file maps and byte-identical rebuilds from the same snapshot.
- [x] Test History grouping, content preservation, event-time ordering, explicit timestamp-tie semantics, and bounded paths.
- [x] Test Wrong Answer versions, true source/Study references, provenance summary allowlisting, and asset-reference-only behavior.
- [x] Test malformed DTOs, duplicate IDs, count mismatches, unsafe Study relations, Gateway page bounds, per-record and aggregate size/count limits, and absence of real filesystem/database writes.

### Task 2 — Pure projection renderer

- [x] Add typed snapshot/view DTOs and deterministic Markdown rendering.
- [x] Generate dashboard with recent supplied Wrong Answers, History index/conversation pages, Wrong Answer index/source pages, and Agent-reported Knowledge Point/Error Type indexes.
- [x] Use JSON-compatible quoted YAML frontmatter; include `generated: true`, IDs, event/import times, type, and safe provenance summary. Render subject as unavailable because the current Wrong Answer DTO has no subject field.
- [x] Hash logical IDs for output path components and cap the complete rendered payload.

### Task 3 — P12 status and next gates

- [x] Record the renderer as synthetic-only preparation in public P12 docs and `docs/autonomous-run-status.md`.
- [x] Keep real Obsidian GUI, complete DTO collection, real Vault generation, and release gates explicitly BLOCKED or WAITING_FOR_USER.
- [x] Run focused synthetic tests and privacy/diff checks; no real History or Wrong Answer records are used as fixtures.

## Deferred prerequisites

- A consistent, bounded Gateway enumeration contract for complete History and Wrong Answer snapshots.
- History configuration and real source availability.
- Human confirmation of the Obsidian Vault and GUI review.
- A private, ignored generation target and a writer with safe rebuild/stale-file handling.
- Full O1–O13 validation and P12 Step 1 release gate before `v0.3.0`.
