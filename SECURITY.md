# Security policy

## Supported versions

Security fixes are considered for the latest published release on PyPI and for
the active modernization line targeting `0.1.17`. Older patch lines may not
receive backports.

## Reporting a vulnerability

Please **do not** open a public GitHub issue for security vulnerabilities.

Report privately by email to
[travis.j.kessler@gmail.com](mailto:travis.j.kessler@gmail.com) with:

- A description of the issue and its impact
- Steps to reproduce, or a proof of concept if available
- Affected versions / commit hashes if known

You should receive an acknowledgment within a few business days. We will
coordinate a fix and disclosure timeline as appropriate.

## Scope notes

padelpy shells out to a system `java` executable and vendors third-party JARs
(PaDEL-Descriptor / CDK). Issues that are solely upstream PaDEL/CDK behavior
may be documented as limitations rather than treated as padelpy
vulnerabilities; still report them if you believe they create a security risk
through this wrapper.
