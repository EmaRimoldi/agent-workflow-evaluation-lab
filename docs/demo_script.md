# Demo Script

This is the shortest coherent demo of AgentOps Lab.

## 60-Second Demo

AgentOps Lab measures whether a more complex AI-agent workflow is worth running.

The benchmark is deliberately concrete: agents edit one CIFAR-10 training file,
`autoresearch/train.py`, then run evaluations and try to reduce `val_bpb`
validation loss.

The product question is:

> Should this task be run by one long-running agent, independent parallel
> agents, memory-augmented agents, a blackboard swarm, or a merge workflow?

The repo does three things:

1. Runs the workflows through one CLI: `agentops`.
2. Captures audit evidence: logs, snapshots, traces, shared-memory events, and
   certified hitting time.
3. Preserves the studies showing what was learned.

The strongest current result is the probe ablation study. High-temperature
exploration without memory, `P11`, was unstable: best `val_bpb = 0.934`, mean
`1.816`. The shared-memory version, `P12`, was better and much more stable:
best `0.914`, mean `1.049`, with Mann-Whitney `p < 0.001`.

The takeaway is narrow but useful: more agent exploration is not automatically
better. Routing correction through memory can turn destructive exploration into
controlled exploration.

## 5-Minute Technical Walkthrough

### 1. Show the benchmark task

Files:

- `autoresearch/train.py`
- `autoresearch/prepare.py`
- `autoresearch/program.md`

What to say:

The substrate is intentionally small and inspectable. Agents are allowed to edit
`train.py`; evaluation reports `val_bpb`; fixed-step runs make comparisons less
dependent on machine load.

### 2. Show the CLI surface

```bash
uv run agentops --help
uv run agentops parallel --help
uv run agentops parallel-shared --help
uv run agentops swarm --help
uv run agentops certified-time --help
uv run agentops baseline-calibration --help
```

What to say:

The public surface is one CLI, not a pile of ad hoc scripts. Historical scripts
are still present for provenance, but the canonical route is `agentops`.

### 3. Show the evidence trail

Files:

- `studies/README.md`
- `studies/baseline_headroom/README.md`
- `studies/bp_probe_ablation/results/probe_ablation_summary.md`
- `studies/calibration_design/results/calibration_design_summary.md`

What to say:

The repo is structured as a sequence of studies. Each study has a question,
what was run, the result, the caveat, and the first file to read.

### 4. Show the strongest empirical result

File:

- `studies/bp_probe_ablation/results/probe_ablation_summary.md`

Key numbers:

| Probe | Meaning | Runs | Best `val_bpb` | Mean `val_bpb` |
|---|---|---:|---:|---:|
| `P11` | high-temperature exploration, no memory | 21 | 0.934 | 1.816 |
| `P12` | high-temperature exploration with shared memory | 41 | 0.914 | 1.049 |

What to say:

This is not a general claim that memory always helps. It is evidence that
unguided exploration can become destructive, and that shared memory can reduce
catastrophic repeats in this setting.

### 5. Show what is not claimed

Files:

- `studies/theory_validation/results/README.md`
- `docs/reviewer_checklist.md`

What to say:

The repo is explicit about limits. The BP theory is cleaner than the original
draft, but it is not fully validated. The studies show a path toward rigorous
agent-workflow evaluation, not a finished universal benchmark.

## Local Smoke Demo

This demo does not require Claude Code:

```bash
uv sync --dev
PYTHONPATH=src python -m pytest tests -q
PYTHONPATH=src python -m agentops_lab.cli --help
```

To run agent experiments, follow `docs/reproducibility.md` because those runs
require Claude Code authentication and a clean workspace.
