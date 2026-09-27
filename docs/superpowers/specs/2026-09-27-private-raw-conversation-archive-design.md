# Private Raw Conversation Archive Ingest Design

## Goal

Provide a local, bounded way to preserve official ChatGPT or Gemini ZIP exports byte-for-byte before any format-specific parsing. The feature prepares for P11.3A while leaving export authentication and real History migration blocked until their separate prerequisites pass.

## Context

P11.3A requires lossless raw archives, a verifiable source hash, and a recoverable copy before normalization. ChatGPT and Gemini exports are not currently local; their official download pages require user-completed security verification. Hermes has a local SQLite source, and Codex has candidate JSONL artifacts, but neither is a ZIP export. No raw-archive storage component exists in the repository.

## Selected approach

Add a small `PrivateRawArchiveStore` dedicated to official ZIP exports. It copies one explicitly selected regular file into the existing per-user application state tree under a source-scoped, SHA-256-derived opaque filename, verifies the copied bytes, validates the ZIP structure and CRCs without extracting entries, then atomically publishes a private manifest. The default root is under the configured user state directory and outside the repository. Tests use synthetic ZIP files under private temporary roots.

Two alternatives were considered:

1. Store only a source hash and leave the archive in Downloads. This does not guarantee the raw source remains available for reprocessing.
2. Extract files into the repository or a working directory. This risks private data entering Git and loses the original archive boundary.

The selected approach preserves the exact archive and avoids extraction.

## Interface and data flow

- `PrivateRawArchiveStore(root=None, limits=...)` uses the configured per-user state root by default; an explicit root supports isolated tests and must pass the same containment and private-directory checks.
- `ingest_zip(source_path, source_system)` accepts only `chatgpt` or `gemini` and an absolute regular `.zip` source path.
- It rejects reparse points, repository overlap, invalid ZIPs, encrypted members, and archives exceeding configured bounds.
- It streams the source into an exclusive `.partial` file under the private store while computing SHA-256. It compares source metadata before/after and validates the staged copy's size and digest.
- It checks ZIP central-directory metadata before CRC verification: at most 50,000 members, 512 MiB compressed bytes, 2 GiB declared uncompressed bytes, and 200:1 maximum member compression ratio. It does not extract or return member names.
- It verifies each member CRC with bounded streaming reads, then atomically promotes the staged file to `<source_system>/<sha256>.zip` and writes a sibling JSON manifest containing only source system, archive SHA-256, byte count, member count, declared uncompressed byte count, and UTC ingest time. The manifest contains no original filename, path, member names, conversation text, or account data. Source-scoped paths preserve provenance if two platforms produce identical ZIP bytes.
- If the digest already exists, it validates the existing archive and manifest and returns an idempotent duplicate result without replacing either file. If a prior crash published the ZIP but not its manifest, a retry validates that ZIP and safely completes the missing manifest. A present but invalid manifest fails closed.
- Any failure removes only this call's `.partial` file. Existing archive data is never deleted or overwritten.

## Error behavior

Raise fixed, path-free error codes for unsupported source, unsafe path, source changed, size limit, invalid ZIP, encrypted member, expansion limit, integrity mismatch, and storage unavailable. Errors and result representations must not reveal paths, archive names, entry names, or content.

## Boundaries

- No network download, browser control, credentials, account flow, export request, or CAPTCHA handling.
- No extraction, format-specific parsing, normalization, deduplication, History writes, or Gateway changes.
- No raw archive or real chat content in tracked files, logs, fixtures, or public documentation.
- Source inventory and archive storage remain separate: successful archive preservation does not mark conversations imported or a P11 gate passed.

## Verification

Synthetic tests cover exact byte/hash preservation, successful CRC validation, idempotent duplicate ingest, corrupted ZIP, encrypted member, path/reparse rejection, size/member/expansion limits, source mutation during copy, fixed redacted errors, atomic publication, and cleanup of only the current partial file. A test must verify no extraction occurs and no V2 business storage is opened or changed.

## Acceptance

The component passes focused tests on Windows, stores files only below a private user state root, and leaves the repository without archive fixtures or runtime data. Existing P11 statuses remain unchanged until a real official archive is downloaded by the user and separately parsed, reconciled, and imported through a formally configured Gateway.
