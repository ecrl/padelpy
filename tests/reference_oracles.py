"""Bundled-PaDEL regression oracle anchors for integration tests.

Values are engine self-consistency references for the vendored PaDEL-Descriptor
JAR set, not independent literature tables. See ``tests/fixtures/README.md``.

Numeric comparisons use ``pytest.approx(..., TOL)`` at assertion time only;
descriptor CSV fields remain strings in the public API.
"""

from __future__ import annotations

from pathlib import Path

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"

# Default 1D/2D descriptor mode (fingerprints off)
DESCRIPTOR_COUNT = 1875

# Fingerprint-only mode (descriptors=False, fingerprints=True) — PubChem FP count
FINGERPRINT_COUNT = 881
FINGERPRINT_KEY_SUBSET = (
    "PubchemFP0",
    "PubchemFP1",
    "PubchemFP2",
    "PubchemFP3",
)

# Tolerance consistent with historical padelpy tests (design §11.4)
TOL = 1e-4

ASPIRIN_SDF = FIXTURES_DIR / "aspirin_3d.sdf"
PROPANE_MDL = FIXTURES_DIR / "propane.mdl"

# Propane — SMILES CCC (also intended for propane.mdl in TA.4)
PROPANE = {
    "smiles": "CCC",
    "MW": 44.0626,
    "nC": 3,
}

# Butane — SMILES CCCC
BUTANE = {
    "smiles": "CCCC",
    "MW": 58.07825,
    "nC": 4,
}

# Aspirin — tests/fixtures/aspirin_3d.sdf (PubChem CID 2244)
ASPIRIN = {
    "MW": 180.04225,
    "nC": 9,
    "SsCH3": 1.2209,
}
