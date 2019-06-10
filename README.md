[![UML Energy & Combustion Research Laboratory](http://faculty.uml.edu/Hunter_Mack/uploads/9/7/1/3/97138798/1481826668_2.png)](http://faculty.uml.edu/Hunter_Mack/)

# PaDELPy: A Python wrapper for PaDEL-Descriptor software

[![GitHub version](https://badge.fury.io/gh/ecrl%2Fpadelpy.svg)](https://badge.fury.io/gh/ecrl%2Fpadelpy)
[![PyPI version](https://badge.fury.io/py/padelpy.svg)](https://badge.fury.io/py/padelpy)
[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/ecrl/padelpy/master/LICENSE.txt)
[![Build Status](https://dev.azure.com/travisjkessler/uml.ecrl/_apis/build/status/ECRL.PaDELPy?branchName=master)](https://dev.azure.com/travisjkessler/uml.ecrl/_build/latest?definitionId=2&branchName=master)

PaDELPy provides a Python wrapper for the [PaDEL-Descriptor](http://www.yapcwsoft.com/dd/padeldescriptor/) molecular descriptor calculation software. It was created to allow direct access to the PaDEL-Descriptor command-line interface via Python.

## Installation

Installation via pip:

```
$ pip install padelpy
```

Installation via cloned repository:

```
$ git clone https://github.com/ecrl/padelpy
$ cd padelpy
$ python setup.py install
```

PaDEL-Descriptor is bundled into PaDELPy, therefore an external installation/download of PaDEL-Descriptor is not necessary. There are currently no additional Python dependencies for PaDELPy, however it requires an installation of the [Java JRE](https://www.oracle.com/technetwork/java/javase/downloads/jre8-downloads-2133155.html) version 6+.

## Basic Usage

In addition to providing a complete interface between Python and PaDEL-Descriptor's command line tool, PaDELPy offers two functions to acquire descriptors/fingerprints within Python - obtaining descriptors/fingerprints from a SMILES string, and obtaining descriptors/fingerprints from an MDL MolFile.

### SMILES to Descriptors/Fingerprints

The "from_smiles" function accepts a SMILES string as an argument, and returns a Python dictionary with descriptor/fingerprint names/values as keys/values respectively.

```python
from padelpy import from_smiles

# calculate molecular descriptors for propane
descriptors = from_smiles('CCC')

# in addition to descriptors, calculate PubChem fingerprints
desc_fp = from_smiles('CCC', fingerprints=True)

# only calculate fingerprints
fingerprints = from_smiles('CCC', fingerprints=True, descriptors=False)

# save descriptors to a CSV file
_ = from_smiles('CCC', output_csv='descriptors.csv')
```

### MDL MolFile to Descriptors/Fingerprints

The "from_mdl" function accepts a filepath (to an MDL MolFile) as an argument, and returns a list. Each list element is a dictionary with descriptors/fingerprints corresponding to each supplied molecule (indexed as they appear in the MolFile).

```python
from padelpy import from_mdl

# calculate molecular descriptors for molecules in `mols.mdl`
descriptors = from_mdl('mols.mdl')

# in addition to descriptors, calculate PubChem fingerprints
desc_fp = from_mdl('mols.mdl', fingerprints=True)

# only calculate fingerprints
fingerprints = from_mdl('mols.mdl', fingerprints=True, descriptors=False)

# save descriptors to a CSV file
_ = from_mdl('mols.mdl', output_csv='descriptors.csv')
```

### Command Line Wrapper

Alternatively, you can have more control over PaDEL-Descriptor with the command-line wrapper function. Any combination of arguments supported by PaDEL-Descriptor can be accepted by the "padeldescriptor" function.

```python
from padelpy import padeldescriptor

# to supply a configuration file
padeldescriptor(config='\\path\\to\\config')

# to supply an input and output file
padeldescriptor(mol_dir='molecules.mdl', d_file='descriptors.csv')

# a SMILES file can be supplied
padeldescriptor(mol_dir='molecules.smi', d_file='descriptors.csv')

# a path to a directory containing structural files can be supplied
padeldescriptor(mol_dir='\\path\\to\\mols\\', d_file='descriptors.csv')

# to calculate 2-D and 3-D descriptors
padeldescriptor(d_2d=True, d_3d=True)

# to calculate PubChem fingerprints
padeldescriptor(fingerprints=True)

# to convert molecule into a 3-D structure
padeldescriptor(convert3d=True)

# to supply a descriptortypes file
padeldescriptor(descriptortype='\\path\\to\\descriptortypes')

# to detect aromaticity
padeldescriptor(detectaromaticity=True)

# to calculate fingerprints
padeldescriptor(fingerprints=True)

# to save process status to a log file
padeldescriptor(log=True)

# to remove salts from the molecule(s)
padeldescriptor(removesalt=True)

# to retain 3-D coordinates when standardizing
padeldescriptor(retain3d=True)

# to retain order (output same order as input)
padeldescriptor(retainorder=True)

# to standardize nitro groups to N(:O):O
padeldescriptor(standardizenitro=True)

# to standardize tautomers
padeldescriptor(standardizetautomers=True)

# to specify a SMIRKS tautomers file
padeldescriptor(tautomerlist='\\path\\to\\tautomers\\')

# to use filenames as molecule names
padeldescriptor(usefilenamesasmolname=True)

# to set the maximum number of compounds in a resulting descriptors file
padeldescriptor(maxcpdperfile=32)

# to set the maximum runtime (in mS) per molecule
padeldescriptor(maxruntime=10000)

# to set the maximum number of waiting jobs in the queue
padeldescriptor(waitingjobs=10)

# to set the maximum number of threads used
padeldescriptor(threads=2)
```

## Contributing, Reporting Issues and Other Support

To contribute to PaDELPy, make a pull request. Contributions should include tests for new features added, as well as extensive documentation.

To report problems with the software or feature requests, file an issue. When reporting problems, include information such as error messages, your OS/environment and Python version.

For additional support/questions, contact Travis Kessler (Travis_Kessler@student.uml.edu).
