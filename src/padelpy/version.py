"""Package version resolved from installed distribution metadata."""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version


def _resolve_version() -> str:
    try:
        return version("padelpy")
    except PackageNotFoundError:
        return "0.0.0+unknown"


__version__ = _resolve_version()
