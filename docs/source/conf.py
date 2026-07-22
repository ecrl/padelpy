"""Sphinx configuration for padelpy."""

from __future__ import annotations

import sys
from datetime import UTC, datetime
from pathlib import Path

# Editable / src layout for autodoc
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

project = "padelpy"
author = "Travis Kessler"
copyright = f"{datetime.now(UTC).year}, {author}"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx_copybutton",
]

templates_path = ["_templates"]
exclude_patterns = []

html_theme = "furo"
html_static_path = ["_static"]

autodoc_typehints = "description"
napoleon_google_docstring = False
napoleon_numpy_docstring = True

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}
