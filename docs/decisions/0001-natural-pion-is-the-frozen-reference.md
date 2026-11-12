# ADR 0001 -- Natural Pion is the frozen reference; its code comes in by copy

- **Status:** Accepted
- **Date:** 2026-11-12
- **Decided by:** the user (new repository beside Natural-Pion, not inside it)

## Context

The new project builds on Natural Pion, which is published (arXiv submission 8361028, github.com/Max0072/NaturalPion)
and frozen by Natural-Pion's ADR 0017. Changing it in place would change the published method and its records.

## Decision

`/onyx/data/p330/Natural-Pion` is read-only from this project. Code taken from it is copied here with the source commit
named in the commit message; the copied Natural Pion stays the reference implementation, and every new variant is a
separate class checked against it (same trajectory when the new parts are switched off). Natural-Pion's run records
may be cited by path as evidence.

## Consequences

Two copies of the optimizer exist; a bug found here is reported to Natural-Pion as a bug (its ADR 0017 reopens only for
bugs), not fixed silently. Which code to copy, and when, is open (`docs/RESUME.md`).

## Evidence

Natural-Pion `docs/decisions/0017-the-method-is-frozen.md`; Natural-Pion commit afcc459 (the preprint as submitted).
