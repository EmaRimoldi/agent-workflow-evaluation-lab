# AgentOps Lab Architecture

AgentOps Lab treats `agentic_systems` as the public package surface while the
current tested runtime remains under `agent_parallelization_new`. The public
architecture is split between stable interfaces, compatibility runtime,
evaluation tooling, and experiment evidence.

## Canonical Runtime Shape

```text
agentic CLI
  -> modes.parallel       -> agent_parallelization_new.launcher.main_parallel
  -> modes.single_long    -> agent_parallelization_new.launcher.main_single_long
  -> modes.merge          -> agent_parallelization_new.merger.MergeOrchestrator
  -> modes.swarm          -> integrated blackboard surface and swarm runtime

agentic_systems.config
  -> AgentConfig, ExperimentConfig from agent_parallelization_new.config

agentic_systems.orchestrator
  -> Orchestrator from agent_parallelization_new.orchestrator

agentic_systems.communication
  -> SharedMemory blackboard
  -> coordinator helpers

agentic_systems.analysis
  -> H_prior / H_post diversity metrics

agentic_systems.instrumentation
  -> snapshotting
  -> reasoning traces
  -> certified time
```

## Configuration

There is one canonical config surface:

```python
from agentic_systems.config import AgentConfig, ExperimentConfig
```

During this public-release phase it re-exports the runtime dataclasses from
`agent_parallelization_new.config`. This keeps existing behavior stable while
runtime ownership moves behind the canonical package surface.

## Orchestration

There is one canonical orchestrator surface:

```python
from agentic_systems.orchestrator import Orchestrator
```

It currently delegates to `agent_parallelization_new.orchestrator.Orchestrator`.
The existing orchestrator owns process spawning, git worktree isolation, worker
integration, output collection, and report generation.

## Modes

| Mode | Module | Current integration status |
|---|---|---|
| `parallel` | `agentic_systems.modes.parallel` | Thin wrapper around the runtime launcher |
| `single_long` | `agentic_systems.modes.single_long` | Thin wrapper around the runtime launcher |
| `merge` | `agentic_systems.modes.merge` | Wrapper around `MergeOrchestrator`; CLI also preserves script behavior |
| `swarm` | `agentic_systems.modes.swarm` | Canonical blackboard creation plus `--run` delegation to the swarm runtime |

## Integrated Components

### Blackboard Communication

`src/agentic_systems/communication/blackboard.py` provides:

- append-only JSONL shared memory
- file locking via `fcntl`
- claim/dedup/release flow
- best-result sidecar
- context filtering for "other agents" reads

### Swarm Coordinator

`src/agentic_systems/communication/coordinator.py` imports the canonical
blackboard module and exposes local coordination helpers for shared-memory
agent workflows.

### Diversity Metrics

`src/agentic_systems/analysis/diversity.py` consolidates H_prior/H_post-style
analysis. Lightweight trajectory DTW is dependency-free; embedding and
weight-space metrics import heavy ML dependencies lazily.

### Instrumentation

`src/agentic_systems/instrumentation/` consolidates:

- snapshotting
- reasoning traces
- certified-time analysis

## Output And Reporting

The canonical reporting pipeline is still the runtime output stack under
`src/agent_parallelization_new/outputs/` plus merge/report scripts and the swarm
reporter path. A future cleanup should move that ownership under
`agentic_systems.outputs` and leave compatibility imports behind.
