# Synthetic Cross-Agent MCP Parity Plan

> **For agentic workers:** Execute inline using the existing P12 preparation boundary. These steps use synthetic data and never claim a real WorkBuddy or Hermes gate.

**Goal:** Verify that two independent MCP stdio clients can use the same configured Gateway and temporary store across process restarts.

**Architecture:** Preload one synthetic document as a valid Wrong Answer source reference in a temporary SQLite store. Client A registers a source and writes version 1 through the public MCP tools; client B reconnects in a separate Gateway subprocess, reads the bundle and search result, writes version 2 with `expected_version`, and client A reconnects to read the persisted successor. Both clients discover the same canonical workflow resource. This is host-neutral protocol coverage only.

**Tech Stack:** Existing Python MCP SDK client, Gateway stdio subprocess, temporary SQLite document store, pytest, AnyIO.

## Global Constraints

- Use only a pytest temporary directory and synthetic document/question/analysis content.
- Route Wrong Answer business writes through Gateway MCP tools; direct store use is limited to creating the synthetic source document fixture.
- Configure both clients with identical `read` and `write` capabilities; do not read or change WorkBuddy/Hermes user configuration.
- Report caller identity as synthetic and unverified; never claim a real Host pass.
- Do not access private History/Wrong Answer stores, export data, push, tag, release, or change P11/P12 gate state.

## Task 1: Independent stdio client persistence and workflow parity

**Files:**
- Create: `tests/test_cross_agent_stdio_parity.py`
- Modify: `docs/p12-host-compatibility.md`
- Modify: `docs/autonomous-run-status.md`
- Modify: `docs/roadmap.md`
- Modify: `var/p11-p12-resume/checkpoint.json` (ignored)

**Test interface:** One test creates a synthetic document in `tmp_path`, writes a temporary MCP config for SQLite and `read`/`write`, and launches the repository Gateway module with the independent MCP SDK. It opens three sequential stdio sessions so writes must survive Gateway process shutdown/restart:

1. Client A lists the `study-workflow://wrong-answer` resource, registers a synthetic source, and saves analysis version 1 through MCP.
2. Client B lists the same workflow, reads/searches version 1, and saves version 2 with `expected_version=1` through MCP.
3. Client A reconnects and reads version 2, including its `supersedes_analysis_id` and caller-reported/unverified provenance.

- [ ] Write the failing synthetic integration test with exact expected versions, source/analysis ID linkage, workflow equality, and provenance status.
- [ ] Run the new test and confirm the parity test file/behavior is absent.
- [ ] Implement only the test harness; do not add host-specific adapters or Gateway behavior unless the test exposes a genuine product defect.
- [ ] Run the parity test plus existing Wrong Answer MCP and independent stdio process tests.
- [ ] Review the diff for temporary-only data and fixed privacy boundaries; run `git diff --check`.
- [ ] Update public P12 docs and ignored checkpoint, commit locally, and leave all real host gates `WAITING_FOR_USER`.
