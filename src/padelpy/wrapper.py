#!/usr/bin/env python
#
# padelpy/wrapper.py
# v.0.1.10
# Developed in 2021 by Travis Kessler <travis.j.kessler@gmail.com>
#
# Contains the `padeldescriptor` function, a wrapper for PaDEL-Descriptor
#

# stdlib. imports
from os.path import abspath, dirname, join
from shutil import which
from subprocess import PIPE, Popen, TimeoutExpired

# PaDEL-Descriptor is packaged with PaDELPy
_PADEL_PATH = join(
    dirname(abspath(__file__)), "PaDEL-Descriptor", "PaDEL-Descriptor.jar"
)

__all__ = [
    "padeldescriptor",
]


def _popen_timeout(command: list[str], timeout: int) -> tuple:
    """Calls PaDEL-Descriptor, with optional subprocess timeout

    Args:
        command (list[str]): argv list for subprocess.Popen
        timeout (int): if not None, times out after this many seconds

    Returns:
        tuple: (stdout of process, stderr of process)
    """

    p = Popen(command, stdout=PIPE, stderr=PIPE)
    try:
        return p.communicate(timeout=timeout)
    except TimeoutExpired:
        p.kill()
        p.communicate()
        return (-1, b"PaDEL-Descriptor timed out during subprocess call")


def padeldescriptor(
    maxruntime: int = -1,
    waitingjobs: int = -1,
    threads: int = -1,
    d_2d: bool = False,
    d_3d: bool = False,
    config: str = None,
    convert3d: bool = False,
    descriptortypes: str = None,
    detectaromaticity: bool = False,
    mol_dir: str = None,
    d_file: str = None,
    fingerprints: bool = False,
    log: bool = False,
    maxcpdperfile: int = 0,
    removesalt: bool = False,
    retain3d: bool = False,
    retainorder: bool = True,
    standardizenitro: bool = False,
    standardizetautomers: bool = False,
    tautomerlist: str = None,
    usefilenameasmolname: bool = False,
    sp_timeout: int = None,
    headless: bool = True,
) -> None:
    """Run the bundled PaDEL-Descriptor CLI with the given options.

    Parameters
    ----------
    maxruntime : int, default -1
        Maximum running time per molecule in milliseconds (``-1`` = unlimited).
    waitingjobs : int, default -1
        Maximum queued jobs for worker threads (``-1`` = PaDEL default).
    threads : int, default -1
        Maximum threads (``-1`` = number of CPU cores).
    d_2d : bool, default False
        If True, calculate 2-D descriptors.
    d_3d : bool, default False
        If True, calculate 3-D descriptors.
    config : str, optional
        Path to a configuration file.
    convert3d : bool, default False
        If True, convert molecules to 3-D.
    descriptortypes : str, optional
        Path to a descriptor-types file.
    detectaromaticity : bool, default False
        If True, re-detect aromaticity before descriptor calculation.
    mol_dir : str, optional
        Path to a structure file or directory of structures.
    d_file : str, optional
        Output CSV path for calculated descriptors/fingerprints.
    fingerprints : bool, default False
        If True, calculate fingerprints.
    log : bool, default False
        If True, write a log file alongside the descriptor file.
    maxcpdperfile : int, default 0
        Maximum compounds per descriptor file (``0`` = unlimited).
    removesalt : bool, default False
        If True, remove salts.
    retain3d : bool, default False
        If True, retain 3-D coordinates when standardizing.
    retainorder : bool, default True
        If True, retain input molecule order in the output.
    standardizenitro : bool, default False
        If True, standardize nitro groups to ``N(:O):O``.
    standardizetautomers : bool, default False
        If True, standardize tautomers.
    tautomerlist : str, optional
        Path to a SMIRKS tautomers file.
    usefilenameasmolname : bool, default False
        If True, use the filename (without extension) as the molecule name.
    sp_timeout : int, optional
        Subprocess timeout in seconds; ``None`` waits indefinitely.
    headless : bool, default True
        If True, run Java headless (no PaDEL splash window).

    Returns
    -------
    None

    Raises
    ------
    ReferenceError
        If ``java`` is not found on ``PATH``.
    RuntimeError
        If PaDEL reports an error on stderr or the subprocess times out.
    """

    if which("java") is None:
        raise ReferenceError(
            "Java not found on PATH (required for PaDEL-Descriptor). "
            "Install a Java JRE 8+ and ensure the `java` executable is available "
            "in this environment (for example, `java -version` succeeds)."
        )
    command: list[str] = ["java"]
    if headless:
        command.append("-Djava.awt.headless=true")
    command.extend(["-jar", _PADEL_PATH])
    command.extend(
        [
            "-maxruntime",
            str(maxruntime),
            "-waitingjobs",
            str(waitingjobs),
            "-threads",
            str(threads),
            "-maxcpdperfile",
            str(maxcpdperfile),
        ]
    )
    if d_2d is True:
        command.append("-2d")
    if d_3d is True:
        command.append("-3d")
    if config is not None:
        command.extend(["-config", config])
    if convert3d is True:
        command.append("-convert3d")
    if descriptortypes is not None:
        command.extend(["-descriptortypes", descriptortypes])
    if detectaromaticity is True:
        command.append("-detectaromaticity")
    if mol_dir is not None:
        command.extend(["-dir", mol_dir])
    if d_file is not None:
        command.extend(["-file", d_file])
    if fingerprints is True:
        command.append("-fingerprints")
    if log is True:
        command.append("-log")
    if removesalt is True:
        command.append("-removesalt")
    if retain3d is True:
        command.append("-retain3d")
    if retainorder is True:
        command.append("-retainorder")
    if standardizenitro is True:
        command.append("-standardizenitro")
    if standardizetautomers is True:
        command.append("-standardizetautomers")
    if tautomerlist is not None:
        command.extend(["-tautomerlist", tautomerlist])
    if usefilenameasmolname is True:
        command.append("-usefilenameasmolname")

    _, err = _popen_timeout(command, sp_timeout)
    if err != b"":
        raise RuntimeError(
            "PaDEL-Descriptor encountered an error: {}".format(err.decode("utf-8"))
        )
    return
