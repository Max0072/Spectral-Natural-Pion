# Prior work to place the method against

| work | what it does | relation |
|---|---|---|
| Pion (Shi et al. 2026, arXiv 2605.12492) | rotates W on both sides along the raw generator gradient, RMS step length | the geometry |
| pion_msign (Pion authors' repository, not in their paper) | msign on Pion's generators | the closest existing method; numbers in `docs/RESUME.md` |
| Natural Pion (Shikunov 2026, github.com/Max0072/NaturalPion) | F⁻¹ on Pion's generators, K-FAC Fisher inverted exactly | the frozen reference (ADR 0001) |
| Muon (Jordan et al. 2024) | additive step along msign of the momentum | orthogonalisation, additive |
| FISMO (arXiv 2601.21750) | Fisher-structured polar step under a spectral trust region | curvature + msign, additive; claims to beat Muon (not checked) |
| Go-MUON (arXiv 2608.09763) | Muon between K-FAC inverse fourth roots | curvature + msign, additive |
| Mousse (arXiv 2603.09697) | Muon in Shampoo-whitened coordinates | curvature + msign, additive |

Natural-Pion's literature check of 2026-11-03 found no Fisher or Shampoo metric on two-sided rotations, and no
msign + F⁻¹ combination there; re-check before any claim of novelty.
