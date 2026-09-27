from __future__ import annotations

import json
from pathlib import Path

import pytest

import chatgpt_study_system.obsidian_writer as writer_module
from chatgpt_study_system.obsidian_writer import ProjectionWriteError, write_projection


def _read_tree(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def test_first_write_and_rebuild_are_byte_identical(tmp_path: Path) -> None:
    root = tmp_path / "V2Projection"
    files = {
        "Dashboard.md": "# Synthetic dashboard\n",
        "History/index.md": "# Synthetic history\n",
    }

    write_projection(files, root)
    first = _read_tree(root)
    write_projection(files, root)

    assert _read_tree(root) == first
    manifest = json.loads(first[".projection-manifest.json"])
    assert manifest == {"files": sorted(files), "schema_version": 1}


def test_rebuild_removes_only_stale_owned_files_and_preserves_unknown_files(tmp_path: Path) -> None:
    root = tmp_path / "V2Projection"
    write_projection({"old.md": "generated old\n", "keep.md": "generated keep\n"}, root)
    (root / "notes.txt").write_text("user file\n", encoding="utf-8")

    write_projection({"keep.md": "generated keep v2\n"}, root)

    assert not (root / "old.md").exists()
    assert (root / "keep.md").read_text(encoding="utf-8") == "generated keep v2\n"
    assert (root / "notes.txt").read_text(encoding="utf-8") == "user file\n"


@pytest.mark.parametrize("path", ["../outside.md", "/absolute.md", "C:/drive.md", "a\\b.md", ".projection-manifest.json"])
def test_unsafe_or_reserved_output_paths_fail_before_creating_directory(tmp_path: Path, path: str) -> None:
    root = tmp_path / "V2Projection"

    with pytest.raises(ProjectionWriteError, match="Invalid projection output"):
        write_projection({path: "synthetic\n"}, root)

    assert not root.exists()


def test_nonempty_directory_requires_an_existing_valid_manifest(tmp_path: Path) -> None:
    root = tmp_path / "V2Projection"
    root.mkdir()
    (root / "notes.md").write_text("user content\n", encoding="utf-8")

    with pytest.raises(ProjectionWriteError, match="Invalid projection output"):
        write_projection({"Dashboard.md": "synthetic\n"}, root)

    (root / ".projection-manifest.json").write_text("{broken", encoding="utf-8")
    with pytest.raises(ProjectionWriteError, match="Invalid projection output"):
        write_projection({"Dashboard.md": "synthetic\n"}, root)
    assert (root / "notes.md").read_text(encoding="utf-8") == "user content\n"


def test_symlinked_output_file_is_rejected_without_following_it(tmp_path: Path) -> None:
    root = tmp_path / "V2Projection"
    outside = tmp_path / "outside.md"
    outside.write_text("untouched\n", encoding="utf-8")
    write_projection({"Dashboard.md": "initial\n"}, root)
    (root / "Dashboard.md").unlink()
    try:
        (root / "Dashboard.md").symlink_to(outside)
    except (OSError, NotImplementedError):
        pytest.skip("symlink creation is not available")

    with pytest.raises(ProjectionWriteError, match="Invalid projection output"):
        write_projection({"Dashboard.md": "replacement\n"}, root)
    assert outside.read_text(encoding="utf-8") == "untouched\n"


def test_windows_reparse_point_ancestor_is_rejected(tmp_path: Path, monkeypatch) -> None:
    root = tmp_path / "V2Projection"
    root.mkdir()
    reparse_path = root
    original_check = writer_module._is_reparse_point
    monkeypatch.setattr(
        writer_module, "_is_reparse_point",
        lambda path: Path(path) == reparse_path or original_check(Path(path)),
    )

    with pytest.raises(ProjectionWriteError, match="Invalid projection output"):
        write_projection({"Dashboard.md": "synthetic\n"}, root)

    assert list(root.iterdir()) == []


def test_failed_first_write_cleans_new_files_and_directories(tmp_path: Path, monkeypatch) -> None:
    root = tmp_path / "V2Projection"

    def fail_replace(source: Path, destination: Path) -> None:
        raise OSError("simulated failure")

    monkeypatch.setattr(writer_module, "_replace_file", fail_replace)
    with pytest.raises(ProjectionWriteError, match="Invalid projection output"):
        write_projection({"History/index.md": "synthetic\n"}, root)

    assert not root.exists()


def test_manifest_is_published_last_and_old_manifest_survives_failure(tmp_path: Path, monkeypatch) -> None:
    root = tmp_path / "V2Projection"
    old_files = {"Dashboard.md": "old content\n", "Legacy/old.md": "retired\n"}
    write_projection(old_files, root)
    old_manifest = (root / ".projection-manifest.json").read_bytes()
    original_replace = writer_module._replace_file

    def fail_manifest(source: Path, destination: Path) -> None:
        if destination.name == ".projection-manifest.json":
            raise OSError("simulated failure")
        original_replace(source, destination)

    monkeypatch.setattr(writer_module, "_replace_file", fail_manifest)
    with pytest.raises(ProjectionWriteError, match="Invalid projection output"):
        write_projection({"Dashboard.md": "new content\n", "History/index.md": "new\n"}, root)

    assert (root / ".projection-manifest.json").read_bytes() == old_manifest
    assert not (root / "History/index.md").exists()
    assert not (root / "Legacy/old.md").exists()

    monkeypatch.setattr(writer_module, "_replace_file", original_replace)
    write_projection({"Dashboard.md": "new content\n", "History/index.md": "new\n"}, root)
    assert _read_tree(root)[".projection-manifest.json"] != old_manifest
