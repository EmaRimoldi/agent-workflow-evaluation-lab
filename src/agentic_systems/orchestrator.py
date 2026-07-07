"""Canonical orchestrator surface.

The implementation currently delegates to the compatibility runtime so there is
one operational orchestrator behind the public `agentic_systems` import path.
"""

from agent_parallelization_new.orchestrator import Orchestrator

__all__ = ["Orchestrator"]
