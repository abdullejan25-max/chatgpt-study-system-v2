# P13 Gateway Recovery Design

## Authorized scope

Provide a private full V2 snapshot and isolated restore proof. The owner has
authorized autonomous implementation, debugging and non-destructive execution.
WorkBuddy Desktop verification remains a separate incomplete Gate. Recovery
preparation does not authorize V1 retirement while that Gate is incomplete.

## Choice

An Agent-side filesystem/SQLite backup would violate the Gateway-only boundary.
A Gateway-owned configured snapshot is preferred to a general arbitrary-path
backup API: its targets come exclusively from trusted local configuration.
Snapshots and restores live outside Git, outside production and outside their
private migration sidecar input. No deletion or production overwrite operation
is exposed. Existing default configurations and read tools remain compatible.

## Contract

Optional recovery configuration specifies a private root, private migration
sidecar root and explicit relative sidecar exclusions for rebuildable runtimes
or the active recovery Host trace. QMD derived config/index and the original
Gateway config are captured when configured. Snapshot keys are bounded slugs.
Tools require the existing admin capability. The plan returns aggregate size
and capacity; create/verify return logical refs, checksums, counts and proof.
Private manifests contain source locators and per-file checksums, never public
docs or MCP output. No private titles or message text are returned.

## Snapshot

Capture History, Assets metadata/versions/provenance, object files, the whole
configured Study tree, migration ledger/receipts and included sidecar files.
SQLite backup captures committed WAL; acquire database write reservations in
deterministic order to block concurrent domain mutation while materializing.
Compare file inventories before/after. Reject reparse points, aliases, changed
inputs, insufficient capacity and Git overlap. Keep failed staging evidence.
Publish only a fully verified immutable manifest and content tree. Reuse an
existing key only after verifying its complete contents, without overwrite.

Database proof compares schema, counts and deterministic row multisets, with
BLOB byte digests. File proof compares bytes and SHA-256. Canonical provenance
and identity proof runs inside the Gateway. Derived QMD state is retained;
the isolated Study configuration points to restored files.

## Restore

Restore under a new private isolated root, never production. Reject a populated
destination. Verify the source snapshot first, then every restored file and DB.
Compose an isolated read-only Gateway to check source/canonical counts,
canonical integrity and source preservation; preserve all original provenance.
Include migration-ledger proof. Persist proof privately. Later verification
rechecks the restored target rather than accepting a stale success receipt.

## Validation

Only invented fixtures: committed WAL, distinct domain stores, source-only and
canonical records, Study files, private synthetic ledger, idempotent reuse,
corrupt/missing/extra files, malformed manifest, symlink/hardlink/Git overlap,
changed input, traversal key, permission guard, no production overwrite and
restore corruption. Real production access must be a native Host Gateway call.
