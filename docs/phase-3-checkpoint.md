# Phase 3 Checkpoint

## Scope

This checkpoint tracks implementation of the read-only MCP spike. Repository bootstrap, the pure application layer, the synthetic QMD adapter, and stdio MCP protocol integration with synthetic data are complete. Real QMD and Codex host E2E remain separate gates.

## Completed

- Created the new V2 repository on local branch `main` with no remote.
- Added privacy rules, example configuration, architecture notes, fixture rules, and the six accepted ADRs.
- Fixed a P1 privacy issue: the initial recursive fixture exception (`!tests/fixtures/**`) could override sensitive ignore rules inside the fixture tree. The current rules keep ordinary synthetic fixtures trackable while sensitive file and directory patterns remain effective everywhere, including under `tests/fixtures/`.
- Verified with `git check-ignore --no-index`: `tests/fixtures/synthetic.md` and `tests/fixtures/synthetic.json` are not ignored; `tests/fixtures/.env`, `tests/fixtures/config.local.toml`, `tests/fixtures/memory.db`, `tests/fixtures/private.pdf`, and `tests/fixtures/var/secret.txt` are ignored.
- Created the Phase 3 implementation branch after the bootstrap commit.
- Added the Python 3.11+ project, locked minimal declared dependencies, and created an ignored Python 3.12 `.venv` with `uv`.
- Implemented typed backend contracts, explicit configuration, canonical Study path containment, `NotConfiguredHistoryBackend`, and the read-only Gateway operations `health_report` and `search_study`.
- The Gateway derives safe relative source IDs, bounds and cleans result text, maps stable errors without exposing backend details, and adds a correlation ID to internal errors. No QMD or MCP adapter is part of this commit.
- Added `QmdStudyBackend` behind `StudyBackend`. It requires an explicit local assertion of QMD 2.8.3, builds one fixed `search --format json --collection studyvault` argv with `--` before the query, runs with `shell=False`, timeout, fixed Study-root cwd and an allowlisted environment, then validates every QMD URI against the canonical Study root. It refuses unresolved paths and Windows `.cmd`/`.bat`/`.ps1` launchers before spawning. The assertion does not verify the installed binary or bind it to an audited launcher.
- Added official MCP SDK 1.30.0 stdio transport with exactly `health_report` and `search_study`. It calls Gateway methods only, rejects extra tool arguments, and returns structured `{ok: true, ...}` or safe `{ok: false, error: {code, message, correlation_id?}}` responses. The transport has no QMD/subprocess implementation.
- Added a small composition root that reads only an explicitly provided local TOML path and constructs `Gateway` with `QmdStudyBackend` and `NotConfiguredHistoryBackend`; it creates no config, database, cache, or state. The stdio entrypoint requires `--config` and exposes no HTTP service.

## Tests and data safety

- Application tests: 49 passed, 1 skipped on Windows (physical symlink creation requires unavailable privilege). A separate non-skipped deterministic resolved symlink/junction escape test passed.
- TDD RED: three test modules initially failed collection because `chatgpt_study_system` did not exist; after implementation, targeted tests exposed NUL result text and malicious backend diagnostic/name leaks before those were fixed. GREEN: `.venv/Scripts/python.exe -m pytest -q` yielded 29 passed, 1 skipped.
- Review fix RED: targeted tests showed 9 failures for raw health probe exceptions, embedded/root-relative local paths, huge numeric score mapping, and missing top-level `backend`/`truncated`. A second focused RED showed 3 failures for slash-rooted paths and an ordinary HTTPS URL. GREEN: the full suite yielded 48 passed, 1 skipped. QMD discovery failure now reports `discoverable: false`; History probe failure raises sanitized `INTERNAL_ERROR` with a correlation ID.
- History health projection RED: a nonthrowing hostile backend returned path/token text in `backend` and `status`, and the public report exposed it. GREEN: only the exact Phase 3 `not_configured` pair is preserved; all other returned metadata becomes `unavailable`. The full suite yielded 49 passed, 1 skipped.
- QMD adapter TDD RED: after minimal import scaffolding, all 32 synthetic cases failed on absent command/error/path behavior. A second focused RED showed 3 failures for unsafe Windows script launchers. GREEN: adapter tests yielded 37 passed; full suite yielded 86 passed, 1 skipped. All QMD runner calls in these tests used an injected fake; no installed QMD was executed.
- QMD review fix RED: 9 focused failures exposed missing `--` query termination and rejection of absent/null snippets. GREEN: 49 adapter tests and the full suite of 98 passed, 1 skipped. The `.ps1` launcher rejection is also now covered by an explicit test.
- MCP TDD RED: 7 focused tests failed on the missing server/composition functions. GREEN: 8 synthetic in-memory MCP protocol tests passed after implementation. A second RED showed 2 unsafe local-config cases accepted; after validation of public version and absolute Study root, the focused suite passed 10 tests. The full suite passed **108 tests, 1 skipped**.
- MCP protocol tests verify the exact two-tool inventory and strict search input fields; success preserves Gateway health and safe source fields, and errors do not echo private input, backend diagnostics, or unsafe correlation IDs. An in-memory test forbids application socket binds after the Windows asyncio loop starts. Windows asyncio itself uses a transient socketpair during event-loop initialization; this is not an MCP listener. No QMD process or real data was used.
- MCP schema review fix RED: the advertised `search_study.query` JSON Schema accepted empty, 501-character, and NUL-containing strings. GREEN: the schema now advertises `minLength: 1`, `maxLength: 500`, and a NUL-excluding pattern, while runtime validation still checks trimmed length and NUL. Focused MCP tests: 11 passed; full suite: **109 passed, 1 skipped**.
- `health_report` uses a synthetic tree snapshot (hash, mtime, file/directory inventory), blocks subprocess calls, and confirms no DB/log/cache or absolute root path appears.
- Real-data QMD smoke: not run. Read-only package discovery found the PATH entry is `qmd.cmd`/`.ps1` while the native `node.exe` and QMD JavaScript CLI are separate. The adapter deliberately rejects these script launchers; its synthetic `2.8.3` configuration assertion does not verify the installed CLI. A fixed, audited Node+CLI launcher/version binding and confirmation of `--` parser behavior are needed before any real smoke. Earlier read-only review also identified potential SQLite index writes during QMD search, so the index side-effect risk must be resolved before touching it.
- Codex MCP E2E: not run.
- StudyVault, QMD index, Basic Memory, archives, and V1: not accessed or modified by this implementation milestone.

## Current Git state

Bootstrap commit: `e04888ebfb58bd53730f34f265feb354ef0342fc` (`chore: initialize privacy-safe v2 repository`).
P1 fixture privacy correction: `c7b2342e38e57c0c051ec9532007d06c5b1a3f96` (`fix: keep sensitive fixture files ignored`).
The implementation branch is `phase-3-readonly-mcp-spike`.
Application-layer commit: `3ae858761e8beb660b0bd544d1bf94054ba86472` (`feat: implement gateway contracts and read-only policy`).
Review fix commit: `fb18a3cf4b355377f5548d88a92902bfe0d92c26` (`fix: sanitize gateway probes and result metadata`).
Slash-rooted path fix commit: `b9696b53ba7d8fc2e45f7fdd6f9ff40e2b8895ce` (`fix: detect slash-rooted study result paths`).
History health projection commit: `17a56016744c143fb0e7031cbb7d4420ac3425d7` (`fix: constrain public history health fields`).
QMD adapter commit: `651915aca09e9016421057fc5e73b02b2d216726` (`feat: add qmd study backend`).
QMD review fix commit: `4e88cac` (`fix: keep qmd queries positional and accept empty snippets`).
Stdio MCP transport commit: `9cf9f240a85a5ba3cd0f57f7ff652fdbe92d4c9c` (`feat: add stdio mcp transport`).
MCP query schema review fix commit: `dc1c6b4266df1a1350f66d8af498a5383bf0f908` (`fix: constrain mcp study query schema`).
Phase 3 partial report: `b7449a7b1c8d24a0736f8b25c0e9ce2734473e68` (`docs: add phase 3 partial report`).
Resolved dependencies include `mcp==1.30.0` and `pytest==9.1.1`; `.venv` is Git-ignored. No Git remote is configured.

## Remaining

- Decide on an audited fixed native Node+QMD CLI launcher/version binding, verify its `--` query separator, and establish a strictly read-only index strategy before any real-data QMD smoke test; current adapter safely rejects the discovered `.cmd`/`.ps1` PATH launchers.
- After the real-data gate is satisfied, configure the server as a Codex project-level MCP tool and verify `health_report` and `search_study` from the host. No Codex MCP configuration or E2E call has been made yet.
- Update this checkpoint after each meaningful implementation milestone.
