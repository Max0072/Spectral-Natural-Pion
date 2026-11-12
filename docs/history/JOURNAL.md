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
scripts/jobs/snp.sbatch: row 0 control (Natural Pion from this copy, 6e-4; must reproduce k-m3k-6e-4 3.6878), rows
1-4 form 1 at 3e-4..2.4e-3. Configurations diffed against k-m3k-6e-4 before submission: only optimizer, out_dir,
defaults_version differ. Not submitted: waiting for the user's go-ahead.

2026-11-12 23:40. Form 1 at 3000 steps, seed 0 (val): control Natural Pion from this copy 3.6878272533 = k-m3k-6e-4
exactly. SNP 3e-4 3.6995, 6e-4 3.6669, 1.2e-3 (see below); 2.4e-3, 1.5e-4, 7.5e-5 cancelled before start (the user
first asked for a smaller step on the incomplete grid; once 6e-4 finished best, interior, they were dropped).
SNP 6e-4 is 0.021 below Natural Pion and 0.011 below pion_msign; Muon (3k, lr 1e-3, AdamW 8e-3,
runs-muon/muon-lr0.001-s0-0fbb2f2ae7) 3.6505, so SNP closes 0.021 of Natural Pion's 0.037 gap to Muon. One seed, scale
chosen on it. SNP was ahead of Natural Pion at every evaluation up to 2000 steps at both 3e-4 and 6e-4.
Submitted (user): SNP at 15k and 30k, grid {1.5e-4, 3e-4, 6e-4} (rows 7-12, jobs 413949, 413950); 45k and full take
the 30k choice. Muon at 15k and 30k with the full-length run's command (Natural-Muon journal 2026-11-03), only
--train-steps and --eval-every changed, code of Natural-Muon unchanged: jobs 413955 (15k), 413956 (30k), outputs in
$DATA_p330/runs-muon. Natural Pion's runs at these lengths: Natural-Pion runs-record/npv2/k-m15k-*, k-m30k-*.
