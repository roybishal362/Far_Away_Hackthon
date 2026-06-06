"""Official Japanese government statistics — e-Stat API 3.0 (JSON).

Real authoritative data on foreign-worker employment & residents. Used by the
Demand agent to back sector-demand claims with a government source (not vibes).

Two modes:
  - search(word): find the right statsDataId (run once to discover IDs)
  - data(stats_data_id): fetch the real series

Note: the exact statsDataId for "Employment Situation of Foreign Workers" is
discovered via search() once the key is set, then pinned in DEMAND_STATS_IDS.
"""
from __future__ import annotations

import requests

from config import SETTINGS
from core.tools.base import Tool, ToolResult
from core.types import Citation

BASE = "https://api.e-stat.go.jp/rest/3.0/app/json"

# Pinned after discovery via search(); see ARCHITECTURE §8.
DEMAND_STATS_IDS: dict[str, str] = {}


class EstatTool(Tool):
    name = "estat"
    description = "Official Japan government statistics (e-Stat)."

    def available(self) -> bool:
        return bool(SETTINGS.estat_app_id)

    def search(self, word: str, limit: int = 10) -> ToolResult:
        if not self.available():
            return ToolResult.unconfigured(self.name, "ESTAT_APP_ID")
        try:
            r = requests.get(
                f"{BASE}/getStatsList",
                params={"appId": SETTINGS.estat_app_id, "searchWord": word, "limit": limit, "lang": "E"},
                timeout=25,
            )
            r.raise_for_status()
            tables = (
                r.json().get("GET_STATS_LIST", {})
                .get("DATALIST_INF", {})
                .get("TABLE_INF", [])
            )
            if isinstance(tables, dict):
                tables = [tables]
            hits = [{"id": t.get("@id"), "title": str(t.get("TITLE", ""))[:120]} for t in tables[:limit]]
            return ToolResult(ok=True, source="e-Stat (gov statistics list)", data=hits)
        except requests.RequestException as exc:
            return ToolResult(ok=False, source="e-Stat", error=f"e-Stat search failed: {exc}")

    def data(self, stats_data_id: str, limit: int = 50) -> ToolResult:
        if not self.available():
            return ToolResult.unconfigured(self.name, "ESTAT_APP_ID")
        try:
            r = requests.get(
                f"{BASE}/getStatsData",
                params={"appId": SETTINGS.estat_app_id, "statsDataId": stats_data_id, "limit": limit, "lang": "E"},
                timeout=30,
            )
            r.raise_for_status()
            sd = r.json().get("GET_STATS_DATA", {}).get("STATISTICAL_DATA", {})
            values = sd.get("DATA_INF", {}).get("VALUE", [])
            if isinstance(values, dict):
                values = [values]
            series = [{"category": v.get("@cat01") or v.get("@area") or v.get("@time"), "value": v.get("$")} for v in values[:limit]]
            cite = Citation(
                source_url=f"https://www.e-stat.go.jp/en/dbview?sid={stats_data_id}",
                title="e-Stat — Official Statistics of Japan",
            )
            return ToolResult(ok=True, source="e-Stat (gov statistics)", data=series, citations=[cite])
        except requests.RequestException as exc:
            return ToolResult(ok=False, source="e-Stat", error=f"e-Stat data fetch failed: {exc}")

    def run(self, stats_data_id: str | None = None, search_word: str | None = None) -> ToolResult:  # type: ignore[override]
        if stats_data_id:
            return self.data(stats_data_id)
        if search_word:
            return self.search(search_word)
        return ToolResult(ok=False, source="e-Stat", error="provide stats_data_id or search_word")
