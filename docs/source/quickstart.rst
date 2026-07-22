Quickstart
==========

padelpy wraps the PaDEL-Descriptor Java engine
(Yap, 2011; DOI `10.1002/jcc.21707 <https://doi.org/10.1002/jcc.21707>`_).
Ensure Java 8+ is on ``PATH`` before calling the API (see :doc:`installation`).

Descriptors from SMILES
-----------------------

.. code-block:: python

   from padelpy import from_smiles

   descriptors = from_smiles("CCC")
   print(descriptors["MW"], descriptors["nC"])

   # list input → list of mappings
   rows = from_smiles(["CCC", "CCCC"])

   # PubChem fingerprints only
   fps = from_smiles("CCC", fingerprints=True, descriptors=False)

MDL and SDF files
-----------------

.. code-block:: python

   from padelpy import from_mdl, from_sdf

   mdl_rows = from_mdl("mols.mdl")
   sdf_rows = from_sdf("mols.sdf")

Lower-level CLI wrapper
-----------------------

.. code-block:: python

   from padelpy import padeldescriptor

   padeldescriptor(
       mol_dir="molecules.smi",
       d_file="descriptors.csv",
       d_2d=True,
       d_3d=True,
       retainorder=True,
       headless=True,
   )

Full signatures appear in :doc:`api`. Compatibility expectations are described
in :doc:`api_stability`.
