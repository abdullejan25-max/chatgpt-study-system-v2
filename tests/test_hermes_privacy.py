"""Hermes host artifacts must not become public source/package candidates."""

from pathlib import Path
import subprocess

import pytest


@pytest.mark.parametrize("path", [
    ".hermes/config.yaml",
    ".hermes/sessions/export.jsonl",
    ".hermes/memories/MEMORY.md",
    ".hermes/auth.json",
    "nested/.hermes/config.yaml",
])
def test_hermes_private_host_tree_is_ignored(path: str) -> None:
    root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        ["git", "check-ignore", "--no-index", path], cwd=root,
        capture_output=True, text=True, check=False,
    )
    assert result.returncode == 0, f"Hermes private artifact is not excluded: {path}"
