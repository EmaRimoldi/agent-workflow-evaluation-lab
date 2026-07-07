# Agent Workflow Feasibility Pilot

**Status**: archived historical study
**Period**: April 2026
**Purpose**: test whether the first end-to-end agent workflow experiment could be
run, measured, and interpreted.

This folder is the repository's earliest full agent experiment. It is preserved
because it explains why later studies needed deterministic evaluation, starting
model calibration, and cleaner probe design.

## What This Study Asked

The study tested whether a 2x2 agent workflow design could be instrumented:

| | No shared memory | Shared or external memory |
| --- | --- | --- |
| One agent | `d00` | `d10` |
| Two parallel agents | `d01` | `d11` |

Each agent edited `autoresearch/train.py`, trained a small CIFAR-10 CNN, and
tried to lower validation loss (`val_bpb`). The study also tried to compute the
Beneventano-Poggio four-term decomposition over those runs.

## What It Contains

| path | role |
| --- | --- |
| [`results/agent_workflow_feasibility_summary.md`](results/agent_workflow_feasibility_summary.md) | main human-readable report |
| [`results/figures/`](results/figures/) | curated figures used by the report |
| [`results/raw_2x2_agent_pilot/`](results/raw_2x2_agent_pilot/) | raw JSON extracted from the 12-run 2x2 pilot |
| [`results/fixed_step_cpu_contention_followup/`](results/fixed_step_cpu_contention_followup/) | follow-up benchmark isolating CPU contention under fixed training steps |

## What Was Actually Run

- 12 primary agent runs: 4 cells x 3 repetitions.
- 8 short exploratory agent runs used while iterating on the setup.
- A fixed-time CPU contention benchmark with 1, 2, 4, and 8 concurrent training
  processes.
- A later fixed-step CPU contention follow-up with 300 optimizer updates per
  worker.

## What It Showed

- The agent loop, memory variants, token accounting, mode labeling, figures, and
  decomposition aggregation could run end to end.
- The study was not strong enough for a confirmatory claim: 3 repetitions per
  cell were too few, first edits differed across runs, and CPU contention
  confounded the parallel cells.
- The four-term decomposition mostly collapsed to the cost term because the runs
  produced too few accepted edits and too little category diversity.
- The CPU follow-up clarified an important confound: fixed-time parallel
  evaluation can hurt quality by reducing completed optimizer updates; fixed-step
  evaluation equalizes quality but changes wall-clock cost.

## How To Read It

Read the main summary first:

[`results/agent_workflow_feasibility_summary.md`](results/agent_workflow_feasibility_summary.md)

Then use the raw artifact directories only if you need provenance for a specific
table, figure, or decomposition value.
