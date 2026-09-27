"""Explicit configuration; constructing it performs no I/O."""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AppConfig:
    gateway_version: str
    study_root: Path | None = None
    collection: str = "studyvault"
    expected_qmd_version: str = "2.8.3"
    history_database: Path | None = None
    asset_root: Path | None = None
    asset_database: Path | None = None
    asset_ingest_root: Path | None = None
