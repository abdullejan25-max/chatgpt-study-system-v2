# Phase 8 Checkpoint — Safe Write Layer

## Implemented

- Gateway capabilities are `read`, `write`, `ingest`, and `admin`; absent local configuration defaults to `read` only. Capability checks run in Gateway methods, and stdio MCP tool discovery hides disabled operations.
- Asset/document, History, and wrong-answer writes append metadata-only SQLite audit events in the same transaction as the corresponding data mutation. Events store operation, resource type, logical resource ID, UTC timestamp, and success outcome; they do not store source text or private paths. A separate common `write_provenance` ledger records source/origin/version/import metadata in that same local transaction.
- Explicit asset/document roots, database parents, database files, and blob paths are checked for symlinks and Windows reparse-point attributes. Storage rejects unsafe paths with a fixed `STORAGE_UNAVAILABLE` error.
- Existing ingestion limits and document transaction rollback remain enforced. Synthetic tests cover disabled writes, config parsing, discovery, path boundary checks, audit metadata, and audit rollback.

## Tests

- Targeted security and affected module tests: `86 passed` before final discovery/error assertions.
- Final Phase 8 security tests: `9 passed`.
- Full regression suite: `229 passed, 4 skipped`.
- The Phase 8 Windows junction integration test skips because this host does not permit creating NTFS junctions; a deterministic reparse-attribute test still verifies rejection logic.
- Tests do not access real History, StudyVault write surfaces, or personal documents.

## Decisions and limitations

- Capability checks do not provide OS sandboxing and do not defend against a malicious local process racing filesystem paths between checks and access. Roots remain private and explicitly configured.
- Audit is transaction-coupled success audit, not a separate durable log of failed attempts; failed transactions leave no success event.
- Admin is a deliberate local opt-in with all capabilities; MCP does not infer or grant it.
