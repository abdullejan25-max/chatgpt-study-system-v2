"""P13 raw archives and receipts must not be public Git candidates."""

from pathlib import Path
import subprocess

import pytest


@pytest.mark.parametrize("path", [
    "export-copy.jsonl", "nested/session-copy.jsonl", "renamed-export.zip",
    "migration-receipts/import.json", "nested/migration-ledger/inventory.json",
    "private-migration/raw.json", "exports/conversations.json",
    "nested/result.receipt.json", "gemini-exports/MyActivity.json",
])
def test_private_p13_artifacts_are_excluded(path):
    root = Path(__file__).resolve().parents[1]
    result = subprocess.run(["git", "check-ignore", "--no-index", path], cwd=root,
                            capture_output=True, text=True)
    assert result.returncode == 0, f"Private migration artifact not excluded: {path}"
