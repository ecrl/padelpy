"""Unit tests for padelpy.wrapper with mocked subprocess (no Java)."""

from __future__ import annotations

from subprocess import PIPE, TimeoutExpired
from unittest.mock import MagicMock, patch

import pytest

from padelpy.wrapper import _PADEL_PATH, _popen_timeout, padeldescriptor

_ERROR_PREFIX = "PaDEL-Descriptor encountered an error:"
_TIMEOUT_STDERR = b"PaDEL-Descriptor timed out during subprocess call"


def _assert_flag_value(argv: list[str], flag: str, value: str) -> None:
    idx = argv.index(flag)
    assert argv[idx + 1] == value


@patch("padelpy.wrapper.which", return_value="/usr/bin/java")
@patch("padelpy.wrapper._popen_timeout", return_value=(b"", b""))
def test_padeldescriptor_kitchen_sink_flags(mock_popen, _mock_which) -> None:
    result = padeldescriptor(
        maxruntime=1000,
        waitingjobs=2,
        threads=4,
        d_2d=True,
        d_3d=True,
        config="/tmp/config.txt",
        convert3d=True,
        descriptortypes="/tmp/types.xml",
        detectaromaticity=True,
        mol_dir="/tmp/mols with spaces",
        d_file="/tmp/out.csv",
        fingerprints=True,
        log=True,
        maxcpdperfile=10,
        removesalt=True,
        retain3d=True,
        retainorder=True,
        standardizenitro=True,
        standardizetautomers=True,
        tautomerlist="/tmp/tautomers.txt",
        usefilenameasmolname=True,
        sp_timeout=30,
        headless=True,
    )

    assert result is None
    mock_popen.assert_called_once()
    argv, timeout = mock_popen.call_args.args
    assert timeout == 30
    assert isinstance(argv, list)
    assert argv[0] == "java"
    assert "-Djava.awt.headless=true" in argv
    assert argv[argv.index("-jar") + 1] == _PADEL_PATH
    _assert_flag_value(argv, "-maxruntime", "1000")
    _assert_flag_value(argv, "-waitingjobs", "2")
    _assert_flag_value(argv, "-threads", "4")
    _assert_flag_value(argv, "-maxcpdperfile", "10")  # forwarded; see issue #56 triage
    assert "-2d" in argv
    assert "-3d" in argv
    _assert_flag_value(argv, "-config", "/tmp/config.txt")
    assert "-convert3d" in argv
    _assert_flag_value(argv, "-descriptortypes", "/tmp/types.xml")
    assert "-detectaromaticity" in argv
    _assert_flag_value(argv, "-dir", "/tmp/mols with spaces")
    _assert_flag_value(argv, "-file", "/tmp/out.csv")
    assert "-fingerprints" in argv
    assert "-log" in argv
    assert "-removesalt" in argv
    assert "-retain3d" in argv
    assert "-retainorder" in argv
    assert "-standardizenitro" in argv
    assert "-standardizetautomers" in argv
    _assert_flag_value(argv, "-tautomerlist", "/tmp/tautomers.txt")
    assert "-usefilenameasmolname" in argv


@patch("padelpy.wrapper.which", return_value="/usr/bin/java")
@patch("padelpy.wrapper._popen_timeout", return_value=(b"", b""))
def test_padeldescriptor_headless_false(mock_popen, _mock_which) -> None:
    padeldescriptor(headless=False, mol_dir="/tmp/m", d_file="/tmp/o.csv")
    argv, _timeout = mock_popen.call_args.args
    assert isinstance(argv, list)
    assert "-Djava.awt.headless=true" not in argv
    assert argv[:3] == ["java", "-jar", _PADEL_PATH]
    assert "-retainorder" in argv  # default True


@patch("padelpy.wrapper.which", return_value="/usr/bin/java")
@patch(
    "padelpy.wrapper._popen_timeout",
    return_value=(-1, _TIMEOUT_STDERR),
)
def test_padeldescriptor_timeout_raises_runtime_error_with_prefix(
    _mock_popen, _mock_which
) -> None:
    with pytest.raises(RuntimeError, match=_ERROR_PREFIX) as exc_info:
        padeldescriptor(mol_dir="/tmp/m", d_file="/tmp/o.csv", sp_timeout=1)
    assert "timed out during subprocess call" in str(exc_info.value)


@patch("padelpy.wrapper.Popen")
def test_popen_timeout_kills_and_returns_timeout_stderr(mock_popen_cls) -> None:
    proc = MagicMock()
    proc.communicate.side_effect = [
        TimeoutExpired(cmd=["java"], timeout=2),
        (b"", b""),  # drain after kill
    ]
    mock_popen_cls.return_value = proc

    argv = ["java", "-jar", "/tmp/fake.jar"]
    stdout, stderr = _popen_timeout(argv, timeout=2)

    assert stdout == -1
    assert stderr == _TIMEOUT_STDERR
    mock_popen_cls.assert_called_once_with(argv, stdout=PIPE, stderr=PIPE)
    proc.communicate.assert_any_call(timeout=2)
    proc.kill.assert_called_once()
    assert proc.communicate.call_count == 2


@patch("padelpy.wrapper.Popen")
def test_popen_timeout_none_uses_communicate(mock_popen_cls) -> None:
    proc = MagicMock()
    proc.communicate.return_value = (b"out", b"")
    mock_popen_cls.return_value = proc

    argv = ["java", "-jar", "/tmp/fake.jar"]
    stdout, stderr = _popen_timeout(argv, timeout=None)

    assert stdout == b"out"
    assert stderr == b""
    mock_popen_cls.assert_called_once_with(argv, stdout=PIPE, stderr=PIPE)
    proc.communicate.assert_called_once_with(timeout=None)
    proc.kill.assert_not_called()
