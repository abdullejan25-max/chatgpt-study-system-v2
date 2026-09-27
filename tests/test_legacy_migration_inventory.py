"""Synthetic source inventories; never use personal files as fixtures."""

import hashlib
import sqlite3
from pathlib import Path

import pytest

import chatgpt_study_system.migration.inventory as inventory
from chatgpt_study_system.migration.planner import plan_records


def test_study_root_reuses_authority_and_archives_unpaired_wrong_answer_files(tmp_path: Path) -> None:
    study = tmp_path / "Study"
    (study / "algebra").mkdir(parents=True)
    (study / "wrong_answer" / "set-a").mkdir(parents=True)
    (study / "algebra" / "lesson.md").write_text("synthetic lesson", encoding="utf-8")
    (study / "algebra" / "book.pdf").write_bytes(b"synthetic pdf bytes")
    (study / "wrong_answer" / "set-a" / "note.md").write_text(
        "synthetic wrong-answer note", encoding="utf-8")
    (study / "wrong_answer" / "set-a" / "image.jpg").write_bytes(b"synthetic image bytes")

    records = inventory.scan_study_root(study)
    actions = {(item.category, item.legacy_source_type): item.intended_action for item in records}
    assert actions[("Study", "study_file_markdown")] == "reuse"
    assert actions[("Documents", "study_file_pdf")] == "reuse"
    assert actions[("Wrong Answers", "legacy_wrong_answer_note")] == "archive"
    assert actions[("Assets", "legacy_wrong_answer_image")] == "archive"
    assert all(item.validation_state == "unresolved" for item in records
               if item.category in {"Wrong Answers", "Assets"})
    assert all(str(study) not in repr(item) for item in records)


def test_chinese_wrong_answer_directory_is_classified_as_legacy_evidence(tmp_path: Path) -> None:
    study = tmp_path / "Study"
    evidence = study / "错题集"
    evidence.mkdir(parents=True)
    (evidence / "note.md").write_text("synthetic note", encoding="utf-8")
    (evidence / "photo.jpg").write_bytes(b"synthetic photo")

    records = inventory.scan_study_root(study)
    assert {item.category for item in records} == {"Wrong Answers", "Assets"}
    assert all(item.intended_action == "archive" for item in records)


def test_study_inventory_fingerprint_uses_metadata_without_reading_authoritative_bytes(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    study = tmp_path / "Study"
    study.mkdir()
    (study / "lesson.md").write_bytes(b"synthetic authoritative content")

    def fail_read(_path: Path) -> bytes:
        raise AssertionError("Study reuse must not hash or rewrite authoritative content")

    monkeypatch.setattr(inventory, "_read_bytes", fail_read)
    record = inventory.scan_study_root(study)[0]
    assert record.intended_action == "reuse"
    assert len(record.source_fingerprint) == 64


def test_personal_chat_export_is_archived_without_parsing_or_rewriting_messages(tmp_path: Path) -> None:
    personal = tmp_path / "Personal"
    imports = personal / "imported-chats"
    imports.mkdir(parents=True)
    transcript = imports / "private-name.md"
    raw = ("---\ntype: imported_chat\nconversation_id: conversation-7\n"
           "created_at: 2024-06-05T10:11:12Z\n---\n## User\nsynthetic body\n").encode()
    transcript.write_bytes(raw)

    records = inventory.scan_personal_root(personal)
    assert len(records) == 1
    record = records[0]
    assert record.category == "Raw transcripts"
    assert record.legacy_item_id == "conversation-7"
    assert record.source_event_time == "2024-06-05T10:11:12Z"
    assert record.source_fingerprint == hashlib.sha256(raw).hexdigest()
    assert record.intended_action == "archive"
    assert b"synthetic body" not in repr(record).encode()
    assert str(personal) not in repr(record)


def test_personal_export_unknown_time_stays_unknown_and_malformed_frontmatter_isolated(
        tmp_path: Path) -> None:
    imports = tmp_path / "Personal" / "imported-chats"
    imports.mkdir(parents=True)
    (imports / "unknown-time.md").write_text(
        "---\ntype: imported_chat\nconversation_id: conversation-8\ncreated_at: unknown\n---\nbody",
        encoding="utf-8",
    )
    (imports / "malformed.md").write_bytes(b"---\ntype: imported_chat\n\xff")

    records = inventory.scan_personal_root(imports.parent)
    by_id = {record.legacy_item_id: record for record in records}
    assert by_id["conversation-8"].source_event_time is None
    assert by_id["conversation-8"].intended_action == "archive"
    malformed = next(record for record in records if record.validation_state == "unresolved")
    assert malformed.reason_code == "malformed_frontmatter"
    plan = plan_records([malformed], existing_targets=set(), target_health={})[0]
    assert plan.status == "unresolved"


def test_native_memory_fact_is_typed_as_unresolved_annotation_and_read_only(
        tmp_path: Path) -> None:
    project = tmp_path / "legacy-project"
    database_dir = project / "data"
    database_dir.mkdir(parents=True)
    database = database_dir / "synthetic_memory.sqlite3"
    with sqlite3.connect(database) as connection:
        connection.execute("CREATE TABLE memories(id TEXT, kind TEXT, content TEXT, created_at TEXT)")
        connection.execute(
            "INSERT INTO memories VALUES (?, ?, ?, ?)",
            ("fact-1", "preference", "synthetic fact", "2024-01-02T03:04:05Z"),
        )
    before = hashlib.sha256(database.read_bytes()).hexdigest()

    records = inventory.scan_native_memory_db(database, project_root=project)
    assert len(records) == 1
    assert records[0].category == "Atomic Facts"
    assert records[0].target_type == "history_annotation"
    assert records[0].intended_action == "import"
    assert records[0].validation_state == "unresolved"
    assert records[0].reason_code == "annotation_contract_pending"
    assert hashlib.sha256(database.read_bytes()).hexdigest() == before
    assert "synthetic fact" not in repr(records[0])


def test_invalid_native_memory_row_remains_unresolved_without_invented_time(
        tmp_path: Path) -> None:
    project = tmp_path / "legacy-project"
    database_dir = project / "data"
    database_dir.mkdir(parents=True)
    database = database_dir / "synthetic_memory.sqlite3"
    with sqlite3.connect(database) as connection:
        connection.execute("CREATE TABLE memories(id TEXT, kind TEXT, content TEXT, created_at TEXT)")
        connection.execute("INSERT INTO memories VALUES (?, ?, ?, ?)",
                           (None, "preference", sqlite3.Binary(b"\xff"), "not-a-time"))

    record = inventory.scan_native_memory_db(database, project_root=project)[0]
    assert record.validation_state == "unresolved"
    assert record.legacy_item_id == "row-1"
    assert record.source_event_time is None
    assert record.source_size_bytes == 0
    assert "not-a-time" not in repr(record)


def test_asset_target_hashes_are_read_only_and_validate_schema(tmp_path: Path) -> None:
    database = tmp_path / "assets.db"
    with sqlite3.connect(database) as connection:
        connection.execute("CREATE TABLE assets(uri TEXT, sha256 TEXT, media_type TEXT, size INTEGER)")
        connection.execute("INSERT INTO assets VALUES (?, ?, ?, ?)",
                           ("asset://sha256/" + "a" * 64, "a" * 64, "image/jpeg", 12))
    before = hashlib.sha256(database.read_bytes()).hexdigest()
    assert inventory.read_existing_asset_hashes(database) == {("asset", "a" * 64)}
    assert hashlib.sha256(database.read_bytes()).hexdigest() == before

    invalid = tmp_path / "invalid.db"
    with sqlite3.connect(invalid) as connection:
        connection.execute("CREATE TABLE assets(uri TEXT)")
    with pytest.raises(inventory.InventoryError, match="Invalid asset target"):
        inventory.read_existing_asset_hashes(invalid)


def test_inventory_rejects_reparse_source_root_without_scanning(tmp_path: Path,
                                                                 monkeypatch: pytest.MonkeyPatch) -> None:
    source = tmp_path / "source"
    source.mkdir()
    monkeypatch.setattr(inventory, "_path_has_reparse_point", lambda _path: True)
    with pytest.raises(inventory.InventoryError, match="Unsafe migration source"):
        inventory.scan_study_root(source)
