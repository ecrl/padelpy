# Test fixtures (PaDEL engine self-consistency)

Structure files used by the PaDELPy test suite as **regression oracles** against the
**bundled** PaDEL-Descriptor JAR set shipped with this repository. Expected descriptor
counts and selected numeric values in tests are engine self-consistency anchors for that
vendored binary bundle. They are **not** independent literature reference tables.

## Contents

| File | Format | Structure | Role |
|------|--------|-----------|------|
| `aspirin_3d.sdf` | SDF (V2000) | Aspirin (PubChem CID 2244), 3D | `from_sdf` integration / golden oracles |
| `propane.mdl` | MDL Molfile (V2000) | Propane (SMILES `CCC`), heavy atoms | `from_mdl` integration / golden oracles |

## Provenance

- **`aspirin_3d.sdf`:** Existing repository test asset (OEChem-tagged SDF header; PubChem CID
  2244). Retained as a fixture when the contract suite was introduced; not regenerated for
  this modernization.
- **`propane.mdl`:** Minimal V2000 molfile constructed for tests (three carbon atoms, two
  single bonds). Intended to match the propane SMILES (`CCC`) already used in SMILES-based
  oracles.

## License and redistribution

Fixture files are small public-domain-style chemical structure records for software testing.
The PaDEL/CDK engine itself remains under its upstream licenses in
`src/padelpy/PaDEL-Descriptor/license/`.

## Limitations

- Numeric descriptor outputs depend on the **exact** bundled PaDEL/CDK JAR versions. Changing
  those JARs may invalidate oracles and requires a separate approved parity plan.
- Values may differ from other descriptor engines (for example Mordred or RDKit) for the same
  structure; cross-engine agreement is not claimed.
- `propane.mdl` omits explicit hydrogens; the engine may implicit-hydrogenate during
  calculation.

## Engine literature

PaDEL-Descriptor (the Java tool wrapped by this package):

- Yap CW. PaDEL-Descriptor: An open source software to calculate molecular descriptors and
  fingerprints. *J Comput Chem.* 2011;32(7):1466-1474.
  DOI: [10.1002/jcc.21707](https://doi.org/10.1002/jcc.21707) /
  PMID: [21425294](https://pubmed.ncbi.nlm.nih.gov/21425294/).
