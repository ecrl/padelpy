"""Lock public API parameter names and defaults (design §8.1 / §11.1)."""

from __future__ import annotations

import inspect

import pytest

from padelpy import from_mdl, from_sdf, from_smiles, padeldescriptor

_EMPTY = inspect.Parameter.empty

# Expected (name, default) in declaration order. Defaults only — not annotations.
_EXPECTED_SIGNATURES: dict[str, list[tuple[str, object]]] = {
    "from_smiles": [
        ("smiles", _EMPTY),
        ("output_csv", None),
        ("descriptors", True),
        ("fingerprints", False),
        ("timeout", 60),
        ("maxruntime", -1),
        ("threads", -1),
    ],
    "from_mdl": [
        ("mdl_file", _EMPTY),
        ("output_csv", None),
        ("descriptors", True),
        ("fingerprints", False),
        ("timeout", 60),
        ("maxruntime", -1),
        ("threads", -1),
    ],
    "from_sdf": [
        ("sdf_file", _EMPTY),
        ("output_csv", None),
        ("descriptors", True),
        ("fingerprints", False),
        ("timeout", 60),
        ("maxruntime", -1),
        ("threads", -1),
    ],
    "padeldescriptor": [
        ("maxruntime", -1),
        ("waitingjobs", -1),
        ("threads", -1),
        ("d_2d", False),
        ("d_3d", False),
        ("config", None),
        ("convert3d", False),
        ("descriptortypes", None),
        ("detectaromaticity", False),
        ("mol_dir", None),
        ("d_file", None),
        ("fingerprints", False),
        ("log", False),
        ("maxcpdperfile", 0),
        ("removesalt", False),
        ("retain3d", False),
        ("retainorder", True),
        ("standardizenitro", False),
        ("standardizetautomers", False),
        ("tautomerlist", None),
        ("usefilenameasmolname", False),
        ("sp_timeout", None),
        ("headless", True),
    ],
}

_CALLABLES = {
    "from_smiles": from_smiles,
    "from_mdl": from_mdl,
    "from_sdf": from_sdf,
    "padeldescriptor": padeldescriptor,
}


@pytest.mark.parametrize("name", list(_EXPECTED_SIGNATURES))
def test_public_signature_names_and_defaults(name: str) -> None:
    fn = _CALLABLES[name]
    expected = _EXPECTED_SIGNATURES[name]
    params = list(inspect.signature(fn).parameters.values())

    actual = [(p.name, p.default) for p in params]
    assert actual == expected, (
        f"{name} signature drift:\n  expected={expected!r}\n  actual  ={actual!r}"
    )
