"""Explicit, manifest-bounded writer for generated Obsidian projection files."""

from __future__ import annotations

from collections.abc import Mapping
import json
import os
from pathlib import Path, PurePosixPath
import re
import tempfile


_MANIFEST = ".projection-manifest.json"
_SCHEMA_VERSION = 1
_MAX_FILES = 10_006
_MAX_BYTES = 64 * 1024 * 1024
_WINDOWS_RESERVED = re.compile(r"(?i)(?:CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\..*)?\Z")


class ProjectionWriteError(ValueError):
    """Fixed-message error that does not expose file paths or content."""

    def __init__(self) -> None:
        super().__init__("Invalid projection output")


def _checked_relative_path(value: object) -> str:
    if type(value) is not str or not value or value == _MANIFEST or "\\" in value \
            or value.startswith("/") or re.match(r"[A-Za-z]:", value):
        raise ProjectionWriteError
    try:
        value.encode("utf-8")
    except UnicodeEncodeError:
        raise ProjectionWriteError from None
    if any(ord(char) < 0x20 or ord(char) == 0x7F for char in value):
        raise ProjectionWriteError
    parts = value.split("/")
    if any(part in {"", ".", ".."} or part.endswith((" ", "."))
           or any(char in '<>:"|?*' for char in part)
           or _WINDOWS_RESERVED.fullmatch(part)
           for part in parts):
        raise ProjectionWriteError
    if PurePosixPath(value).as_posix() != value:
        raise ProjectionWriteError
    return value


def _manifest_files(content: bytes) -> tuple[str, ...]:
    if len(content) > 4 * 1024 * 1024:
        raise ProjectionWriteError
    try:
        value = json.loads(content.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise ProjectionWriteError from None
    if type(value) is not dict or set(value) != {"files", "schema_version"} \
            or type(value.get("schema_version")) is not int \
            or value["schema_version"] != _SCHEMA_VERSION \
            or type(value.get("files")) is not list or len(value["files"]) > _MAX_FILES:
        raise ProjectionWriteError
    paths = tuple(_checked_relative_path(path) for path in value["files"])
    if paths != tuple(sorted(set(paths))):
        raise ProjectionWriteError
    return paths


def _is_reparse_point(path: Path) -> bool:
    try:
        info = path.lstat()
    except FileNotFoundError:
        return False
    except OSError:
        return True
    return path.is_symlink() or bool(getattr(info, "st_file_attributes", 0) & 0x400)


def _reject_symlink_components(path: Path, stop: Path) -> None:
    current = path
    while current != stop:
        if _is_reparse_point(current):
            raise ProjectionWriteError
        parent = current.parent
        if parent == current:
            raise ProjectionWriteError
        current = parent
    if _is_reparse_point(stop):
        raise ProjectionWriteError


def _replace_file(source: Path, destination: Path) -> None:
    os.replace(source, destination)


def _atomic_write(destination: Path, content: bytes) -> None:
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb", dir=destination.parent, prefix=f".{destination.name}.",
            suffix=".tmp", delete=False,
        ) as stream:
            temporary = Path(stream.name)
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        _replace_file(temporary, destination)
        temporary = None
    finally:
        if temporary is not None:
            try:
                temporary.unlink(missing_ok=True)
            except OSError:
                pass


def _ensure_safe_parent(
    root: Path, relative: str, *, create: bool = False, created_dirs: list[Path] | None = None,
) -> Path:
    target = root.joinpath(*relative.split("/"))
    current = root
    for part in relative.split("/")[:-1]:
        current = current / part
        if current.exists():
            if _is_reparse_point(current) or not current.is_dir():
                raise ProjectionWriteError
        elif create:
            current.mkdir()
            if created_dirs is not None:
                created_dirs.append(current)
    if _is_reparse_point(target) or (target.exists() and not target.is_file()):
        raise ProjectionWriteError
    return target


def _write_projection(files: Mapping[str, str], projection_dir: Path) -> None:
    """Write one rendered projection into an explicit dedicated directory.

    The manifest is the sole ownership record. Unknown files are preserved;
    only stale files listed by the previous valid manifest can be removed.
    """
    if not isinstance(files, Mapping) or not isinstance(projection_dir, Path):
        raise ProjectionWriteError
    if len(files) > _MAX_FILES:
        raise ProjectionWriteError

    encoded: dict[str, bytes] = {}
    total_bytes = 0
    for raw_path, content in files.items():
        path = _checked_relative_path(raw_path)
        if type(content) is not str:
            raise ProjectionWriteError
        try:
            data = content.encode("utf-8")
        except UnicodeEncodeError:
            raise ProjectionWriteError from None
        total_bytes += len(data)
        if total_bytes > _MAX_BYTES:
            raise ProjectionWriteError
        encoded[path] = data
    if len(encoded) != len(files):
        raise ProjectionWriteError

    root = projection_dir.absolute()
    if root == Path(root.anchor) or root.name.casefold() != "v2projection":
        raise ProjectionWriteError
    parent = root.parent
    if not parent.is_dir():
        raise ProjectionWriteError
    _reject_symlink_components(root, Path(root.anchor))
    root_created = False
    if root.exists():
        if _is_reparse_point(root) or not root.is_dir():
            raise ProjectionWriteError
    else:
        root.mkdir()
        root_created = True

    manifest_path = root / _MANIFEST
    if _is_reparse_point(manifest_path) or (manifest_path.exists() and not manifest_path.is_file()):
        raise ProjectionWriteError
    old_files: tuple[str, ...]
    if manifest_path.exists():
        try:
            old_files = _manifest_files(manifest_path.read_bytes())
        except OSError:
            raise ProjectionWriteError from None
    else:
        try:
            if next(root.iterdir(), None) is not None:
                raise ProjectionWriteError
        except OSError:
            raise ProjectionWriteError from None
        old_files = ()

    old_set = set(old_files)
    for relative in old_files:
        target = _ensure_safe_parent(root, relative)
        if target.exists() and not target.is_file():
            raise ProjectionWriteError
    for relative in encoded:
        target = _ensure_safe_parent(root, relative)
        if target.exists() and relative not in old_set:
            raise ProjectionWriteError

    manifest_bytes = (json.dumps(
        {"files": sorted(encoded), "schema_version": _SCHEMA_VERSION},
        ensure_ascii=False, sort_keys=True, separators=(",", ":"),
    ) + "\n").encode("utf-8")
    if len(manifest_bytes) > 4 * 1024 * 1024:
        raise ProjectionWriteError

    created_paths: list[Path] = []
    created_dirs: list[Path] = []
    try:
        for relative in sorted(encoded):
            target = _ensure_safe_parent(root, relative, create=True, created_dirs=created_dirs)
            if relative not in old_set:
                created_paths.append(target)
            _atomic_write(target, encoded[relative])
        for relative in sorted(old_set - set(encoded)):
            target = root.joinpath(*relative.split("/"))
            if _is_reparse_point(target):
                raise ProjectionWriteError
            if target.exists():
                if not target.is_file():
                    raise ProjectionWriteError
                target.unlink()
        _atomic_write(manifest_path, manifest_bytes)
    except (OSError, ProjectionWriteError):
        for path in reversed(created_paths):
            try:
                path.unlink(missing_ok=True)
            except OSError:
                pass
        for directory in reversed(created_dirs):
            try:
                directory.rmdir()
            except OSError:
                pass
        if root_created:
            try:
                root.rmdir()
            except OSError:
                pass
        raise ProjectionWriteError from None


def write_projection(files: Mapping[str, str], projection_dir: Path) -> None:
    """Write one rendered projection into an explicit ``V2Projection`` directory."""
    try:
        _write_projection(files, projection_dir)
    except OSError:
        raise ProjectionWriteError from None
