# Phase 9 Checkpoint — Agent Interoperability

## Implemented

- The same stdio MCP server and configured Gateway serve Codex and independent MCP clients; there is no Host-specific Core or copied business logic.
- Standard MCP resource templates provide bounded document-page text with page/text-origin metadata and original asset bytes up to 64 KiB. Larger assets remain available through the existing bounded range-fetch tool. Resource reads obey the Gateway `read` capability and return fixed safe errors.
- Page, rendered-image, and original-asset resources include the same append-only write provenance exposed by typed Gateway reads. Optional write identity fields are explicitly caller-reported and never treated as authenticated.
- An independent official MCP SDK client starts the actual server as a subprocess over stdio. With disposable synthetic History and Asset/Document databases, it exercises tool discovery/schema validation, health, History search, document ingestion, document search, page resource retrieval, and a denied wrong-answer write.
- An opt-in real Codex CLI Host test uses read-only sandboxing, `--ephemeral`, `--ignore-user-config`, a transient inline MCP server config, and synthetic History only. It invokes `health_report` and `search_history` through the same stdio server and verifies tool-call events and returned synthetic provenance. It validates MCP Host interoperability, not project-config bootstrap, ordinary new-task setup, write capabilities, or the Wrong Answer save flow. The CLI runs under the host's existing authentication context; test code does not read or copy credential values.

## Tests and host evidence

- Independent stdio process E2E: `1 passed`.
- MCP resource templates, binary/text retrieval, size cap, missing-resource error, disabled-read boundary, unexpected-error sanitization, and truncation provenance: `2 passed`.
- Historical real Codex CLI Host E2E: `1 passed` with `CODEX_HOST_E2E=1`; the installed CLI reported `0.155.0-alpha.16.4` during that run. This was the inline-override, read-only synthetic smoke described above, not normal project bootstrap.
- Full regression after the Phase 6 PDF follow-up: `251 passed, 5 skipped` with `uv run --extra dev pytest -q -rs -p no:cacheprovider`.
- Skips: Codex Host smoke is opt-in (`CODEX_HOST_E2E=1`), this host cannot create NTFS junctions, this host does not permit symlink creation, the protected real-QMD smoke requires explicit `QMD_REAL_SMOKE_*` settings, and the real QMD runtime smoke requires explicit `QMD_SMOKE_NODE_EXE` / `QMD_SMOKE_CLI_ENTRYPOINT` settings.
- Phase 3 `health_report` and `search_study` Codex Host evidence remains recorded in `docs/phase-3-report.md`; this Phase 9 smoke additionally verifies the current server contract and History path without accessing StudyVault.
- ChatGPT remote MCP / Secure MCP Tunnel remains deferred as an external capability and is not a Phase 9 gate.
- Codex project startup uses `.codex/config.toml`; Codex loads that project layer only after the user trusts the project. See `docs/codex-host-setup.md` for the one-time host prerequisites.
- A later rerun of the opt-in smoke on this Host failed: Codex logged `MCP server startup failed ... handshaking with MCP server failed: connection closed: initialize response`. The agent consequently did not see the synthetic tools. Setting the synthetic server `required=true`, specifying the existing repository as its working directory, and retaining a 30-second startup timeout produced two consecutive passes. This is consistent with an optional-server startup/catalog race, but does not prove that was the sole cause. The ordinary project configuration has not been validated here because this project is currently untrusted.

## Data and limits

- All new process/client/Host fixtures are synthetic and disposable. Independent-client tests use only disposable local databases; the Codex test configures only synthetic History. The opt-in Codex CLI may use the host's existing authentication context; credential values are not read by test code. The test verifies the two expected MCP tool calls but does not audit every possible Host-internal tool event.
- The resource API uses standard MCP `ResourceTemplate`/`ReadResourceContents`; it returns logical identifiers only. Full image understanding remains the active Agent's task; Gateway serves bytes and deterministic extracted text only.
- No HTTP server, remote endpoint, model API, or new inference dependency was introduced.
