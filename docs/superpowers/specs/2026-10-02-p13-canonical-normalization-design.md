# P13 deterministic conversation normalization

## Entry gate and scope

Source-only completion is PASS for acquired inputs: 1,692 unique acquisition
fingerprints and 1,776 Gateway evidence indexes, with exact-byte/provenance rerun
proof. ChatGPT remains acquisition_pending; its later incremental acquisition is
supported. The active post-inventory log tail is explicitly deferred. Owner
authorization permits design and implementation without another approval pause.

Source evidence remains immutable. Add derived tables in the configured History
SQLite database, not another database/Memory, and leave existing History, Study,
Wrong Answer, Assets, Documents and Projection interfaces compatible.

## Identity and views

Extending the old required-timestamp History DTO would fabricate unknown dates.
A separate conversation per file would duplicate logical conversations across
snapshots. Use shared canonical identities plus source-specific views instead.

- Conversation identity hashes source system and an explicit native conversation
  key. If a documented export object defines a boundary without a native key,
  its source fingerprint and structural pointer define a derived-safe identity.
- Message identity hashes conversation, explicit native message key (or stable
  source-defined position), role and exact derived content/time representation.
  Changed native payloads remain distinct variants rather than being overwritten.
- Each source view records original sequence or parent-child structure, message
  locators, confidence, title/time assertions and its source reference. Multiple
  snapshots do not force a single ordering. Tree views retain branches; no main
  branch is guessed. Conversation/message source evidence refs accumulate through
  immutable evidence links, without replacing earlier provenance.
- Identities omit private absolute paths and import/normalization clocks.

## Canonical records

Conversations declare conversation ID, source system, view/source refs, participant
metadata, nullable reliable created/updated time and title assertions, provenance
and normalization state. Messages declare message ID, conversation ID, explicit
role, ordered content parts, text, nullable occurrence time, source-view position
or parent relation, evidence locators, attachments, reliable explicit model metadata
and provenance. Unknown optional values remain null, never import time.

Each derived record/evidence link declares `p13-normalize-1`, adapter/method,
normalized_at/recorded_at, source ID/fingerprint, source occurrence-time quality,
confidence and source imported_at. First successful normalization time/provenance
is stable on rerun. Original bytes, role labels and raw timestamps remain evidence.

## Confidence and adapters

`exact` requires explicit boundary, role, ordering and reliable source timestamp.
`derived-safe` requires a documented deterministic boundary/ordering mapping and
an explicit role. Missing optional time remains unknown; partial/unreliable time
is never reconstructed. Unknown role, conflicting boundaries, inconsistent graphs,
incomplete streamed records or unsupported content remain ambiguous/source-only.
Only exact/derived-safe candidates are persisted. No LLM, embeddings or semantic
reconstruction is involved. Non-message runtime/tool events are not human messages.

Thin, versioned adapters:

- Codex JSONL: one explicit session_meta ID; explicit response_item message roles;
  original physical-line order/byte spans. Other events remain source evidence.
- WorkBuddy native JSONL: explicit sessionId, role-bearing messages and native IDs;
  original order/parent assertions. Private legacy format status is explicit.
  Hook archives and session metadata are not treated as a complete chat transcript.
- Hermes session records: explicit session ID and ordered message array with roles,
  timestamps and native message IDs. Runtime failures/profile/request metadata are
  unsupported; compacted/hidden flags remain assertions, not guessed actors.
- ChatGPT JSON/ZIP: explicit export conversation objects and mapping graph; validate
  parent/children, retain branching/hidden/null nodes. Do not flatten regenerated
  responses or infer a main branch. Synthetic contract now, real validation pending.
- Gemini activity archives and legacy Markdown/SQLite/facts: retain source-only when
  conversation boundary/role evidence is absent. Uploaded opaque members are not
  reclassified as Gemini messages.

Attachments use verified existing logical refs or exact embedded bytes registered
by the Gateway. Missing/unresolvable files retain evidence-backed missing metadata;
no path guessing, network download or fake Asset. Original multimodal parts remain
traceable even when a part cannot be materialized.

## Execution, reconciliation and readback

Gateway/MCP exposes source-set snapshot identity, bounded deterministic normalization,
summary, conversation search/view read and message read. Ingest/read capabilities
apply. Each call pins the immutable source-set digest; additions cause conflict and
require an explicit incremental snapshot. Per-source canonical writes and outcome
are atomic; source-only outcomes and fixed errors are durable too. Batch receipts
stay private. Re-running a completed source/version/plan does not add records.

Reports distinguish packages, files/members, candidates, canonical conversations,
messages/views, exact, derived-safe, ambiguous, malformed, unsupported, source-only,
duplicates and pending/deferred. Every source has an explained outcome. Readback and
cross-agent verification use formal Gateway only. Backup/isolated restore and V1
unique-data/logical retirement follow normalization reconciliation. Physical deletion
remains a single owner-confirmed destructive transaction.
