# Journal

Dated record of reasoning and decisions. Append; newest last.

2026-11-12. Repository initialised (user): github.com/Max0072/Spectral-Natural-Pion, cloned to
/onyx/data/p330/Spectral-Natural-Pion, beside Natural-Pion. Rules in CLAUDE.md are the user's standing rules from
Natural-Pion. ADR 0001: Natural Pion is the frozen reference, copied in with its commit, never edited in place.
Starting facts (read by hand from Natural-Pion logs, 3000 steps, seed 0): Pion 3.8412, Natural Pion 3.6878,
pion_msign 3.6780 at lr 2e-2, best of {5e-3, 1e-2, 2e-2, 4e-2, 8e-2} (4e-2 3.7559 and 8e-2 3.8710 finished
2026-11-11, jobs 412062_500/501). msign alone on Pion's generators is already ahead of F⁻¹ alone on one seed, by more
than Natural Pion's 4-seed range (0.006). Open for the user: the method's exact form, baselines, which code to copy,
the run directory.

2026-11-12 evening. Form 1 (user: msign(F^-1 G) first). Code copied from Natural-Pion afcc459 (ngd_pion, harness,
tests, pyproject, kseries, v2.sbatch for reference, prepare_data); copied suite passes (190). New package spectral_pion:
SpectralNaturalPion = NaturalPionFast + skew(msign(F^-1 M)) in the _correct hook (ADR 0002); one optimizer registry
in harness/config.py. 7 new tests; 197 passed, 1 skipped. Found: Natural-Pion's planes="equal" (exact polar of
F^-1 M, angle rule) diverged at 0.1/0.2 and was never run lower, so form 1 is untried at a sensible scale. Found:
Muon's quintic msign is soft (gain 0.73 at 1% of the top singular value, 0.23 at 0.3%, 0.08 at 0.1%).
pion_msign grid completed (4e-2 3.7559, 8e-2 3.8710): best 2e-2 3.6780 inside the grid.
scripts/runs/snp.sbatch: row 0 control (Natural Pion from this copy, 6e-4; must reproduce k-m3k-6e-4 3.6878), rows
1-4 form 1 at 3e-4..2.4e-3. Configurations diffed against k-m3k-6e-4 before submission: only optimizer, out_dir,
defaults_version differ. Not submitted: waiting for the user's go-ahead.
