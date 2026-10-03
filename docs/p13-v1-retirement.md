# V1 logical retirement

P13 reuses the accepted P11 migration and the private P13 acquisition ledger.
Authoritative V1 inputs were located from the original migration descriptor,
the known legacy router configuration, and explicitly selected archive roots.
No unrelated disk, credential store or browser profile was searched.

The initial bounded unique-data audit covered 442 original input files (67,641,056 bytes).
Every file has an exact source-evidence mapping. Two preserved Native Memory DBs
contain the same single user row but have different raw bytes; both are retained
as separate evidence, with a duplicate-candidate relation rather than a merge.
The prior P11 accounting remains accepted: 1,209 objects, including 1,048 Study
objects reused in place, 84 typed source documents, 70 image inputs and seven
intentionally skipped files. These accounting universes overlap and are not
added together.

The current audit captured those seven previously skipped files and 19 archive
files generated after the earlier acquisition cutoff. All 26 were incrementally
imported through the formal Gateway. Replaying the same manifests created zero
new records; checksums and provenance are stable. Their conversation structure
is unsupported, so they add source-only outcomes and no canonical messages.
At the release checkpoint, production had 1,802 sources/outcomes, 487 conversations, 7,334 messages and
1,349 wholly source-only records. Gemini and the earlier normalization were not
rerun. ChatGPT remains acquisition_pending.

V1-only unknown = 0 after the producer freeze. The original StudyVault remains
the authoritative static Study source and is outside the deletion transaction.
Legacy notes whose complete Wrong Answer semantics remain uncertain retain
their original documents, image refs and accepted source-only representation.

## Runtime cutover

The old Native Memory router has no active process or scheduled dependency.
The legacy Basic Memory Host entry was already disabled. A remaining WorkBuddy
archive hook still launched a Basic Memory writer independently of that entry;
six matching hook triggers were removed with an exact private configuration
backup. Other hooks/settings are preserved. The cold router is explicitly marked
deprecated. No raw input, DB, archive or backup was deleted.

Configuration backups, checksums, mappings, source proofs and the exact runtime
audit remain outside Git. Rollback requires an explicit decision to restore the
archived configuration; ordinary agents must continue to use the V2 Gateway.

## Physical transaction boundary

The current state is **V1 logically retired / data retained**. Recovery success
and source completeness do not authorize deletion. The owner receives concrete
private input locations, categories, size, reconciliation and recovery evidence
before the one final physical-deletion question. Only explicit confirmation may
authorize that transaction. Retaining cold archives is an accepted completion
state. V2 stores, V2 recovery snapshots and authoritative StudyVault files are
never V1 deletion candidates.

## Final freshness delta

Final exact-file and bounded directory-set validation found one archive that had
grown and one unlisted archive created before the producer freeze. Both were
imported/reused through native Gateway tools and retained source-only; earlier
source versions remain preserved. The final 443 original inputs total 67,700,601
bytes, with V1-only unknown = 0 and exact directory-set equality. A reversible
collector entry-point guard prevents cached hooks and manual commands from
restarting the legacy writer. Only exact manifest files may be considered for
owner-confirmed deletion; authoritative Study and V2 recovery data are retained.