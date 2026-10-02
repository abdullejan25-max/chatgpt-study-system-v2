# V2 Architecture

## Product and development roles

The calling Agent host interprets requests, teaches, plans, and decides which tool to call. ChatGPT remains the intended primary product host; Codex is the developer and integration test host, and P12 Step 2 validates WorkBuddy as another local MCP Host. All use the same host-neutral application contracts.

```text
User → Agent host → transport adapter → Local Gateway → Services/Adapters → Local data
Developer → Codex → stdio MCP adapter → same Local Gateway
```

## Boundaries

P12 Step 4 acceptance uses independent Hermes, WorkBuddy and Codex sessions
against one shared isolated Gateway/store. Cross-Agent shared data does not
mean shared conversation context: later Hosts discover records from a marker
through Gateway search, without inherited object IDs or prior Agent responses.
No second business layer or Host-owned canonical memory is introduced.
Document/source and each analysis preserve Gateway-recorded timestamps and
provenance; Host identity remains caller-reported / unverified. The final
cross-Host acceptance status is tracked in the Step 4 checkpoint, separately
from earlier single-Host acceptance and synthetic SDK regression.

- **Transport** validates and maps protocol requests to gateway operations. The current adapter is stdio MCP; it contains no Study or History business logic.
- **Gateway** validates typed inputs, applies permissions and path allowlists, invokes services, standardizes results, and maps errors.
- **Study adapter** implements a replaceable `StudyBackend`. The initial candidate is QMD search against the fixed `studyvault` collection and an explicitly configured Study root.
- **History adapter** implements a replaceable `HistoryBackend`. Phase 5 adds an explicit private SQLite store for manually registered sources and imported items; it does not access Basic Memory or discover sources.
- **Asset/document adapter** stores explicitly supplied source bytes under an explicitly configured private root and indexes deterministic text pages/chunks in a private SQLite database. Public operations use content-addressed logical URIs, with no filesystem path in metadata.
- **Wrong-answer adapter** links immutable user-provided problem records to existing asset/document URIs and appends versioned client-supplied analyses. It validates schema, provenance references, and Study relations; it does not infer any learning judgment. Its versions explicitly supersede earlier analyses without deleting them.
- **Local data** remains external and protected. StudyVault is the authoritative Study Knowledge Base; the Phase 3 spike is read-only.
- **Phase 11 migration boundary** uses the local-only `study-migrate` CLI for explicit dry-run and validated apply, with private checkpoint journals and verified recovery snapshots. Apply calls domain transactions and is not exposed as an Agent-facing MCP write tool. The journal and its SQLite sidecars are rejected if they overlap the repository, any selected source/target root, or a configured database, and multiply linked journal files are rejected. When inventory must inspect SQLite, it snapshots the selected DB and WAL to temporary local scratch outside every configured source/target path and the repository, verifies source hashes before and after copying, and reads only the scratch copy so SQLite cannot alter a source `-shm` sidecar.

The Agent host is the only intelligence layer: it interprets requests and chooses tools. The V2 Python runtime does not import model-provider clients, run an LLM/VLM, route by user intent, execute arbitrary shell commands, or write ordinary conversations to durable memory. QMD remains an external retrieval adapter with the existing Phase 3 behavior. Phase 5 adds read-only History listing, search, and fetch tools. Phase 6 adds explicit asset/document ingestion, deterministic PDF text-layer extraction, and an optional traditional OCR fallback for pages without extractable text; OCR output is marked as derived and never interpreted by the Gateway. Phase 7 adds explicit wrong-answer source registration and versioned Agent-analysis writes alongside read operations. Analyses are supplied by the calling Agent and never overwrite source records. Phase 9 exposes bounded document-page text and original-asset bytes through standard MCP resource templates as well as the typed tools; both use the same Gateway, capability policy, and local store.

Core modules (`contracts`, `config`, `gateway`, `policy`, `runtime`, and adapters) do not import the MCP SDK or transport package. They operate on Python contracts and can be called directly. `transports/mcp_stdio.py` owns the SDK-specific schemas and error projection. Future transports must call the same Gateway operations and enforce the same policy.

Public `GatewayError` codes are fixed vocabulary, not backend exception text. The MCP adapter maps each to a fixed safe message. Capabilities are explicit local configuration: `read`, `ingest`, `write`, `projection`, and `admin`; an omitted permission section defaults to `read`. MCP discovery hides operations the configured capability set cannot use, while Gateway methods enforce the same boundary even for direct calls. Persistent records have append-only `write_provenance` in the same local SQLite transaction, with runtime UTC time, data origin, logical source refs, version/supersession, import metadata where relevant, and optional caller-reported identity marked unverified. Operation audit remains a separate metadata-only operation/outcome log. Private roots and database paths must be explicitly configured; symlink and Windows reparse-point path components are rejected.

## Replaceable connections

The cross-agent Wrong Answer procedure has exactly one canonical body at `src/chatgpt_study_system/workflows/wrong_answer.md`, shipped as package data and exposed through MCP as `study-workflow://wrong-answer`. Relevant tool descriptions point agents to that resource; a standard user-invoked MCP Prompt exposes the same text for clients that offer prompt menus. Prompt/resource presentation is host-controlled, so the model-controlled tool descriptions also identify workflow applicability. No host-specific Skill is required for correctness, and host-specific adapters must remain pointers rather than copies.

Codex and WorkBuddy local stdio MCP are the verified host integrations. A remote transport or Secure MCP Tunnel is future non-Core work, subject to a separate capability and deployment decision. Neither is a prerequisite for developing or testing Core, and neither is implemented in this phase. No public endpoint or inbound port is part of the current runtime. ChatGPT account capabilities must be verified separately before they become a dependency.

## Memory boundaries

- ChatGPT Memory stores stable preferences and collaboration style.
- Personal History is accessed through `HistoryBackend` and remains unconfigured unless a private SQLite database path is explicitly supplied. Raw imported messages and any future Agent annotations occupy separate data models; History imports preserve source event time separately from runtime import time and do not create an Agent-facing import tool.
- Study Knowledge Base is the StudyVault source accessed through `StudyBackend`.
- Archive is original evidence and is not automatically treated as durable memory.

P11 adds immutable legacy source documents alongside raw History messages. `legacy_markdown`, `legacy_wrong_answer_document`, `legacy_derived_fact` and `codex_jsonl` retain exact UTF-8 bytes, measured hashes, deterministic source ordering, known source time and runtime import provenance. They do not invent message roles, authors, threads or event boundaries. Three read-only Gateway/MCP operations list, search and fetch bounded original source ranges; canonical message tools remain separate. Internal local migration services validate explicit source sets, prove target snapshot/restore, call domain transactions and reconcile durable checkpoints through deterministic retry. Image atomic units are single validated Assets. They are not Agent-facing write tools or arbitrary SQL importers.

See the accepted [ADRs](adr/) for decision context and consequences.

## P13 history completion and recovery (local, not released)

The formal release baseline remains v0.6.0. P13 extends the configured History
store with immutable source evidence and a separate deterministic canonical
derived layer. Adapters map only proven boundaries, roles, ordering and optional
occurrence time. Ambiguous or unsupported inputs remain source-only; normalization
does not use an LLM, replace source bytes or infer attachment files. Stable
identities exclude private paths and migration clocks, and source-specific views
preserve independent export order and conversation branches. Import and
normalization retries reuse evidence, canonical identities and provenance.

The acquired-data verification covers 1,776 sources, 487 canonical conversations,
7,334 distinct messages and 494 source-specific views; 1,323 sources remain wholly
source-only. Native Codex Desktop and Hermes History reads/no-result have passed.
ChatGPT is acquisition_pending for incremental ingestion after its export arrives.
WorkBuddy's P13 History Host acceptance is DEFERRED and nonblocking; its established
P12 integration/cross-agent PASS remains valid. Neither pending acquisition nor
deferred Host acceptance is claimed as a real-data or Host PASS.

Agents perform all V2 reads, counts, existence checks and writes through configured
native Gateway/MCP tools, including recovery targets. Source ingestion and
normalization require explicit read+ingest capabilities; recovery requires the
existing admin capability and trusted private roots. Offline utilities may prepare
selected legacy inputs and their private migration ledger, but cannot replace
Agent Gateway access with direct V2 database or store inspection.

The real V2 backup is PASS_NATIVE: 3,778 files / 44,380,473,111 bytes, supported by
actual native tool traces and positive Agent usage. Snapshot/restore operations
preserve source and canonical identity, provenance, configured Study/Assets data,
and private ledger/configuration evidence. The isolated restore, V1 unique-data
audit and logical retirement remain pending. A restore target is a verification
copy and never a second authoritative data layer. Production writable ingress
will reuse existing Gateway permissions, versioning and provenance; its current
acceptance is pending. Physical V1 deletion requires separate owner confirmation.

Protocol details are documented in [source ingestion](history-source-ingestion.md),
[canonical History](history-normalization.md) and [private recovery](p13-recovery.md).
Actual Gate states live in the [P13 checkpoint](p13-history-completion-checkpoint.md).
Public code, packages and fixtures contain no real sources, transcripts, ledger,
receipts, stores, configuration or backups. The future release upgrade sequence
is backup, frozen/non-editable install, private Gateway version update, then Host
reload and native readback; the current P13 engineering is not a v0.7.0 release.

## Obsidian projection (P12 Step 1)

The existing collector consumes bounded `projection_snapshot` pages from configured Gateway stores. Canonical History, Wrong Answers and immutable imported source documents use independent append-only watermarks, not a cross-store atomic snapshot. The separate `projection` capability controls bulk enumeration; ordinary read does not include it. Legacy source pages contain allowlisted metadata/provenance and logical asset references only. Source documents remain distinct from canonical messages, with unknown role/author/conversation boundaries.

The pure renderer produces deterministic Markdown maps. The writer restricts output to a dedicated manifest-owned `V2Projection`, validates Windows-safe paths, rejects repository overlap and unowned collisions, preserves user notes and rolls back handled failures through hard-link backups. It does not guarantee crash-atomic directory replacement. The explicit build entrypoint loads the official private config, requires an existing Vault containing the authoritative Study root, refuses Study/output overlap and reparse points, indexes original Study through relative links, and verifies read-back plus a second fresh collection/rebuild. Private output and raw assets/documents never enter Git or release packages.

Real integration, Windows/Unicode and owner GUI acceptance are recorded in [P12 Step 1](p12-step1-real-projection-checkpoint.md). Metadata-only source views and independent store consistency points are deliberate limitations. WorkBuddy and Hermes integrations are recorded below; real Cross-Agent acceptance is recorded in Step 4. Canonical normalization is now validated in the separate P13 History layer; this does not assert refreshed Projection coverage. Physical deletion and incremental projection remain deferred.

## Hermes integration (P12 Step 3, v0.5.0)

Hermes uses the native standard MCP stdio client without a business adapter.
Production `study_system` exposes read capability; the differently named isolated
server owns independent synthetic test stores and a separate Projection Vault.
Reads, counts, existence checks and writes all use Gateway operations. Tool-search
schema/call bridges are Host protocol mechanisms, not a second data layer.

Hermes built-in Memory and user profile persistence are disabled for the configured
home. Product session/runtime metadata remains permitted, but cannot replace V2
retrieval or become authoritative Study, History or Wrong Answers. Caller identity
is reported/unverified. Actual CLI Host process exit/restart preserves the formal
Gateway DTO identities, timestamps, provenance and version graph. Existing scoped
collector, renderer and manifest-owned writer project isolated Hermes records;
the Projection is derived and provenance is its established privacy summary.

## WorkBuddy integration (P12 Step 2, v0.4.0)

WorkBuddy performs V2 reads, counts, existence checks and writes through the
same Gateway. The project rule points to canonical tools/workflow; it contains
no domain implementation. Caller identity remains reported/unverified.
At the P12 Step 2 boundary, Basic Memory was disabled without deletion or history
migration; later P13 source acquisition remains a separate migration operation.
An independent temporary `study_system_p12_isolated` entry avoids relying on unresolved
Desktop 5.6.2 same-name configuration precedence; the managed production
entry is preserved. Real Host evidence and its limits are recorded in the
[Step 2 checkpoint](p12-step2-workbuddy-checkpoint.md).

An explicit `collect_wrong_answer_projection` entry reuses permission-controlled
Gateway snapshot paging and completeness checks for isolated targets without
History. Omitted domains are outside the supplied input scope, not asserted
empty. The default three-domain collector remains unchanged and still reports
unavailable backends. Rendering and writing use the existing deterministic,
manifest-owned pipeline; output stays outside the repository, with logical
references only and no invented Study links or original Asset bytes.
