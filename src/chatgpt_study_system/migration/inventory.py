"""Read-only scanners for explicitly supplied legacy roots."""

from contextlib import closing
from datetime import datetime
import hashlib
import os
from pathlib import Path
import re
import sqlite3
from typing import Iterator

from ..adapters.documents import _path_has_reparse_point
from .planner import SourceRecord


_FRONTMATTER = re.compile(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", re.DOTALL)
_FIELD = re.compile(r"^([A-Za-z][A-Za-z0-9_-]*):\s*(.*?)\s*$")
_HASH = re.compile(r"[0-9a-f]{64}\Z")
_WRONG_ANSWER_WORDS = re.compile(r"wrong[ _-]*answers?", re.IGNORECASE)
_IMAGE_SUFFIXES = frozenset({".jpg", ".jpeg", ".png", ".webp", ".heic", ".tif", ".tiff"})


class InventoryError(ValueError):
    """A source cannot be safely inventoried; messages are intentionally path-free."""


def _validate_root(root: Path) -> Path:
    root = Path(root)
    if not root.is_absolute() or not root.is_dir() or _path_has_reparse_point(root):
        raise InventoryError("Unsafe migration source")
    try:
        return root.resolve(strict=True)
    except OSError:
        raise InventoryError("Unsafe migration source") from None


def _walk_files(root: Path) -> Iterator[Path]:
    root = _validate_root(root)

    def onerror(_error: OSError) -> None:
        raise InventoryError("Unreadable migration source") from None

    for current, directories, filenames in os.walk(root, topdown=True, followlinks=False,
                                                   onerror=onerror):
        current_path = Path(current)
        directories.sort(key=str.casefold)
        filenames.sort(key=str.casefold)
        for name in tuple(directories):
            candidate = current_path / name
            if _path_has_reparse_point(candidate):
                raise InventoryError("Unsafe migration source")
        for name in filenames:
            candidate = current_path / name
            if _path_has_reparse_point(candidate):
                raise InventoryError("Unsafe migration source")
            if not candidate.is_file():
                raise InventoryError("Invalid migration source entry")
            yield candidate


def _read_bytes(path: Path) -> bytes:
    if _path_has_reparse_point(path):
        raise InventoryError("Unsafe migration source")
    try:
        with path.open("rb") as stream:
            return stream.read()
    except OSError:
        raise InventoryError("Unreadable migration source") from None


def _path_identity(relative_path: str) -> str:
    return "path-" + hashlib.sha256(relative_path.encode("utf-8")).hexdigest()


def _metadata_fingerprint(relative_path: str, size: int, mtime_ns: int) -> str:
    payload = f"{relative_path}\0{size}\0{mtime_ns}".encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _content_fingerprint(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _is_legacy_wrong_answer_collection(name: str) -> bool:
    normalized = name.casefold()
    return bool(_WRONG_ANSWER_WORDS.search(name) or "错题" in normalized or "錯題" in normalized)


def scan_study_root(root: Path) -> tuple[SourceRecord, ...]:
    """Inventory the authoritative Study root without reading its file bodies."""
    root = _validate_root(root)
    records = []
    for path in _walk_files(root):
        relative_path = path.relative_to(root).as_posix()
        parts = Path(relative_path).parts
        info = path.stat(follow_symlinks=False)
        under_wrong_answers = bool(parts) and _is_legacy_wrong_answer_collection(parts[0])
        if not under_wrong_answers:
            category = "Documents" if path.suffix.casefold() == ".pdf" else "Study"
            source_type = ("study_file_pdf" if category == "Documents" else
                           "study_file_markdown" if path.suffix.casefold() == ".md" else
                           "study_file_authoritative")
            target_type = "study_source"
            fingerprint = _metadata_fingerprint(relative_path, info.st_size, info.st_mtime_ns)
            action = "reuse"
            reason = "same_authoritative_root"
        else:
            raw = _read_bytes(path)
            fingerprint = _content_fingerprint(raw)
            if path.suffix.casefold() == ".md":
                category = "Wrong Answers"
                source_type = "legacy_wrong_answer_note"
                target_type = "wrong_answer_source"
                reason = "legacy_record_unlinked"
            elif path.suffix.casefold() in _IMAGE_SUFFIXES:
                category = "Assets"
                source_type = "legacy_wrong_answer_image"
                target_type = "asset"
                reason = "unpaired_evidence"
            else:
                category = "Other / Unsupported"
                source_type = "unsupported_wrong_answer_file"
                target_type = "archive_record"
                reason = "unsupported_file_type"
            action = "archive" if category != "Other / Unsupported" else "skip"
        records.append(SourceRecord(
            category=category,
            legacy_system="studyvault_legacy",
            legacy_source_type=source_type,
            legacy_item_id=_path_identity(relative_path),
            source_fingerprint=fingerprint,
            target_type=target_type,
            target_logical_id=None,
            source_event_time=None,
            intended_action=action,
            validation_state=("unresolved" if under_wrong_answers else "valid"),
            requires_backend=None,
            reason_code=reason,
            source_size_bytes=info.st_size,
        ))
    return tuple(records)


def _parse_frontmatter(raw: bytes) -> tuple[dict[str, str], bool]:
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        return {}, False
    match = _FRONTMATTER.match(text)
    if match is None or len(match.group(1)) > 32_768:
        return {}, False
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        found = _FIELD.match(line)
        if found is None:
            continue
        key, value = found.groups()
        if key in {"type", "conversation_id", "created_at"}:
            if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
                value = value[1:-1]
            fields[key] = value
    return fields, True


def _timestamp_or_none(value: str | None) -> str | None:
    if value is None or not value or len(value) > 40:
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return value if parsed.tzinfo is not None else None


def scan_personal_root(root: Path) -> tuple[SourceRecord, ...]:
    """Inventory the configured Personal History tree without emitting its content."""
    root = _validate_root(root)
    records = []
    for path in _walk_files(root):
        relative_path = path.relative_to(root).as_posix()
        path_id = _path_identity(relative_path)
        info = path.stat(follow_symlinks=False)
        if path.suffix.casefold() != ".md":
            records.append(SourceRecord(
                category="Other / Unsupported",
                legacy_system="basic_memory_legacy",
                legacy_source_type="unsupported_personal_file",
                legacy_item_id=path_id,
                source_fingerprint=_metadata_fingerprint(relative_path, info.st_size, info.st_mtime_ns),
                target_type="archive_record",
                target_logical_id=None,
                source_event_time=None,
                intended_action="skip",
                validation_state="unresolved",
                requires_backend=None,
                reason_code="unsupported_personal_file",
                source_size_bytes=info.st_size,
            ))
            continue

        raw = _read_bytes(path)
        fingerprint = _content_fingerprint(raw)
        fields, valid_frontmatter = _parse_frontmatter(raw)
        record_type = fields.get("type")
        if record_type == "imported_chat":
            category = "Raw transcripts"
            source_type = "legacy_chat_markdown_archive"
            reason = "not_message_granular"
        elif record_type in {"imported_chat_index", "imported_chat_note"}:
            category = "Other / Unsupported"
            source_type = "legacy_chat_index_or_note"
            reason = "index_or_note_artifact"
        else:
            category = "Other / Unsupported"
            source_type = "legacy_personal_markdown"
            reason = "unsupported_personal_markdown"
        stable_id = fields.get("conversation_id") if record_type == "imported_chat" else None
        if not stable_id or len(stable_id) > 256:
            stable_id = path_id
        event_time = _timestamp_or_none(fields.get("created_at"))
        valid_metadata = valid_frontmatter and record_type is not None
        records.append(SourceRecord(
            category=category,
            legacy_system="basic_memory_legacy",
            legacy_source_type=source_type,
            legacy_item_id=stable_id,
            source_fingerprint=fingerprint,
            target_type="history_archive" if category == "Raw transcripts" else "archive_record",
            target_logical_id=None,
            source_event_time=event_time,
            intended_action="archive",
            validation_state="valid" if valid_metadata else "unresolved",
            requires_backend=None,
            reason_code=reason if valid_metadata else "malformed_frontmatter",
            source_size_bytes=len(raw),
        ))
    return tuple(records)


def scan_native_memory_db(database_path: Path, *, project_root: Path) -> tuple[SourceRecord, ...]:
    """Read only the known native-memory table within the explicitly selected project."""
    project_root = _validate_root(project_root)
    database_path = Path(database_path)
    if not database_path.is_absolute() or not database_path.is_file() \
            or _path_has_reparse_point(database_path):
        raise InventoryError("Unsafe legacy database")
    try:
        database_path.resolve(strict=True).relative_to(project_root)
    except (ValueError, OSError):
        raise InventoryError("Unsafe legacy database") from None

    uri = database_path.resolve(strict=True).as_uri() + "?mode=ro"
    try:
        with closing(sqlite3.connect(uri, uri=True, timeout=5)) as connection:
            connection.row_factory = sqlite3.Row
            connection.execute("PRAGMA query_only=ON")
            columns = {row[1] for row in connection.execute("PRAGMA table_info(memories)")}
            required = {"id", "kind", "content", "created_at"}
            if not required <= columns:
                raise InventoryError("Unsupported legacy memory schema")
            rows = connection.execute(
                "SELECT id, kind, content, created_at FROM memories ORDER BY id LIMIT 10001"
            ).fetchall()
    except InventoryError:
        raise
    except sqlite3.Error:
        raise InventoryError("Unreadable legacy database") from None
    if len(rows) > 10_000:
        raise InventoryError("Legacy database inventory limit exceeded")

    records = []
    for index, row in enumerate(rows):
        content = row["content"]
        valid_content = type(content) is str
        raw_content = content.encode("utf-8") if valid_content else b""
        legacy_id = row["id"] if type(row["id"]) is str and row["id"] else f"row-{index + 1}"
        event_time = _timestamp_or_none(row["created_at"] if type(row["created_at"]) is str else None)
        records.append(SourceRecord(
            category="Atomic Facts",
            legacy_system="workbuddy_native_memory",
            legacy_source_type="legacy_atomic_fact",
            legacy_item_id=legacy_id,
            source_fingerprint=_content_fingerprint(raw_content),
            target_type="history_annotation",
            target_logical_id=None,
            source_event_time=event_time,
            intended_action="import",
            validation_state="unresolved",
            requires_backend="history",
            reason_code="annotation_contract_pending",
            source_size_bytes=len(raw_content),
        ))
    return tuple(records)


def read_existing_asset_hashes(database_path: Path) -> set[tuple[str, str]]:
    """Read content hashes from the configured V2 Asset database without writes."""
    database_path = Path(database_path)
    if not database_path.is_absolute() or not database_path.is_file() \
            or _path_has_reparse_point(database_path):
        raise InventoryError("Invalid asset target")
    uri = database_path.resolve(strict=True).as_uri() + "?mode=ro"
    try:
        with closing(sqlite3.connect(uri, uri=True, timeout=5)) as connection:
            connection.execute("PRAGMA query_only=ON")
            columns = {row[1] for row in connection.execute("PRAGMA table_info(assets)")}
            if not {"uri", "sha256"} <= columns:
                raise InventoryError("Invalid asset target")
            rows = connection.execute("SELECT uri, sha256 FROM assets").fetchall()
    except InventoryError:
        raise
    except sqlite3.Error:
        raise InventoryError("Invalid asset target") from None
    result = set()
    for uri_value, digest in rows:
        if type(digest) is not str or not _HASH.fullmatch(digest) \
                or uri_value != "asset://sha256/" + digest:
            raise InventoryError("Invalid asset target")
        result.add(("asset", digest))
    return result
