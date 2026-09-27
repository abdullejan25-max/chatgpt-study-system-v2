"""CLI coverage uses only synthetic sources and targets."""

import json
import hashlib
from pathlib import Path
import sqlite3

from chatgpt_study_system.migration.cli import main


def test_dry_run_writes_private_manifest_and_prints_only_safe_summary(
        tmp_path: Path, capsys) -> None:
    study = tmp_path / "Study"
    personal = tmp_path / "Personal"
    legacy_project = tmp_path / "LegacyProject"
    (study / "math").mkdir(parents=True)
    (personal / "imported-chats").mkdir(parents=True)
    legacy_project.mkdir()
    (study / "math" / "lesson.md").write_text("synthetic study body", encoding="utf-8")
    (personal / "imported-chats" / "chat.md").write_text(
        "---\ntype: imported_chat\nconversation_id: conversation-1\n"
        "created_at: 2024-01-02T03:04:05Z\n---\nsynthetic private transcript body",
        encoding="utf-8",
    )
    config = tmp_path / "config.local.toml"
    asset_root = tmp_path / "asset-root"
    ingest_root = tmp_path / "asset-inbox"
    asset_root.mkdir()
    ingest_root.mkdir()
    asset_database = tmp_path / "assets.sqlite3"
    with sqlite3.connect(asset_database) as connection:
        connection.execute("CREATE TABLE assets(uri TEXT, sha256 TEXT, media_type TEXT, size INTEGER)")
        connection.execute("INSERT INTO assets VALUES (?, ?, ?, ?)",
                           ("asset://sha256/" + "b" * 64, "b" * 64, "image/jpeg", 14))
    asset_database_before = hashlib.sha256(asset_database.read_bytes()).hexdigest()
    config.write_text(
        "[gateway]\nversion = \"0.1.0\"\n\n"
        f"[study]\nroot = {json.dumps(str(study))}\n"
        "qmd_collection = \"studyvault\"\nqmd_version = \"2.8.3\"\n"
        "qmd_executable = \"qmd\"\n\n"
        "[history]\nbackend = \"not_configured\"\n\n"
        "[assets]\nbackend = \"sqlite\"\n"
        f"root = {json.dumps(str(asset_root))}\n"
        f"database = {json.dumps(str(asset_database))}\n"
        f"ingest_root = {json.dumps(str(ingest_root))}\n\n"
        "[permissions]\ncapabilities = [\"read\"]\n",
        encoding="utf-8",
    )
    journal_path = tmp_path / "private" / "migration.sqlite3"
    journal_path.parent.mkdir()

    arguments = [
        "dry-run", "--config", str(config), "--personal-root", str(personal),
        "--legacy-project-root", str(legacy_project), "--journal", str(journal_path),
        "--run-id", "migration-synthetic-cli",
    ]
    result = main(arguments)

    captured = capsys.readouterr()
    output = json.loads(captured.out)
    assert result == 0
    assert output["run_id"] == "migration-synthetic-cli"
    assert output["counts"]["Study"]["reuse"] == 1
    assert output["counts"]["Raw transcripts"]["skip"] == 1
    assert output["target_health"]["history"] == "not_configured"
    assert str(tmp_path) not in captured.out
    assert "synthetic private transcript body" not in captured.out
    assert journal_path.is_file()
    assert hashlib.sha256(asset_database.read_bytes()).hexdigest() == asset_database_before

    assert main(arguments) == 0
    replay_output = json.loads(capsys.readouterr().out)
    assert replay_output == output
    assert hashlib.sha256(asset_database.read_bytes()).hexdigest() == asset_database_before


def test_dry_run_rejects_a_journal_under_the_repository(tmp_path: Path, capsys) -> None:
    study = tmp_path / "Study"
    personal = tmp_path / "Personal"
    legacy_project = tmp_path / "LegacyProject"
    study.mkdir()
    personal.mkdir()
    legacy_project.mkdir()
    config = tmp_path / "config.local.toml"
    config.write_text(
        "[gateway]\nversion = \"0.1.0\"\n\n"
        f"[study]\nroot = {json.dumps(str(study))}\n"
        "qmd_collection = \"studyvault\"\nqmd_version = \"2.8.3\"\n"
        "qmd_executable = \"qmd\"\n\n"
        "[history]\nbackend = \"not_configured\"\n",
        encoding="utf-8",
    )
    repository = Path(__file__).resolve().parents[1]

    result = main([
        "dry-run", "--config", str(config), "--personal-root", str(personal),
        "--legacy-project-root", str(legacy_project),
        "--journal", str(repository / "private-migration.sqlite3"),
        "--run-id", "migration-synthetic-cli",
    ])

    captured = capsys.readouterr()
    assert result == 2
    assert str(repository) not in captured.err
    assert "Unable to create a private migration manifest" in captured.err
    assert not (repository / "private-migration.sqlite3").exists()


def test_dry_run_sanitizes_private_journal_errors(tmp_path: Path, capsys) -> None:
    study = tmp_path / "Study"
    personal = tmp_path / "Personal"
    legacy_project = tmp_path / "LegacyProject"
    study.mkdir()
    personal.mkdir()
    legacy_project.mkdir()
    config = tmp_path / "config.local.toml"
    config.write_text(
        "[gateway]\nversion = \"0.1.0\"\n\n"
        f"[study]\nroot = {json.dumps(str(study))}\n"
        "qmd_collection = \"studyvault\"\nqmd_version = \"2.8.3\"\n"
        "qmd_executable = \"qmd\"\n\n"
        "[history]\nbackend = \"not_configured\"\n",
        encoding="utf-8",
    )
    journal_path = tmp_path / "private" / "bad.sqlite3"
    journal_path.parent.mkdir()
    journal_path.write_bytes(b"synthetic invalid journal bytes")

    result = main([
        "dry-run", "--config", str(config), "--personal-root", str(personal),
        "--legacy-project-root", str(legacy_project), "--journal", str(journal_path),
        "--run-id", "migration-synthetic-cli",
    ])

    captured = capsys.readouterr()
    assert result == 2
    assert str(tmp_path) not in captured.err
    assert "Unable to create a private migration manifest" in captured.err
