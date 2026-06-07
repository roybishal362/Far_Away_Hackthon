"""The orchestration engine — the single entrypoint the UI calls.

UI usage:
    from core.engine import Engine, WorkerProfile
    result = Engine().run(profile, on_step=callback)

The Engine threads each agent's output into a shared `context`, records every
reasoning step for the live timeline, and aggregates a run-level grounding metric.
Agents are registered in `default_agents()` (filled in as we build each one).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from core.agents.base import Agent, AgentResult, ReasoningStep
from core.types import WorkerProfile

StepCallback = Callable[[str, ReasoningStep], None]   # (agent_name, step) -> None for live UI
ApproveCallback = Callable[[str], bool]               # (action_desc) -> approved? (human-in-the-loop)


@dataclass
class RunResult:
    profile: WorkerProfile
    results: dict[str, AgentResult] = field(default_factory=dict)
    timeline: list[tuple[str, ReasoningStep]] = field(default_factory=list)
    metrics: dict = field(default_factory=dict)
    ok: bool = True

    def grounding_score(self) -> float:
        """Run-level Source-Grounding Score: fraction of agents whose claims are cited."""
        produced = [r for r in self.results.values() if r.ok]
        if not produced:
            return 0.0
        return sum(1 for r in produced if r.grounded()) / len(produced)


def default_agents() -> list[Agent]:
    """Registered agents, in execution order (each threads context to the next)."""
    from core.agents.pathway import PathwayAgent
    from core.agents.jobs import JobsAgent
    from core.agents.procedure import ProcedureAgent
    from core.agents.prep import PrepAgent
    from core.agents.journey import JourneyAgent
    from core.agents.synthesis import SynthesisAgent

    return [PathwayAgent(), JobsAgent(), ProcedureAgent(), PrepAgent(), JourneyAgent(), SynthesisAgent()]


# SSW-specific agents that don't apply when the worker is routed off SSW (e.g. IT -> Engineer visa).
_SSW_ONLY = {"procedure", "prep", "journey"}


class Engine:
    def __init__(self, agents: list[Agent] | None = None) -> None:
        self.agents = agents if agents is not None else default_agents()

    def run(
        self,
        profile: WorkerProfile,
        on_step: StepCallback | None = None,
        approve: ApproveCallback | None = None,
    ) -> RunResult:
        result = RunResult(profile=profile)
        context: dict = {"approve": approve}

        for agent in self.agents:
            # Adaptive orchestration: if Pathway routed the worker off SSW (e.g. IT -> Engineer
            # visa), skip the SSW-only agents — don't show irrelevant SSW steps.
            pw = result.results.get("pathway")
            if (
                agent.name in _SSW_ONLY
                and pw
                and getattr(pw, "data", None)
                and pw.data.get("eligibility_verdict") == "redirect"
            ):
                skip = ReasoningStep(f"{agent.name.capitalize()} skipped — not applicable for this visa route", kind="skip")
                result.timeline.append((agent.name, skip))
                if on_step:
                    on_step(agent.name, skip)
                continue
            try:
                ar = agent.run(profile, context)
            except Exception as exc:  # an agent failing must not kill the whole run
                ar = AgentResult(agent=agent.name, ok=False, error=str(exc))

            result.results[agent.name] = ar
            context[agent.name] = ar
            for step in ar.steps:
                result.timeline.append((agent.name, step))
                if on_step:
                    on_step(agent.name, step)

        result.metrics["grounding_score"] = result.grounding_score()
        result.ok = any(r.ok for r in result.results.values()) if result.results else False
        return result
