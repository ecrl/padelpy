API stability policy
====================

This page states the public API contract for **padelpy** and how version numbers
relate to compatible change. The repository root file ``API_STABILITY.md``
mirrors this policy for contributors who browse the source tree.

Frozen public surface
---------------------

The following callables are the supported import surface and must remain
drop-in compatible within a compatibility series:

.. code-block:: python

   from padelpy import from_smiles, from_mdl, from_sdf, padeldescriptor

Parameter **names** and **defaults** for these callables are frozen. Additive
optional keyword arguments may be introduced when they do not change existing
call sites. Renaming callables, making new arguments required, changing primary
return container types, or changing documented exception types for existing
failure modes requires an explicit, versioned compatibility decision.

Version export
~~~~~~~~~~~~~~

``padelpy.__version__`` is part of the public surface (resolved from package
metadata).

Versioning
----------

1. **Patch (``0.1.x``):** bugfixes, tooling, internal hardening, and
   documentation that preserve the frozen API. Descriptor and fingerprint
   **oracles must match**. The API-stable modernization program ships as
   **``0.1.17``** after its planned phases complete.
2. **Minor (``0.2.0`` and later):** reserved for future additive, still
   API-compatible work after ``0.1.17``. Oracles must match.
3. **Major (``1.0.0`` or higher):** only after an explicit stability promise;
   preferably still API-compatible. Upgrades to the bundled PaDEL/CDK JAR set,
   or intentional changes to the descriptor/fingerprint schema, require
   dual-run numeric parity evidence and a clear migration note.

Oracle parity as a release gate
-------------------------------

Regression oracles in the test suite (fixed SMILES, SDF, and MDL fixtures
against the **bundled** PaDEL-Descriptor engine) are part of the compatibility
contract for the ``0.1.x`` / subsequent compatible series. Releases that alter
public call behavior or descriptor outputs beyond documented tolerances must
not proceed without updating the versioning story above and recording parity
evidence.

Fixture values are engine self-consistency anchors for the vendored JAR set,
not independent literature tables, unless explicitly expanded later.

Runtime prerequisite
--------------------

padelpy shells out to a system ``java`` executable. A Java JRE **8+** must be
installed and discoverable on ``PATH`` (``java -version`` in the same
environment). Missing Java raises ``ReferenceError`` from
:func:`padelpy.padeldescriptor` (and from helpers that call it).

Known limitations
-----------------

These items are tracked for maintainer clarity. They do not change the frozen
API. See the corresponding GitHub issues for discussion history.

* `#55 <https://github.com/ecrl/padelpy/issues/55>`_ — Missing Java:
  clearer ``ReferenceError`` messaging (JRE 8+, ``PATH`` check).
* `#45 <https://github.com/ecrl/padelpy/issues/45>`_ — Hang/timeout on some
  structures: real subprocess timeouts; some inputs remain expensive inside
  PaDEL until timeout.
* `#51 <https://github.com/ecrl/padelpy/issues/51>`_ — Mid-batch
  ``RuntimeError``: per-structure engine failures; callers should catch or
  pre-validate.
* `#56 <https://github.com/ecrl/padelpy/issues/56>`_ — Fingerprint batch caps:
  split inputs; ``maxcpdperfile`` is forwarded but engine/XML limits may apply.
* `#58 <https://github.com/ecrl/padelpy/issues/58>`_ — Some SMILES fail
  fingerprint/descriptor calculation (engine/input limitation).
* `#29 <https://github.com/ecrl/padelpy/issues/29>`_ — Cross-run descriptor
  inconsistency for some keys (PaDEL upstream); prefer ``threads=1`` when
  bit-identical repeats are required.
* `#37 <https://github.com/ecrl/padelpy/issues/37>`_ — MOF / complex SDF
  failures often outside PaDEL/CDK scope.

Related engine citation
-----------------------

PaDEL-Descriptor (the Java tool wrapped by this package):

- Yap CW. PaDEL-Descriptor: An open source software to calculate molecular
  descriptors and fingerprints. *J Comput Chem.* 2011;32(7):1466-1474.
  DOI: `10.1002/jcc.21707 <https://doi.org/10.1002/jcc.21707>`_ /
  PMID: `21425294 <https://pubmed.ncbi.nlm.nih.gov/21425294/>`_.
