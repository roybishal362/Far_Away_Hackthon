"""Live job openings in Japan — JSearch API via OpenWeb Ninja (real-time).

Pulls real postings (Google for Jobs / Indeed / LinkedIn etc.). Each job's real
apply-link becomes a citation, so the UI can prove the listing exists.
"""
from __future__ import annotations

import requests

from config import SETTINGS
from core.tools.base import Tool, ToolResult
from core.types import Citation

JSEARCH_URL = "https://api.openwebninja.com/jsearch/search-v2"


def _extract_jobs(payload: dict) -> list[dict]:
    """search-v2 may return data as a list-of-pages (each with .jobs), a single
    page dict (.jobs), or a flat list. Tolerate all shapes — never index blindly."""
    data = payload.get("data")
    if isinstance(data, dict):
        return data.get("jobs") or []
    if isinstance(data, list):
        if data and isinstance(data[0], dict) and "jobs" in data[0]:
            return data[0].get("jobs") or []
        return data
    return []


class JobsTool(Tool):
    name = "jobs"
    description = "Real-time job openings in Japan (JSearch / OpenWeb Ninja)."

    def available(self) -> bool:
        return bool(SETTINGS.jsearch_api_key)

    def run(self, query: str, location: str = "Japan", limit: int = 20, num_pages: int = 2) -> ToolResult:  # type: ignore[override]
        if not self.available():
            return ToolResult.unconfigured(self.name, "JSEARCH_API_KEY")

        try:
            r = requests.get(
                JSEARCH_URL,
                headers={"x-api-key": SETTINGS.jsearch_api_key},
                params={"query": f"{query} in {location}", "country": "jp", "page": "1", "num_pages": str(num_pages)},
                timeout=30,
            )
            r.raise_for_status()
            payload = r.json()
        except requests.RequestException as exc:
            return ToolResult(ok=False, source="JSearch", error=f"JSearch request failed: {exc}")

        jobs = []
        for j in _extract_jobs(payload)[:limit]:
            jobs.append({
                "title": j.get("job_title"),
                "employer": j.get("employer_name"),
                "city": j.get("job_city") or j.get("job_location") or j.get("job_country"),
                "apply_link": j.get("job_apply_link"),
                "posted": j.get("job_posted_at_datetime_utc") or j.get("job_posted_at"),
                "employment_type": j.get("job_employment_type"),
            })

        citations = [
            Citation(source_url=j["apply_link"], title=f'{j["title"]} - {j["employer"]}')
            for j in jobs if j.get("apply_link") and j.get("title")
        ][:5]
        return ToolResult(ok=True, source="JSearch (real-time jobs)", data=jobs, citations=citations)
