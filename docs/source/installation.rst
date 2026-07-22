Installation
============

Install **padelpy** from PyPI:

.. code-block:: bash

   pip install padelpy

Or from a clone of the repository:

.. code-block:: bash

   git clone https://github.com/ecrl/padelpy
   cd padelpy
   pip install .

Requirements
------------

- Python 3.10 or newer (see package classifiers)
- A system Java JRE **8+** on ``PATH`` such that ``java -version`` succeeds

Continuous integration uses Eclipse Temurin 17. A convenient source of JREs is
`Adoptium <https://adoptium.net/>`_.

PaDEL-Descriptor is bundled with padelpy, so a separate PaDEL download is not
required. The project has no default Python dependencies beyond the standard
library. Distribution wheels are large (approximately 20+ MB) because they
include the vendored PaDEL JAR and supporting libraries.

Missing Java raises ``ReferenceError`` from :func:`padelpy.padeldescriptor`
(and from helpers that call it). See :doc:`api_stability` for the runtime
prerequisite and known limitations.

Optional extras
---------------

Development tooling:

.. code-block:: bash

   pip install -e ".[dev]"

Documentation build dependencies:

.. code-block:: bash

   pip install -e ".[docs]"
