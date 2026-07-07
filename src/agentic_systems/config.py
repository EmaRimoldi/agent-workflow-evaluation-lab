"""Canonical experiment configuration schema.

The consolidated repo keeps one config schema by re-exporting the base
`agent_parallelization_new` dataclasses during the preservation-first phase.
Future cleanup should move the implementation here and leave compatibility
imports behind.
"""

from agent_parallelization_new.config import AgentConfig, ExperimentConfig

__all__ = ["AgentConfig", "ExperimentConfig"]
