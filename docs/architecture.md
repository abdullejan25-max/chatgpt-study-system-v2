# V2 Architecture

## Product and development roles

In the finished product, ChatGPT is the primary user host and the only system that interprets requests, teaches, plans, and decides which tool to call. During development, Codex is the developer agent and MCP integration test host. This distinction does not change the host-neutral application contracts.

```text
User → Agent host → transport adapter → Local Gateway → Services/Adapters → Local data
Developer → Codex → stdio MCP adapter → same Local Gateway
```

## Boundaries

- **Transport** validates and maps protocol requests to gateway operations. The current adapter is stdio MCP; it contains no Study or History business logic.
- **Gateway** validates typed inputs, applies permissions and path allowlists, invokes services, standardizes results, and maps errors.
- **Study adapter** implements a replaceable `StudyBackend`. The initial candidate is QMD search against the fixed `studyvault` collection and an explicitly configured Study root.
- **History adapter** implements a replaceable `HistoryBackend`. Phase 5 adds an explicit private SQLite store for manually registered sources and imported items; it does not access Basic Memory or discover sources.
- **Asset/document adapter** stores explicitly supplied source bytes under an explicitly configured private root and indexes deterministic text pages/chunks in a private SQLite database. Public operations use content-addressed logical URIs, with no filesystem path in metadata.
- **Wrong-answer adapter** links immutable user-provided problem records to existing asset/document URIs and appends versioned client-supplied analyses. It validates schema, provenance references, and Study relations; it does not infer any learning judgment. Its versions explicitly supersede earlier analyses without deleting them.
- **Local data** remains external and protected. StudyVault is the authoritative Study Knowledge Base; the Phase 3 spike is read-only.
- **Phase 11 migration boundary** is a local-only `study-migrate dry-run` CLI with a private checkpoint journal; it has no business-data apply mode and is not exposed as an Agent-facing MCP write tool. The journal and its SQLite sidecars are rejected if they overlap the repository, any selected source/target root, or a configured database, and multiply linked journal files are rejected. When inventory must inspect SQLite, it snapshots the selected DB and WAL to temporary local scratch outside every configured source/target path and the repository, verifies source hashes before and after copying, and reads only the scratch copy so SQLite cannot alter a source `-shm` sidecar.

The Agent host is the only intelligence layer: it interprets requests and chooses tools. The V2 Python runtime does not import model-provider clients, run an LLM/VLM, route by user intent, execute arbitrary shell commands, or write ordinary conversations to durable memory. QMD remains an external retrieval adapter with the existing Phase 3 behavior. Phase 5 adds read-only History listing, search, and fetch tools. Phase 6 adds explicit asset/document ingestion, deterministic PDF text-layer extraction, and an optional traditional OCR fallback for pages without extractable text; OCR output is marked as derived and never interpreted by the Gateway. Phase 7 adds explicit wrong-answer source registration and versioned Agent-analysis writes alongside read operations. Analyses are supplied by the calling Agent and never overwrite source records. Phase 9 exposes bounded document-page text and original-asset bytes through standard MCP resource templates as well as the typed tools; both use the same Gateway, capability policy, and local store.

Core modules (`contracts`, `config`, `gateway`, `policy`, `runtime`, and adapters) do not import the MCP SDK or transport package. They operate on Python contracts and can be called directly. `transports/mcp_stdio.py` owns the SDK-specific schemas and error projection. Future transports must call the same Gateway operations and enforce the same policy.

Public `GatewayError` codes are fixed vocabulary, not backend exception text. The MCP adapter maps each to a fixed safe message. Capabilities are explicit local configuration: `read`, `ingest`, `write`, and `admin`; an omitted permission section defaults to `read`. MCP discovery hides operations the configured capability set cannot use, while Gateway methods enforce the same boundary even for direct calls. Persistent records have append-only `write_provenance` in the same local SQLite transaction, with runtime UTC time, data origin, logical source refs, version/supersession, import metadata where relevant, and optional caller-reported identity marked unverified. Operation audit remains a separate metadata-only operation/outcome log. Private roots and database paths must be explicitly configured; symlink and Windows reparse-point path components are rejected.

## Replaceable connections

The cross-agent Wrong Answer procedure has exactly one canonical body at `src/chatgpt_study_system/workflows/wrong_answer.md`, shipped as package data and exposed through MCP as `study-workflow://wrong-answer`. Relevant tool descriptions point agents to that resource; a standard user-invoked MCP Prompt exposes the same text for clients that offer prompt menus. Prompt/resource presentation is host-controlled, so the model-controlled tool descriptions also identify workflow applicability. No host-specific Skill is required for correctness, and host-specific adapters must remain pointers rather than copies.

Codex local stdio MCP is the current host integration. A remote transport or Secure MCP Tunnel is future non-Core work, subject to a separate capability and deployment decision. Neither is a prerequisite for developing or testing Core, and neither is implemented in this phase. No public endpoint or inbound port is part of the current runtime. ChatGPT account capabilities must be verified separately before they become a dependency.

## Memory boundaries

- ChatGPT Memory stores stable preferences and collaboration style.
- Personal History is accessed through `HistoryBackend` and remains unconfigured unless a private SQLite database path is explicitly supplied. Raw imported messages and any future Agent annotations occupy separate data models; History imports preserve source event time separately from runtime import time and do not create an Agent-facing import tool.
- Study Knowledge Base is the StudyVault source accessed through `StudyBackend`.
- Archive is original evidence and is not automatically treated as durable memory.

See the accepted [ADRs](adr/) for decision context and consequences.
