"""Documented failure-type contracts (design §8.2 / §11.1)."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from padelpy import from_mdl, from_sdf, from_smiles, padeldescriptor


@pytest.mark.integration
def test_invalid_smiles_single_raises_runtime_error() -> None:
    with pytest.raises(RuntimeError):
        from_smiles("SJLDFGSJ")


@pytest.mark.integration
def test_invalid_smiles_in_list_raises_runtime_error() -> None:
    with pytest.raises(RuntimeError):
        from_smiles(["SJLDFGSJ", "CCC"])


def test_bad_smiles_type_raises_runtime_error() -> None:
    with pytest.raises(RuntimeError, match="Unknown input format for `smiles`"):
        from_smiles(123)  # type: ignore[arg-type]


def test_from_mdl_bad_extension_raises_value_error() -> None:
    with pytest.raises(ValueError, match=r"\.mdl"):
        from_mdl("molecule.sdf")


def test_from_sdf_bad_extension_raises_value_error() -> None:
    with pytest.raises(ValueError, match=r"\.sdf"):
        from_sdf("molecule.mdl")


def test_padeldescriptor_missing_java_raises_reference_error() -> None:
    with patch("padelpy.wrapper.which", return_value=None):
        with pytest.raises(ReferenceError, match="Java not found on PATH") as exc_info:
            padeldescriptor(mol_dir="unused.smi", d_file="unused.csv")
    msg = str(exc_info.value)
    assert "JRE 8+" in msg
    assert "java -version" in msg


def test_from_smiles_missing_java_raises_reference_error() -> None:
    with patch("padelpy.wrapper.which", return_value=None):
        with pytest.raises(ReferenceError, match="Java not found on PATH"):
            from_smiles("CCC")


def test_timeout_runtime_error_mentions_stable_timeout_text() -> None:
    """Regression lock for #45-style hangs: timeout surfaces as RuntimeError."""
    timeout_stderr = b"PaDEL-Descriptor timed out during subprocess call"
    with patch("padelpy.wrapper.which", return_value="/usr/bin/java"):
        with patch(
            "padelpy.wrapper._popen_timeout",
            return_value=(-1, timeout_stderr),
        ):
            with pytest.raises(
                RuntimeError, match="PaDEL-Descriptor encountered an error:"
            ) as exc_info:
                padeldescriptor(mol_dir="unused.smi", d_file="unused.csv", sp_timeout=1)
    assert "timed out during subprocess call" in str(exc_info.value)
