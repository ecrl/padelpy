"""Verify sdist/wheel ship the vendored PaDEL JAR bundle."""

from __future__ import annotations

import subprocess
import sys
import tarfile
import zipfile
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
JAR_WHEEL_PATH = "padelpy/PaDEL-Descriptor/PaDEL-Descriptor.jar"
LICENSE_PREFIX = "padelpy/PaDEL-Descriptor/license/"


@pytest.fixture(scope="module")
def built_artifacts(tmp_path_factory) -> tuple[Path, Path]:
    dist_dir = tmp_path_factory.mktemp("dist")
    subprocess.run(
        [sys.executable, "-m", "build", "--outdir", str(dist_dir)],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    wheels = list(dist_dir.glob("*.whl"))
    sdists = list(dist_dir.glob("*.tar.gz"))
    assert len(wheels) == 1, f"expected one wheel, found {wheels}"
    assert len(sdists) == 1, f"expected one sdist, found {sdists}"
    return wheels[0], sdists[0]


def test_wheel_contains_padel_jar_and_licenses(
    built_artifacts: tuple[Path, Path],
) -> None:
    wheel_path, _sdist_path = built_artifacts
    with zipfile.ZipFile(wheel_path) as wheel:
        names = set(wheel.namelist())
    assert JAR_WHEEL_PATH in names
    assert any(name.startswith(LICENSE_PREFIX) for name in names)


def test_sdist_contains_padel_package_data(built_artifacts: tuple[Path, Path]) -> None:
    _wheel_path, sdist_path = built_artifacts
    with tarfile.open(sdist_path, "r:gz") as sdist:
        names = set(sdist.getnames())
    # setuptools sdist layout: padelpy-*/src/padelpy/PaDEL-Descriptor/...
    jar_members = [
        name
        for name in names
        if name.endswith("/src/padelpy/PaDEL-Descriptor/PaDEL-Descriptor.jar")
        or name.endswith("/padelpy/PaDEL-Descriptor/PaDEL-Descriptor.jar")
    ]
    assert jar_members, f"JAR missing from sdist; sample members: {sorted(names)[:20]}"
    license_members = [name for name in names if "/PaDEL-Descriptor/license/" in name]
    assert license_members
