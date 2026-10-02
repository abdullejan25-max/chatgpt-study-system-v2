# Private Gateway recovery

Recovery is opt-in and uses the existing `admin` capability. Default read-only
Hosts do not discover recovery tools. Data locations come from trusted private
configuration; tools accept a bounded snapshot key, never arbitrary paths.
Keep configuration, snapshots, restores, manifests and receipts outside Git.

```toml
[recovery]
root = "<ABSOLUTE_PRIVATE_RECOVERY_ROOT>"
sidecar_root = "<ABSOLUTE_PRIVATE_MIGRATION_LEDGER_ROOT>"
exclude_sidecar_paths = ["<REBUILDABLE_RUNTIME>", "<ACTIVE_OPERATOR_TRACE>"]
```

The root must not overlap production data, migration inputs or another Git
checkout. Exclusions are explicit relative paths, recorded in the private
manifest. Original evidence, ledger and durable migration receipts must remain
included. Canonical integrity must already be available for full P13 recovery.

Use actual configured native MCP tools:

1. `recovery_snapshot_plan` returns component sizes and available capacity.
2. `create_recovery_snapshot(snapshot_key=...)` captures committed SQLite WAL,
   configured Study files, Assets objects/metadata, History sources/canonical
   records, migration sidecar and explicit Gateway/QMD configuration.
3. `verify_recovery_snapshot(snapshot_key=..., restore=true)` checks the snapshot
   again and restores to a distinct target. It verifies every file checksum,
   database schema/row multiset, source/canonical identity and provenance, ledger,
   and the isolated Study no-result query. Production is never overwritten.

Snapshot creation reserves database writers in deterministic order, recomputes
WAL-aware capacity, compares inventory and rehashes source files before publish.
Large BLOBs are streamed. Manifests have a bounded size and a separate immutable
catalog checksum anchor; only a complete verified snapshot is published. These
checksums establish integrity under the trusted local owner, not authentication
against an attacker controlling both the artifact and catalog.

Recovery MCP calls run outside the protocol event loop so long copies and
integrity checks leave native ping requests responsive. A transport interruption
is not proof that the operation failed or completed: use a fresh configured
Host to verify the snapshot key. Never start a concurrent retry while the
original Gateway process is still running. Cancellation of the MCP await does
not stop an already running worker: it may retain database reservations and
finish publishing. Recovery does not claim cooperative cancellation support.
Partial attempts remain private.

Reusing a key re-verifies its complete artifact. Restore receipts do not replace
readback: existing targets are checked again. Unrelated populated restore targets
are refused. Failure evidence is retained; a failed partial target is never
silently overwritten or deleted. Retain the failed attempt and use a new key
after correcting the cause. This API has no deletion operation.

Isolated Study proof requires the configured disposable `qmd_runtime`, its
approved software dependencies, and archived config/index. The derived restore
configuration uses restored Study/config/index and private disposable QMD state.
Legacy ambient `qmd_executable` mode cannot establish isolation and is refused.
Database modules unsupported by the verifier fail closed; no skipped table is
reported as a verified count. Immutable evidence and original configs survive.

Synthetic tests are engineering evidence. Production acceptance requires actual
native Host calls, positive Agent usage/tool traces, durable private receipts,
and returned verification states. Never inspect V2 DBs or backup stores directly
from an Agent. A backup does not itself authorize V1 retirement or deletion.
