# P12 Step 1 — Obsidian Reality Audit

Checked: 2026-09-27. This audit uses repository contracts and safe host metadata; it does not open a private StudyVault, enumerate learning records, or claim a GUI pass.

| O1 item | Evidence | Status |
|---|---|---|
| Obsidian installation | The read-only host audit recorded Obsidian 1.13.7 from installed-app metadata and executable metadata. | Installed; GUI and target Vault remain unverified. |
| StudyVault structure and `.obsidian` | No target Vault has been confirmed for this projection task. | `WAITING_FOR_USER: OBSIDIAN_VAULT_SELECTION`; no private Vault paths or contents inspected. |
| Study authority | Repository rules keep Study in its authoritative Markdown location; the projection does not copy or rewrite Study files. | Contract confirmed; real Vault navigation not checked. |
| History model | `HistorySource` reports a source ID and item count. `HistoryItem` carries logical/source/conversation IDs, event time, content, and provenance. History search requires a query; item fetch requires a known ID. | Model confirmed; current `health_report` says History is `not_configured`, and `list_history_sources` returns `HISTORY_UNAVAILABLE`. |
| Snapshot/storage boundary | `AppConfig` has an independent optional `history_database`; runtime constructs History and Assets/Document stores separately. Wrong Answers use the document store, while History uses its configured backend. Current read APIs search or fetch known IDs and do not enumerate the full corpus. | No shared cross-store transaction is established. A future exporter must state separate per-store consistency points and reconcile each store's counts; it must not claim a global atomic snapshot without a coordinating mechanism. |
| Wrong Answer model | A source has a logical source ID, source URI, optional page, question/answer text, and creation time. Analyses are versioned and carry an analysis ID, source refs, Study refs, Agent provenance, and write provenance. Sources and analyses are immutable/append-only in the Gateway store. | Contract confirmed from the adapter; no private records read. |
| Asset logical IDs | Assets use `asset://sha256/<64 lowercase hex>`; documents use `document://sha256/<64 lowercase hex>`. | Renderer preserves source references and does not copy bytes. |
| Knowledge relations | `study_relations` are explicit `study:` references from an analysis. A knowledge-point label is a separate Agent-supplied field; it is not proof of a Study link. | Indexes show Agent-reported terms and link back to supplied Wrong Answer pages; no Study graph edges are inferred. |
| Missing facets | The current Wrong Answer DTO has no subject field. The projection input contains no V2 runtime status or unresolved Legacy summary. | Dashboard labels these facets unavailable instead of deriving them. |

## Projection scope

The renderer creates a dashboard, a recent-supplied-source list, History indexes and a cross-conversation timeline, Wrong Answer pages, and Agent-reported Knowledge Point/Error Type indexes. All outputs remain `provided_input_only`. The bounded collector now supplies the complete synthetic DTO snapshot after per-source and per-domain count reconciliation. A separate writer writes an explicit projection into a caller-selected dedicated `V2Projection` directory, uses an ownership manifest for repeatable rebuilds, and refuses unsafe or unowned targets. Collector → renderer → writer was exercised together only with synthetic data; no real Vault has been selected or written, and no generated personal Markdown exists in the repository.

The projection and writer test baselines were 20 renderer tests, 11 writer tests with 1 Windows symlink skip, and 31 combined tests with 1 skip. The Gateway/MCP `projection_snapshot` tool provides bounded per-store History and Wrong Answer pages, independent SQLite high-water tokens, totals, and byte limits. It requires the separate `projection` capability; ordinary `read` does not expose it. The Gateway redacts paths, validates logical source references, and only returns categorical provenance fields needed by the renderer. The collector consumes every page, checks source/token/cursor consistency, reconciles per-source and domain totals, and creates a `ProjectionSnapshot` only after reconciliation. Five synthetic collector tests exercise 21-source page boundaries, a 21-analysis record boundary, mismatch and malformed count rejection, stalled cursor rejection, renderer handoff, and the complete synthetic writer pipeline. That pipeline exposed an overlong nested SHA path on Windows; the renderer now hashes composite History identity into one path segment. Projection/collector/writer tests report **36 passed, 1 skipped**; full suite reports **433 passed, 8 skipped**. The stores do not share a global atomic snapshot. The writer's implementation boundaries and recovery behavior are recorded in the [writer design](superpowers/specs/2026-09-27-obsidian-generated-writer-design.md).

The collector now consumes every page for each source, verifies continuation under the returned per-store token, reconciles per-source record counts against domain totals, and only then builds renderer input. History and Wrong Answer remain separate consistency points; a cross-store atomicity claim is outside the current architecture. Remaining gates require private Host configuration and human Vault/GUI verification.

## Remaining O1 and release gates

- Human confirms the private Vault and reviews the rendered view in Obsidian; synthetic verification does not imply real-store collection.
- Any eventual writer targets a confirmed private/ignored location and supports safe rebuilds.
- Complete O1–O13 validation passes before `v0.3.0`.
