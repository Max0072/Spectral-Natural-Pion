# ADR 0002 -- Form 1: X = skew(msign(F^-1 M)) inside Natural Pion

- **Status:** Accepted
- **Date:** 2026-11-12
- **Decided by:** the user (msign(F^-1 G) first); implementation choices proposed in the session, open to the user

## Context

Natural Pion steps along X = F^-1 M (M: Lie momentum of the generator). The Pion authors' pion_msign steps along
msign(M) and reaches 3.6780 at 3000 steps against Natural Pion's 3.6878 (seed 0). Natural-Pion's `planes="equal"`
ablation (exact polar factor of F^-1 M, angle rule) was run only at angles 0.1 and 0.2 and diverged; pion_msign's
optimum lr 2e-2 suggests those angles were 5-10x too large, so form 1 has not been tried at a sensible scale.

## Decision

`spectral_pion.SpectralNaturalPion` is `NaturalPionFast` with one change: after X = F^-1 M, X <- skew(msign(X)).
msign is Muon's / pion_msign's: five quintic Newton-Schulz iterations in bf16 on X / ||X||_F. Length rule (Pion's
RMS rule), squared Cayley retraction, statistics, floor and schedules are Natural Pion's. `msign=False` is Natural Pion
bit for bit. The comparison is against Natural Pion; pion_msign differs from both in momentum (ambient 0.95),
alternating sides, length rule and retraction, so it is a reference number, not a one-change control.

## Consequences

Muon's msign is soft: planes below ~1% of the largest singular value are raised less (0.73 at 1%, 0.08 at 0.1%).
Open alternatives, not built: exact polar factor (eigh), the angle rule (length="spectral", where c = lr since
sigma ~ 1), msign in F-whitened coordinates.

## Evidence

tests/test_spectral_natural_pion.py; Natural-Pion journal lines 7345-7346 (planes equal diverged at 0.1, 0.2);
Natural-Pion runs-record/npv2/k-pmsign-*, k-m3k-6e-4.
