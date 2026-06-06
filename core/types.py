"""Shared data types used across agents, tools, and the engine."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Citation:
    """A pointer to a REAL source backing a claim. No citation => not shown as fact."""
    source_url: str
    title: str
    snippet: str = ""

    def short(self) -> str:
        return self.title or self.source_url


@dataclass
class WorkerProfile:
    """What the worker tells us. Kept minimal by design (privacy)."""
    skills: str = ""                 # free text, e.g. "nursing, 3 yrs hospital"
    sector_interest: str = ""        # desired SSW sector, optional
    years_experience: float = 0.0
    japanese_level: str = "none"     # none | JFT-Basic | N5 | N4 | N3+
    education: str = ""
    origin_city: str = "Delhi"
    target_city: str = "Tokyo"       # for jobs + flights
    lang: str = "en"                 # output language: en | hi | ja
    languages: list[str] = field(default_factory=lambda: ["en"])

    def redacted(self) -> dict:
        """A log-safe view: no raw PII, just coarse signals."""
        return {
            "has_skills": bool(self.skills),
            "sector_interest": self.sector_interest or "unspecified",
            "japanese_level": self.japanese_level,
            "experience_band": "0-1" if self.years_experience < 1 else ("1-3" if self.years_experience < 3 else "3+"),
        }
