# Unified Write Provenance Design

## Goal

Make important persisted writes traceable across History, assets, documents, derived OCR, and Wrong Answer data while keeping source evidence, deterministic derived data, Agent-authored data, imports, and system-generated data semantically distinct.

## Current findings

- Wrong Answer source rows are immutable and point to verified `asset://` or `document://` evidence. Analysis rows are append-only and versioned, but expose only `generated_by_agent`, `agent_supplied`, and a runtime `created_at`; they do not identify the caller or link versions explicitly.
- History import preserves the source event time in `history_items.created_at`, but does not store the actual Gateway import time, source system, or import batch. The import API is currently an internal adapter operation, not an MCP write tool.
- Asset/document storage uses content-addressed immutable source assets and deterministic page/chunk rows. OCR continuation updates current derived page text in place. Its audit event is transaction-coupled, but the current audit schema has no actor/source detail.
- History and Asset/Document stores are separate databases. They cannot share a physical ledger transaction, so they need the same logical schema and local transaction semantics rather than a cross-database transaction.

## Decision

Add an append-only `write_provenance` ledger with the same columns and constraints to each configured SQLite database. Keep each domain's existing tables as the typed current/business representation. Write a provenance row in the same SQLite transaction as each successful persistent mutation; link revisions through `supersedes_provenance_id`. The ledger records logical references and hashes/identifiers only, never source text or filesystem paths.

The ledger records `data_origin` (`source`, `deterministic_derived`, `agent_generated`, `imported`, or `system_generated`) separately from `actor_type` (`external_client`, `importer`, `system`, or `unknown`). The caller may supply an optional `provenance` object containing `reported_agent`, `reported_client`, and `run_id`; these values are bounded, sanitized, and explicitly reported rather than authenticated. There is no `verified_agent` field and no claim that MCP client metadata proves a human or Agent identity.

The Gateway generates every `recorded_at` timestamp using UTC at write time. Caller-supplied source timestamps are preserved only as `original_created_at`. History import rows additionally retain `imported_at`, `source_system`, and a Gateway-generated `import_batch_id`; the source's logical ID is retained. New imports are tagged `legacy_status='native'` or `imported` according to their operation. Existing records discovered during additive migration receive `legacy_status='pre_provenance'` and are not assigned invented actor identities or source-system metadata.

Wrong Answer analysis remains append-only. Its existing `version` remains authoritative, while each version gains an explicit link to the preceding analysis and its provenance row. Updates use the same optimistic version check and idempotency behavior. Source rows stay immutable, and an Agent analysis cannot change the origin or bytes of its source Asset/Document.

Document ingestion records source-data provenance for the original asset and document, with the document referencing its original asset. Extracted/OCR page writes record deterministic-derived provenance referencing the source document and asset. OCR revisions get increasing provenance versions and supersede prior page provenance, while the page/chunk tables continue to represent the current search index. This ledger proves when and from which source the current derived page was written; it is not a content archive for old OCR text.

History imports remain an explicit importer API and do not become an Agent-facing MCP capability. No additional write permission is exposed. The MCP Wrong Answer and asset/document write schemas accept only the optional reported identity/session envelope; provenance categories, timestamps, origin, version, and previous-version links are created by the Gateway/storage layer.

## Migration and compatibility

Schema changes are additive and run inside existing write transactions. A `schema_migrations` marker makes upgrades idempotent. Existing rows are retained, not rewritten or deleted; the upgrade emits one `pre_provenance` ledger entry for legacy records where a domain timestamp can be safely reused, and leaves unknown historical actor/import fields null. Legacy compatibility rules for the existing Wrong Answer source ID are preserved. Reads return the existing domain fields plus a nested provenance projection; MCP JSON shapes stay backward compatible for prior fields.

## Alternatives considered

1. Add provenance columns independently to every domain table. This makes queries simple but duplicates evolving identity/source/import rules and makes revision history awkward across unrelated types.
2. Use the audit table as the provenance source. Audit currently represents operations/outcomes, including retries, while provenance describes the origin/version of persisted records; merging them would blur those meanings and still fail to represent superseded content.
3. Use one shared SQLite file for all domains. This would introduce a larger migration and configuration change and would not solve transactions with external QMD or Study files.

The append-only per-database ledger keeps a common contract, preserves domain-specific models, and commits atomically with its local records.

## Safety and verification

- No model/provider client, remote transport, credential, or public listener is added.
- No real History, StudyVault, textbook, or image data is read or modified. Tests use synthetic temporary databases and assets.
- MCP identity fields are caller-reported and untrusted. Timestamps and versions are Gateway-controlled.
- Migration tests cover existing databases, rollback, duplicate writes, optimistic conflicts, source-ref validation, and migration repeatability.
- Full local regression is the release gate for this change; Phase 10 and real-data E2E remain out of scope.
