# Codex JSONL Structural Inspection Design

## Goal

Inspect an already verified private Codex JSONL snapshot to determine which source structures a future lossless History adapter must preserve. The inspection is read-only and produces counts only.

## Evidence motivating this step

The verified local snapshot contains 82 JSONL candidates. A bounded exploratory scan observed multiple `session_meta` records per file, repeated message IDs with the same role/content but differing timestamps, `developer` role messages, and image data URIs embedded in user messages. These observations demonstrate that file count is not a conversation count and that the current text-only History import contract cannot represent the source without losses. No user-facing content, IDs, file names, or hashes were emitted.

## Chosen approach

Add an inspector that accepts only a published snapshot path and expected snapshot digest, verifies the manifest and every file before parsing, then streams JSONL records under fixed line and record-count ceilings. It reports allowlisted event/content/role categories, parseability, metadata-ID cardinalities from the observed outer `payload.id` or nested `payload.meta.id` layouts, duplicate-message-ID conflict categories, timestamp syntax coverage, and inline image data URI integrity/deduplication counts. If both metadata ID locations are present and differ, inspection fails closed. Its result contains aggregate counts only; identifiers, text, paths, image bytes, and digests never leave the function.

The inspector is not a normalizer or importer. It does not assign canonical conversation/message counts, choose timestamps for conflicting duplicate IDs, map `developer` to another role, flatten tool events, or create Assets. Those choices require an explicit lossless History representation and remain blocked from business writes while the History target is unconfigured.

## Alternatives considered

1. Normalize user/assistant text immediately. Rejected because it would omit developer messages, event/tool records, and attachment relations, while silently resolving repeated IDs with conflicting timestamps.
2. Expand Gateway History to a multimodal/event model before understanding the source. Deferred because the source also contains non-message events and branches; a broader model should follow a documented field mapping and synthetic compatibility plan.
3. Read-only structural inspector. Selected because it turns the private snapshot into reproducible, bounded evidence without claiming unsupported semantics or changing authoritative stores.

## Bounds and privacy

- Reuse the snapshot store's manifest, SHA-256, private-path, and size checks before inspection.
- Cap each JSONL record at 16 MiB and total records at 1,000,000; stop with a fixed path-free error when a bound is exceeded.
- Cap distinct message IDs at 250,000, decoded inline image bytes at 512 MiB total, and unique image payload tracking at 100,000 images / 256 MiB. Exceeded state or image bounds fail closed instead of exhausting memory.
- Never return or log raw data, source identifiers, filenames, paths, content, image bytes, or digests.
- Image data URIs are decoded only in memory for integrity and deduplication counts; no Asset registration or file extraction occurs.
- All persisted fixtures are synthetic. Real inspection results go only to the ignored private checkpoint; public docs contain aggregate observations and uncertainty only.

## Verification

Synthetic tests cover valid/invalid JSONL, non-object records, line and total-record bounds, fixed path-free failures, category counts, both metadata ID layouts and conflicting metadata IDs, repeated message IDs with time/content conflicts, valid and invalid inline image data, image deduplication, and snapshot verification before reads. Tests prove the result representation contains no fixture content, ID, filename, path, or digest.

## Acceptance

On the existing private snapshot, the inspector completes within bounds and agrees with manifest file/byte totals. Its output remains aggregate-only. No History backend, Gateway capability, or V2 business database is read or written by this inspection step.
