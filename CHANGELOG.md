# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
within the compatibility policy described in [API_STABILITY.md](API_STABILITY.md).

## [Unreleased]

### Added

- CI `audit` job running `pip-audit --strict` on the default install and
  `[dev]` extras; `pip-audit` listed under `[dev]`
- SHA-256 inventory of vendored PaDEL artifacts
  (`docs/security/vendored-artifacts.sha256`) and an expanded threat model in
  `SECURITY.md`
- GitHub private vulnerability reporting documented alongside email disclosure

### Changed

- PyPI publish workflow pins `pypa/gh-action-pypi-publish` to a full commit SHA
  (v1.14.1)

## [0.1.17] - 2026-07-22

API-compatible modernization release. Public callables remain
`from_smiles`, `from_mdl`, `from_sdf`, and `padeldescriptor`. Requires a system
Java JRE **8+** on `PATH`. Bundled PaDEL JARs are unchanged.

### Added

- Contract test suite (API signatures, golden oracles, error paths) and
  `API_STABILITY.md`
- `src/padelpy/` packaging layout, `[dev]` / `[docs]` extras, ruff, pre-commit,
  and coverage gate (≥90%)
- CI workflow for Python 3.10–3.13 with Eclipse Temurin 17 (lint, tests, docs)
  on the `release/v0.1.17` branch
- Official support for Python 3.10+ (`requires-python = ">=3.10"`)
- Packaging tests that assert PaDEL JAR and license files ship in wheels/sdists
- Sphinx + Furo documentation (installation, quickstart, API, stability policy)
  and Read the Docs config
- Governance: `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`,
  `CITATION.cff`, issue/PR templates, Dependabot
- PyPI Trusted Publishing (OIDC) publish workflow

### Changed

- Internal I/O uses secure temporary directories (no CWD pollution on success)
- PaDEL subprocess invocation uses an argv list and real
  `communicate(timeout=...)` timeouts
- CSV reads require UTF-8 and raise a clear `RuntimeError` on decode failure
- Clearer `ReferenceError` when `java` is missing from `PATH` (JRE 8+)
- README corrections (Java 8+, license badge, SDF example, `descriptortypes`,
  related-projects note)
- Version resolved via `importlib.metadata` and exported as `__version__`

### Fixed

- Public NumPy-style docstrings for Sphinx autodoc (`sphinx-build -W`)

## [0.1.16] - 2023-11-10

### Note

Baseline release prior to the API-stable modernization series.
