padelpy
=======

**padelpy** is a Python wrapper for the PaDEL-Descriptor molecular descriptor
and fingerprint engine. It exposes a small public API for SMILES, MDL MolFile,
and SDF inputs, and vendors the PaDEL Java bundle so a separate PaDEL install
is not required.

A system Java JRE 8+ must be available on ``PATH``. Continuous integration uses
Eclipse Temurin 17.

Primary literature for the underlying engine:

- Yap CW. PaDEL-Descriptor: An open source software to calculate molecular
  descriptors and fingerprints. *J Comput Chem.* 2011;32(7):1466-1474.
  DOI: `10.1002/jcc.21707 <https://doi.org/10.1002/jcc.21707>`_ /
  PMID: `21425294 <https://pubmed.ncbi.nlm.nih.gov/21425294/>`_.

.. toctree::
   :maxdepth: 2
   :caption: Contents

   installation
   quickstart
   api
   api_stability
