# P11 Real Migration Completion

Date: 2026-09-30. **P11 Gate: PASS for V1 source migration and V2 cutover.** This supersedes the earlier dry-run BLOCKED checkpoint. It does not certify complete canonical conversation normalization or external platform history unification.

## Scope and representation

`v0.2.0` covers V1 to V2 legacy migration and V2 cutover. Original V1 material is retained as typed source documents and original image Assets. The formal source domain distinguishes `legacy_markdown`, `legacy_wrong_answer_document`, `legacy_derived_fact` and `codex_jsonl` from raw History messages. It preserves exact UTF-8 bytes, stable source identity, measured file hash, deterministic source ordering, proven source time, import time and provenance. Unknown authors, roles and message boundaries remain unknown. Derived facts are not raw messages.

The previous all-platform History preparation is a separate expansion track. ChatGPT/Gemini downloads, Hermes normalization and WorkBuddy source discovery are not prerequisites for migrating material already present in V1. Their registry states remain explicit; none is reported as migrated. The existing raw-message History API still contains zero imported canonical messages. Source documents are retrieved with `list_legacy_sources`, `search_legacy_sources` and `fetch_legacy_source`.

## Actual accounting

| V1 category | found | imported | reused / content deduplicated | archived only | skipped | errors |
|---|---:|---:|---:|---:|---:|---:|
| Study Markdown | 537 | 0 | 537 | 0 | 0 | 0 |
| Study Documents | 511 | 0 | 511 | 0 | 0 | 0 |
| Legacy chat documents | 55 | 55 | 0 | 0 | 0 | 0 |
| Legacy wrong-answer documents | 28 | 28 | 0 | 0 | 0 | 0 |
| Original image Assets | 70 | 66 | 4 | 0 | 0 | 0 |
| Legacy derived fact | 1 | 1 | 0 | 0 | 0 | 0 |
| Other / unsupported | 7 | 0 | 0 | 0 | 7 | 0 |
| **Total V1** | **1,209** | **150** | **1,052** | **0** | **7** | **0** |

Separately, **82 Codex JSONL source documents** were imported from the existing verified immutable snapshot, preserving **322,967,757 bytes**. Together the source store contains **166 documents**: 55 legacy chats, 28 wrong-answer documents, 1 derived fact and 82 Codex source files. These counts are documents, not verified conversations or messages. All 166 sources and all 70 image byte sequences passed hash/size read-back. The Native Memory database is also retained in a verified private source archive, preserving fact metadata beyond the 33-byte typed fact payload.

Same-source reruns produced **0 new source documents / 166 reused**, and **0 new Assets / 70 reused**. Source IDs and Asset URIs stayed identical. Existing import times and provenance were retained. The original four native Assets kept their original provenance; their migration journal time is explicitly checkpoint acquisition time, not a guessed original import time.

### Preserved semantic uncertainty

A final bounded check found **97 explicit document-to-image references**, covering all **70 images**, in the 28 notes. The earlier claim that no note/image references could be proven is superseded. These references identify images named by a document; they do not establish every image's semantic question/answer role or a complete current Wrong Answer record. Only 13 notes have both original-question and student-answer sections, and no note directly satisfies every required analysis field without interpretation.

All 28 notes are therefore preserved as typed source documents, with their 97 exact Asset references. **28 notes remain unresolved for complete Wrong Answer business reconstruction**; this is an additional semantic-coverage dimension, not another item count to add to the accounting table. No artificial question, answer, role, version or analysis was created. The existing active path remains **5 Wrong Answer sources and 5 analyses**, unchanged. Content duplication was not treated as semantic duplication.

This uncertainty does not block the accepted V1 preservation/cutover gate: originals and explicit references are preserved and retrievable, counts and hashes reconcile, and the active V2 Wrong Answer path does not depend on reconstructing these notes. Future reconstruction requires new reliable semantics and the formal wrong-answer workflow.

## Source identity

The Codex registry's `source_hash` is the digest of stable snapshot fields. Its `manifest_hash` is the SHA-256 of original manifest bytes, including capture metadata. They are different identities and must not be compared to each other. Each matches its corresponding existing snapshot evidence; all 82 members were reverified. The original registration and acquisition locator were preserved; no re-registration or new source scan was necessary.

Codex remains source-only. Developer/tool events, attachments, message-ID timestamp conflicts and session/branch metadata have not been normalized into canonical conversation records. Exact raw JSONL bytes remain available through bounded source reads.

## Apply, recovery and privacy

The local internal migration services accept explicit source descriptors and reuse formal domain validation. They are not MCP write tools and provide no arbitrary SQL import. All sources are validated before mutation. History source batches use transactions and read-back before journal checkpoints. Image atomic units are single original Assets, each with its own domain transaction and checkpoint. A failure may leave earlier units committed; deterministic IDs permit a safe retry.

Before real writes, self-contained target DB snapshots were verified, including committed WAL content. The image snapshot also includes every previously registered original blob. Isolated restores reopen through domain readers and verify bytes, types, counts and provenance. Original target sidecars are not opened to make a read snapshot. Database, sidecar and blob aliases through reparse points or hard links are refused. If a target is restored to an older state, a later committed journal is rejected before writes; recovery uses a new run token. Snapshot/journal paths, source locators, private hashes, config backups and receipts remain private.

Study stays **REUSE-IN-PLACE**. Study and Personal root identity, every file's size and modification time were checked before and after migration and rerun. This task did not repeat the earlier 42 GB content scan. All selected migrating sources were hashed again; original Study files were not written. The existing QMD runtime uses disposable copies for retrieval.

Public Git history and the staged release tree were scanned for real user paths, credential patterns, databases, images, PDFs, raw JSONL/archives and local configuration. Only code, synthetic tests and public aggregate documentation are published. Private refs and the prior public tag are preserved.

## Retrieval and Host evidence

Two newly started official MCP stdio clients used the final installed `0.2.0` wheel and this checkout's private configuration. Both reported protocol/Gateway version `0.2.0` and History `sqlite/ready`; all 166 IDs returned matching source type, hash, deterministic source order, nullable original time, distinct import time, unknown author/role, provenance and exact original byte ranges. A literal keyword query returned **52 source documents across 3 source groups** (35 Codex files, 5 legacy chats, 12 wrong-answer documents). Pagination retained deterministic ordering without duplicates. A random no-result query returned zero. All 97 image references were verified. Study retrieval returned 3 results. Reopening the second process proved restart persistence.

This is fresh stdio transport/Gateway evidence. The already-running MCP connection in the initiating Codex chat still holds its earlier `not_configured` configuration and tool list; it must reconnect/reload to discover the new source tools. Its cached health response is not evidence of the new configuration having loaded. Reconnecting clients does not rerun migration.

## Release verification

The final default/dev environment suite passed **605 tests, 12 skipped**. Skips identify Windows symlink/POSIX limitations, opt-in Host/QMD smokes and the non-default PyMuPDF extra; the actual MCP/Study retrieval above was run separately. The source distribution and wheel build passed. Default installation excludes PyMuPDF, and the wheel includes the legacy domain, both apply services and the canonical wrong-answer workflow resource. All 200 members across the two package artifacts passed a private-path/runtime/binary-material audit.

Publication uses a normal fast-forward into `main`, verification on the merged tree, a normal push, an annotated `v0.2.0` tag and the [v0.2.0 GitHub Release](https://github.com/abdullejan25-max/chatgpt-study-system-v2/releases/tag/v0.2.0). Tag and remote commit identity are verified after publication. `v0.1.0` and private refs are not rewritten.

## P11 Gate

| Gate | Status | Evidence / boundary |
|---|---|---|
| Architecture | PASS | Agent intelligence stays external; domain executes validated internal imports |
| Legacy Inventory | PASS | Existing 1,209-item journal reused; bounded final source reconciliation |
| Study | PASS | Original root/files retained in place; actual retrieval |
| History Strategy | PASS | Typed source documents; no invented raw messages |
| History Target | PASS | New private target, fresh MCP `sqlite/ready` |
| History Migration | PASS | 84 V1 source documents persisted and read back |
| Codex History Source Identity | PASS | Correct digest meanings and all 82 member hashes verified |
| Atomic Fact | PASS | 1 typed derived fact, original DB metadata archived |
| Assets/Documents | PASS | 66 new/4 reused image Assets; 511 authoritative documents reused |
| Wrong Answers | PASS | Active business path unchanged; all legacy note/image source artifacts preserved |
| Unresolved Legacy Evidence | PASS | 28 semantic reconstructions unresolved; 97 explicit refs retained; accepted limitation |
| Apply | PASS | Real source and image domain writes with durable checkpoints |
| Transactions | PASS | Source batch transactions and single-image atomic units |
| Idempotency | PASS | Real rerun zero new items, stable IDs/import times |
| Snapshot | PASS | Self-contained DB/WAL and existing original blob backups |
| Restore | PASS | Isolated target reopen and domain byte/provenance verification |
| Provenance | PASS | New records `legacy_import`; original native provenance preserved |
| Privacy | PASS | Private runtime and receipts outside Git; published history/tree audit |
| Real Migration | PASS | 150 V1 new records plus 82 source-only Codex extension documents |
| Count Reconciliation | PASS | 1,209 = 150 imported + 1,052 reused + 7 skipped |
| Hash Validation | PASS | 166 source records and 70 image byte sequences verified |
| Retrieval E2E | PASS | Official fresh stdio calls, cross-source search, no-result guard and Study search |
| Restart Persistence | PASS | Two fresh processes agree on persisted source counts and IDs |
| Cutover | PASS | This project's private configuration selects authoritative V2 stores |
| V1 Retirement | PASS | V1 runtime/code retired for this project; preserved, not deleted |
| Git Hygiene | PASS | Normal public-safe commits/push; no private ref publication |
| Documentation | PASS | Scope, counts, uncertainty, recovery, Host limitation and retirement documented |

Cutover concerns this project's active learning runtime. No V1 project process or scheduled action referencing its old checkout was found in the bounded local runtime check. This does not certify WorkBuddy/Hermes GUI integrations or remove their user-managed settings; those belong to P12. See [V1 deletion candidate report](v1-deletion-candidates.md).

## Conversation sources and next work

| Source | v0.2.0 status | Remaining |
|---|---|---|
| V1 | Migrated source documents, derived fact, original Assets; Study reused | 28 complete Wrong Answer semantic reconstructions remain unresolved |
| Codex | Identity PASS; 82 source-only original JSONL documents | Canonical conversation/message/attachment normalization deferred |
| Hermes | Registered; no history imported in this task | Source and normalization expansion deferred |
| WorkBuddy | Registered installation; no conversations claimed imported | Reliable history source and GUI/client E2E deferred |
| ChatGPT | Registry remains WAITING_FOR_USER | Official export/sign-in verification; later expansion |
| Gemini | Registry remains WAITING_FOR_USER | Official export download verification; later expansion |

P12 preparation is retained without additional product features. The next P12 task is real Obsidian projection/GUI and explicit WorkBuddy/Hermes client integration, after a separate target/client decision. Existing clients first reload their MCP connection. Canonical source normalization and stronger indexed source retrieval are technical debt, not completed features.
