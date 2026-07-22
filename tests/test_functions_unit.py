"""Unit tests for padelpy.functions with mocked padeldescriptor (no Java)."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from unittest.mock import patch

import pytest

from padelpy import from_mdl, from_sdf, from_smiles


def _write_csv(path: str, rows: list[dict[str, str]]) -> None:
    if not rows:
        Path(path).write_text("Name,MW,nC\n")
        return
    headers = list(rows[0].keys())
    lines = [",".join(headers)]
    for row in rows:
        lines.append(",".join(row[h] for h in headers))
    Path(path).write_text("\n".join(lines) + "\n")


def _padel_writes_rows(rows: list[dict[str, str]]):
    def _side_effect(**kwargs):
        _write_csv(kwargs["d_file"], rows)

    return _side_effect


@pytest.fixture
def chdir_tmp(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    return tmp_path


@patch("padelpy.functions.padeldescriptor")
def test_from_smiles_maxruntime_seconds_to_milliseconds(mock_padel, chdir_tmp) -> None:
    mock_padel.side_effect = _padel_writes_rows(
        [{"Name": "AUTOGEN_CCC", "MW": "44.06", "nC": "3"}]
    )
    from_smiles("CCC", maxruntime=5)
    assert mock_padel.call_args.kwargs["maxruntime"] == 5000


@patch("padelpy.functions.padeldescriptor")
def test_from_mdl_maxruntime_seconds_to_milliseconds(mock_padel, tmp_path) -> None:
    mdl = tmp_path / "mol.mdl"
    mdl.write_text("propane\n\n  0  0\nM  END\n")
    out = tmp_path / "out.csv"
    mock_padel.side_effect = _padel_writes_rows(
        [{"Name": "mol", "MW": "44.06", "nC": "3"}]
    )
    from_mdl(str(mdl), output_csv=str(out), maxruntime=7)
    assert mock_padel.call_args.kwargs["maxruntime"] == 7000


@patch("padelpy.functions.padeldescriptor")
def test_from_smiles_retry_succeeds_on_third_attempt(mock_padel, chdir_tmp) -> None:
    rows = [{"Name": "AUTOGEN_CCC", "MW": "44.06", "nC": "3"}]

    def _side_effect(**kwargs):
        if mock_padel.call_count < 3:
            raise RuntimeError("transient")
        _write_csv(kwargs["d_file"], rows)

    mock_padel.side_effect = _side_effect
    result = from_smiles("CCC")
    assert mock_padel.call_count == 3
    assert isinstance(result, Mapping)
    assert result["MW"] == "44.06"
    assert "Name" not in result


@patch("padelpy.functions.padeldescriptor")
def test_from_smiles_retry_fails_after_three(mock_padel, chdir_tmp) -> None:
    mock_padel.side_effect = RuntimeError("always fails")
    with pytest.raises(RuntimeError):
        from_smiles("CCC")
    assert mock_padel.call_count == 3
    assert list(chdir_tmp.glob("*.smi")) == []
    assert list(chdir_tmp.glob("*.csv")) == []


@patch("padelpy.functions.DictReader")
@patch("padelpy.functions.padeldescriptor")
def test_from_smiles_empty_row_raises_runtime_error(
    mock_padel, mock_reader, chdir_tmp
) -> None:
    mock_padel.side_effect = _padel_writes_rows(
        [{"Name": "AUTOGEN_CCC", "MW": "44.06", "nC": "3"}]
    )
    mock_reader.return_value = [{}]
    with pytest.raises(RuntimeError, match="Ensure input structure is correct"):
        from_smiles(["CCC"])


@patch("padelpy.functions.padeldescriptor")
def test_from_mdl_retry_fails_after_three(mock_padel, tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    mdl = tmp_path / "mol.mdl"
    mdl.write_text("propane\n\n  0  0\nM  END\n")
    mock_padel.side_effect = RuntimeError("always fails")
    with pytest.raises(RuntimeError):
        from_mdl(str(mdl))  # auto temp csv → TemporaryDirectory cleanup path
    assert mock_padel.call_count == 3
    assert list(tmp_path.glob("*.csv")) == []


@patch("padelpy.functions.padeldescriptor")
def test_from_smiles_success_leaves_no_cwd_temp_files(mock_padel, chdir_tmp) -> None:
    mock_padel.side_effect = _padel_writes_rows(
        [{"Name": "AUTOGEN_CCC", "MW": "44.06", "nC": "3"}]
    )
    from_smiles("CCC")
    assert list(chdir_tmp.glob("*.smi")) == []
    assert list(chdir_tmp.glob("*.csv")) == []


@patch("padelpy.functions.padeldescriptor")
def test_from_smiles_preserves_user_output_csv(mock_padel, chdir_tmp) -> None:
    out = chdir_tmp / "user_out.csv"
    mock_padel.side_effect = _padel_writes_rows(
        [{"Name": "AUTOGEN_CCC", "MW": "44.06", "nC": "3"}]
    )
    from_smiles("CCC", output_csv=str(out))
    assert out.is_file()
    assert list(chdir_tmp.glob("*.smi")) == []


@patch("padelpy.functions.padeldescriptor")
def test_from_mdl_success_leaves_no_cwd_temp_csv(mock_padel, chdir_tmp) -> None:
    mdl = chdir_tmp / "mol.mdl"
    mdl.write_text("propane\n\n  0  0\nM  END\n")
    mock_padel.side_effect = _padel_writes_rows(
        [{"Name": "mol", "MW": "44.06", "nC": "3"}]
    )
    from_mdl(str(mdl))
    assert list(chdir_tmp.glob("*.csv")) == []
    assert mdl.is_file()


@patch("padelpy.functions.padeldescriptor")
def test_from_smiles_utf8_csv_with_non_ascii_ok(mock_padel, chdir_tmp) -> None:
    mock_padel.side_effect = _padel_writes_rows(
        [{"Name": "café", "MW": "44.06", "nC": "3"}]
    )
    result = from_smiles("CCC")
    assert result["MW"] == "44.06"


@patch("padelpy.functions.padeldescriptor")
def test_from_smiles_invalid_utf8_csv_raises_runtime_error(
    mock_padel, chdir_tmp
) -> None:
    def _write_invalid_utf8(**kwargs):
        # 0xff is invalid in UTF-8; reproduces UnicodeDecodeError class of failure
        Path(kwargs["d_file"]).write_bytes(b"Name,MW\nAUTOGEN_\xff,1.0\n")

    mock_padel.side_effect = _write_invalid_utf8
    with pytest.raises(RuntimeError, match="not valid UTF-8"):
        from_smiles("CCC")


@patch("padelpy.functions.padeldescriptor")
def test_from_mdl_invalid_utf8_csv_raises_runtime_error(mock_padel, tmp_path) -> None:
    mdl = tmp_path / "mol.mdl"
    mdl.write_text("propane\n\n  0  0\nM  END\n")
    out = tmp_path / "out.csv"

    def _write_invalid_utf8(**kwargs):
        Path(kwargs["d_file"]).write_bytes(b"Name,MW\nmol\xff,1.0\n")

    mock_padel.side_effect = _write_invalid_utf8
    with pytest.raises(RuntimeError, match="not valid UTF-8"):
        from_mdl(str(mdl), output_csv=str(out))


@patch("padelpy.functions.padeldescriptor")
def test_from_smiles_single_returns_mapping_without_name(mock_padel, chdir_tmp) -> None:
    mock_padel.side_effect = _padel_writes_rows(
        [{"Name": "AUTOGEN_CCC", "MW": "44.06", "nC": "3"}]
    )
    result = from_smiles("CCC")
    assert isinstance(result, Mapping)
    assert not isinstance(result, list)
    assert "Name" not in result
    assert result["nC"] == "3"


@patch("padelpy.functions.padeldescriptor")
def test_from_smiles_list_returns_list_without_name(mock_padel, chdir_tmp) -> None:
    mock_padel.side_effect = _padel_writes_rows(
        [
            {"Name": "a", "MW": "44.06", "nC": "3"},
            {"Name": "b", "MW": "58.08", "nC": "4"},
        ]
    )
    result = from_smiles(["CCC", "CCCC"])
    assert isinstance(result, list)
    assert len(result) == 2
    assert all("Name" not in row for row in result)
    assert result[1]["MW"] == "58.08"


def test_from_mdl_bad_extension_raises_value_error() -> None:
    with pytest.raises(ValueError, match=r"\.mdl"):
        from_mdl("x.sdf")


def test_from_sdf_bad_extension_raises_value_error() -> None:
    with pytest.raises(ValueError, match=r"\.sdf"):
        from_sdf("x.mdl")


@patch("padelpy.functions.padeldescriptor")
def test_from_mdl_removes_name_column(mock_padel, tmp_path) -> None:
    mdl = tmp_path / "mol.mdl"
    mdl.write_text("propane\n\n  0  0\nM  END\n")
    out = tmp_path / "out.csv"
    mock_padel.side_effect = _padel_writes_rows(
        [{"Name": "mol", "MW": "44.06", "nC": "3"}]
    )
    rows = from_mdl(str(mdl), output_csv=str(out))
    assert isinstance(rows, list)
    assert len(rows) == 1
    assert "Name" not in rows[0]
    assert rows[0]["MW"] == "44.06"


@patch("padelpy.functions.padeldescriptor")
def test_from_sdf_removes_name_column(mock_padel, tmp_path) -> None:
    sdf = tmp_path / "mol.sdf"
    sdf.write_text("mol\n\n  0  0\nM  END\n$$$$\n")
    out = tmp_path / "out.csv"
    mock_padel.side_effect = _padel_writes_rows(
        [{"Name": "mol", "MW": "180.04", "nC": "9"}]
    )
    rows = from_sdf(str(sdf), output_csv=str(out))
    assert isinstance(rows, list)
    assert "Name" not in rows[0]
    assert rows[0]["nC"] == "9"
