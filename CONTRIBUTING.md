# Contributing to padelpy

Thanks for improving padelpy. This guide covers the local workflow used by
maintainers and continuous integration.

## Prerequisites

- Python 3.10+
- A Java JRE **8+** on `PATH` (`java -version` should succeed). CI uses Eclipse
  Temurin 17 for integration tests that call the bundled PaDEL engine.
- Git

## Development setup

The package uses a `src/` layout. Install in editable mode with development
extras:

```bash
git clone https://github.com/ecrl/padelpy
cd padelpy
pip install -e ".[dev]"
```

For documentation builds, also install:

```bash
pip install -e ".[docs]"
```

Optional: install pre-commit hooks so ruff runs on commit:

```bash
pre-commit install
```

## Local verification

These commands match the CI lint, test, and docs jobs. Run them before opening
a pull request:

```bash
ruff check src tests
ruff format --check src tests
pytest tests/ --cov=padelpy --cov-report=term-missing
sphinx-build -W -b html docs/source docs/_build/html
```

Coverage must stay at or above **90%** (`fail_under` in `pyproject.toml`).
The docs job installs `.[docs]` and fails the build on Sphinx warnings.

When packaging is in scope:

```bash
python -m build
```

## Pull request checklist

- [ ] Public API unchanged unless intentionally versioned
  (`from_smiles`, `from_mdl`, `from_sdf`, `padeldescriptor`, `__version__`)
- [ ] Tests added or updated for the change; integration oracles still pass with Java
- [ ] `ruff check` / `ruff format --check` pass on `src` and `tests`
- [ ] Coverage remains ≥90%
- [ ] Docs updated when behavior or install story changes (`README.md`, Sphinx)
- [ ] No secrets or large unrelated binary churn (do not upgrade bundled PaDEL JARs
      without an approved parity plan)

## API and oracle policy

See [API_STABILITY.md](API_STABILITY.md) and the Sphinx *API stability policy*
page. Descriptor/fingerprint oracles against the bundled engine are a release
gate for the compatibility series.

## Reporting issues

Use GitHub Issues. Include error text, OS, Python version, and `java -version`
when reporting runtime failures.

## Security and supply chain

- Follow [SECURITY.md](SECURITY.md) for vulnerability reports (GitHub private
  advisories preferred; email accepted).
- CI runs `pip-audit --strict` on the default install and `[dev]` extras.
  Locally: `pip install -e ".[dev]" && pip-audit --strict`.
- Vendored PaDEL artifact digests live in
  `docs/security/vendored-artifacts.sha256`. After intentional bundle changes,
  regenerate that file and update the threat-model notes in `SECURITY.md`
  (JAR upgrades also require an approved parity plan).
- Third-party notices for the bundled PaDEL/CDK tree are summarized in
  [NOTICE](NOTICE); full license texts remain under
  `src/padelpy/PaDEL-Descriptor/license/`.
- Coverage uploads to Codecov from the Ubuntu Python 3.12 CI leg via GitHub
  Actions OIDC (`use_oidc: true`) and the Codecov GitHub App installed on
  `ecrl` (no `CODECOV_TOKEN` required).

## Publishing releases (maintainers)

PyPI uploads use **Trusted Publishing (OIDC)** via
`.github/workflows/publish_to_pypi.yml`. The workflow does not use a long-lived
`PYPI_API_TOKEN` secret.

Before the first OIDC publish for a release:

1. On PyPI, add a Trusted Publisher for project `padelpy` pointing at
   GitHub owner `ecrl`, repository `padelpy`, workflow
   `publish_to_pypi.yml`, and environment `pypi`.
2. In this GitHub repository, create an Environment named `pypi` (optional
   protection rules as desired).
3. Publish a GitHub Release; the workflow builds with `python -m build` and
   uploads via `pypa/gh-action-pypi-publish` using `id-token: write`.

If Trusted Publishing cannot be enabled for an emergency publish, that path
requires an explicit maintainer decision and a temporary token-based workflow
change — do not commit API tokens to the repository.

## Code of conduct

Participation is governed by [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
