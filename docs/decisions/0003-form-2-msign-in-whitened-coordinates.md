# ADR 0003 -- Form 2: X = F^-1/2 msign(F^-1/2 M), msign where F is the identity

- **Status:** Accepted
- **Date:** 2026-11-12
- **Decided by:** the user (proposed F^-1/2 msign(F^-1/2 G)); the choice of square root, in the session

## Context

Form 1 applies msign after F^-1 (ADR 0002). The additive methods that combine curvature and msign (Mousse, Go-MUON)
take msign in coordinates whitened by the curvature instead.

## Decision

`SpectralNaturalPion(form="whitened")`: in each side's generalized eigenbasis P, with K_ij = (lambda_i + lambda_j)/2,
X = P [msign((P^T M P) / sqrt(K)) / sqrt(K)] P^T. The square root of F^-1 is the one of the eigenbasis (B = P D_K^-1/2
in coordinates); msign depends on that choice, and the Frobenius-symmetric root has no cheap form. Everything else is
form 1's (length rule, retraction, statistics, precision).

## Consequences

Same products as Natural Pion's F^-1 plus one msign. With msign replaced by the identity it is F^-1 M exactly
(test), so the coordinates are right. Another root of F^-1 would give another method.

## Evidence

tests/test_spectral_natural_pion.py (test_whitened_form_*).
