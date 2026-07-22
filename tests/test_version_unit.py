"""Unit tests for padelpy.version (importlib.metadata)."""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as package_version
from unittest.mock import patch

import padelpy
from padelpy import version as version_mod


def test_resolve_version_via_importlib_metadata() -> None:
    with patch.object(version_mod, "version", return_value="9.9.9") as mock_version:
        assert version_mod._resolve_version() == "9.9.9"
        mock_version.assert_called_with("padelpy")


def test_resolve_version_fallback_when_package_not_found() -> None:
    with patch.object(
        version_mod,
        "version",
        side_effect=PackageNotFoundError("padelpy"),
    ):
        assert version_mod._resolve_version() == "0.0.0+unknown"


def test_public_all_and_version_export() -> None:
    assert padelpy.__version__ == package_version("padelpy")
    assert padelpy.__version__  # non-empty package metadata version
    assert set(padelpy.__all__) == {
        "from_smiles",
        "from_mdl",
        "from_sdf",
        "padeldescriptor",
        "__version__",
    }


def test_no_pkg_resources_in_version_module() -> None:
    import inspect

    source = inspect.getsource(version_mod)
    assert "pkg_resources" not in source
