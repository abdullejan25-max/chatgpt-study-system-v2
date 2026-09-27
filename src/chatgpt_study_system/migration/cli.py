"""Local-only, read-only dry-run command for the Phase 11 migration."""

import argparse
import json
import os
from pathlib import Path
import sys
from uuid import uuid4

from ..runtime import load_gateway_from_config
from .inventory import (
    InventoryError,
    read_existing_asset_hashes,
    scan_native_memory_db,
    scan_personal_root,
    scan_study_root,
)
from .manifest import MigrationJournal, estimate_storage, summarize
from .planner import plan_records


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="study-migrate")
    subparsers = parser.add_subparsers(dest="command", required=True)
    dry_run = subparsers.add_parser("dry-run", help="Inventory explicit legacy roots without target writes")
    dry_run.add_argument("--config", type=Path, required=True,
                         help="Explicit local V2 config file; never printed")
    dry_run.add_argument("--personal-root", type=Path, required=True,
                         help="Explicit Basic Memory/Personal root; never printed")
    dry_run.add_argument("--legacy-project-root", type=Path, required=True,
                         help="Explicit legacy project root; never printed")
    dry_run.add_argument("--legacy-memory-database", type=Path,
                         help="Explicit legacy memory database inside the selected project; never printed")
    dry_run.add_argument("--journal", type=Path,
                         help="Private journal path outside the repository")
    dry_run.add_argument("--run-id", help="Resume a prior private journal run")
    return parser


def _default_journal_path() -> Path:
    root = os.environ.get("LOCALAPPDATA") or os.environ.get("XDG_STATE_HOME")
    if not root:
        raise InventoryError("Private local journal location is not configured")
    directory = Path(root) / "ChatGPTStudySystemV2" / "migration"
    try:
        directory.mkdir(parents=True, exist_ok=True)
    except OSError:
        raise InventoryError("Private local journal location is not writable") from None
    return directory / "phase-11-manifest.sqlite3"


def _batched(values: tuple, batch_size: int = 250):
    for start in range(0, len(values), batch_size):
        yield start // batch_size + 1, values[start:start + batch_size]


def _run_dry_run(args: argparse.Namespace) -> dict:
    gateway = load_gateway_from_config(args.config)
    if "read" not in gateway.capabilities:
        raise InventoryError("Local read capability is not enabled")

    study_root = gateway.config.study_root
    if study_root is None:
        raise InventoryError("Study source is not configured")
    records = list(scan_study_root(study_root))
    records.extend(scan_personal_root(args.personal_root))

    if args.legacy_memory_database is not None:
        records.extend(scan_native_memory_db(
            args.legacy_memory_database, project_root=args.legacy_project_root,
        ))

    target_health = {"history": "not_configured", "assets": "not_configured"}
    history_health = gateway.history_backend.probe()
    if history_health.status in {"ready", "unavailable", "not_configured"}:
        target_health["history"] = history_health.status

    existing_targets: set[tuple[str, str]] = set()
    if gateway.document_store is not None:
        asset_database = gateway.document_store.database_path
        existing_targets = read_existing_asset_hashes(asset_database)
        target_health["assets"] = "ready"

    planned = plan_records(records, existing_targets=existing_targets,
                           target_health=target_health)
    journal_path = args.journal or _default_journal_path()
    run_id = args.run_id or "migration-" + uuid4().hex
    journal = MigrationJournal(journal_path, run_id=run_id)
    try:
        for batch_number, batch in _batched(planned):
            journal.add_batch(batch, batch_number=batch_number)
        durable_items = journal.list_items()
        counts = summarize(durable_items)
        storage = estimate_storage(durable_items)
        blockers = sorted({item.error_code for item in durable_items
                           if item.status in {"unresolved", "error"} and item.error_code})
        return {
            "status": "BLOCKED" if blockers else "DRY_RUN_PASS",
            "run_id": run_id,
            "counts": counts,
            "storage_estimate": storage,
            "target_health": target_health,
            "blockers": blockers,
            "checkpoints": len(journal.checkpoints()),
        }
    finally:
        journal.close()


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.command != "dry-run":
            raise InventoryError("Unsupported migration operation")
        result = _run_dry_run(args)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0 if result["status"] == "DRY_RUN_PASS" else 1
    except Exception:
        print("Unable to create a private migration manifest", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
