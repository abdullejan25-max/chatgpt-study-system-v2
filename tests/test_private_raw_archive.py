import hashlib
import json
import os
import stat
from types import SimpleNamespace
import zipfile
from pathlib import Path

import pytest

from chatgpt_study_system.migration import raw_archive
from chatgpt_study_system.migration.raw_archive import (
    PrivateRawArchiveStore,
    RawArchiveError,
    RawArchiveLimits,
)


def test_limits_cannot_raise_hard_resource_ceilings() -> None:
    hard_maxima = {
        "max_archive_bytes": 512 * 1024 * 1024,
        "max_members": 50_000,
        "max_uncompressed_bytes": 2 * 1024 * 1024 * 1024,
        "max_member_compression_ratio": 200,
    }
    for field, maximum in hard_maxima.items():
        with pytest.raises(ValueError, match="^Invalid raw archive limits$") as error:
            RawArchiveLimits(**{field: maximum + 1})
        assert str(maximum + 1) not in str(error.value)

    invalid_values = (-1, True, 1.5, "10")
    for field in hard_maxima:
        for value in invalid_values:
            with pytest.raises(ValueError, match="^Invalid raw archive limits$"):
                RawArchiveLimits(**{field: value})

    for field in ("max_archive_bytes", "max_member_compression_ratio"):
        with pytest.raises(ValueError, match="^Invalid raw archive limits$"):
            RawArchiveLimits(**{field: 0})

    RawArchiveLimits(max_archive_bytes=1, max_members=1,
                     max_uncompressed_bytes=1, max_member_compression_ratio=1)
    RawArchiveLimits(max_members=0, max_uncompressed_bytes=0)


def test_tightened_member_limit_leaves_no_published_or_partial_files(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    source_path = tmp_path / "source.zip"
    with zipfile.ZipFile(source_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("synthetic.txt", b"synthetic payload")
    store_root = tmp_path / "private-store"

    with pytest.raises(RawArchiveError) as error:
        PrivateRawArchiveStore(
            root=store_root, limits=RawArchiveLimits(max_members=0)
        ).ingest_zip(source_path, source_system="chatgpt")

    assert error.value.code == "too_many_members"
    destination_dir = store_root / "chatgpt"
    assert not list(destination_dir.glob("*.zip"))
    assert not list(destination_dir.glob("*.manifest.json"))
    assert not list(destination_dir.glob("*.partial"))


def test_ingest_preserves_exact_zip_bytes_and_redacts_manifest(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    source_dir = tmp_path / "incoming"
    source_dir.mkdir()
    source_path = source_dir / "private-source-export.zip"
    with zipfile.ZipFile(source_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("private-sentinel.txt", b"synthetic conversation payload")
    original_bytes = source_path.read_bytes()

    result = PrivateRawArchiveStore(root=tmp_path / "private-store").ingest_zip(
        source_path, source_system="chatgpt"
    )

    assert result.source_system == "chatgpt"
    assert result.sha256 == hashlib.sha256(original_bytes).hexdigest()
    assert result.byte_count == len(original_bytes)
    assert result.member_count == 1
    assert result.uncompressed_byte_count == len(b"synthetic conversation payload")
    assert result.duplicate is False
    assert result.stored_path.read_bytes() == original_bytes

    manifest_path = result.stored_path.with_suffix(".manifest.json")
    manifest_bytes = manifest_path.read_bytes()
    manifest = json.loads(manifest_bytes)
    assert set(manifest) == {
        "source_system",
        "sha256",
        "byte_count",
        "member_count",
        "uncompressed_byte_count",
        "ingested_at",
    }
    for private_value in (
        str(source_path),
        source_path.name,
        "private-sentinel.txt",
        "synthetic conversation payload",
    ):
        assert private_value.encode() not in manifest_bytes


def test_store_root_must_be_under_configured_user_state_root(tmp_path: Path, monkeypatch) -> None:
    configured_root = tmp_path / "configured-state"
    outside_root = tmp_path / "outside-state"
    configured_root.mkdir()
    monkeypatch.setenv("LOCALAPPDATA", str(configured_root))
    monkeypatch.delenv("XDG_STATE_HOME", raising=False)
    # Exercise the POSIX policy on Windows too: containment must not depend on
    # which platform-specific permission branch is active.
    posix_policy_values = vars(os).copy()
    posix_policy_values.update(name="posix", getuid=lambda: os.stat(outside_root).st_uid)
    posix_policy = SimpleNamespace(**posix_policy_values)
    monkeypatch.setattr(raw_archive, "os", posix_policy)
    real_stat = Path.stat

    def private_directory_stat(path: Path, *args, **kwargs):
        if path == outside_root:
            return SimpleNamespace(st_mode=stat.S_IFDIR | 0o700, st_uid=os.stat(path).st_uid)
        return real_stat(path, *args, **kwargs)

    monkeypatch.setattr(Path, "stat", private_directory_stat)
    monkeypatch.setattr(
        raw_archive,
        "validate_private_journal_path",
        lambda path: Path(path),
    )

    with pytest.raises(RawArchiveError) as error:
        PrivateRawArchiveStore(root=outside_root)

    assert error.value.code == "unsafe_path"
    assert str(outside_root) not in str(error.value)


def test_staged_archive_is_rehashed_before_zip_validation(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    source_path = tmp_path / "source.zip"
    with zipfile.ZipFile(source_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("sentinel.txt", b"synthetic payload")

    original_hash_file = getattr(raw_archive, "_hash_file", None)

    def corrupt_then_hash(path: Path) -> tuple[int, str]:
        data = path.read_bytes()
        path.write_bytes(b"X" + data[1:])
        assert original_hash_file is not None
        return original_hash_file(path)

    monkeypatch.setattr(raw_archive, "_hash_file", corrupt_then_hash, raising=False)

    with pytest.raises(RawArchiveError) as error:
        PrivateRawArchiveStore(root=tmp_path / "private-store").ingest_zip(
            source_path, source_system="chatgpt"
        )

    assert error.value.code == "integrity_mismatch"
    assert str(source_path) not in str(error.value)
