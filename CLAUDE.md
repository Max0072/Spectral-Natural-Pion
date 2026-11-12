# Working in this repository

**Spectral Natural Pion** (working name): curvature and orthogonalisation together inside spectrum-preserving
rotations — the Fisher inverse F⁻¹ of Natural Pion and the matrix sign msign (as in Muon) applied to the rotation
generators. Prior work combines the two only for additive steps (FISMO, Go-MUON, Mousse; see `docs/LITERATURE.md`).
Started 2026-11-12. The method is not defined yet: see `docs/RESUME.md`.

Symbols used throughout: W a weight matrix (m × n); G its loss gradient; X_in, X_out the skew-symmetric rotation
generators (n × n and m × m); F the K-FAC Fisher on the generators, F(X) = ½(SXA + AXS) on the input side;
A the second moment of a layer's inputs, D of its output gradients; msign(X) = U Vᵀ for X = U Σ Vᵀ.

## Read first

1. `docs/RESUME.md` — where the work stands, what is open, what is next. A snapshot: rewrite it, do not append.
2. `docs/decisions/` — one record per decision (ADR), with its reason and evidence.
3. `docs/history/JOURNAL.md` — dated record of reasoning and decisions, so the work survives a lost session.

## The sibling project

`/onyx/data/p330/Natural-Pion` (published as github.com/Max0072/NaturalPion; preprint on arXiv) is the source of the
optimizer, the harness and the run records this project starts from. **Natural Pion is frozen there (its ADR 0017)
and is the reference here**: code is copied into this repository with the source commit named, never edited in
place over there, and every new variant is checked against it. Its run records are evidence that may be cited by
path; they are not re-run unless a decision says so.

## Rules (binding; set by the user)

**Cluster (Aphrodite, project p330, shared):**
- Never submit or run GPU compute without the user's explicit go-ahead, given for that campaign. Approval for one
  campaign does not extend to the next.
- Be conservative: the machine is shared. No compute on the login node beyond CPU tests of seconds.
- SLURM's RUNNING is not computing: before reporting on a job, confirm its step counter has advanced.
- Concurrent runs on one node use the same seed (different seeds read different corpus windows and starve each other
  for IOPS), unless the user waives it.
- Verify a diagnosis before spending GPU hours on it; answer a failure by understanding it, not by launching more jobs.
- Preflight before any set of runs: list what could make it obsolete (untested precision, defaults, grid ranges and
  their edges, row format, free disk) and settle it first; include a table "tuned? where?" for every compared arm.

**Comparisons:**
- Change one thing at a time between two compared arms, and diff their manifests to prove it.
- Every compared method is tuned the same way (same grid rule, same budgets, same seeds).
- When a step-size rule or its units change, rescale its absolute companions (lr_min → use a ratio of the peak,
  warmup, caps); otherwise the comparison varies two things.
- When a measurement comes back awkward, do not add a knob: state the hypothesis, the prediction and the control first.
- Build the mechanism as the user describes it and measure it; do not pre-empt a predicted failure with variants.
- Check absolute numbers along an axis before reporting that an advantage grows along it.
- Keep the setting simple and classical; reuse what exists (Natural Pion's harness, LLaMA-60M / C4).

**Numbers and writing:**
- Every number in a report or paper is produced by a runnable script from run records; otherwise it is a placeholder,
  never a typed value.
- Define every symbol, abbreviation and column name at first use.
- Less prose; fix a contradiction by cutting.

**Process:**
- State the plan before executing it.
- Journal reasoning and decisions in `docs/history/JOURNAL.md`; record each decision as an ADR in the commit that acts on it.
- Commit and push directly to `main` (working repository; no feature branches). What ships publicly is a curated
  snapshot folder, as `Final Natural Pion/` was for Natural Pion.
- Never optimise a reference implementation in place; speed work goes into a separate variant checked against it.
- Small checks (tests, lookups) may go to background subagents; discussion stays in the main thread.

## Traps carried over from Natural Pion

- What the GPU calls fp32 is TF32 by default, and it destroys the spectrum: the retraction and the rotation of W run in
  true fp32. Products that only set the direction may be lower precision; measure before assuming.
- An absolute lr_min means different decay depths at different peaks; schedules are cosine to a ratio (1%) of the peak.
- A code path needed by one length rule can survive into another (σ by power iteration under the RMS rule cost 0.84 s
  of a 2.07 s step); after changing a rule, check the step profile.
- msign by Newton–Schulz runs in bf16 in Muon's code; a rotation built from it must still be exactly orthogonal, so
  the retraction stays fp32 whatever produces the generator.
- Run logs are appended across attempts (a start marker separates them); readers take the last attempt.
- Apptainer: temporary directory on local disk; a failed build can print "Build complete" (see Natural-Pion
  `docs/CLUSTER.md`).

## Environment

Container `$DATA_p330/containers/ngd-pion.sif`; corpus `$DATA_p330/c4`; run outputs `$DATA_p330/runs-snp/`
(proposed, see `docs/RESUME.md`); partition `rtx` (RTX PRO 6000 Blackwell, 24 h limit per job). Cluster procedures:
Natural-Pion `docs/CLUSTER.md`.
