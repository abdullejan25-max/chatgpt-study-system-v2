# Private Codex JSONL Snapshot Design

## Goal

Preserve the current bounded set of local Codex `.jsonl` session candidates as exact file bytes in the per-user state directory before any parser or History import is considered.

## Context

The private conversation registry points to one known Codex `sessions` root. A fresh metadata-only recursive inventory found 82 regular JSONL files. A later stable bounded scan and verified private snapshot recorded 82 files totaling 322,967,757 bytes, with no reparse points or other regular-file types in the tree. Earlier public evidence reported 70 files and a different byte total; the enumeration discrepancy remains unexplained. A separate read-only structural inspector later counted records and allowlisted categories from the verified snapshot; it did not emit source content. Canonical conversation and message counts, source identities, boundaries, and content remain unknown.

## Selected approach

Add a Codex-only `PrivateCodexJSONLSnapshotStore` that accepts an explicit absolute source root, recursively enumerates `.jsonl` files under hard file-count, total-entry, total-byte, per-file, and depth ceilings, and copies them byte-for-byte into a private per-user state tree. A private manifest records relative paths, byte counts, and SHA-256 values; the archive identity is a deterministic hash of that manifest's stable fields. A staged copy is published by same-volume directory rename only after per-file copy verification and a second source-tree metadata scan. Repeated identical captures verify and reuse the existing snapshot. The store itself never parses JSONL, touches the Gateway or business databases, changes the source, or returns source paths or file names in errors/results. A separate inspector reads only a fully verified published snapshot and returns aggregate structural observations.

Hard limits are 10,000 JSONL files, 20,000 total directory entries, 512 MiB per file, 2 GiB total JSONL bytes, and 16 directory levels. Reparse points, hard-linked files, special files, unsafe paths, source changes during capture, malformed existing snapshots, and exceeded limits fail closed. A completed staging directory with a valid manifest can be promoted on retry. An incomplete staging directory is preserved and reported as recovery-required; it is never silently deleted. The private registry records `raw_format=jsonl`, candidate item count, unresolved count, source digest, and manifest digest only after the snapshot validates. It does not claim conversations or messages were imported.

## Boundaries

- Only explicit Codex JSONL candidate files are included; this is not proof that attachments or other auxiliary artifacts are captured.
- No content parsing, normalization, deduplication, History/Gateway write, or source deletion.
- Snapshot bytes, relative filenames, IDs, and digests stay outside Git and public documentation.
- The snapshot is raw-source preservation, not a P11 Gate PASS.

## Verification

Synthetic tests cover byte equality and per-file hashes, manifest/path redaction, deterministic identity and duplicate validation, source mutation detection, reparse/hard-link rejection, resource ceilings, handled failure cleanup, completed-stage recovery, preservation of incomplete staging, and Windows long destination paths. Integration metadata tests verify only the private registry fields change and that conversation/message counts remain unknown.

## Acceptance

The synthetic suite passes on Windows. A real capture is performed only from the registry's existing explicit Codex source root, only after a metadata rescan confirms the bounded file set is stable and destination space is sufficient. The real snapshot is kept under the user state root, checked against its manifest, and recorded privately. Public docs retain P11 `BLOCKED`; no real History import or P12 release is implied.
