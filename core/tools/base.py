"""The Tool contract — every real-data client implements this.

Honesty rule baked into the type: a tool that isn't configured returns
`ok=False` with a clear reason. It MUST NOT return fabricated data.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from core.types import Citation


@dataclass
class ToolResult:
    ok: bool
    source: str                      # which real source produced this (for the UI/citations)
    data: object = None              # the real payload (dict/list)
    citations: list[Citation] = field(default_factory=list)
    error: str | None = None         # populated when ok is False (e.g. "ESTAT_APP_ID not configured")

    @classmethod
    def unconfigured(cls, source: str, missing: str) -> "ToolResult":
        return cls(ok=False, source=source, error=f"{missing} not configured — cannot fetch real data")


class Tool(ABC):
    name: str = "tool"
    description: str = ""

    @abstractmethod
    def available(self) -> bool:
        """True only if the tool can actually reach its real source (keys present)."""

    @abstractmethod
    def run(self, **kwargs) -> ToolResult:
        """Fetch REAL data. Never fabricate; on failure return ok=False with a reason."""
