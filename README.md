[![UML Energy & Combustion Research Laboratory](https://sites.uml.edu/hunter-mack/files/2021/11/ECRL_final.png)](http://faculty.uml.edu/Hunter_Mack/)

# PaDELPy: A Python wrapper for PaDEL-Descriptor software

[![GitHub version](https://badge.fury.io/gh/ecrl%2Fpadelpy.svg)](https://badge.fury.io/gh/ecrl%2Fpadelpy)
[![PyPI version](https://badge.fury.io/py/padelpy.svg)](https://badge.fury.io/py/padelpy)
[![GitHub license](https://img.shields.io/github/license/ecrl/padelpy)](https://github.com/ecrl/padelpy/blob/master/LICENSE)

PaDELPy provides a Python wrapper for the
[PaDEL-Descriptor](https://pubmed.ncbi.nlm.nih.gov/21425294/) molecular
descriptor calculation software. It exposes the PaDEL-Descriptor command-line
interface to Python for computing descriptors and fingerprints from SMILES,
MDL MolFiles, and SDF files.

## Installation

Install from PyPI:

```bash
pip install padelpy
```

Or from a clone of this repository:

```bash
git clone https://github.com/ecrl/padelpy
cd padelpy
pip install .
```

**Requirements**

- Python 3.10+ (see package classifiers)
- A system [Java](https://adoptium.net/) JRE **8+** on `PATH`
  (`java -version` should succeed). Continuous integration uses Eclipse Temurin 17.

PaDEL-Descriptor is bundled with PaDELPy, so a separate PaDEL download is not
required. The project has no default Python dependencies beyond the standard
library. Wheels are large (approximately 20+ MB) because they include the
vendored PaDEL JAR and libraries.

## Related projects

PaDELPy is a thin wrapper around the PaDEL-Descriptor Java engine. Other tools
compute related molecular features with different engines or APIs:

- [Mordred](https://doi.org/10.1186/s13321-018-0258-y) — RDKit-based descriptor
  calculator (different engine and dependency stack)
- [RDKit](https://www.rdkit.org/) descriptors and fingerprints — core
  cheminformatics toolkit (different descriptor set)
- [padelpy2](https://github.com/Cognitive-Chemistry-Labs/padelpy2) — alternate
  PaDEL wrapper with an RDKit/pandas-oriented API (not drop-in compatible)

## Basic usage

PaDELPy provides helpers for SMILES, MDL MolFile, and SDF inputs, plus a
lower-level `padeldescriptor` wrapper for direct CLI control.

### SMILES to descriptors / fingerprints

`from_smiles` accepts a SMILES string or a list of SMILES strings. A single
input returns a mapping of descriptor or fingerprint names to values; a list
returns a list of such mappings.

```python
from padelpy import from_smiles

# molecular descriptors for propane
descriptors = from_smiles("CCC")

# propane and butane
descriptors = from_smiles(["CCC", "CCCC"])

# descriptors plus PubChem fingerprints
desc_fp = from_smiles("CCC", fingerprints=True)

# fingerprints only
fingerprints = from_smiles("CCC", fingerprints=True, descriptors=False)

# one worker thread
descriptors = from_smiles(["CCC", "CCCC"], threads=1)

# also write a CSV
_ = from_smiles("CCC", output_csv="descriptors.csv")
```

### MDL MolFile to descriptors / fingerprints

`from_mdl` accepts a path to an MDL MolFile and returns a list of mappings, one
per molecule in file order.

```python
from padelpy import from_mdl

descriptors = from_mdl("mols.mdl")
desc_fp = from_mdl("mols.mdl", fingerprints=True)
fingerprints = from_mdl("mols.mdl", fingerprints=True, descriptors=False)
desc_fp = from_mdl("mols.mdl", threads=1)
_ = from_mdl("mols.mdl", output_csv="descriptors.csv")
```

### SDF to descriptors / fingerprints

`from_sdf` accepts a path to an SDF file and returns a list of mappings, one per
molecule in file order.

```python
from padelpy import from_sdf

descriptors = from_sdf("mols.sdf")
desc_fp = from_sdf("mols.sdf", fingerprints=True)
fingerprints = from_sdf("mols.sdf", fingerprints=True, descriptors=False)
desc_fp = from_sdf("mols.sdf", threads=1)
_ = from_sdf("mols.sdf", output_csv="descriptors.csv")
```

### Command-line wrapper

`padeldescriptor` forwards keyword arguments to the PaDEL-Descriptor CLI.
Any combination of supported flags may be supplied.

```python
from padelpy import padeldescriptor

padeldescriptor(config="path/to/config")
padeldescriptor(mol_dir="molecules.mdl", d_file="descriptors.csv")
padeldescriptor(mol_dir="molecules.sdf", d_file="descriptors.csv")
padeldescriptor(mol_dir="molecules.smi", d_file="descriptors.csv")
padeldescriptor(mol_dir="path/to/mols/", d_file="descriptors.csv")

padeldescriptor(
    mol_dir="molecules.smi",
    d_file="descriptors.csv",
    d_2d=True,
    d_3d=True,
    fingerprints=True,
    convert3d=True,
    descriptortypes="path/to/descriptortypes",
    detectaromaticity=True,
    log=True,
    removesalt=True,
    retain3d=True,
    retainorder=True,
    standardizenitro=True,
    standardizetautomers=True,
    tautomerlist="path/to/tautomers",
    usefilenameasmolname=True,
    maxcpdperfile=32,
    maxruntime=10000,
    waitingjobs=10,
    threads=2,
    headless=True,
)
```

## Contributing, reporting issues, and support

To contribute, open a pull request. New features should include tests and clear
documentation.

To report bugs or request features, file a GitHub issue. Include error messages,
operating system, Java version (`java -version`), and Python version when
reporting problems.

For additional questions, contact Travis Kessler
([travis.j.kessler@gmail.com](mailto:travis.j.kessler@gmail.com)).
