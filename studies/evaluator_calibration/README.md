# Evaluator Calibration

**Status**: superseded design study
**Question**: can the evaluator be made deterministic enough that later agent
workflow comparisons measure agent edits rather than training noise?

## What Was Run

This study used fixed-step evaluation, repeated baseline checks, and early
memory/no-memory calibration reps. Its most important result is that five
unmodified baseline runs produced identical `val_bpb = 0.811222`.

## What It Contributed

The study established that deterministic evaluation was possible, but it also
found design problems: memory anchoring, run-count thresholds, task ceiling
effects, and training-time confounds. Those findings motivated the later
[`agent_memory_ablation/`](../agent_memory_ablation/) study.

## Read First

- [`results/evaluator_calibration_summary.md`](results/evaluator_calibration_summary.md)

## Caveat

This is not the current primary agentic result. It is methodological evidence
that explains why the later ablation was redesigned.
