#!/usr/bin/env python
#
# padelpy/functions.py
# v.0.1.10
# Developed in 2021 by Travis Kessler <travis.j.kessler@gmail.com>
#
# Contains various functions commonly used with PaDEL-Descriptor
#

# stdlib. imports
from collections import OrderedDict
from csv import DictReader
from os.path import join
from re import IGNORECASE, compile
from tempfile import TemporaryDirectory

# PaDELPy imports
from .wrapper import padeldescriptor

__all__ = [
    "from_mdl",
    "from_smiles",
    "from_sdf",
]


def _read_padel_csv_rows(csv_path: str) -> list:
    """Read descriptor rows from a PaDEL CSV file.

    Encoding strategy: decode as UTF-8. On ``UnicodeDecodeError``, raise
    ``RuntimeError`` with a clear message (same exception family as other
    PaDELPy caller-facing failures). No silent fallback encoding.
    """
    try:
        with open(csv_path, encoding="utf-8") as desc_file:
            return list(DictReader(desc_file))
    except UnicodeDecodeError as exc:
        raise RuntimeError(
            "PaDEL-Descriptor CSV is not valid UTF-8: "
            f"{csv_path}. Re-export or convert the file to UTF-8."
        ) from exc


def from_smiles(
    smiles,
    output_csv: str = None,
    descriptors: bool = True,
    fingerprints: bool = False,
    timeout: int = 60,
    maxruntime: int = -1,
    threads: int = -1,
) -> OrderedDict:
    """Convert SMILES to QSPR descriptors and/or fingerprints via PaDEL.

    Parameters
    ----------
    smiles : str or list of str
        SMILES for one molecule, or a list of SMILES strings.
    output_csv : str, optional
        If supplied, also write descriptors to this CSV path.
    descriptors : bool, default True
        If True, calculate descriptors.
    fingerprints : bool, default False
        If True, calculate fingerprints.
    timeout : int, default 60
        Maximum subprocess time in seconds.
    maxruntime : int, default -1
        Maximum running time per molecule in seconds (``-1`` = unlimited).
    threads : int, default -1
        Worker threads (``-1`` = use all available).

    Returns
    -------
    dict or list of dict
        Mapping of labels to values for a single SMILES, or a list of such
        mappings when ``smiles`` is a list.
    """
    # unit conversion for maximum running time per molecule
    # seconds -> milliseconds
    if maxruntime != -1:
        maxruntime = maxruntime * 1000

    if isinstance(smiles, str):
        smiles_text = smiles
    elif isinstance(smiles, list):
        smiles_text = "\n".join(smiles)
    else:
        raise RuntimeError(f"Unknown input format for `smiles`: {type(smiles)}")

    save_csv = output_csv is not None

    with TemporaryDirectory(prefix="padelpy_") as tmpdir:
        smi_path = join(tmpdir, "input.smi")
        with open(smi_path, "w", encoding="utf-8") as smi_file:
            smi_file.write(smiles_text)

        csv_path = output_csv if save_csv else join(tmpdir, "descriptors.csv")

        for attempt in range(3):
            try:
                padeldescriptor(
                    mol_dir=smi_path,
                    d_file=csv_path,
                    convert3d=True,
                    retain3d=True,
                    d_2d=descriptors,
                    d_3d=descriptors,
                    fingerprints=fingerprints,
                    sp_timeout=timeout,
                    retainorder=True,
                    maxruntime=maxruntime,
                    threads=threads,
                )
                break
            except RuntimeError as exception:
                if attempt == 2:
                    raise RuntimeError(exception) from exception
                continue

        rows = _read_padel_csv_rows(csv_path)

        if isinstance(smiles, list) and len(rows) != len(smiles):
            raise RuntimeError(
                "PaDEL-Descriptor failed on one or more mols."
                " Ensure the input structures are correct."
            )
        elif isinstance(smiles, str) and len(rows) == 0:
            raise RuntimeError(
                f"PaDEL-Descriptor failed on {smiles}."
                " Ensure input structure is correct."
            )

        for idx, r in enumerate(rows):
            if len(r) == 0:
                raise RuntimeError(
                    f"PaDEL-Descriptor failed on {smiles[idx]}."
                    " Ensure input structure is correct."
                )

        for idx in range(len(rows)):
            del rows[idx]["Name"]

        if isinstance(smiles, str):
            return rows[0]
        return rows


def from_mdl(
    mdl_file: str,
    output_csv: str = None,
    descriptors: bool = True,
    fingerprints: bool = False,
    timeout: int = 60,
    maxruntime: int = -1,
    threads: int = -1,
) -> list:
    """Convert an MDL MolFile to QSPR descriptors and/or fingerprints.

    Multiple molecules may appear in the MDL file.

    Parameters
    ----------
    mdl_file : str
        Path to an MDL file (``.mdl`` extension required).
    output_csv : str, optional
        If supplied, also write descriptors/fingerprints to this CSV path.
    descriptors : bool, default True
        If True, calculate descriptors.
    fingerprints : bool, default False
        If True, calculate fingerprints.
    timeout : int, default 60
        Maximum subprocess time in seconds.
    maxruntime : int, default -1
        Maximum running time per molecule in seconds (``-1`` = unlimited).
    threads : int, default -1
        Worker threads (``-1`` = use all available).

    Returns
    -------
    list of dict
        One mapping per compound, in file order.
    """

    is_mdl = compile(r".*\.mdl$", IGNORECASE)
    if is_mdl.match(mdl_file) is None:
        raise ValueError(f"MDL file must have a `.mdl` extension: {mdl_file}")

    rows = _from_mdl_lower(
        mol_file=mdl_file,
        output_csv=output_csv,
        descriptors=descriptors,
        fingerprints=fingerprints,
        timeout=timeout,
        maxruntime=maxruntime,
        threads=threads,
    )
    return rows


def from_sdf(
    sdf_file: str,
    output_csv: str = None,
    descriptors: bool = True,
    fingerprints: bool = False,
    timeout: int = 60,
    maxruntime: int = -1,
    threads: int = -1,
) -> list:
    """Convert an SDF file to QSPR descriptors and/or fingerprints.

    Multiple molecules may appear in the SDF file.

    Parameters
    ----------
    sdf_file : str
        Path to an SDF file (``.sdf`` extension required).
    output_csv : str, optional
        If supplied, also write descriptors/fingerprints to this CSV path.
    descriptors : bool, default True
        If True, calculate descriptors.
    fingerprints : bool, default False
        If True, calculate fingerprints.
    timeout : int, default 60
        Maximum subprocess time in seconds.
    maxruntime : int, default -1
        Maximum running time per molecule in seconds (``-1`` = unlimited).
    threads : int, default -1
        Worker threads (``-1`` = use all available).

    Returns
    -------
    list of dict
        One mapping per compound, in file order.
    """

    is_sdf = compile(r".*\.sdf$", IGNORECASE)
    if is_sdf.match(sdf_file) is None:
        raise ValueError(f"sdf file must have a `.sdf` extension: {sdf_file}")

    rows = _from_mdl_lower(
        mol_file=sdf_file,
        output_csv=output_csv,
        descriptors=descriptors,
        fingerprints=fingerprints,
        timeout=timeout,
        maxruntime=maxruntime,
        threads=threads,
    )
    return rows


def _from_mdl_lower(
    mol_file: str,
    output_csv: str = None,
    descriptors: bool = True,
    fingerprints: bool = False,
    timeout: int = 60,
    maxruntime: int = -1,
    threads: int = -1,
) -> list:
    # unit conversion for maximum running time per molecule
    # seconds -> milliseconds
    if maxruntime != -1:
        maxruntime = maxruntime * 1000

    save_csv = output_csv is not None

    with TemporaryDirectory(prefix="padelpy_") as tmpdir:
        csv_path = output_csv if save_csv else join(tmpdir, "descriptors.csv")

        for attempt in range(3):
            try:
                padeldescriptor(
                    maxruntime=maxruntime,
                    mol_dir=mol_file,
                    d_file=csv_path,
                    convert3d=True,
                    retain3d=True,
                    retainorder=True,
                    d_2d=descriptors,
                    d_3d=descriptors,
                    fingerprints=fingerprints,
                    sp_timeout=timeout,
                    threads=threads,
                )
                break
            except RuntimeError as exception:
                if attempt == 2:
                    raise RuntimeError(exception) from exception
                continue

        rows = _read_padel_csv_rows(csv_path)

        if len(rows) == 0:
            raise RuntimeError(
                "PaDEL-Descriptor returned no calculated values."
                + " Ensure the input structure is correct."
            )
        for row in rows:
            del row["Name"]

        return rows
