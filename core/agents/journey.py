"""Journey agent — fetches REAL flight offers (Amadeus) for the relocation and
summarizes cost/timeline. Degrades honestly without a key or a departure date."""
from __future__ import annotations

from core.agents.base import Agent, AgentResult, ReasoningStep
from core.tools.flights import FlightsTool
from core.types import WorkerProfile


class JourneyAgent(Agent):
    name = "journey"

    def __init__(self) -> None:
        self.tool = FlightsTool()

    def run(self, profile: WorkerProfile, context: dict) -> AgentResult:
        departure_date = context.get("departure_date", "")
        steps = [ReasoningStep(f"Planning relocation {profile.origin_city} -> {profile.target_city}", kind="tool_call")]
        result = self.tool.run(
            origin_city=profile.origin_city,
            target_city=profile.target_city,
            departure_date=departure_date,
            limit=5,
        )
        if not result.ok:
            steps.append(ReasoningStep("Flight data unavailable", result.error or "", kind="tool_result"))
            return AgentResult(agent=self.name, ok=False, error=result.error, steps=steps)

        offers = result.data or []
        cheapest = min((float(o["price"]) for o in offers if o.get("price")), default=None)
        steps.append(ReasoningStep(f"Found {len(offers)} real flight offers", result.source, kind="tool_result"))
        summary = f"{len(offers)} real flight options" + (f"; from {cheapest:.0f} {offers[0].get('currency','INR')}" if cheapest else "")
        return AgentResult(
            agent=self.name,
            summary=summary,
            data={"offers": offers, "cheapest": cheapest},
            citations=result.citations,
            confidence=0.9 if offers else 0.3,
            steps=steps,
            ok=True,
        )
