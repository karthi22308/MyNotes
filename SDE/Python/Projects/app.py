"""
Agentic Travel Recommendation App (Streamlit)

Enhancements:
 - Added family_option and genre inputs
 - Added dynamic weather alerts (stormy/rainy conditions flagged)

How to run:
  1) Save this file as app.py
  2) (Recommended) Create a virtual env
  3) pip install -r requirements.txt  (requirements listed below)
  4) streamlit run app.py

Minimal requirements (requirements.txt):
  streamlit>=1.36
  openai>=1.40.0
  pydantic>=2.7
  requests>=2.31
  pandas>=2.2
  python-dateutil>=2.9
"""

from __future__ import annotations
import os
import json
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
except Exception:
    AzureOpenAI = None

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
# Data Models
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
    weather_alert: Optional[str] = None
    rating: Optional[float] = None
    rating_basis: Optional[str] = None


@dataclass
class TripInput:
    origin: str
    destination: Optional[str]
    start_date: str
    end_date: str
    days: int
    international: bool
    family_option: str
    genre: str


# -----------------------------
# LLM Client
# -----------------------------
class LLMClient:
    def __init__(self):
        if AzureOpenAI is None:
            raise RuntimeError("openai>=1.x required. Install with `pip install openai`")
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
# Utilities
# -----------------------------
HEADERS = {"User-Agent": "AgenticTravel/1.0 (contact: demo@example.com)"}


def geocode_place(place: str) -> Optional[Tuple[float, float, Dict[str, Any]]]:
    try:
        url = "https://nominatim.openstreetmap.org/search"
        params = {"q": place, "format": "json", "limit": 1}
        r = requests.get(url, params=params, headers=HEADERS, timeout=15)
        r.raise_for_status()
        data = r.json()
        if not data:
            return None
        return float(data[0]["lat"]), float(data[0]["lon"]), data[0]
    except Exception:
        return None


def fetch_weather_summary(lat: float, lon: float, start_date: str, end_date: str) -> Tuple[Optional[str], Optional[str]]:
    """Fetch weather summary and alerts."""
    try:
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
            return None, None

        tmax = daily.get("temperature_2m_max", [])
        tmin = daily.get("temperature_2m_min", [])
        pmax = daily.get("precipitation_probability_max", [])

        avg_max = sum(tmax) / len(tmax) if tmax else None
        avg_min = sum(tmin) / len(tmin) if tmin else None
        avg_rain = sum(pmax) / len(pmax) if pmax else None

        summary = (
            f"{len(daily['time'])} days | Avg Max: {avg_max:.1f}°C, "
            f"Avg Min: {avg_min:.1f}°C, Avg Rain Prob: {avg_rain:.0f}%"
        )

        # Alerts
        alert = None
        if avg_rain and avg_rain > 70:
            alert = "⚠️ High chance of rain during trip"
        if avg_max and avg_max > 38:
            alert = "⚠️ Very hot weather expected"
        if avg_min and avg_min < 5:
            alert = "⚠️ Cold conditions expected"

        return summary, alert
    except Exception:
        return None, None


# -----------------------------
# Agents
# -----------------------------
class DestinationPlanner:
    SYSTEM = "You are a precise travel planner."

    @staticmethod
    def build_prompt(origin: str, days: int, start_date: str, end_date: str,
                     international: bool, family_option: str, genre: str) -> str:
        return f"""
Origin: {origin}
Trip length: {days} days
Dates: {start_date} to {end_date}
International allowed: {international}
Family/Group type: {family_option}
Genre of trip: {genre}

Task: Suggest 4 destinations (city, country) with ideal days and rationale.
Respond JSON list: [{{"name":"City, Country","country":"Country","region":"Region(optional)","days_suggested":int,"rationale":"..."}}].
"""

    def run(self, llm: LLMClient, origin: str, days: int, start_date: str,
            end_date: str, international: bool, family_option: str, genre: str) -> List[Recommendation]:
        raw = llm.chat(self.SYSTEM,
                       self.build_prompt(origin, days, start_date, end_date, international, family_option, genre))
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
            lat, lon, _ = (None, None, None)
            geo = geocode_place(name)
            if geo:
                lat, lon, _ = geo
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
        text = text.strip()
        start = text.find("[")
        if start == -1:
            start = text.find("{")
        end = text.rfind("]")
        if end == -1:
            end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            return text[start:end + 1]
        return "[]"


class WeatherAgent:
    @staticmethod
    def run(rec: Recommendation, start_date: str, end_date: str) -> Recommendation:
        if rec.lat is None or rec.lon is None:
            geo = geocode_place(rec.name)
            if geo:
                rec.lat, rec.lon, _ = geo
        if rec.lat is not None and rec.lon is not None:
            summary, alert = fetch_weather_summary(rec.lat, rec.lon, start_date, end_date)
            rec.start_date_weather = start_date
            rec.weather_brief = summary or "Weather unavailable"
            rec.weather_alert = alert
        else:
            rec.weather_brief = "Could not geocode"
        return rec


# -----------------------------
# Orchestrator
# -----------------------------
class TravelOrchestrator:
    def __init__(self):
        self.llm = LLMClient()
        self.dest_planner = DestinationPlanner()

    def plan(self, trip: TripInput) -> Dict[str, Any]:
        recs = self.dest_planner.run(
            self.llm, trip.origin, trip.days, trip.start_date, trip.end_date,
            trip.international, trip.family_option, trip.genre
        )
        enriched: List[Recommendation] = []
        for rec in recs:
            rec = WeatherAgent.run(rec, trip.start_date, trip.end_date)
            enriched.append(rec)
        enriched.sort(key=lambda x: (x.rating or 0), reverse=True)
        return {"recommendations": [asdict(r) for r in enriched]}


# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Agentic Travel Recommender", page_icon="✈️", layout="wide")
st.title("✈️ Agentic Travel Recommender")
st.caption("LLM + tools: destination planner • weather checker • genre preferences")

with st.sidebar:
    st.header("Trip Inputs")
    origin = st.text_input("From (City, Country)", value="Coimbatore, India")
    destination = st.text_input("Destination (optional)")
    colA, colB = st.columns(2)
    with colA:
        start_date = st.date_input("From date")
    with colB:
        end_date = st.date_input("To date")
    days_inp = st.number_input("No. of days (0 = auto)", min_value=0, max_value=60, value=0)
    international = st.toggle("Allow international destinations", value=True)
    family_option = st.selectbox("Travel type", ["Solo", "With Family", "With Friends", "Couple", "Group"])
    genre = st.selectbox("Genre of trip", ["Adventure", "Spiritual", "Relaxing", "Cultural", "Friends Trip", "Nature"])
    go = st.button("Plan Trip 🚀")

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
        family_option=family_option,
        genre=genre,
    )

    with st.spinner("Planning trip..."):
        orchestrator = TravelOrchestrator()
        result = orchestrator.plan(trip)

    st.subheader("Results")
    recs = result.get("recommendations", [])
    if not recs:
        st.warning("No recommendations found.")
        st.stop()

    df = pd.DataFrame(recs)
    st.dataframe(df[["name", "country", "region", "days_suggested", "weather_brief", "weather_alert", "rationale"]],
                 use_container_width=True)

    st.markdown("---")
    st.markdown("### Detailed Picks")
    for r in recs:
        with st.container(border=True):
            st.markdown(f"#### {r['name']}")
            st.write(f"**Rationale:** {r['rationale']}")
            st.write(f"**Weather:** {r['weather_brief']}")
            if r.get("weather_alert"):
                st.warning(r["weather_alert"])