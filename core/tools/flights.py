"""Real flight offers India -> Japan — Amadeus Flight Offers Search API.

Uses the free Self-Service test environment. Returns real, indicative offers
(note: low-cost carriers excluded by Amadeus). Powers the journey cost/timeline.
"""
from __future__ import annotations

import requests

from config import SETTINGS
from core.tools.base import Tool, ToolResult
from core.types import Citation

# Minimal city -> IATA map for the corridor (extend as needed).
CITY_IATA = {
    "delhi": "DEL", "new delhi": "DEL", "mumbai": "BOM", "bangalore": "BLR",
    "bengaluru": "BLR", "chennai": "MAA", "hyderabad": "HYD", "kolkata": "CCU",
    "tokyo": "NRT", "osaka": "KIX", "nagoya": "NGO", "fukuoka": "FUK", "sapporo": "CTS",
}


def to_iata(city: str, default: str) -> str:
    return CITY_IATA.get((city or "").strip().lower(), default)


class FlightsTool(Tool):
    name = "flights"
    description = "Real flight offers (Amadeus)."
    BASE = "https://test.api.amadeus.com"

    def available(self) -> bool:
        return bool(SETTINGS.amadeus_client_id and SETTINGS.amadeus_client_secret)

    def _token(self) -> str:
        r = requests.post(
            f"{self.BASE}/v1/security/oauth2/token",
            data={
                "grant_type": "client_credentials",
                "client_id": SETTINGS.amadeus_client_id,
                "client_secret": SETTINGS.amadeus_client_secret,
            },
            timeout=20,
        )
        r.raise_for_status()
        return r.json()["access_token"]

    def run(  # type: ignore[override]
        self,
        origin_city: str = "Delhi",
        target_city: str = "Tokyo",
        departure_date: str = "",
        adults: int = 1,
        currency: str = "INR",
        limit: int = 5,
    ) -> ToolResult:
        if not self.available():
            return ToolResult.unconfigured(self.name, "AMADEUS_CLIENT_ID/SECRET")
        if not departure_date:
            return ToolResult(ok=False, source="Amadeus", error="departure_date (YYYY-MM-DD) required")

        origin, dest = to_iata(origin_city, "DEL"), to_iata(target_city, "NRT")
        try:
            token = self._token()
            r = requests.get(
                f"{self.BASE}/v2/shopping/flight-offers",
                headers={"Authorization": f"Bearer {token}"},
                params={
                    "originLocationCode": origin,
                    "destinationLocationCode": dest,
                    "departureDate": departure_date,
                    "adults": adults,
                    "currencyCode": currency,
                    "max": limit,
                },
                timeout=30,
            )
            r.raise_for_status()
            payload = r.json()
        except requests.RequestException as exc:
            return ToolResult(ok=False, source="Amadeus", error=f"Amadeus request failed: {exc}")

        offers = []
        for o in payload.get("data", [])[:limit]:
            itin = (o.get("itineraries") or [{}])[0]
            segs = itin.get("segments") or []
            offers.append({
                "price": o.get("price", {}).get("total"),
                "currency": o.get("price", {}).get("currency", currency),
                "duration": itin.get("duration"),
                "stops": max(len(segs) - 1, 0),
                "carrier": segs[0].get("carrierCode") if segs else None,
                "from": origin,
                "to": dest,
                "departure": segs[0].get("departure", {}).get("at") if segs else None,
            })

        cite = Citation(
            source_url="https://developers.amadeus.com/self-service/category/flights/api-doc/flight-offers-search",
            title=f"Amadeus Flight Offers — {origin}→{dest} {departure_date}",
        )
        return ToolResult(ok=True, source="Amadeus (real flight offers)", data=offers, citations=[cite])
