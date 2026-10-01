# Cross-Agent Integration Implementation Plan

**Goal:** Prove real Hermes → WorkBuddy → Codex discovery and versioned handoff
on one isolated Gateway, then release v0.6.0 after every Gate passes.

**Architecture:** Reuse the formal Gateway and existing Projection pipeline.
Separate persistent Host aliases point to one synthetic store; fresh session
prompts contain no inherited DTOs. Raw receipts remain outside Git.

**Tech stack:** Python, MCP stdio, real local Hosts, pytest, existing Projection.

## Constraints

- Gateway-only reads/writes; no private store inspection.
- No production writes; reported/unverified identity; no human data relay.
- No re-audit of accepted P11/Step 1/2/3 without regression evidence.
- Keep version 0.5.0 until functional acceptance; final release validation is now 0.6.0.

## Tasks

- [x] Verify clean worktree, remote main/tag baseline and Host version delta.
- [x] Back up configs outside Git and add distinct persistent aliases pointing
  to one isolated Gateway config. Preserve production and disabled memory.
- [x] Run Hermes Stage A with natural-language synthetic save request; export
  only that official Host session and retain formal DTO baseline privately.
- [x] Run fresh WorkBuddy Stage B with marker-only discovery/revision request;
  verify Gateway v2, exact request replay and preserved v1 provenance.
- [x] Run fresh Codex Stage C with marker-only discovery; verify trace, complete
  graph, exact DTO persistence, nonexistent query and Gateway stale conflict.
- [x] Extend `tests/test_cross_agent_stdio_parity.py` only where meaningful
  cross-client document/provenance/schema/persistence coverage is missing;
  run focused tests and require an observed failure before behavior changes.
- [x] Run scoped Projection twice on the shared isolated target; compare
  Markdown and manifest bytes through the existing writer and Gateway DTOs.
- [x] Record 25 Gate outcomes in `docs/p12-step4-cross-agent-checkpoint.md`,
  update current state/architecture/compatibility and redact all public evidence.
- [x] After every real Gate passes, set version/config example/lock to 0.6.0,
  write release notes, run targeted/full tests and `git diff --check`.
- [ ] Build wheel/sdist, inspect actual contents and public candidate tree,
  inspect reachable objects since v0.5.0 including new annotated tag.
- [ ] Commit, fast-forward main, normal push, create GitHub Release; verify
  remote refs and fresh public clone frozen install/version/stdio/privacy.

If a real Host GUI/trust blocker occurs, finish independent preparation and
record a resumable WAITING checkpoint; do not substitute SDK evidence or release.

## Historical resume snapshots (superseded by final acceptance below)

Resume delta: WorkBuddy upgraded to 5.7.3; owner MCP trust is confirmed.
The first Stage B used direct stdio fallback and copied V2 content into local
Memory, so it is rejected. Preserve that fixture/evidence outside Git; rerun
only the affected chain on a fresh single shared target with a fresh marker.
Require native MCP tools and actual trace proof; do not use SDK as Host PASS.

Fresh shared target Stage A is now REAL VALIDATED. Hermes corrected an initial
Base64 encoding mistake after Gateway readback; the final source references
the correct Document/Asset, with exactly v1. Intermediate Document is retained.
Official WorkBuddy task deeplink requested a fresh marker-only task. Receipt
logs do not confirm input prefill; the owner reports an empty input. Retried
without changing cwd; GUI input/send remains pending because capture fails.

Fresh WorkBuddy Stage B native MCP is REAL VALIDATED: initial bundle exact,
v2 append, exact replay, preserved source/v1, no-result and no v3. Only post-task
engineering status was logged; no canonical content/IDs copy or memory reads.
Scoped Projection rebuilt twice with 14 Markdown and byte-identical manifest.
Windows denied stopping the finished Host process; owner application exit is
pending before the prepared fresh Codex persistence/conflict session starts.

## Final verified acceptance

Final acceptance supersedes resume notes above: fresh Codex after A/B exit
passed exact DTO/Asset persistence, actual Gateway stale CONFLICT, final no-v3
and no-result. 25/25 Gate PASS; 0.6.0 targeted144/4, full622/12, wheel/sdist
privacy, clean wheel install/stdio PASS. Final commit/tag audit and normal
publish/fresh public-clone verification remain mandatory release transactions.
