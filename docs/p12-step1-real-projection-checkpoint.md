# P12 Step 1 real projection checkpoint

Checked: 2026-10-01. Target release: `v0.3.0 — Obsidian Visualization`.
Step 1 Gate: **PASS**. The owner completed human GUI validation on 2026-10-01 and explicitly authorized version updates, full verification, privacy/package audits and release. Package and Gateway target version is `0.3.0`. P11 remains PASS.

## Recovered baseline and implementation

The clean live checkout started on `main`, at `41a821c`, also tagged `v0.2.0`, with the same locally recorded remote main. The connected Host reports Gateway `0.2.0`, `health_report.ok=true`, Study configured/readable and History `sqlite/ready`. This task does not resume scheduled work or rerun migration.

The existing collector, pure renderer and manifest-owned writer are reused. `projection_snapshot` adds a `legacy_sources` domain under the existing opt-in `projection` permission. It enumerates bounded, metadata-only pages at an append-only SQLite row watermark, reconciles counts and rejects duplicate logical source IDs. History messages, Wrong Answers and imported source documents retain separate consistency points; this is not a global atomic snapshot. No database business-model or migration changes are made.

Source pages display source ID, logical record ID, source type/order, known source time, import time, byte count, categorical provenance and explicit asset refs. Original source time keeps its known timezone offset. Author, role and conversation boundary are explicitly unknown. Source text, raw hashes, source locators, caller identities and import batch IDs are not projected. Original content remains available through `fetch_legacy_source`; these pages are metadata views, not copies of chat archives or normalized message streams.

The existing registered StudyVault is reused; generated files are confined to its `V2Projection` subtree. The authoritative Study root already belongs to that Vault. Its Markdown files are indexed through percent-encoded relative links, without copying or rewriting their content. Study and generated output must be disjoint before any write. The build command refuses an unregistered-looking Vault without `.obsidian`, unsafe reparse points, Study outside the selected Vault, and output overlapping Study. The existing writer continues to reject repository overlap, unsafe filenames and unowned destination collisions. User notes outside its manifest are preserved. Handled writer failures roll back through the existing hard-link recovery mechanism; abrupt process/power failure is not crash-atomic.

Explicit local build entrypoint:

```powershell
$env:PYTHONPATH = Join-Path (Get-Location) 'src'
uv run --no-sync python -m chatgpt_study_system.obsidian_build --config config.local.toml --vault <existing-private-vault>
```

Enable `projection` in the official ignored private config. This task enabled it there; it did not create a temporary MCP override. The command loads the configured Gateway, collects, renders, writes, reads every generated file back, recollects and rebuilds, checks relative links and compares all generated-file/manifest hashes. CLI output contains aggregate checks only; failure output omits private paths and content.

## Real evidence

- Imported source documents: **166**; `codex-source=82`, `v1-legacy=55`, `v1-wrong=28`, `v1-fact=1`. Unique logical IDs reconcile with the advertised total. They are not conversation/message counts.
- Canonical History messages: **0**. Active Wrong Answer sources/analyses: **5 / 5**. No legacy Wrong Answer semantic relation is invented.
- Explicit legacy image references: **97 occurrences / 70 unique logical Asset URIs**, independently checked through fresh official MCP pagination.
- Generated Markdown files: **184**, plus one ownership manifest. Views include Dashboard, four Source categories, canonical History, Wrong Answers, Agent-reported Knowledge Points/Error Types, Study index and logical Asset/Document references.
- Every generated file was read back as exact UTF-8 bytes. A second fresh Gateway collection/rebuild was byte-identical, including the manifest. No randomized IDs or duplicate pages appeared. All emitted Markdown relative links resolved to existing files within the selected Vault.
- The current explicitly configured Study root contains **1,146 files / 564 Markdown files**. This is the current index scope, distinct from the earlier migration selection counts. Every Study file's size and nanosecond mtime remained unchanged across the build. This check does not claim a new full-content hash audit of all Study documents.
- Windows real-Vault validation covered Chinese Study titles, Unicode links, encoded filenames, two builds and filesystem read-back. Maximum generated absolute path length: **142 characters**. Generated source filenames use stable hashes. The projection absolute-path scan passed; private data/config/Vault remain outside tracked output.
- Obsidian installation and opened GUI identify **1.13.7**. The existing Vault and generated Dashboard opened; accessibility text reports 166 source documents, 0 canonical messages and 5 Wrong Answers. Two native screenshot requests timed out, so visual readability and actual GUI link navigation are not accepted from filesystem/accessibility evidence alone.
- Relevant collector/renderer/writer/build/legacy-source/official-stdio test modules: **94 passed, 1 skipped**. The skip is the existing Windows symlink limitation. Regression tests cover source pagination across 20 records, original timezone offsets, watermark exclusion of later imports, Study/output overlap refusal, user-note preservation, manifest count limits and CLI recovery flags without private logs. The historical full suite has not been rerun before the GUI gate.

## Minimal MCP compatibility decision

The new Codex Host session loads the server and exposes its tools. Its `resources/list` still returns `Unexpected response type`; canonical `resources/read` and `health_report` work. Host initialize/tools discovery are evidenced by the loaded server/tools, not by a raw Host initialization trace.

One fresh official MCP SDK stdio client successfully performed initialize, resources/list, canonical workflow resources/read and tools/list against the official private config, reporting version `0.2.0`. Another fresh client verified the enabled projection tool and all 166 source records. This follows user rule A: record a Host/session compatibility issue, stop investigation and continue projection. No compatibility fix/commit was made. Host resources/list remains independent technical debt.

## Gate

| Item | Status | Evidence / boundary |
|---|---|---|
| Architecture | PASS | Existing Gateway → collector → renderer → writer; no second projection or intelligence layer |
| Real Gateway Input | PASS | Official private config, real collection and fresh MCP enumeration |
| Source Projection | PASS | 166 unique metadata pages, four explicit categories |
| History Source Semantics | PASS | 0 canonical messages; no invented roles or conversation boundaries |
| Study Boundary | PASS | Existing authority, references only, disjointness preflight and unchanged size/mtime |
| Renderer | PASS | Existing renderer extended with validated deterministic source metadata |
| Collector | PASS | Bounded pagination, independent watermarks and count/ID reconciliation |
| Writer | PASS | Existing validated writer reused; handled-failure recovery retained |
| Manifest Ownership | PASS | Manifest/file map reconciled; unknown user notes preserved by tests |
| Deterministic Rebuild | PASS | Independent recollection and exact file/manifest hashes |
| Idempotency | PASS | Repeated builds retain byte-identical generated outputs |
| Privacy | PASS | No source text/absolute paths in public changes; private output scanned |
| Windows/Unicode | PASS | Real Windows filesystem, Chinese titles, encoded links, bounded paths |
| Asset/Document References | PASS | Logical refs retained; original bytes not copied |
| Real Vault | PASS | Existing registered Vault, 184 generated files read back |
| GUI Validation | PASS | Owner confirmation on 2026-10-01: navigation, graph, Unicode, boundaries and original Study all normal |
| MCP Compatibility | PASS | Fresh official client passes; Host resources/list deferred under rule A |

## Human GUI acceptance and release authorization

In the existing StudyVault, open `V2Projection/Dashboard.md` in reading mode. Follow Sources → Legacy Chat Sources and a source page; also inspect Codex Sources (82), Legacy Wrong Answer Sources (28), and Derived Facts (1). Confirm known metadata/provenance and unknown author/role rather than fictitious messages. Return to Dashboard and follow Wrong Answers into one page, then Knowledge Points and Error Types and their backlinks. Follow Study references into an original Chinese-title Study note. Check generated boundaries, readable Unicode, no broken paths, duplicate pages or exposed absolute paths. Source and Asset/Document logical URIs are identifiers, not promised native Obsidian hyperlinks.

The owner confirmed Dashboard, Sources, Wrong Answers, Knowledge Points, Error Types, Study links and the relationship graph. V1/V2 views coexist in the existing Vault with clear source/generated boundaries; no garbled text, obvious broken links, duplicates, private absolute paths or Study anomalies were observed. This human acceptance closes the GUI gate despite the earlier automation screenshot timeouts. Release verification is recorded in [v0.3.0 release notes](releases/v0.3.0.md).

Remaining limitations: Host resources/list compatibility; no crash-atomic writer guarantee; metadata-only source views; independent store consistency points. Deferred scope remains source/message normalization, external agents/imports, V1 deletion and incremental projection redesign.

## Final release verification (2026-10-01)

The default/dev full suite passed **614 tests, 12 skipped**. Skips cover existing platform/symlink, opt-in Host/QMD and optional PDF/OCR conditions; actual fresh official MCP and real-Vault checks were run separately. Wheel and source distribution build passed. Package audits confirm version `0.3.0`, Apache-2.0 license metadata/LICENSE, canonical workflow data and optional-only PyMuPDF; no private config, Vault, images, databases or raw exports are included. The public tree and new Git objects are audited before push. Real 0.3.0 Gateway health and stable 166-source/184-file projection were revalidated after installation.
