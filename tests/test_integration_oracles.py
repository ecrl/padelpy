"""Golden descriptor oracles against the bundled PaDEL engine (Java required)."""

from __future__ import annotations

from collections.abc import Mapping

import pytest

from padelpy import from_mdl, from_sdf, from_smiles, padeldescriptor
from reference_oracles import (
    ASPIRIN,
    ASPIRIN_SDF,
    BUTANE,
    DESCRIPTOR_COUNT,
    FINGERPRINT_COUNT,
    FINGERPRINT_KEY_SUBSET,
    PROPANE,
    PROPANE_MDL,
    TOL,
)

pytestmark = pytest.mark.integration


def _assert_descriptor_row(
    row: Mapping, *, mw: float, n_c: int, ssch3: float | None = None
) -> None:
    assert len(row) == DESCRIPTOR_COUNT
    assert float(row["MW"]) == pytest.approx(mw, TOL)
    assert int(row["nC"]) == n_c
    if ssch3 is not None:
        assert float(row["SsCH3"]) == pytest.approx(ssch3, TOL)


def test_from_smiles_single_propane_oracle() -> None:
    descriptors = from_smiles(PROPANE["smiles"])
    # Live API returns a plain dict row (not list).
    # Design §8.2 mentions OrderedDict historically.
    assert isinstance(descriptors, Mapping)
    assert not isinstance(descriptors, list)
    _assert_descriptor_row(descriptors, mw=PROPANE["MW"], n_c=PROPANE["nC"])


def test_from_smiles_multi_propane_butane_oracle() -> None:
    rows = from_smiles([PROPANE["smiles"], BUTANE["smiles"]])
    assert isinstance(rows, list)
    assert len(rows) == 2
    _assert_descriptor_row(rows[0], mw=PROPANE["MW"], n_c=PROPANE["nC"])
    _assert_descriptor_row(rows[1], mw=BUTANE["MW"], n_c=BUTANE["nC"])


def test_from_sdf_aspirin_oracle() -> None:
    rows = from_sdf(str(ASPIRIN_SDF))
    assert isinstance(rows, list)
    assert len(rows) >= 1
    _assert_descriptor_row(
        rows[0],
        mw=ASPIRIN["MW"],
        n_c=ASPIRIN["nC"],
        ssch3=ASPIRIN["SsCH3"],
    )


def test_from_mdl_propane_oracle() -> None:
    rows = from_mdl(str(PROPANE_MDL))
    assert isinstance(rows, list)
    assert len(rows) == 1
    assert isinstance(rows[0], Mapping)
    assert "Name" not in rows[0]
    _assert_descriptor_row(rows[0], mw=PROPANE["MW"], n_c=PROPANE["nC"])


def test_from_mdl_bad_extension_raises_value_error() -> None:
    with pytest.raises(ValueError):
        from_mdl(str(ASPIRIN_SDF))  # .sdf is not .mdl


def test_from_mdl_empty_file_raises_runtime_error(tmp_path) -> None:
    empty_mdl = tmp_path / "empty.mdl"
    empty_mdl.write_text("")
    with pytest.raises(RuntimeError):
        from_mdl(str(empty_mdl))


def test_from_smiles_fingerprint_only_propane() -> None:
    """Happy-path fingerprint contract (issue #58 triage)."""
    fps = from_smiles(
        PROPANE["smiles"],
        descriptors=False,
        fingerprints=True,
    )
    assert isinstance(fps, Mapping)
    assert not isinstance(fps, list)
    assert len(fps) == FINGERPRINT_COUNT
    for key in FINGERPRINT_KEY_SUBSET:
        assert key in fps


def test_padeldescriptor_smoke_writes_csv(tmp_path) -> None:
    smi_path = tmp_path / "mol.smi"
    csv_path = tmp_path / "descriptors.csv"
    smi_path.write_text(PROPANE["smiles"] + "\n")

    result = padeldescriptor(
        mol_dir=str(smi_path),
        d_file=str(csv_path),
        convert3d=True,
        retain3d=True,
        d_2d=True,
        d_3d=True,
        fingerprints=False,
        retainorder=True,
    )

    assert result is None
    assert csv_path.is_file()
    assert csv_path.stat().st_size > 0
    # headless=True / retainorder=True defaults remain locked by TA.2 signatures.
