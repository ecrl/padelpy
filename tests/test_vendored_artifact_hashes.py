"""Integrity checks for the vendored PaDEL artifact SHA-256 inventory."""

from __future__ import annotations

import hashlib
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
_HASH_FILE = _REPO_ROOT / "docs" / "security" / "vendored-artifacts.sha256"


def test_vendored_artifact_sha256_inventory() -> None:
    assert _HASH_FILE.is_file(), f"missing hash inventory: {_HASH_FILE}"
    lines = [
        line.strip()
        for line in _HASH_FILE.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    ]
    assert lines, "hash inventory is empty"

    for line in lines:
        digest, rel_path = line.split(maxsplit=1)
        path = _REPO_ROOT / rel_path
        assert path.is_file(), f"missing vendored path listed in inventory: {rel_path}"
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        assert actual == digest, f"SHA-256 mismatch for {rel_path}"
