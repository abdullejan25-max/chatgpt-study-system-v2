# Lossless Imported History Envelope Design

## Status

Design plus in-memory DTO and pure single-line adapter prototypes in `migration/history_occurrence.py` and `migration/codex_occurrence_adapter.py`. The adapter is verified only with synthetic fixtures and is not connected to snapshot traversal. Nothing changes the Gateway, SQLite schema, MCP capabilities, or private/business stores. History remains unconfigured and P11 remains blocked.

## Problem

The current `HistoryImportItem` / `HistoryItem` contract stores one text string, a closed role set (`user`, `assistant`, `system`, `tool`), one timestamp, one conversation ID, and one source item ID. The verified Codex snapshot shows message-shaped records with `developer` roles and inline image blocks, repeated message IDs with differing timestamps, tool/event records outside the message shape, and multiple session metadata IDs in some files. Therefore, mapping the source into the current contract would lose source structures or make unsupported identity, timestamp, and deduplication choices.

Codex rollout formats can evolve. The upstream fixture checked on 2026-09-27 constructs a `session_meta` payload from a `SessionMetaLine` wrapper containing `meta` and `git`; that current fixture is useful schema evidence, but it does not prove that the already captured local files use the same version or field layout. A future adapter must profile the verified source snapshot itself, support only explicitly verified variants, and keep all other structures opaque. [Upstream rollout fixture](https://github.com/openai/codex/blob/main/codex-rs/app-server/tests/common/rollout.rs)

The current upstream [`ContentItem` model](https://github.com/openai/codex/blob/main/codex-rs/protocol/src/models.rs) includes text, image, and audio variants. The synthetic parser maps only explicit input/output text blocks; image, audio, event/tool, and unknown content remain references into the raw member. This is current upstream evidence, not a claim that every local rollout uses these variants.

An aggregate-only field-location check on the verified local snapshot found all 100 `session_meta` IDs at the outer `payload.id` location, none at `payload.meta.id`, and no records containing both locations. The inspector now recognizes either location and fails closed if both are present with different values; it does not infer any conversation relation from these IDs.

An aggregate comparison found 57 equal outer `payload.id` / `payload.session_id` pairs and 43 non-matching pairs. Non-matching is not treated as a conflict and no identifier mapping is chosen. All 60,846 records have an exact non-negative top-level `ordinal`; per-file adjacent comparisons found zero equal values and zero regressions. This does not establish conversation or message-order semantics.

## Design goals

- Keep original source bytes in the already verified private snapshot as the immutable evidence.
- Represent a parsed occurrence separately from any claim that it is a canonical message or conversation.
- Preserve source ordering, raw timestamp spelling, role/type values, content block boundaries, and unknown fields without coercing them into the current closed text model.
- Make duplicate identity and field conflicts explicit; never select a winner based on traversal order.
- Keep source-derived identifiers, opaque payloads, and file/offset locators private. Public status contains only aggregate counts and fixed gate states.
- Keep all writes behind the configured History target and explicit migration gate. No write adapter is part of this design-only step.

## Proposed versioned envelope

Use a versioned `ImportedHistoryOccurrence` envelope with these conceptual parts:

| Part | Meaning |
|---|---|
| `source_system` | Validated source namespace, such as Codex, ChatGPT, Gemini, Hermes, or WorkBuddy. |
| `source_ref` | Private immutable snapshot identity plus private member reference and line/record ordinal. It is an evidence locator, not a user-facing filename. |
| `occurrence_id` | Deterministic identity for one source occurrence, derived from the source namespace and stable locator. It does not imply message identity. |
| `source_item_id` | Original source message/event identifier when present, kept in the source namespace and treated as a possibly duplicated hint. |
| `conversation_ref` / title | Optional source conversation ID and title, populated only when the export reliably provides the value and its relationship. Otherwise remain unknown. |
| `order` | Preserve member and record ordinals as locators. Store source-declared conversation/message sequence separately when present. A sorted filename or timestamp is never promoted to semantic conversation order. |
| `timestamps` | Raw source created/updated values, optional parsed UTC observations, and parse/status fields. Parsing does not establish event-time semantics. `imported_at` is assigned by the importer at actual import time. |
| `kind` / `role` / author / model | Open source values. Record role, author, and model only when explicitly present; do not infer one from another. Unknown values remain intact. |
| `content_blocks` / attachment refs | Ordered typed blocks. Text, inline image refs, tool/event payload refs, and unknown blocks retain boundaries and opaque source refs. Retrieved attachment bytes require the formal Assets/Documents content-addressing, deduplication, and provenance path; a URL or expired reference is not archived bytes. |
| `provenance` / source relation | Snapshot hash, source system, importer/batch identity, and explicit legacy/source relation. Preserve source hash and provenance without copying private paths into public output. |
| `branches` | Source-provided branch, edit, or regeneration references when reliably available; otherwise unknown. Never flatten alternatives into a single linear transcript. |
| `extensions` | Versioned source-specific fields not yet promoted to shared semantics; unknown keys are preserved in the raw snapshot and may be indexed only through a bounded, private opaque representation. |
| `conflicts` | Explicit references to duplicate-ID groups and per-field conflict classifications; no automatic merge or winner selection. |

The shared envelope should not duplicate entire raw records into the History database. The verified snapshot remains the lossless source of truth; envelope fields are an index/projection with enough private provenance to re-read exact source bytes. If the source snapshot is unavailable or its integrity check fails, the envelope cannot be treated as independently lossless.

## Exact raw-member locator contract

For JSONL, `record_ordinal` means the zero-based physical line index within one manifest member. Every LF-delimited span advances it, including blank, malformed, non-object, and over-limit lines; a final unterminated non-empty span also advances it. LF belongs to that span, so CRLF retains both terminator bytes. A trailing LF does not invent an additional empty span. The adapter's caller supplies this physical locator index; it is never copied from the source JSON object's own `ordinal` property. That source property remains opaque until its semantics are independently established.

A durable raw locator should bind the verified snapshot identity and private manifest member reference to `record_ordinal`, zero-based `byte_start`, and exclusive `byte_end`. The byte span includes any LF/CRLF terminator. A resolver must verify snapshot and member integrity before reading, require the requested span to align with a complete physical line, and fail with a fixed error if bytes or manifest identity differ. Malformed and over-limit spans remain addressable evidence but are not passed to the occurrence adapter. Conversation order and message order remain separate optional source-declared relations; neither physical line position nor the source `ordinal` property is promoted to either semantic order without evidence.

The current in-memory DTO prototype carries member reference and physical `record_ordinal`, while its compact block references use that ordinal only. A synthetic-only bounded span iterator now computes exact physical line byte spans; it does not access the private snapshot, verify a manifest, or resolve locators against stored members. The DTO still lacks durable byte-span fields and raw-byte resolution, and must not be described as independently lossless without the verified immutable snapshot.

## Mapping rules for current evidence

1. **Conversation identity:** JSONL member count and distinct `session_meta` ID count are observations, not canonical conversation counts. No conversation reference is assigned until record-to-session linkage is evidenced.
2. **Message identity:** a repeated source message ID creates an occurrence group. The observed timestamp conflicts mean that ID alone cannot be the unique item key. Keep each occurrence and report content/role/timestamp conflict flags.
3. **Roles and event kinds:** keep the original role/kind as open values. Do not map `developer` to `system`, flatten tool calls into text, or discard non-message event records.
4. **Ordering and time:** line ordinal preserves order within a member. Cross-member or conversation order remains unknown unless the source gives an explicit sequence/relation. A parseable UTC timestamp is stored as a parsed observation alongside its raw value; it does not replace source order or prove event-time meaning.
5. **Attachments:** inline image data remains represented by a private reference into the immutable source snapshot. Do not create an Asset or extract a file until an explicit attachment mapping and formal Asset workflow exist.
6. **Unknown fields:** preserve them in the immutable source bytes and expose only a safe, allowlisted classification in general History search/projection. Never silently discard them during import.
7. **Adapter boundary:** the current pure parser recognizes only a small set of explicit record/content shapes. It keeps conversation links, title, model, branch relations, and source-declared ordering unset; tests on synthetic fixtures do not establish local-source mapping correctness.
8. **Ambiguous JSON objects:** reject any record containing duplicate object keys at any depth with a fixed, path-free error. Do not accept the JSON decoder's default last-value-wins behavior for identity, role, content, or metadata fields. The immutable raw snapshot remains the evidence for later review.

## Coverage and retrieval requirements

For every source, the migration report distinguishes discovered, accessible, exported, raw archived, normalized, imported, deduplicated, unresolved, and waiting-for-user counts plus known coverage gaps. Counts must state whether they are source-reported, observed occurrences, or canonical normalized items. Before a release gate can pass, synthetic and eligible real read-back tests must cover source filtering, keyword and exact-phrase search, multiple items in one conversation, source-time filtering when known, cross-source retrieval, no-result behavior, and duplicate conflict correctness. Real chat text must not enter tracked logs or docs.

## Compatibility path

- Keep the existing text-only import contract for sources proven to contain ordinary user/assistant text and timestamps.
- Introduce a separate versioned envelope/import API only after a migration plan, schema migration, transaction/idempotency rules, and retrieval behavior are reviewed.
- Existing History readers must continue returning legacy items unchanged. Envelope-aware readers can expose typed blocks and source ordering; legacy text search may index only explicitly extracted text blocks and must not claim full-source retrieval coverage.
- A batch is accepted only when every occurrence has a stable source locator, source snapshot identity, and deterministic occurrence key. Duplicate handling is conflict-aware and rerunnable.

## Required gates before implementation or real import

- Define and test source record-to-session linkage using synthetic fixtures with multiple session metadata records, interleaved events, and branches.
- Specify exact raw-byte locator behavior across newline variants, malformed lines, oversized lines, and source changes.
- Review database migration, provenance, privacy, rollback, idempotency, and projection/search semantics.
- Add synthetic round-trip tests proving all source record classes and unknown fields remain recoverable from snapshot reference plus envelope.
- Confirm configured History target, write capability, and explicit source/import gates before any business write. The current real target is not configured, so no real import is eligible.

## Non-goals

- This design does not establish canonical conversation/message counts for Codex or any other source.
- It does not solve cross-source deduplication, source export acquisition, authentication, branch semantics, image Asset relations, or WorkBuddy/Hermes host authorization.
- It authorizes only the synthetic pure-line parser prototype. It does not authorize running that parser on real private records, real normalization, History writes, source deletion, publishing, or release.
