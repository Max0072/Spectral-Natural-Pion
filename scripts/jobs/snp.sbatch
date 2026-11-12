#!/bin/bash
#SBATCH -A p330
#SBATCH -J snp
#SBATCH -p rtx
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH -t 02:00:00
#SBATCH -o logs/%x-%A_%a.out
#SBATCH -e logs/%x-%A_%a.err
# Spectral Natural Pion runs, one row per run:  TAG | OPTIMIZER | STEPS | LR (peak step scale) | SEED | EXTRA
# (EXTRA: further harness flags; Natural Pion's flags below go only to natural-pion-fast and spectral-natural-pion)
# Every row: Natural Pion's settings of its 3000-step reference run (Natural-Pion runs-record/npv2/k-m3k-6e-4):
# RMS length rule, TF32 before the rotation, bf16 F^-1, floor 1e-3, cosine to 1% of the peak, Lie momentum 0.9,
# AdamW 8e-3. Output: $DATA_p330/runs-snp/<TAG>/.
#   sbatch -x rtx6003,rtx6004 --array=<rows> scripts/jobs/snp.sbatch
REPO="${REPO:-$DATA_p330/Spectral-Natural-Pion}"; SIF="${SIF:-$DATA_p330/containers/ngd-pion.sif}"; DATA="${DATA:-$DATA_p330/c4}"
NP=natural-pion-fast; SNP=spectral-natural-pion
# pion_msign exactly as Natural-Pion v2.sbatch rows 497-501 (k-pmsign-*, 3000 steps)
PMSIGN="--pion-scaling msign --pion-momentum ambient --pion-beta1 0.95 --pion-alternate true --lr-min-ratio 0.01"
ROWS=(
"np-3k-6e-4|$NP|3000|6e-4|0"
"snp1-3k-3e-4|$SNP|3000|3e-4|0"
"snp1-3k-6e-4|$SNP|3000|6e-4|0"
"snp1-3k-1.2e-3|$SNP|3000|1.2e-3|0"
"snp1-3k-2.4e-3|$SNP|3000|2.4e-3|0"
"snp1-3k-1.5e-4|$SNP|3000|1.5e-4|0"
"snp1-3k-7.5e-5|$SNP|3000|7.5e-5|0"
"snp1-15k-1.5e-4|$SNP|15000|1.5e-4|0"
"snp1-15k-3e-4|$SNP|15000|3e-4|0"
"snp1-15k-6e-4|$SNP|15000|6e-4|0"
"snp1-30k-1.5e-4|$SNP|30000|1.5e-4|0"
"snp1-30k-3e-4|$SNP|30000|3e-4|0"
"snp1-30k-6e-4|$SNP|30000|6e-4|0"
"pmsign-15k-1e-2|pion|15000|1e-2|0|$PMSIGN"
"pmsign-15k-2e-2|pion|15000|2e-2|0|$PMSIGN"
"pmsign-30k-1e-2|pion|30000|1e-2|0|$PMSIGN"
"pmsign-30k-2e-2|pion|30000|2e-2|0|$PMSIGN"
)
# row 0 (2026-11-12): control, Natural Pion from this repository's copy; must reproduce k-m3k-6e-4 (3.6878)
# rows 1-4 (2026-11-12): form 1, X = msign(F^-1 M) (ADR 0002), grid of factors of two as Natural Pion's at 3000 steps
# rows 5-6 (2026-11-12): the grid extended down; cancelled before start, once 6e-4 finished best (3.6669)
# rows 13-16 (2026-11-12): pion_msign at 15k and 30k, lr {1e-2, 2e-2} (its 3000-step best 2e-2); submit -t 03:00:00
# (15k), -t 06:00:00 (30k)
# rows 7-12 (2026-11-12): form 1 at 15 000 and 30 000 steps, grid {1.5e-4, 3e-4, 6e-4} (Natural Pion's optimum
# there was 3e-4); 45 000 and full length take the 30 000-step choice, as for Natural Pion. Submit with -t 03:00:00
# (15k) and -t 06:00:00 (30k).
IFS='|' read -r TAG OPT STEPS LR SEED EXTRA <<< "${ROWS[$SLURM_ARRAY_TASK_ID]}"
NPFLAGS=()
case "$OPT" in $NP|$SNP) NPFLAGS=(--np-kwargs '{"length":"rms","tf32":"upstream","fisher_dtype":"bf16"}' --ngd-eps 1e-3 --lr-min-ratio 0.01) ;; esac
EV=500; [ "$STEPS" -gt 3000 ] && EV=1000; [ "$STEPS" -gt 15000 ] && EV=2000
OUT="$DATA_p330/runs-snp/$TAG"; mkdir -p "$OUT"
echo "row $SLURM_ARRAY_TASK_ID: $TAG $OPT steps $STEPS lr $LR seed $SEED $EXTRA"
apptainer exec --env PYTHONUNBUFFERED=1 --env PYTHONPATH="$REPO" --env PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True \
    --nv --bind "$DATA_p330:$DATA_p330" --pwd "$REPO" "$SIF" \
    python -m harness.run --optimizer "$OPT" "${NPFLAGS[@]}" $EXTRA \
      --lr "$LR" --ngd-beta1 0.9 --train-steps "$STEPS" --batch-sequences 512 --micro-batch 256 --rho-micro 128 \
      --precision bf16 --seed "$SEED" --device cuda --log-every 23 --eval-every "$EV" --adamw-lr 8e-3 \
      --data-path "$DATA/c4_train.bin" --val-path "$DATA/c4_val.bin" --out-dir "$OUT"
