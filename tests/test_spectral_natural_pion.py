"""Spectral Natural Pion, form 1: X = skew(msign(F^-1 M)) inside Natural Pion (spectral_pion/spectral_natural_pion.py)."""
import torch

from ngd_pion.linalg import skew
from ngd_pion.natural_pion import NaturalPionFast
from ngd_pion.pion_baseline import _msign
from spectral_pion import SpectralNaturalPion, msign_batched
from tests.test_natural_pion import SHAPES, _drive, _weights

COS = lambda t: 3e-4 * (1 + torch.cos(torch.tensor(t / 15 * 3.14159)).item()) / 2 + 3e-6


def _skew_batch(seed, k=3, n=12):
    g = torch.Generator().manual_seed(seed)
    return skew(torch.randn(k, n, n, generator=g))


def test_batched_msign_is_pion_msign_per_matrix():
    """The batched form does per matrix what the Pion baseline's msign (their pion_msign) does."""
    X = _skew_batch(1)
    Y = msign_batched(X)
    for k in range(X.shape[0]):
        assert torch.allclose(Y[k], _msign(X[k]), atol=2e-2), (Y[k] - _msign(X[k])).abs().max()


def test_msign_equalises_the_planes_above_a_few_percent_of_the_largest():
    """Muon's quintic msign is soft: on a skew matrix with a geometric spectrum from 1 to 1e-3, planes at >= 3% of the
    largest singular value come out in [0.9, 1.2]; below 1% it fades (measured 2026-11-12: 0.73 at 1%, 0.23 at 0.3%,
    0.08 at 0.1%), so the weakest planes of F^-1 M are not raised to the full angle."""
    g = torch.Generator().manual_seed(2)
    U, _, Vh = torch.linalg.svd(skew(torch.randn(512, 512, generator=g)).double())
    s = torch.logspace(0, -3, 512, dtype=torch.float64)
    X = skew(((U * s) @ Vh).float())[None]
    Y = skew(msign_batched(X))[0]
    assert (msign_batched(X)[0] - Y).abs().max() < 2e-2              # skew up to bf16 round-off before skew()
    U2, S2, V2 = torch.linalg.svd(X[0].double())
    gain = torch.diag(U2.T @ Y.double() @ V2.T)                       # what msign does to each plane of X
    r = S2 / S2[0]
    assert gain[r >= 0.03].min() > 0.9 and gain[r >= 0.03].max() < 1.2, gain[r >= 0.03]
    assert gain[r <= 0.002].max() < 0.3, (r.min(), gain[-4:])


def test_without_msign_it_is_natural_pion_bit_for_bit():
    a, b = _weights(61), _weights(61)
    ref = NaturalPionFast(a, lr=3e-4, t_fac=5, stats_window=3)
    opt = SpectralNaturalPion(b, lr=3e-4, t_fac=5, stats_window=3, msign=False)
    for x, y in zip(_drive(ref, a, 15, 62, COS)[-1], _drive(opt, b, 15, 62, COS)[-1]):
        assert torch.equal(x, y)


def test_it_keeps_the_spectrum_and_moves():
    params = _weights(63)
    s0 = [torch.linalg.svdvals(p.detach().double()) for p in params]
    w0 = [p.detach().clone() for p in params]
    opt = SpectralNaturalPion(params, lr=3e-4, t_fac=5, stats_window=3)
    _drive(opt, params, 15, 64, COS)
    for p, s, w in zip(params, s0, w0):
        assert torch.allclose(torch.linalg.svdvals(p.detach().double()), s, rtol=1e-4)
        assert (p.detach() - w).abs().max() > 1e-4


def test_msign_differs_from_natural_pion():
    a, b = _weights(65), _weights(65)
    ref = NaturalPionFast(a, lr=3e-4, t_fac=5, stats_window=3)
    opt = SpectralNaturalPion(b, lr=3e-4, t_fac=5, stats_window=3)
    diff = max((x - y).abs().max().item() for x, y in zip(_drive(ref, a, 10, 66, COS)[-1], _drive(opt, b, 10, 66, COS)[-1]))
    assert diff > 1e-4


class _Capture(SpectralNaturalPion):
    """Records msign(F^-1 M) and msign(M) for the same momentum M."""
    seen: list = []

    def _correct(self, X, G, P, den, items, rows, group):
        Y = super()._correct(X, G, P, den, items, rows, group)
        self.seen.append((Y, skew(msign_batched(G))))
        return Y


def test_msign_keeps_the_basis_of_the_fisher():
    """First check 2 of docs/RESUME.md, on synthetic statistics: msign(F^-1 M) is not msign(M). msign keeps the singular
    vectors of its argument, and F^-1 changes them, not only the singular values. The size of the difference on a real
    model is a measurement, not this test."""
    params = _weights(67)
    opt = _Capture(params, lr=3e-4, t_fac=5, stats_window=3)
    g = torch.Generator().manual_seed(68)
    for p in params:                                             # anisotropic statistics, so F is far from a multiple of I
        m, n = p.shape
        opt.observe(p, torch.randn(256, n, generator=g) * torch.linspace(3, 0.1, n))
        opt.observe_backward(p, torch.randn(256, m, generator=g) * torch.linspace(0.1, 3, m) / 64)
        p.grad = torch.randn(m, n, generator=g)
    _Capture.seen = []
    opt.step()
    rel = [((y - z).norm() / z.norm()).item() for y, z in _Capture.seen]
    assert min(rel) > 0.1, rel


def test_the_harness_builds_it():
    from harness.config import RunConfig
    from harness.train import build_optimizers
    from harness.model import Transformer
    from tests.test_harness import SMALL
    model = Transformer(SMALL)
    cfg = RunConfig(optimizer="spectral-natural-pion", model=SMALL, lr=3e-4)
    rot, _, rec = build_optimizers(model, cfg)
    assert isinstance(rot, SpectralNaturalPion) and rot.msign
    assert cfg.hash != RunConfig(optimizer="natural-pion-fast", model=SMALL, lr=3e-4).hash
    rec.remove()
