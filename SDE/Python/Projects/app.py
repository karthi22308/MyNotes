"""
Agentic Travel Recommendation App (Streamlit)

How to run:
  1) Save this file as app.py
  2) (Recommended) Create a virtual env
  3) pip install -r requirements.txt  (requirements listed below)
  4) streamlit run app.py

Env vars (recommended):
  AZURE_OPENAI_API_KEY=...           # If not set, the hardcoded fallback below is used
  AZURE_OPENAI_ENDPOINT=...          # Optional; fallback below
  AZURE_OPENAI_API_VERSION=2024-06-01
  GOOGLE_PLACES_API_KEY=...          # Optional: to fetch real ratings & reviews

Minimal requirements (put these into requirements.txt):
  streamlit>=1.36
  openai>=1.40.0
  pydantic>=2.7
  requests>=2.31
  pandas>=2.2
  python-dateutil>=2.9

Note: The Places API integration is optional. If you do not set GOOGLE_PLACES_API_KEY,
      the RatingAgent will use the LLM to infer ratings heuristically.
"""

from __future__ import annotations
import os
import math
import json
import time
import uuid
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Any, Tuple

import requests
import pandas as pd
from dateutil import parser as dateparser
import streamlit as st

# -----------------------------
# Azure OpenAI Client (LLM)
# -----------------------------
try:
    from openai import AzureOpenAI
except Exception as e:
    AzureOpenAI = None

# --- Your provided Azure OpenAI config (fallbacks). ---
FALLBACK_AZURE_CONFIG = dict(
    api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-06-01"),
    azure_endpoint=os.getenv(
        "AZURE_OPENAI_ENDPOINT",
        "https://hexavarsity-secureapi.azurewebsites.net/api/azureai",
    ),
    api_key=os.getenv("AZURE_OPENAI_API_KEY", "922892c42af122a9"),
)

MODEL_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini")

# -----------------------------
# Lightweight Agent Framework
# -----------------------------
@dataclass
class Recommendation:
    name: str
    country: Optional[str]
    region: Optional[str]
    lat: Optional[float]
    lon: Optional[float]
    days_suggested: int
    rationale: str
    start_date_weather: Optional[str] = None
    weather_brief: Optional[str] = None
    rating: Optional[float] = None
    rating_basis: Optional[str] = None


class LLMClient:
    def __init__(self):
        if AzureOpenAI is None:
            raise RuntimeError(
                "openai>=1.x is required. Please install with `pip install openai`"
            )
        self.client = AzureOpenAI(**FALLBACK_AZURE_CONFIG)
        self.model = MODEL_DEPLOYMENT

    def chat(self, system: str, user: str, temperature: float = 0.4, max_tokens: int = 1000) -> str:
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return resp.choices[0].message.content


# -----------------------------
# Utilities: geocode & weather
# -----------------------------
HEADERS = {"User-Agent": "AgenticTravel/1.0 (contact: demo@example.com)"}


def geocode_place(place: str) -> Optional[Tuple[float, float, Dict[str, Any]]]:
    """Geocode a place name using Nominatim (OpenStreetMap)."""
    try:
        url = "https://nominatim.openstreetmap.org/search"
        params = {"q": place, "format": "json", "limit": 1}
        r = requests.get(url, params=params, headers=HEADERS, timeout=15)
        r.raise_for_status()
        data = r.json()
        if not data:
            return None
        lat = float(data[0]["lat"]) if "lat" in data[0] else None
        lon = float(data[0]["lon"]) if "lon" in data[0] else None
        return (lat, lon, data[0])
    except Exception:
        return None


def fetch_weather_summary(lat: float, lon: float, start_date: str, end_date: str) -> Optional[str]:
    """Fetch a basic weather summary using Open-Meteo (no API key)."""
    try:
        # Daily temps and precipitation probability
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "start_date": start_date,
            "end_date": end_date,
            "daily": [
                "temperature_2m_max",
                "temperature_2m_min",
                "precipitation_probability_max",
            ],
            "timezone": "auto",
        }
        r = requests.get(url, params=params, timeout=20)
        r.raise_for_status()
        d = r.json()
        daily = d.get("daily", {})
        if not daily:
            return None
        days = len(daily.get("time", []))
        tmax = daily.get("temperature_2m_max", [])
        tmin = daily.get("temperature_2m_min", [])
        pmax = daily.get("precipitation_probability_max", [])
        if not days:
            return None
        avg_max = sum(tmax) / len(tmax) if tmax else None
        avg_min = sum(tmin) / len(tmin) if tmin else None
        avg_rain = sum(pmax) / len(pmax) if pmax else None
        summary = (
            f"{days} days | Avg Max: {avg_max:.1f}°C, Avg Min: {avg_min:.1f}°C, "
            f"Avg Rain Prob: {avg_rain:.0f}%"
        )
        return summary
    except Exception:
        return None


# -----------------------------
# Agents
# -----------------------------
class DestinationPlanner:
    SYSTEM = (
        "You are a precise travel planner. Propose travel destinations or in-city spots "
        "that fit within a user's trip duration, origin, international preference, and season. "
        "Prefer options with minimal transit if days are few. Return concise JSON with 3-6 candidates."
    )

    @staticmethod
    def build_prompt(origin: str, days: int, start_date: str, end_date: str, international: bool) -> str:
        return f"""
Origin: {origin}
Trip length: {days} days
Dates: {start_date} to {end_date}
International allowed: {international}

Task: Suggest 4 destination cities (country too) that best fit the dates and length.
For each, include ideal days to spend (<= trip length) and a short rationale (weather/seasonality, travel time, vibe).
Respond as compact JSON list with objects: [{{"name":"City, Country","country":"Country","region":"Region/State(optional)","days_suggested":int,"rationale":"..."}}].
Keep names conventional (e.g., "Bali, Indonesia" not just "Bali").
"""

    def run(self, llm: LLMClient, origin: str, days: int, start_date: str, end_date: str, international: bool) -> List[Recommendation]:
        raw = llm.chat(self.SYSTEM, self.build_prompt(origin, days, start_date, end_date, international))
        try:
            data = json.loads(DestinationPlanner._extract_json(raw))
        except Exception:
            data = []
        recs: List[Recommendation] = []
        for item in data[:6]:
            name = item.get("name") or ""
            country = item.get("country")
            region = item.get("region")
            days_suggested = int(item.get("days_suggested", days))
            rationale = item.get("rationale", "")
            lat, lon, _meta = (None, None, None)
            geo = geocode_place(name)
            if geo:
                lat, lon, _meta = geo
            recs.append(
                Recommendation(
                    name=name,
                    country=country,
                    region=region,
                    lat=lat,
                    lon=lon,
                    days_suggested=min(days_suggested, days),
                    rationale=rationale,
                )
            )
        return recs

    @staticmethod
    def _extract_json(text: str) -> str:
        # Try to pull the first JSON array/object from LLM output
        text = text.strip()
        start = text.find("[")
        if start == -1:
            start = text.find("{")
        end = text.rfind("]")
        if end == -1:
            end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            return text[start : end + 1]
        return "[]"


class InCitySpotPlanner:
    SYSTEM = (
        "You are a local guide. Given a destination city and trip length, propose the top 5 must-visit spots "
        "(landmarks, neighborhoods, nature, food zones). Prefer diversity. Return JSON list of spots with short rationale."
    )

    @staticmethod
    def build_prompt(city: str, days: int) -> str:
        return f"""
City: {city}
Trip days: {days}
Task: Suggest top 5 spots within the city/nearby with short rationales.
Return JSON list: [{{"name":"Spot Name","rationale":"why it's great"}}]
Keep names canonical (no emojis)."""

    def run(self, llm: LLMClient, city: str, days: int) -> List[Dict[str, str]]:
        raw = llm.chat(self.SYSTEM, self.build_prompt(city, days))
        try:
            data = json.loads(DestinationPlanner._extract_json(raw))
        except Exception:
            data = []
        spots: List[Dict[str, str]] = []
        for s in data[:5]:
            name = s.get("name") or ""
            rationale = s.get("rationale", "")
            spots.append({"name": name, "rationale": rationale})
        return spots


class WeatherAgent:
    @staticmethod
    def run(rec: Recommendation, start_date: str, end_date: str) -> Recommendation:
        if rec.lat is None or rec.lon is None:
            geo = geocode_place(rec.name)
            if geo:
                rec.lat, rec.lon, _ = geo
        if rec.lat is not None and rec.lon is not None:
            summary = fetch_weather_summary(rec.lat, rec.lon, start_date, end_date)
            rec.start_date_weather = start_date
            rec.weather_brief = summary or "Weather data unavailable"
        else:
            rec.weather_brief = "Could not geocode destination"
        return rec


class RatingAgent:
    SYSTEM = (
        "You rate destinations/spots based on general traveler sentiment, safety, cleanliness, affordability, and attractions. "
        "Return a float 1.0-5.0 and a 1-sentence reason."
    )

    @staticmethod
    def google_places_rating(query: str, api_key: Optional[str]) -> Optional[Tuple[float, str]]:
        if not api_key:
            return None
        try:
            # Text Search to get place_id
            ts_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
            params = {"query": query, "key": api_key}
            r = requests.get(ts_url, params=params, timeout=20)
            r.raise_for_status()
            data = r.json()
            if data.get("status") != "OK" or not data.get("results"):
                return None
            place = data["results"][0]
            rating = place.get("rating")
            user_ratings_total = place.get("user_ratings_total")
            if rating is None:
                return None
            reason = f"Google rating {rating} from {user_ratings_total} reviews"
            return float(rating), reason
        except Exception:
            return None

    def run(self, llm: LLMClient, name: str, country: Optional[str]) -> Tuple[float, str]:
        # First try Google Places (if key present). Fallback to LLM heuristic.
        api_key = os.getenv("GOOGLE_PLACES_API_KEY")
        gp = self.google_places_rating(f"{name} {country or ''}".strip(), api_key)
        if gp:
            return gp
        prompt = f"Rate '{name}' (country: {country or 'Unknown'}) from 1.0-5.0. Respond JSON: {{\"rating\":float, \"reason\":\"...\"}}"
        raw = llm.chat(self.SYSTEM, prompt)
        try:
            data = json.loads(DestinationPlanner._extract_json(raw))
        except Exception:
            data = {}
        rating = float(data.get("rating", 4.2))
        reason = data.get("reason", "Generally positive traveler reviews.")
        rating = max(1.0, min(5.0, rating))
        return rating, reason


# -----------------------------
# Orchestrator
# -----------------------------
@dataclass
class TripInput:
    origin: str
    destination: Optional[str]
    start_date: str
    end_date: str
    days: int
    international: bool


class TravelOrchestrator:
    def __init__(self):
        self.llm = LLMClient()
        self.dest_planner = DestinationPlanner()
        self.spot_planner = InCitySpotPlanner()
        self.rating_agent = RatingAgent()

    def plan(self, trip: TripInput) -> Dict[str, Any]:
        # 1) Destination selection
        if (trip.destination or "").strip():
            # Destination provided: build in-city plan
            dest_name = trip.destination.strip()
            geo = geocode_place(dest_name)
            lat = lon = None
            if geo:
                lat, lon, _ = geo
            rec = Recommendation(
                name=dest_name,
                country=None,
                region=None,
                lat=lat,
                lon=lon,
                days_suggested=trip.days,
                rationale="User-selected destination",
            )
            rec = WeatherAgent.run(rec, trip.start_date, trip.end_date)
            # Spots
            spots = self.spot_planner.run(self.llm, dest_name, trip.days)
            # Rate destination
            r, why = self.rating_agent.run(self.llm, rec.name, rec.country)
            rec.rating, rec.rating_basis = r, why
            return {
                "mode": "in-city",
                "destination": asdict(rec),
                "spots": spots,
            }
        else:
            # Destination not provided: call DestinationPlanner agent
            recs = self.dest_planner.run(
                self.llm, trip.origin, trip.days, trip.start_date, trip.end_date, trip.international
            )
            # Weather + ratings per rec
            enriched: List[Recommendation] = []
            for rec in recs:
                rec = WeatherAgent.run(rec, trip.start_date, trip.end_date)
                r, why = self.rating_agent.run(self.llm, rec.name, rec.country)
                rec.rating, rec.rating_basis = r, why
                enriched.append(rec)
            # Sort by rating desc
            enriched.sort(key=lambda x: (x.rating or 0), reverse=True)
            return {
                "mode": "multi-dest",
                "recommendations": [asdict(r) for r in enriched],
            }


# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Agentic Travel Recommender", page_icon="✈️", layout="wide")

st.title("✈️ Agentic Travel Recommender")
st.caption("LLM + tools: destination planner • weather checker • ratings agent")

with st.sidebar:
    st.header("Trip Inputs")
    origin = st.text_input("From (City, Country)", value="Coimbatore, India")
    destination = st.text_input("Destination (optional)")
    colA, colB = st.columns(2)
    with colA:
        start_date = st.date_input("From date")
    with colB:
        end_date = st.date_input("To date")
    days_inp = st.number_input("No. of days (optional, 0 = auto)", min_value=0, max_value=60, value=0, step=1)
    international = st.toggle("Allow international destinations", value=True)
    go = st.button("Plan Trip 🚀")

# Normalize inputs
if go:
    if not origin.strip():
        st.error("Please enter 'From'.")
        st.stop()
    if start_date > end_date:
        st.error("From date must be on or before To date.")
        st.stop()

    sd = start_date.isoformat()
    ed = end_date.isoformat()
    auto_days = (end_date - start_date).days + 1
    days = days_inp if days_inp > 0 else auto_days

    trip = TripInput(
        origin=origin.strip(),
        destination=destination.strip() or None,
        start_date=sd,
        end_date=ed,
        days=days,
        international=international,
    )

    with st.spinner("Asking agents to plan..."):
        try:
            orchestrator = TravelOrchestrator()
            result = orchestrator.plan(trip)
        except Exception as e:
            st.exception(e)
            st.stop()

    st.subheader("Results")
    if result["mode"] == "in-city":
        d = result["destination"]
        spots = result.get("spots", [])
        left, right = st.columns([1, 1])
        with left:
            st.metric(d.get("name", "Destination"), f"Rating {d.get('rating', '—')}")
            st.write(d.get("rationale"))
            st.write("**Weather**:", d.get("weather_brief", "-"))
        with right:
            if d.get("lat") and d.get("lon"):
                st.map(pd.DataFrame([{"lat": d["lat"], "lon": d["lon"]}]))
        st.markdown("---")
        st.markdown("### Top Spots")
        for s in spots:
            st.markdown(f"- **{s['name']}** — {s['rationale']}")

    else:
        recs = result.get("recommendations", [])
        if not recs:
            st.warning("No recommendations were produced. Try adjusting inputs.")
            st.stop()
        df = pd.DataFrame(recs)
        # Select key columns and order by rating desc
        show_cols = [
            "name",
            "country",
            "region",
            "days_suggested",
            "weather_brief",
            "rating",
            "rating_basis",
            "rationale",
        ]
        df_show = df[show_cols].sort_values(by="rating", ascending=False)
        st.dataframe(df_show, use_container_width=True)

        # Map points
        coords = [
            {"lat": r["lat"], "lon": r["lon"]}
            for r in recs
            if r.get("lat") is not None and r.get("lon") is not None
        ]
        if coords:
            st.markdown("#### Map of suggested destinations")
            st.map(pd.DataFrame(coords))

        # Cards
        st.markdown("---")
        st.markdown("### Picks (ordered by rating)")
        for r in recs:
            with st.container(border=True):
                st.markdown(f"#### {r['name']}  ")
                cols = st.columns([2, 1])
                with cols[0]:
                    st.markdown(f"**Rating:** {r.get('rating', '—')}  ")
                    st.markdown(f"**Why it fits:** {r.get('rationale', '')}")
                    st.markdown(f"**Rating basis:** {r.get('rating_basis', '')}")
                    st.markdown(f"**Weather:** {r.get('weather_brief', '-')}")
                    st.markdown(f"**Suggested days:** {r.get('days_suggested', '-')}")
                with cols[1]:
                    if r.get("lat") and r.get("lon"):
                        st.map(pd.DataFrame([{"lat": r["lat"], "lon": r["lon"]}]))

# Footer
st.markdown("""
---
**Notes**
- Ratings come from Google Places when `GOOGLE_PLACES_API_KEY` is provided; otherwise an LLM-based heuristic is used.
- Weather summaries are from Open-Meteo and are approximate.
- Geocoding is via OpenStreetMap Nominatim.
""")
