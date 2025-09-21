"""
Smart Crop Advisory System for Small and Marginal Farmers
Streamlit single-file app: app.py

How to run:
 1) Save this file as app.py
 2) (Recommended) Create a virtual env
 3) pip install -r requirements.txt
 4) streamlit run app.py

Minimal requirements (requirements.txt):
  streamlit>=1.36
  requests>=2.31
  pandas>=2.2
  python-dateutil>=2.9
  pydantic>=2.7
  openai>=1.40.0   # optional (LLM-based detailed advice)

This app is a prototype demonstrating core features:
 - multilingual UI (English, हिंदी, தமிழ்)
 - location-based weather alerts and basic forecasts
 - soil health & fertilizer suggestions (heuristic rules)
 - crop selection guidance
 - simple market price mock (placeholder to integrate real APIs)
 - feedback collection saved locally (feedback.json)

Note: Replace any mocked APIs with real data sources for production.
"""

from __future__ import annotations
import os
import json
from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any, Tuple, List
from datetime import date

import requests
import pandas as pd
from dateutil import parser as dateparser
import streamlit as st

# -----------------------------
# Config
# -----------------------------
st.set_page_config(page_title="Smart Crop Advisory", page_icon="🌾", layout="wide")

HEADERS = {"User-Agent": "SmartCropAdvisory/1.0 (contact: demo@example.com)"}

FEEDBACK_FILE = os.getenv("SC_ADVISORY_FEEDBACK", "feedback.json")

# Optional: OpenAI LLM client (if configured)
try:
    from openai import AzureOpenAI
except Exception:
    AzureOpenAI = None

FALLBACK_AZURE_CONFIG = dict(
    api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-12-01-preview"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT", "https://learningllmmodel.cognitiveservices.azure.com/"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY", "DagkDMkW44hoRl0tn3GvcI0R9HYZze9gJDWSDOAxux13aod5S8RwJQQJ99BIAC77bzfXJ3w3AAAAACOGPc0o"),
)
MODEL_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-5-mini")


# -----------------------------
# Data classes
# -----------------------------
@dataclass
class Advisory:
    location_name: str
    lat: Optional[float]
    lon: Optional[float]
    crop: str
    soil_ph: Optional[float]
    soil_n: Optional[float]
    soil_p: Optional[float]
    soil_k: Optional[float]
    recommended_fertilizer: str
    weather_summary: Optional[str]
    weather_alert: Optional[str]
    market_price: Optional[float]
    tips: str


# -----------------------------
# Utilities: geocode, weather, market price
# -----------------------------

def geocode_place(place: str) -> Optional[Tuple[float, float, Dict[str, Any]]]:
    """Use OpenStreetMap Nominatim to geocode a place name. Returns (lat, lon, raw).
    Note: Use responsibly (rate limits)."""
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
    """Fetch simple daily summary with open-meteo public API. Returns (summary, alert).
    Alerts are heuristic: heavy rain probability, extreme temps."""
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
            f"{len(daily.get('time', []))} days | Avg Max: {avg_max:.1f}°C, "
            f"Avg Min: {avg_min:.1f}°C, Avg Rain Prob: {avg_rain:.0f}%"
        )

        alert = None
        if avg_rain and avg_rain > 70:
            alert = "⚠️ High chance of rain during period"
        if avg_max and avg_max > 40:
            alert = "⚠️ Very hot weather expected"
        if avg_min and avg_min < 5:
            alert = "⚠️ Cold conditions expected"

        return summary, alert
    except Exception:
        return None, None


def fetch_market_price_mock(crop_name: str, location: Optional[str]) -> Optional[float]:
    """Placeholder for market price. Replace with real API (e.g., Agmarknet) integration.
    This mock returns prices based on simple heuristics.
    """
    base_prices = {
        "rice": 25.0,
        "wheat": 22.0,
        "maize": 18.0,
        "cotton": 60.0,
        "sugarcane": 3.0,
        "tomato": 15.0,
        "potato": 10.0,
        "onion": 20.0,
        "groundnut": 50.0,
        "millet": 20.0,
    }
    k = crop_name.strip().lower()
    price = base_prices.get(k, None)
    if price is None:
        # estimate using length of name (deterministic mock)
        price = float(10 + (len(k) % 30))
    # slight location adjustment
    if location and "north" in (location.lower()):
        price *= 0.95
    return round(price, 2)


# -----------------------------
# Soil advisory heuristics
# -----------------------------

def fertilizer_recommendation(ph: Optional[float], n: Optional[float], p: Optional[float], k: Optional[float], crop: str) -> str:
    """Return simple fertilizer/soil-health advice. This is heuristic and for demo only.
    ph: soil pH (5-9 typical), n/p/k in mg/kg or relative units (0-100 scale expected here).
    """
    adv = []
    if ph is not None:
        if ph < 5.5:
            adv.append("Soil is acidic — consider lime application to raise pH gradually.")
        elif ph > 7.8:
            adv.append("Soil is alkaline — consider gypsum and organic matter to lower pH effects.")
        else:
            adv.append("Soil pH is within an acceptable range.")

    # Nitrogen
    if n is not None:
        if n < 20:
            adv.append("Low nitrogen: apply nitrogen-rich fertilizers (e.g., urea or vermicompost) at recommended doses.")
        elif n > 60:
            adv.append("High nitrogen: avoid extra N fertiliser; focus on balanced NPK and green manures.")
        else:
            adv.append("Nitrogen level acceptable.")

    # Phosphorus
    if p is not None:
        if p < 15:
            adv.append("Low phosphorus: apply single super phosphate or rock phosphate as per crop requirement.")
        else:
            adv.append("Phosphorus level acceptable.")

    # Potassium
    if k is not None:
        if k < 50:
            adv.append("Low potassium: use muriate of potash or organic sources (crop residues, compost).")
        else:
            adv.append("Potassium level acceptable.")

    # Crop-specific tip (very simple)
    crop = crop.strip().lower()
    if crop in ("rice", "paddy"):
        adv.append("For paddy, maintain puddled soil; split N application recommended.")
    elif crop in ("maize", "corn"):
        adv.append("For maize, ensure N during vegetative growth and K near flowering.")
    elif crop in ("cotton",):
        adv.append("For cotton, balance N and avoid excess during boll formation.")

    return "\n".join(adv)


# -----------------------------
# Basic multilingual strings (English, Hindi, Tamil)
# For production, integrate proper i18n
# -----------------------------
STRINGS = {
    "en": {
        "title": "Smart Crop Advisory",
        "desc": "Location-specific crop recommendations, soil health tips, weather alerts, and market price guidance.",
        "location": "Village / Town / Landmark",
        "crop": "Crop",
        "soil_ph": "Soil pH (optional)",
        "soil_n": "Nitrogen (N) - relative (0-100)",
        "soil_p": "Phosphorus (P) - relative (0-100)",
        "soil_k": "Potassium (K) - relative (0-100)",
        "start_date": "From date",
        "end_date": "To date",
        "plan": "Get Advisory",
        "feedback_prompt": "Any feedback to help us improve?",
        "submit_feedback": "Submit Feedback",
    },
    "hi": {
        "title": "स्मार्ट फसल सलाह",
        "desc": "स्थान-विशिष्ट फसल सुझाव, मिट्टी स्वास्थ्य, मौसम चेतावनी और बाजार मूल्य मार्गदर्शन।",
        "location": "गाँव / शहर / लैंडमार्क",
        "crop": "फसल",
        "soil_ph": "मिट्टी का pH (वैकल्पिक)",
        "soil_n": "नाइट्रोजन (N) - सापेक्ष (0-100)",
        "soil_p": "फॉस्फोरस (P) - सापेक्ष (0-100)",
        "soil_k": "पोटैशियम (K) - सापेक्ष (0-100)",
        "start_date": "शुरू तारीख",
        "end_date": "समाप्ति तारीख",
        "plan": "सलाह लें",
        "feedback_prompt": "बेहतर बनाने के लिए कोई सुझाव?",
        "submit_feedback": "प्रतिक्रिया भेजें",
    },
    "ta": {
        "title": "ஸ்மார்ட் பயிர் ஆலோசனை",
        "desc": "இடத்துக்கு சிறப்பான பயிர் பரிந்துரை, மண்ணின் ஆரோக்கியம், வானிலை எச்சரிக்கை மற்றும் சந்தை விலை வழிகாட்டுதல்.",
        "location": "ஊர் / நகரம் / சிலுவை",
        "crop": "பயிர்",
        "soil_ph": "மண்ணின் pH (விருப்பம்)",
        "soil_n": "நைட்ரஜன் (N) - தொடர்புடைய (0-100)",
        "soil_p": "பாஸ்பரஸ் (P) - தொடர்புடைய (0-100)",
        "soil_k": "பொட்டாசியம் (K) - தொடர்புடைய (0-100)",
        "start_date": "தொடக்கம் தேதி",
        "end_date": "முடிவு தேதி",
        "plan": "ஆலோசனை பெறு",
        "feedback_prompt": "மேம்படுத்த எந்த கருத்தும்?",
        "submit_feedback": "பின்னூட்டம் அனுப்பு",
    },
}


# -----------------------------
# LLM Client wrapper (optional)
# -----------------------------
class LLMClient:
    def __init__(self):
        if AzureOpenAI is None:
            self.client = None
            return
        if not FALLBACK_AZURE_CONFIG.get("api_key"):
            self.client = None
            return
        self.client = AzureOpenAI(**FALLBACK_AZURE_CONFIG)
        self.model = MODEL_DEPLOYMENT

    def available(self) -> bool:
        return self.client is not None

    def chat(self, system: str, user: str, temperature: float = 0.4, max_tokens: int = 400) -> str:
        if not self.available():
            return ""
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return resp.choices[0].message.content


# -----------------------------
# Feedback storage
# -----------------------------

def save_feedback(payload: Dict[str, Any]):
    try:
        existing = []
        if os.path.exists(FEEDBACK_FILE):
            with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
                existing = json.load(f)
        existing.append(payload)
        with open(FEEDBACK_FILE, "w", encoding="utf-8") as f:
            json.dump(existing, f, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False


# -----------------------------
# Streamlit UI
# -----------------------------

st.markdown("# 🌾 Smart Crop Advisory System")
cols = st.columns([1, 2])
with cols[0]:
    lang = st.selectbox("Language / भाषा / மொழி", ["en", "hi", "ta"], index=0)
strings = STRINGS.get(lang, STRINGS["en"])

st.markdown(f"## {strings['title']}")
st.caption(strings['desc'])

with st.sidebar:
    st.header(strings['title'])
    st.write(strings['desc'])
    # quick links / contact
    st.markdown("---")
    st.write("Contact: local-agri-office@example.com")

# Main input form
with st.form("advisory_form"):
    st.subheader("Provide farm and crop details")
    location_inp = st.text_input(strings['location'], value="Coimbatore, India")
    crop = st.text_input(strings['crop'], value="Rice")

    col1, col2, col3 = st.columns(3)
    with col1:
        soil_ph = st.number_input(strings['soil_ph'], min_value=3.0, max_value=10.0, format="%.2f", value=6.5)
    with col2:
        soil_n = st.number_input(strings['soil_n'], min_value=0.0, max_value=200.0, format="%.1f", value=30.0)
    with col3:
        soil_p = st.number_input(strings['soil_p'], min_value=0.0, max_value=200.0, format="%.1f", value=20.0)
    soil_k = st.number_input(strings['soil_k'], min_value=0.0, max_value=200.0, format="%.1f", value=60.0)

    col4, col5 = st.columns(2)
    with col4:
        start_date = st.date_input(strings['start_date'], value=date.today())
    with col5:
        end_date = st.date_input(strings['end_date'], value=date.today())

    submit = st.form_submit_button(strings['plan'])


if submit:
    if not location_inp.strip():
        st.error("Please enter a location.")
        st.stop()
    if start_date > end_date:
        st.error("Start date must be on or before end date.")
        st.stop()

    sd = start_date.isoformat()
    ed = end_date.isoformat()

    # Geocode
    with st.spinner("Geocoding location..."):
        geo = geocode_place(location_inp)
    if geo:
        lat, lon, raw = geo
        st.success(f"Located: {raw.get('display_name', '')} (lat={lat:.3f}, lon={lon:.3f})")
    else:
        lat = None
        lon = None
        st.warning("Could not geocode location — weather and local price may be unavailable.")

    # Weather
    weather_summary, weather_alert = None, None
    if lat is not None and lon is not None:
        with st.spinner("Fetching weather summary..."):
            weather_summary, weather_alert = fetch_weather_summary(lat, lon, sd, ed)

    # Market price (mock)
    with st.spinner("Fetching market price (mock)..."):
        market_price = fetch_market_price_mock(crop, location_inp)

    # Soil advisory
    rec_fert = fertilizer_recommendation(soil_ph, soil_n, soil_p, soil_k, crop)

    # Compose tips (LLM-enhanced if available)
    llm = LLMClient()
    tips = ""
    if llm.available():
        try:
            system = "You are an expert agronomist. Provide short, practical tips for smallholder farmers in simple language."
            user_prompt = (
                f"Location: {location_inp}\nCrop: {crop}\nSoil pH: {soil_ph}\nN: {soil_n}\nP: {soil_p}\nK: {soil_k}\n"
                f"Dates: {sd} to {ed}\nWeather summary: {weather_summary}\nProvide 5 short tips and a fertilizer recommendation."
            )
            llm_resp = llm.chat(system, user_prompt, temperature=0.3, max_tokens=300)
            tips = llm_resp.strip()
        except Exception:
            tips = ""  # fallback to heuristics
    if not tips:
        tips = rec_fert + "\n\nGeneral tips: \n- Use certified seeds and follow recommended sowing density.\n- Monitor pests; use integrated pest management.\n- Maintain records for future decisions."

    advisory = Advisory(
        location_name=location_inp,
        lat=lat,
        lon=lon,
        crop=crop,
        soil_ph=float(soil_ph) if soil_ph is not None else None,
        soil_n=float(soil_n) if soil_n is not None else None,
        soil_p=float(soil_p) if soil_p is not None else None,
        soil_k=float(soil_k) if soil_k is not None else None,
        recommended_fertilizer=rec_fert,
        weather_summary=weather_summary,
        weather_alert=weather_alert,
        market_price=market_price,
        tips=tips,
    )

    # Show results
    st.markdown("---")
    st.header("Advisory Result")
    col_a, col_b = st.columns([2, 1])
    with col_a:
        st.subheader(f"Crop: {advisory.crop}")
        st.write(f"**Location:** {advisory.location_name}")
        if advisory.lat and advisory.lon:
            st.write(f"**Coordinates:** {advisory.lat:.3f}, {advisory.lon:.3f}")
        st.write(f"**Soil pH:** {advisory.soil_ph}")
        st.write(f"**N-P-K:** {advisory.soil_n} - {advisory.soil_p} - {advisory.soil_k}")
        st.markdown("**Recommended actions / Fertilizer guidance:**")
        st.write(advisory.recommended_fertilizer)
        st.markdown("**Tips:**")
        st.write(advisory.tips)

    with col_b:
        st.subheader("Weather & Market")
        st.write(f"**Weather summary:** {advisory.weather_summary}")
        if advisory.weather_alert:
            st.warning(advisory.weather_alert)
        st.write(f"**Estimated market price (₹/kg):** {advisory.market_price}")

    # Save advisory snapshot for farmer (option)
    if st.button("Save advisory to JSON"):
        out = asdict(advisory)
        fname = f"advisory_{crop}_{date.today().isoformat()}.json"
        with open(fname, "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=2)
        st.success(f"Saved advisory: {fname}")

    st.markdown("---")

    # Feedback
    st.subheader(strings['feedback_prompt'])
    feedback_text = st.text_area(strings['feedback_prompt'], value="")
    if st.button(strings['submit_feedback']):
        payload = {
            "timestamp": pd.Timestamp.now().isoformat(),
            "location": location_inp,
            "crop": crop,
            "feedback": feedback_text,
        }
        ok = save_feedback(payload)
        if ok:
            st.success("Thank you — feedback saved.")
        else:
            st.error("Could not save feedback. Please try again or contact support.")

# Admin / Developer section (local only)
st.sidebar.markdown("---")
if st.sidebar.checkbox("Show saved feedback (dev)"):
    if os.path.exists(FEEDBACK_FILE):
        try:
            with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
                arr = json.load(f)
            st.sidebar.write(f"{len(arr)} feedback entries")
            st.sidebar.dataframe(pd.DataFrame(arr))
        except Exception:
            st.sidebar.warning("Could not read feedback file.")
    else:
        st.sidebar.info("No feedback yet.")


# End of app

