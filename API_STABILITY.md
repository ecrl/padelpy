# API stability policy

This document states the public API contract for **padelpy** and how version numbers
relate to compatible change. The same policy is published in the Sphinx site as
`docs/source/api_stability.rst` (built HTML: *API stability policy*).

## Frozen public surface

The following callables are the supported import surface and must remain drop-in
compatible within a compatibility series:

```python
from padelpy import from_smiles, from_mdl, from_sdf, padeldescriptor
```

Parameter **names** and **defaults** for these callables are frozen. Additive optional
keyword arguments may be introduced when they do not change existing call sites.
Renaming callables, making new arguments required, changing primary return container
types, or changing documented exception types for existing failure modes requires an
explicit, versioned compatibility decision.

### Version export

`padelpy.__version__` is intended to be part of the public surface (resolved from
package metadata). Callers may rely on it once exported from `padelpy` in the
modernization release line.

## Versioning

1. **Patch (`0.1.x`):** bugfixes, tooling, internal hardening, and documentation that
   preserve the frozen API. Descriptor and fingerprint **oracles must match**. The
   current API-stable modernization program ships as **`0.1.17`** after its planned
   phases complete.
2. **Minor (`0.2.0` and later):** reserved for future additive, still API-compatible
   work after `0.1.17`. Oracles must match.
3. **Major (`1.0.0` or higher):** only after an explicit stability promise; preferably
   still API-compatible. Upgrades to the bundled PaDEL/CDK JAR set, or intentional
   changes to the descriptor/fingerprint schema, require dual-run numeric parity
   evidence and a clear migration note.

## Oracle parity as a release gate

Regression oracles in the test suite (fixed SMILES, SDF, and MDL fixtures against the
**bundled** PaDEL-Descriptor engine) are part of the compatibility contract for the
`0.1.x` / subsequent compatible series. Releases that alter public call behavior or
descriptor outputs beyond documented tolerances must not proceed without updating the
versioning story above and recording parity evidence.

Fixture values are engine self-consistency anchors for the vendored JAR set, not
independent literature tables, unless explicitly expanded later.

## Runtime prerequisite

PaDELPy shells out to a system `java` executable. A Java JRE **8+** must be installed
and discoverable on `PATH` (`java -version` in the same environment). Missing Java
raises `ReferenceError` from `padeldescriptor` (and from helpers that call it).

## Known limitations (issue triage)

These items are tracked for maintainer clarity. They do not change the frozen API.

| Issue | Topic | Outcome |
|-------|--------|---------|
| [#55](https://github.com/ecrl/padelpy/issues/55) | Missing / undiscoverable Java | **Fixed in wrapper messaging + tests:** clearer `ReferenceError` text (JRE 8+, `PATH` check). Install docs expanded in the docs phase. |
| [#45](https://github.com/ecrl/padelpy/issues/45) | Hang / timeout on some structures (e.g. peptides) | **Limitation (PaDEL upstream) + wrapper timeout fix:** subprocess timeouts use real `communicate(timeout=...)` and raise `RuntimeError` with a stable “timed out” message. Some inputs remain expensive or non-terminating inside PaDEL until that timeout. |
| [#51](https://github.com/ecrl/padelpy/issues/51) | `RuntimeError` mid-batch over many SMILES | **Limitation (engine / input):** individual structures can fail inside PaDEL; the thin wrapper surfaces that as `RuntimeError` and does not skip bad rows. Callers should catch per-molecule errors or pre-validate structures. Not a JAR upgrade path in this release line. |
| [#56](https://github.com/ecrl/padelpy/issues/56) | Fingerprint runs capped near ~99 compounds | **Limitation (PaDEL / descriptor-types config):** `padeldescriptor(..., maxcpdperfile=...)` is forwarded, but custom fingerprint XML / engine behavior can still cap output. Workaround: split the input `.smi` into batches. No bundled JAR change in this release line. |
| [#58](https://github.com/ecrl/padelpy/issues/58) | Some SMILES fail fingerprint / descriptor calc | **Limitation (engine / input):** failures surface as `RuntimeError`. Happy-path fingerprints remain locked by the propane fingerprint oracle (`descriptors=False`, `fingerprints=True`). Example `C=C` succeeds on the current vendored engine; remaining failures are structure- or environment-specific, not a thin-wrapper API bug. |
| [#29](https://github.com/ecrl/padelpy/issues/29) | Inconsistent descriptor values across runs | **Limitation (PaDEL upstream):** some descriptors can vary with threading / 3-D conversion / engine internals. Compatibility oracles lock selected keys for fixed fixtures under the vendored JAR set. Prefer `retainorder=True` (default) and consider `threads=1` when bit-identical repeats are required. No JAR upgrade here. |
| [#37](https://github.com/ecrl/padelpy/issues/37) | MOF / complex SDF failures | **Limitation (PaDEL / CDK scope):** large or metal–organic frameworks are often outside what the bundled PaDEL/CDK path handles. Failures raise `RuntimeError` / empty results as today. Out of scope for the thin wrapper without an approved engine upgrade. |

## Related engine citation

PaDEL-Descriptor (the Java tool wrapped by this package):

- Yap CW. PaDEL-Descriptor: An open source software to calculate molecular descriptors
  and fingerprints. *J Comput Chem.* 2011;32(7):1466-1474.
  DOI: [10.1002/jcc.21707](https://doi.org/10.1002/jcc.21707) /
  PMID: [21425294](https://pubmed.ncbi.nlm.nih.gov/21425294/).
