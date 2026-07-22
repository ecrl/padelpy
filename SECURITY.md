# Security policy

## Supported versions

Security fixes are considered for the latest published release on PyPI and for
the active modernization line targeting `0.1.17`. Older patch lines may not
receive backports.

## Reporting a vulnerability

Please **do not** open a public GitHub issue for security vulnerabilities.

Prefer GitHub’s private vulnerability reporting for
[ecrl/padelpy](https://github.com/ecrl/padelpy/security/advisories/new).
That path creates a private advisory draft maintainers can triage without
public disclosure.

Alternatively, report by email to
[travis.j.kessler@gmail.com](mailto:travis.j.kessler@gmail.com) with:

- A description of the issue and its impact
- Steps to reproduce, or a proof of concept if available
- Affected versions / commit hashes if known

You should receive an acknowledgment within a few business days. We will
coordinate a fix and disclosure timeline as appropriate.

## Threat model

padelpy is a thin local wrapper. Typical use is a researcher or pipeline
invoking descriptor calculation on inputs they already control. It is not a
network service and does not expose an HTTP API.

### Trust boundaries

| Boundary | Assumptions |
|----------|-------------|
| Caller | Controls SMILES/MDL/SDF content and optional filesystem paths passed to `padeldescriptor` (`config`, `mol_dir`, `d_file`, `descriptortypes`, `tautomerlist`). Path arguments are forwarded to the PaDEL CLI as local trusted inputs, not as a sandbox. |
| Wrapper | Builds a Java argv list (no shell), writes temporary structure files under a process-private temporary directory, and optionally enforces a subprocess timeout. |
| System Java | The `java` executable on `PATH` is trusted. A compromised or unexpected JRE is outside padelpy’s control. |
| Vendored PaDEL/CDK | Bundled JARs under `src/padelpy/PaDEL-Descriptor/` execute as part of descriptor calculation. Bytecode behavior and upstream library CVEs may affect the process; see below. |

### Likely vs unlikely risks

- **In scope for padelpy:** wrapper command construction, temporary-file handling,
  packaging/supply-chain of the Python distribution, and publish CI integrity.
- **Often upstream / environmental:** PaDEL hangs or crashes on particular
  structures; CVEs in Guava/CDK/other bundled libraries that require attack
  patterns PaDEL does not expose (for example remote deserialization); a
  malicious or mismatched system `java`.
- **Caller responsibility:** Do not pass untrusted path arguments into
  `padeldescriptor` in multi-tenant or web-facing services without an outer
  sandbox. Prefer `from_smiles` / `from_mdl` / `from_sdf` with timeouts when
  wrapping user-supplied chemical structures.

Issues that are solely upstream PaDEL/CDK behavior may be documented as
limitations rather than treated as padelpy vulnerabilities; still report them
if you believe they create a security risk through this wrapper.

## Vendored Java artifacts

Each wheel and sdist ships the PaDEL-Descriptor tree (approximately 23 MB),
including third-party JARs such as CDK and Guava. Descriptor numeric parity for
the `0.1.x` compatibility series depends on this frozen bundle; upgrades require
an approved dual-run parity plan (see `docs/design/DESIGN.md`).

### Integrity

SHA-256 digests for bundled jars and supporting data files are recorded in
[`docs/security/vendored-artifacts.sha256`](docs/security/vendored-artifacts.sha256).
Paths are relative to the repository root. Verify a checkout with:

```bash
shasum -a 256 -c docs/security/vendored-artifacts.sha256
```

Regenerate after any intentional change to the vendored tree:

```bash
find src/padelpy/PaDEL-Descriptor -type f \( -name '*.jar' -o -name '*.xml' -o -name '*.xls' \) \
  | sort \
  | xargs shasum -a 256 \
  > docs/security/vendored-artifacts.sha256
```

### Advisory posture

Some bundled libraries are old relative to current upstream releases (for
example Guava 17.0). Public advisories may list those versions as affected even
when a practical exploit path through the PaDEL CLI is unlikely. Until a
parity-gated JAR modernization lands, treat such findings as known supply-chain
debt: report them privately if you have evidence of impact via padelpy, and
prefer process isolation when running padelpy on untrusted chemical inputs in
shared environments.

## Python dependency auditing

Runtime padelpy installs have no Python dependencies beyond the standard
library. Development and CI use `pip-audit` on the installed environment (see
the `audit` job in `.github/workflows/ci.yml`). Run locally after
`pip install -e ".[dev]"`:

```bash
pip-audit --strict
```
