# V1 Deletion Candidate Report

Date: 2026-09-30. V2 is this project's active authoritative learning system after P11 source migration. **No V1 files or backups were deleted.** This report classifies candidates; it does not authorize deletion.

| Category | Classification | Reason |
|---|---|---|
| Shared authoritative StudyVault files | KEEP_AS_AUTHORITATIVE | V2 directly reuses the existing Study root; files are not migration leftovers |
| Original V1 chat Markdown | KEEP_AS_ARCHIVE | Exact V2 source documents verified; original provenance/archive remains valuable |
| Original wrong-answer notes and images | KEEP_AS_ARCHIVE | Exact bytes and explicit refs preserved; complete business semantics remain unresolved |
| Original Native Memory DB and verified source snapshot | KEEP_AS_ARCHIVE | Retain original fact metadata alongside the typed derived-fact record |
| Immutable Codex source snapshot and manifest | KEEP_AS_ARCHIVE | Source identity and raw-event provenance; canonical normalization is deferred |
| V2 History/Asset stores, journals and recovery receipts | KEEP_AS_AUTHORITATIVE | Active stores or migration/recovery evidence; never treat as disposable V1 files |
| Verified pre-migration DB/blob/config backups | KEEP_AS_ARCHIVE | Retain recovery evidence; no unique backup deletion |
| V1 runtime code and reproducible build/cache artifacts | SAFE_TO_DELETE_LATER | Runtime retired for this project; a later explicitly authorized deletion must recheck live dependencies |
| Seven unsupported Personal items / external client settings | REVIEW | No guessed migration or deletion decision; user-managed integrations may still use them |

No destructive reset, original-data deletion, backup deletion or global client-setting removal was performed. WorkBuddy/Hermes integration retirement outside this project's runtime remains a separate P12 verification.
