"""Adaptive orchestration: the engine must SKIP SSW-only agents on a reroute —
and run them otherwise. This is the 'agentic, not a workflow' claim, as a test."""
from core.agents.base import Agent, AgentResult
from core.engine import Engine
from core.types import WorkerProfile


class FakePathway(Agent):
    name = "pathway"

    def __init__(self, verdict):
        self.verdict = verdict

    def run(self, profile, context):
        return AgentResult(agent=self.name, ok=True, data={"eligibility_verdict": self.verdict})


class FakeProcedure(Agent):
    name = "procedure"  # in the engine's SSW-only set
    ran = False

    def run(self, profile, context):
        FakeProcedure.ran = True
        return AgentResult(agent=self.name, ok=True)


def test_redirect_skips_ssw_only_agents():
    FakeProcedure.ran = False
    res = Engine([FakePathway("redirect"), FakeProcedure()]).run(WorkerProfile())
    assert not FakeProcedure.ran, "engineer-route profile must never run SSW-only agents"
    assert any(step.kind == "skip" for _, step in res.timeline), "the skip must be visible in the timeline"
    assert "procedure" not in res.results


def test_ssw_route_runs_everything():
    FakeProcedure.ran = False
    res = Engine([FakePathway("eligible"), FakeProcedure()]).run(WorkerProfile())
    assert FakeProcedure.ran
    assert res.results["procedure"].ok


def test_one_failing_agent_does_not_kill_the_run():
    class Exploder(Agent):
        name = "exploder"

        def run(self, profile, context):
            raise RuntimeError("boom")

    res = Engine([FakePathway("eligible"), Exploder()]).run(WorkerProfile())
    assert res.results["exploder"].ok is False
    assert res.ok  # pathway still succeeded
