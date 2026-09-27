import hashlib
import json
import zipfile
from pathlib import Path

from chatgpt_study_system.migration.raw_archive import PrivateRawArchiveStore


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
