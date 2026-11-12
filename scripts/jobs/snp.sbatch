#!/bin/bash
#SBATCH -A p330
#SBATCH -J snp
#SBATCH -p rtx
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH -t 02:00:00
#SBATCH -o logs/%x-%A_%a.out
#SBATCH -e logs/%x-%A_%a.err
# Spectral Natural Pion runs, one row per run:  TAG | OPTIMIZER | STEPS | LR (peak step scale) | SEED
# Every row: Natural Pion's settings of its 3000-step reference run (Natural-Pion runs-record/npv2/k-m3k-6e-4):
# RMS length rule, TF32 before the rotation, bf16 F^-1, floor 1e-3, cosine to 1% of the peak, Lie momentum 0.9,
# AdamW 8e-3. Output: $DATA_p330/runs-snp/<TAG>/.
#   sbatch -x rtx6003,rtx6004 --array=<rows> scripts/jobs/snp.sbatch
REPO="${REPO:-$DATA_p330/Spectral-Natural-Pion}"; SIF="${SIF:-$DATA_p330/containers/ngd-pion.sif}"; DATA="${DATA:-$DATA_p330/c4}"
NP=natural-pion-fast; SNP=spectral-natural-pion
ROWS=(
"np-3k-6e-4|$NP|3000|6e-4|0"
"snp1-3k-3e-4|$SNP|3000|3e-4|0"
"snp1-3k-6e-4|$SNP|3000|6e-4|0"
"snp1-3k-1.2e-3|$SNP|3000|1.2e-3|0"
"snp1-3k-2.4e-3|$SNP|3000|2.4e-3|0"
"snp1-3k-1.5e-4|$SNP|3000|1.5e-4|0"
"snp1-3k-7.5e-5|$SNP|3000|7.5e-5|0"
)
# row 0 (2026-11-12): control, Natural Pion from this repository's copy; must reproduce k-m3k-6e-4 (3.6878)
# rows 1-4 (2026-11-12): form 1, X = msign(F^-1 M) (ADR 0002), grid of factors of two as Natural Pion's at 3000 steps
# rows 5-6 (2026-11-12): the grid extended down (best finished point 3e-4 at its lower edge)
IFS='|' read -r TAG OPT STEPS LR SEED <<< "${ROWS[$SLURM_ARRAY_TASK_ID]}"
EV=500; [ "$STEPS" -gt 3000 ] && EV=1000; [ "$STEPS" -gt 15000 ] && EV=2000
OUT="$DATA_p330/runs-snp/$TAG"; mkdir -p "$OUT"
echo "row $SLURM_ARRAY_TASK_ID: $TAG $OPT steps $STEPS lr $LR seed $SEED"
apptainer exec --env PYTHONUNBUFFERED=1 --env PYTHONPATH="$REPO" --env PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True \
    --nv --bind "$DATA_p330:$DATA_p330" --pwd "$REPO" "$SIF" \
    python -m harness.run --optimizer "$OPT" --np-kwargs '{"length":"rms","tf32":"upstream","fisher_dtype":"bf16"}' \
      --ngd-eps 1e-3 --lr-min-ratio 0.01 \
      --lr "$LR" --ngd-beta1 0.9 --train-steps "$STEPS" --batch-sequences 512 --micro-batch 256 --rho-micro 128 \
      --precision bf16 --seed "$SEED" --device cuda --log-every 23 --eval-every "$EV" --adamw-lr 8e-3 \
      --data-path "$DATA/c4_train.bin" --val-path "$DATA/c4_val.bin" --out-dir "$OUT"
