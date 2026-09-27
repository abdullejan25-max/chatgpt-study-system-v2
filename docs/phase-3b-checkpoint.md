# Phase 3B Checkpoint — Disposable Runtime Synthetic Smoke Complete

## Status

The `disposable runtime synthetic smoke` node is complete and **PASS**. A real
QMD 2.8.3 `update` and `search` process was run with synthetic data only. No
protected StudyVault, real QMD configuration or index, Basic Memory, V1, or
WorkBuddy data was read, changed, or copied.

The smoke used the fixed native `node.exe` and audited
`dist/cli/qmd.js`, with `shell=False`, an isolated disposable `cwd`, and
runtime-contained QMD state paths. Windows native Node additionally required
the OS `SYSTEMROOT` bootstrap variable; this is process startup metadata, not
a QMD data/cache path.

## Completed

- Read the Phase 3 report and checkpoint. Phase 3 remains `PARTIAL`; its
  synthetic MCP tests had already passed (`109 passed, 1 skipped`).
- Inspected the installed QMD 2.8.3 package and Windows launchers without
  executing QMD.
- Confirmed the package binding evidence:
  - package: `@tobilu/qmd`, version `2.8.3` in its installed `package.json`;
  - installed npm launchers are `qmd.cmd` and `qmd.ps1`, so they remain
    rejected by the V2 adapter;
  - the audited JavaScript entrypoint is
    `dist/cli/qmd.js`, runnable directly by a fixed native `node.exe` without
    invoking an npm shell launcher.
- Confirmed parser evidence from `dist/cli/qmd.js`: it uses
  `process.argv.slice(2)` and `util.parseArgs`; the real smoke retained the
  `--` separator before the user query.
- Traced the QMD `search` path. It opens the SQLite store read-write,
  enables WAL, initializes/migrates tables, and synchronizes configuration.
  Direct search against the protected index is therefore unsafe.
- Traced the source-content search path: ordinary JSON `search` reads indexed
  `content.doc`; the reviewed path does not write StudyVault Markdown. The
  future smoke must not use `--full-path`, which can stat source files.
- Identified runtime controls in the installed package:
  - `INDEX_PATH` for the SQLite index;
  - `QMD_CONFIG_DIR` (before `XDG_CONFIG_HOME`) for configuration;
  - `XDG_CACHE_HOME`, `HOME`, and `USERPROFILE` for cache/model/default-home
    locations;
  - an isolated `cwd` is required because an ancestor `.qmd/index.yaml` or
    `.yml` can override the expected local-config/index selection.
- Identified a snapshot constraint: a live WAL database must not be copied as
  only `index.sqlite`; a later real-data smoke needs a consistent SQLite
  backup or a verified quiescent DB plus WAL/SHM snapshot.
- Added `QmdRuntime` to the QMD adapter. It validates a native `node.exe`, the
  package's `dist/cli/qmd.js` relationship, package name/version `2.8.3`, an
  isolated working directory, and runtime-contained index/config/cache/home
  paths. It builds the fixed Node-plus-CLI argv and an allowlisted environment
  containing `INDEX_PATH`, `QMD_CONFIG_DIR`, `XDG_CACHE_HOME`, `HOME`, and
  `USERPROFILE`.
- The runtime path has no executable resolution and refuses script launchers;
  execution remains `shell=False`. User query text is appended only after `--`.
- Added synthetic tests for runtime path escape, script/unreviewed launcher
  rejection, environment isolation, fixed executable/CLI argv, and option-like
  queries. The Windows native Node path now also passes the required OS
  `SYSTEMROOT` bootstrap variable.
- Static audit of QMD 2.8.3 confirmed that this `update` path does not call
  model download, network, or custom hook code when the synthetic config has
  no `update` hook or custom model.
- Added `tests/test_qmd_runtime_smoke.py`, which creates a disposable root,
  synthetic Markdown, synthetic `index.yml`, runtime manifest, and an external
  sentinel manifest. It runs one real `update` and one real `search`.
- The option-looking query `--all` was passed after the real `--` separator;
  QMD returned valid JSON `[]` with exit code 0. The test also asserts the
  exact argv tail `--`, `--all`.
- The external sentinel file list, SHA-256 values, and mtimes were identical
  before and after the smoke.
- The runtime manifest delta recorded exactly:
  - created: `index/index.sqlite`;
  - modified: `config/index.yml` (QMD added its default `models` metadata);
  - removed: none; no cache, WAL, or SHM files remained after process shutdown.

## Real QMD Smoke Gate (completed after this checkpoint)

- Added a SQLite `backup`-API snapshot helper. It opens the source index with
  `mode=ro` and writes only a new database in the disposable runtime. This
  preserves committed WAL content; copying `index.sqlite` alone would not.
- Added a real-data smoke test that is opt-in through local environment
  variables only. It copies the real QMD config and snapshots the real derived
  index into `pytest` temporary state, then performs one fixed R0 search using
  the audited native Node plus QMD 2.8.3 JavaScript entrypoint.
- The real smoke passed on 2026-09-25. It compared full SHA-256, size, and
  mtime manifests of the configured StudyVault before and after the search.
  All StudyVault and original QMD-config entries were identical.
- The original `index.sqlite` and its WAL contents/sizes remained identical.
  SQLite's read-only WAL reader refreshed the source `index.sqlite-shm` mtime
  while preserving its hash and size. This is a controlled, documented
  side-effect on a rebuildable derived index, not an authority-data write.
- The first real smoke exposed a Windows-only adapter defect: `subprocess`
  defaulted to GBK while QMD emits UTF-8 JSON. The adapter now explicitly uses
  strict UTF-8 decoding, covered by a synthetic regression assertion. The
  final real smoke passed with this fix.

## In Progress

Codex MCP Host E2E is the remaining Phase 3 gate. The current composition root
still uses the deliberately rejected PATH launcher, so it must be extended to
create the same disposable QMD runtime lazily for `search_study`. This must not
affect the pure, zero-write `health_report` operation.

## Not Started

- Configure project-level Codex MCP and run host E2E for `health_report` and
  `search_study`.
- Update `docs/phase-3-report.md` from `PARTIAL` only if all required gates
  pass.

## Current Blocking Point

The direct protected-index route remains rejected: QMD `search` is not
physically read-only. The real smoke passed only because the QMD config/index,
cache, home, and working directory were confined to disposable state. The next
gate is project-level Codex MCP Host E2E after composition uses that same
runtime factory.

## Evidence Locations

- QMD 2.8.3 is installed outside the repository; its machine-specific installation path is redacted.
- `...\\bin\\qmd` and the npm `qmd.cmd` / `qmd.ps1` shims (launcher chain)
- `...\\dist\\cli\\qmd.js` (argument parser, search dispatch, store setup,
  local-config selection)
- `...\\dist\\store.js` and `...\\dist\\db.js` (SQLite initialization, WAL,
  config synchronization, indexed-content lookup)
- `...\\dist\\collections.js`, `...\\dist\\paths.js`, and
  `...\\dist\\llm.js` (runtime path resolution and lazy model loading)
- `tests/test_qmd_runtime_smoke.py` (real synthetic disposable-runtime smoke)

## Git State at Checkpoint

- Branch: `phase-3-readonly-mcp-spike`
- This checkpoint includes the minimal runtime implementation, the Windows
  native Node bootstrap fix, and the synthetic disposable-runtime smoke test.
- The small implementation/documentation commit for this task is the last
  action; no later Roadmap node is included.
