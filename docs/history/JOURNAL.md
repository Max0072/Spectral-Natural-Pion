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
exactly. SNP 3e-4 3.6995, 6e-4 3.6669, 1.2e-3 3.7105; 2.4e-3, 1.5e-4, 7.5e-5 cancelled before start (the user
first asked for a smaller step on the incomplete grid; once 6e-4 finished best, interior, they were dropped).
SNP 6e-4 is 0.021 below Natural Pion and 0.011 below pion_msign; Muon (3k, lr 1e-3, AdamW 8e-3,
runs-muon/muon-lr0.001-s0-0fbb2f2ae7) 3.6505, so SNP closes 0.021 of Natural Pion's 0.037 gap to Muon. One seed, scale
chosen on it. SNP was ahead of Natural Pion at every evaluation up to 2000 steps at both 3e-4 and 6e-4.
Submitted (user): SNP at 15k and 30k, grid {1.5e-4, 3e-4, 6e-4} (rows 7-12, jobs 413949, 413950); 45k and full take
the 30k choice. Muon at 15k and 30k with the full-length run's command (Natural-Muon journal 2026-11-03), only
--train-steps and --eval-every changed, code of Natural-Muon unchanged: jobs 413955 (15k), 413956 (30k), outputs in
$DATA_p330/runs-muon. Natural Pion's runs at these lengths: Natural-Pion runs-record/npv2/k-m15k-*, k-m30k-*.

2026-11-13 00:10. User: is F^-1 worth its cost on top of msign? At 3000 steps SNP saves ~7% of steps over pion_msign
(0.011 at a local slope of 0.16 per e-fold of steps) and costs ~8-10% more time per step: a wash. Submitted
(user): pion_msign at 15k and 30k, lr {1e-2, 2e-2}, configuration of k-pmsign-2e-2 except steps and eval cadence
(rows 13-16, jobs 413968, 413969). Step-time comparisons across separate runs disagree (Pion 0.524 vs Natural Pion 0.497
s/step from runs on different days); a same-job timing is needed before any cost claim.
Form 2 (user: F^-1/2 msign(F^-1/2 G)), ADR 0003, implemented and tested (199 passed); rows 17-19 at 3000 steps written,
not submitted.

2026-11-13 14:30. Results, seed 0, val (best of each grid; scale):
            3000              15000             30000
Muon        3.6505 (1e-3)     3.4136            3.3540            (untuned, one point)
SNP f1 RMS  3.6669 (6e-4)     3.4399 (3e-4)     3.3735 (3e-4)     (all interior)
SNP f1 fix  3.6690 (2e-2)     running           running           (3k interior: 1e-2 3.6905, 4e-2 3.7214, 5e-3 3.7792)
SNP f2 RMS  3.6737 (6e-4)     -                 -                 (3e-4 3.7104, 1.2e-3 3.7087)
NatPion     3.6878 (6e-4)     3.4465 (3e-4)     3.3802 (3e-4)     (Natural-Pion records)
pion_msign  3.6780 (2e-2)     3.4503 (2e-2)     3.3842 (1e-2, EDGE of {1e-2, 2e-2})
Pion        3.8412            3.5254            3.4460            (Natural-Pion records)
SNP form 1 (RMS) minus Natural Pion: -0.021, -0.007, -0.007; minus pion_msign: -0.011, -0.010, -0.011; minus Muon:
+0.016, +0.026, +0.019. pion_msign is behind Natural Pion at 15k and 30k (ahead at 3k), but its 30k best is at the
grid edge. Form 2 and the fixed length rule do not beat form 1 with RMS at 3k. Mid-schedule losses at 30k were level
with Natural Pion; the gap opens in the decay, as at 15k. Open: pion_msign 30k at 5e-3; SNP seeds.

2026-11-14 00:30. All submitted runs finished. Form 1 (RMS) at 15k, 3e-4, seeds 0-3: 3.4399, 3.4367, 3.4368, 3.4369
(mean 3.4376, range 0.003) against Natural Pion's 3.4465, 3.4481, 3.4483, 3.4483 (mean 3.4478): better on every seed,
by 0.010 in the mean. Form 1 with a fixed length (c = theta): 15k 1e-2 3.4373 (5e-3 3.4730, 2e-2 3.4563), 30k 1e-2
3.3723 (5e-3 3.3944, 2e-2 3.4008), both interior and equal to the RMS rule (3.4376 mean, 3.3735): the length rule does
not matter for form 1. pion_msign 30k at 5e-3: 3.4157, so its optimum 1e-2 (3.3842) is interior.
