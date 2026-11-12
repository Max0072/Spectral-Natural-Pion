"""Spectral Natural Pion: Natural Pion with msign on the rotation generators.

form "msign_after" (form 1, ADR 0002):   X = skew(msign(F^-1 M)).
form "whitened"    (form 2, ADR 0003):   X = F^-1/2 msign(F^-1/2 M), msign in coordinates where F is the identity.

Natural Pion (`ngd_pion.natural_pion.NaturalPionFast`, copied from Natural-Pion commit afcc459, unchanged) forms the
direction X = F^-1 M from the Lie momentum M of each side's generator, then sets the step length by Pion's RMS rule
and rotates W by the squared Cayley retraction. This class changes one thing: right after X = F^-1 M it replaces X by
its matrix sign msign(X) = U V^T (X = U S V^T), so every rotation plane of the direction gets the same weight. Length
rule, retraction, statistics and floor are Natural Pion's.

msign is the one of Muon and of the Pion authors' pion_msign: five "quintic" Newton-Schulz iterations in bf16 on X
scaled to unit Frobenius norm (coefficients `ngd_pion.pion_baseline._NS_QUINTIC`). It is soft: planes with a
singular value of at least ~3% of the largest come out at 0.9-1.2, weaker ones are raised less (0.73 at 1%, 0.23 at
0.3%, 0.08 at 0.1%; tests/test_spectral_natural_pion.py), so the faintest planes of F^-1 M do not get the full angle. The result is made exactly skew in fp32 (the iteration is an odd polynomial, so it
is skew in exact arithmetic; skew() removes the bf16 round-off). The retraction stays in true fp32.

`msign=False` gives Natural Pion's trajectory bit for bit (tests/test_spectral_natural_pion.py).

Form 2. In the generalized eigenbasis P of a side (P^T A P = I, P^T S P = diag(lambda)), with K_ij = (lambda_i +
lambda_j)/2 (Natural Pion's denominator `den`), write X = P Xt P^T. Then <X, F X> = sum_ij K_ij Xt_ij^2 and
<G, X> = <P^T G P, Xt>. In Z = sqrt(K) o Xt the metric is Frobenius and the
gradient is (P^T G P) / sqrt(K). msign is taken there and mapped back:
    X = P [ msign((P^T M P) / sqrt(K)) / sqrt(K) ] P^T.
This is one square root B of F^-1 (B B^* = F^-1), the one of the eigenbasis; msign is not invariant to the choice of B,
so "F^-1/2" here means this B, not the Frobenius-symmetric root of F^-1 (which has no cheap form). Products as in
Natural Pion's F^-1 (bf16 when fisher_dtype is bf16), result made exactly skew in fp32.
"""
from __future__ import annotations

import torch

from ngd_pion.linalg import skew
from ngd_pion.natural_pion import NaturalPionFast
from ngd_pion.pion_baseline import _NS_QUINTIC


@torch.no_grad()
def msign_batched(X: torch.Tensor, eps: float = 1e-7) -> torch.Tensor:
    """msign of a batch of square matrices (..., n, n): Muon's quintic Newton-Schulz in bf16, returned in fp32.
    Per matrix the same arithmetic as `ngd_pion.pion_baseline._msign`."""
    x = X.float()
    x = x / torch.linalg.matrix_norm(x).clamp_min(eps)[..., None, None]
    x = x.to(torch.bfloat16)
    for a, b, c in _NS_QUINTIC:
        gram = x @ x.mT
        poly = b * gram + c * (gram @ gram)
        x = a * x + poly @ x
    return x.float()


class SpectralNaturalPion(NaturalPionFast):
    def __init__(self, params, lr: float = 3e-4, *, msign: bool = True, form: str = "msign_after", **kwargs) -> None:
        if form not in ("msign_after", "whitened"):
            raise ValueError(f"form must be msign_after or whitened, got {form!r}")
        self.msign, self.form = msign, form
        super().__init__(params, lr, **kwargs)

    def _solve(self, P, Pt, G, den):
        if not (self.msign and self.form == "whitened"):
            return super()._solve(P, Pt, G, den)
        r = den.sqrt()
        if self.fisher_dtype == "bf16":
            Pb, Ptb = P.to(torch.bfloat16), Pt.to(torch.bfloat16)
            Y = (Ptb @ G.to(torch.bfloat16) @ Pb).float() / r
            Z = skew(msign_batched(skew(Y))) / r
            return skew((Pb @ Z.to(torch.bfloat16) @ Ptb).float())
        Z = skew(msign_batched(skew((Pt @ G @ P) / r))) / r
        return skew(P @ Z @ Pt)

    def _correct(self, X, G, P, den, items, rows, group):
        X = super()._correct(X, G, P, den, items, rows, group)
        if self.msign and self.form == "msign_after":
            X = skew(msign_batched(X))
        return X


BY_NAME = {"spectral-natural-pion": SpectralNaturalPion}
