# Where the work stands (snapshot; rewrite, do not append)

**2026-11-12: form 1 implemented, not run.** X = skew(msign(F⁻¹M)) inside Natural Pion (ADR 0002,
`spectral_pion/`), 197 tests pass; `scripts/jobs/snp.sbatch` rows 0-4 (control + 3000-step grid) await the go-ahead.

## The idea

Natural Pion (sibling repository, frozen) rotates W along X = F⁻¹G with Pion's RMS step length. Muon-style msign
equalises the singular values of an update. The question: does putting both on the rotation generators — e.g.
X = msign(F⁻¹G), or msign in F's whitened coordinates — beat Natural Pion, at what cost? The exact composition is
not chosen yet; it is the user's to specify.

## What is already known (Natural-Pion run records, LLaMA-60M / C4, 3000 steps, seed 0, validation loss)

| method | step scale | val | source |
|---|---|---|---|
| Pion | lr 1e-3 | 3.8412 | Natural-Pion `docs/paper/numbers.json`, key pion3000_s0 |
| Natural Pion | 6e-4 | 3.6878 | same, key v2_3000_s0 (mean of 4 seeds 3.6848) |
| pion_msign (msign on Pion's generators; the Pion authors' repository variant, not in their paper) | lr 2e-2 | **3.6780** | Natural-Pion `runs-record/npv2/k-pmsign-2e-2` |

pion_msign's grid: 5e-3 3.7972, 1e-2 3.7097, 2e-2 3.6780, 4e-2 3.7559, 8e-2 3.8710 (the last two finished
2026-11-11, jobs 412062_500/501, logs in `$DATA_p330/runs/npv2/k-pmsign-{4e-2,8e-2}`, not yet in Natural-Pion's
runs-record). Its best is inside the grid and 0.010 below Natural Pion on seed 0 — more than Natural Pion's 4-seed range
(0.006, key v2_3000_range) — but it is one seed, on which its lr was also chosen, at one horizon. Its spectrum drift at 3000 steps is 6.7e-4 (Natural Pion 3.7e-6). The numbers here
were read by hand from the logs on 2026-11-12; any use in a report goes through a script.

## First checks (from the Natural-Pion journal, 2026-11-10)

1. pion_msign against Natural Pion beyond one seed and 3000 steps (seeds 1–3, then 15 000 steps), because msign alone
   already beats F⁻¹ alone on seed 0 at 3000 steps. If it holds, the project's reference is pion_msign, not Natural Pion.
2. Does msign after F⁻¹ keep anything of F⁻¹? msign sets every singular value of the generator to 1, F⁻¹ reweights
   them; the composition may reduce to msign in a rotated basis. Settle on paper and on a CPU test before any run.
3. Cost: msign is five Newton–Schulz iterations on top of Natural Pion's step.

## Open decisions (the user's)

- Baseline(s): Natural Pion as published; published Pion; pion_msign? Muon for reference?
- The method's exact form: form 1 chosen (ADR 0002); its implementation choices (Muon's msign, RMS rule) are open.
- Run output directory `$DATA_p330/runs-snp/` (proposed).
- Goal: a paper built on a positive empirical result, as for Natural Pion (assumed; confirm).
