"""Release packaging tests."""

from __future__ import annotations

from pathlib import Path


def test_release_file_exists():
    assert Path("RELEASE.md").exists()


def test_package_metadata_mentions_proprietary_sdk():
    pyproject = Path("pyproject.toml").read_text(encoding="utf-8")
    assert 'name = "agent-graph-sdk"' in pyproject
    assert 'license = "LicenseRef-OpenAutonomyx-All-Rights-Reserved"' in pyproject
