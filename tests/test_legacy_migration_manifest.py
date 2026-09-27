"""Synthetic migration journal records; never use personal data here."""

from pathlib import Path

import pytest

import chatgpt_study_system.migration.manifest as manifest_module
from chatgpt_study_system.migration.manifest import (
    ManifestConflict,
    MigrationItem,
    MigrationJournal,
    stable_migration_key,
    summarize,
)


def _item(**overrides) -> MigrationItem:
    values = {
        "category": "History",
        "legacy_system": "synthetic-legacy",
        "legacy_source_type": "chat_message",
        "legacy_item_id": "message-1",
        "source_fingerprint": "a" * 64,
        "target_type": "history_item",
        "target_logical_id": None,
        "action": "import",
        "status": "planned",
        "source_event_time": "2024-01-02T03:04:05Z",
        "imported_at": None,
        "dedup_decision": "none",
        "validation_state": "valid",
        "reason_code": None,
        "error_code": None,
        "source_size_bytes": 12,
    }
    values.update(overrides)
    return MigrationItem(**values)


def test_stable_migration_key_uses_system_identity_and_content_hash() -> None:
    first = stable_migration_key("legacy-a", "item-7", "a" * 64)
    assert first == stable_migration_key("legacy-a", "item-7", "a" * 64)
    assert first != stable_migration_key("legacy-a", "item-8", "a" * 64)
    assert first != stable_migration_key("legacy-a", "item-7", "b" * 64)
    assert first.startswith("migration:")


def test_journal_reopens_and_reruns_items_without_duplicate_rows(tmp_path: Path) -> None:
    path = tmp_path / "private-migration.sqlite3"
    first = MigrationJournal(path, run_id="migration-synthetic-1")
    item = _item()
    first.add_batch([item], batch_number=1)
    first.close()

    resumed = MigrationJournal(path, run_id="migration-synthetic-1")
    resumed.add_batch([item], batch_number=1)
    assert resumed.list_items() == (item,)
    assert resumed.checkpoints() == (1,)
    resumed.close()


def test_journal_write_connections_use_full_synchronous_wal_durability(tmp_path: Path) -> None:
    journal = MigrationJournal(tmp_path / "private-migration.sqlite3", run_id="migration-wal-test")
    with manifest_module.closing(journal._connect(write=True)) as connection:
        assert connection.execute("PRAGMA journal_mode").fetchone()[0].casefold() == "wal"
        assert connection.execute("PRAGMA synchronous").fetchone()[0] == 2
    journal.close()


def test_manifest_keeps_source_event_time_separate_from_import_time(tmp_path: Path) -> None:
    item = _item(status="committed", source_event_time="2020-02-03T04:05:06+02:00",
                 imported_at="2026-09-27T08:09:10Z")
    journal = MigrationJournal(tmp_path / "private-migration.sqlite3", run_id="migration-time-test")
    journal.add_batch([item], batch_number=1)
    restored = journal.list_items()[0]
    assert restored.source_event_time == "2020-02-03T04:05:06+02:00"
    assert restored.imported_at == "2026-09-27T08:09:10Z"


def test_duplicate_legacy_identity_conflict_rolls_back_the_whole_batch(tmp_path: Path) -> None:
    journal = MigrationJournal(tmp_path / "private-migration.sqlite3", run_id="migration-test-2")
    existing = _item()
    journal.add_batch([existing], batch_number=1)

    first_new = _item(legacy_item_id="message-2", source_fingerprint="b" * 64)
    conflicting = _item(source_fingerprint="c" * 64)
    with pytest.raises(ManifestConflict):
        journal.add_batch([first_new, conflicting], batch_number=2)

    assert journal.list_items() == (existing,)
    assert journal.checkpoints() == (1,)
    journal.close()


def test_manifest_rejects_absolute_paths_in_identifiers(tmp_path: Path) -> None:
    journal = MigrationJournal(tmp_path / "private-migration.sqlite3", run_id="migration-test-3")
    with pytest.raises(ValueError, match="Invalid migration item"):
        journal.add_batch([_item(legacy_item_id=r"C:\private\message.md")], batch_number=1)
    assert journal.list_items() == ()
    journal.close()


def test_journal_rejects_reparse_point_path(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(manifest_module, "_path_has_reparse_point", lambda _path: True)
    with pytest.raises(ValueError, match="Invalid private migration journal"):
        MigrationJournal(tmp_path / "private-migration.sqlite3", run_id="migration-reparse-test")


def test_summary_counts_actions_and_never_returns_item_identifiers() -> None:
    private_id = "synthetic-secret-item-id"
    items = (
        _item(action="reuse", status="planned", dedup_decision="same_authoritative_root"),
        _item(legacy_item_id=private_id, source_fingerprint="b" * 64,
              action="import", status="planned"),
        _item(legacy_item_id="message-3", source_fingerprint="c" * 64,
              action="skip", status="skipped", dedup_decision="content_hash"),
        _item(legacy_item_id="message-4", source_fingerprint="d" * 64,
              action="archive", status="skipped", reason_code="archive_only"),
        _item(legacy_item_id="message-5", source_fingerprint="e" * 64,
              action="import", status="unresolved", error_code="history_target_not_configured",
              validation_state="unresolved"),
        _item(legacy_item_id="message-6", source_fingerprint="f" * 64,
              action="skip", status="error", error_code="invalid_record",
              validation_state="invalid"),
    )
    result = summarize(items)

    assert result["History"] == {
        "found": 6,
        "reuse": 1,
        "planned_import": 1,
        "deduplicated": 1,
        "skip": 1,
        "unresolved": 1,
        "errors": 1,
    }
    assert private_id not in repr(result)
    assert "source_fingerprint" not in repr(result)
    assert result["History"]["found"] == sum(
        result["History"][key]
        for key in ("reuse", "planned_import", "deduplicated", "skip", "unresolved", "errors")
    )


def test_storage_estimate_counts_only_bytes_that_would_be_imported() -> None:
    from chatgpt_study_system.migration.manifest import estimate_storage

    items = (
        _item(source_size_bytes=100, action="reuse"),
        _item(legacy_item_id="message-2", source_fingerprint="b" * 64,
              source_size_bytes=30, action="import", status="planned"),
        _item(legacy_item_id="message-3", source_fingerprint="c" * 64,
              source_size_bytes=50, action="skip", status="skipped",
              dedup_decision="content_hash"),
        _item(legacy_item_id="message-4", source_fingerprint="d" * 64,
              source_size_bytes=20, action="archive", status="skipped"),
        _item(legacy_item_id="message-5", source_fingerprint="e" * 64,
              source_size_bytes=10, action="import", status="unresolved",
              validation_state="unresolved", error_code="history_target_not_configured"),
    )
    assert estimate_storage(items) == {
        "source_bytes": 210,
        "estimated_import_bytes": 40,
        "ready_import_bytes": 30,
    }
