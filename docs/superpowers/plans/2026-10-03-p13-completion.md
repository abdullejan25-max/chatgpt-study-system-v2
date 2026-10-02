# P13 Completion Execution Plan

> **For agentic workers:** Use executing-plans and test-driven-development; reuse existing PASS evidence.

**Goal:** Finish acquired-data recovery, V1 unique-data audit/logical retirement,
and controlled production writes; stop before owner-confirmed physical deletion.

**Architecture:** Reuse the Gateway, existing immutable snapshot and ledger.
Extend restore capacity/readback checks only where the updated owner requirements
add evidence. WorkBuddy P13 History remains DEFERRED; prior Host PASS remains valid.

**Tech Stack:** Existing Python Gateway/MCP, deterministic migration and native Hosts.

## Ordered tasks

- [x] Verify the running snapshot's actual native result/usage and reuse it.
- [ ] Add restore capacity overhead/reserve and formal Assets/Documents/Wrong
  Answer readback; synthetic RED/GREEN, preserve old snapshot compatibility.
- [ ] Plan current free space through the Gateway, then restore the existing
  verified snapshot to its configured isolated target and reconcile all domains.
- [ ] Audit only known V1 roots/descriptors/config references. Map every object
  to migration/reuse/archive/intentional disposition; stop retirement on unknowns.
- [ ] Logically retire V1 consumers with reversible config backups; retain data.
- [ ] Restore persistent production writable ingress while preserving the
  P13 read-only profile. Run the explicitly authorized marked synthetic smoke
  through formal tools; preserve version/provenance/conflict semantics.
- [ ] Run final targeted/full checks, build/install/package/privacy audits,
  update documentation and decide the public release from actual Gates.
- [ ] Present the concrete deletion audit and request owner confirmation once.

## Constraints

No direct Agent V2 SQLite/store/snapshot reads or copies; no arbitrary target
paths, production overwrite, data deletion, source guessing, or repeated P12
audits. ChatGPT remains acquisition_pending with future incremental import.
Disk safety must account for existing snapshot allocation, restore, temp/WAL
and an explicit reserve. Public outputs contain aggregate statistics only.
