# Lossless Imported History Envelope Design

## Status

Design only. This proposal does not change the Gateway, SQLite schema, MCP capabilities, or any private/business store. History remains unconfigured and P11 remains blocked.

## Problem

The current `HistoryImportItem` / `HistoryItem` contract stores one text string, a closed role set (`user`, `assistant`, `system`, `tool`), one timestamp, one conversation ID, and one source item ID. The verified Codex snapshot shows message-shaped records with `developer` roles and inline image blocks, repeated message IDs with differing timestamps, tool/event records outside the message shape, and multiple session metadata IDs in some files. Therefore, mapping the source into the current contract would lose source structures or make unsupported identity, timestamp, and deduplication choices.

Codex rollout formats can evolve. The upstream fixture checked on 2026-09-27 constructs a `session_meta` payload from a `SessionMetaLine` wrapper containing `meta` and `git`; that current fixture is useful schema evidence, but it does not prove that the already captured local files use the same version or field layout. A future adapter must profile the verified source snapshot itself, support only explicitly verified variants, and keep all other structures opaque. [Upstream rollout fixture](https://github.com/openai/codex/blob/main/codex-rs/app-server/tests/common/rollout.rs)

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
| `source_ref` | Private immutable snapshot identity plus private member reference and line/record ordinal. It is an evidence locator, not a user-facing filename. |
| `occurrence_id` | Deterministic identity for one source occurrence, derived from the source namespace and stable locator. It does not imply message identity. |
| `source_item_id` | Original source identifier when present, kept in the source namespace and treated as a possibly duplicated hint. |
| `conversation_ref` | Optional unresolved source grouping reference. It remains absent until a documented source-to-conversation mapping is proven. |
| `order` | Source member ordinal and record ordinal, retained independently of timestamp. |
| `timestamp` | Raw source value, optional parsed UTC value, and a parse/status field. Parsing does not establish timestamp semantics. |
| `kind` / `role` | Open strings for source record kind and role. Known values are classified for search/display, but unknown values remain intact. |
| `content_blocks` | Ordered typed blocks. Text, inline image references, tool/event payload references, and unknown blocks retain boundaries and opaque source references. |
| `extensions` | Versioned source-specific fields not yet promoted to shared semantics; unknown keys are preserved in the raw snapshot and may be indexed only through a bounded, private opaque representation. |
| `conflicts` | Explicit references to duplicate-ID groups and per-field conflict classifications; no automatic merge or winner selection. |

The shared envelope should not duplicate entire raw records into the History database. The verified snapshot remains the lossless source of truth; envelope fields are an index/projection with enough private provenance to re-read exact source bytes. If the source snapshot is unavailable or its integrity check fails, the envelope cannot be treated as independently lossless.

## Mapping rules for current evidence

1. **Conversation identity:** JSONL member count and distinct `session_meta` ID count are observations, not canonical conversation counts. No conversation reference is assigned until record-to-session linkage is evidenced.
2. **Message identity:** a repeated source message ID creates an occurrence group. The observed timestamp conflicts mean that ID alone cannot be the unique item key. Keep each occurrence and report content/role/timestamp conflict flags.
3. **Roles and event kinds:** keep the original role/kind as open values. Do not map `developer` to `system`, flatten tool calls into text, or discard non-message event records.
4. **Ordering and time:** source ordinal is authoritative for replaying source order. A parseable UTC timestamp is stored as a parsed observation alongside its raw value; it does not replace source order or prove event-time meaning.
5. **Attachments:** inline image data remains represented by a private reference into the immutable source snapshot. Do not create an Asset or extract a file until an explicit attachment mapping and formal Asset workflow exist.
6. **Unknown fields:** preserve them in the immutable source bytes and expose only a safe, allowlisted classification in general History search/projection. Never silently discard them during import.

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
- It does not authorize parsing beyond the bounded aggregate inspector, real normalization, History writes, source deletion, publishing, or release.
