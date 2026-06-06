"""The Agent contract.

Every agent returns an AgentResult carrying its reasoning steps (for the live
timeline UI), its real data, the citations backing it, and a confidence in [0,1].
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from core.types import Citation, WorkerProfile


@dataclass
class ReasoningStep:
    """One visible step in the agent timeline (the 'watch it think' wow)."""
    label: str                       # e.g. "Querying e-Stat for caregiving demand"
    detail: str = ""
    kind: str = "think"              # think | tool_call | tool_result | decide


@dataclass
class AgentResult:
    agent: str
    summary: str = ""                          # human-readable headline
    data: object = None                        # structured result
    citations: list[Citation] = field(default_factory=list)
    confidence: float = 0.0                    # 0..1
    steps: list[ReasoningStep] = field(default_factory=list)
    ok: bool = True
    error: str | None = None

    def grounded(self) -> bool:
        """A result is 'grounded' only if at least one real citation backs it."""
        return bool(self.citations)


class Agent(ABC):
    name: str = "agent"

    @abstractmethod
    def run(self, profile: WorkerProfile, context: dict) -> AgentResult:
        """Do this agent's job. `context` carries results from earlier agents."""
