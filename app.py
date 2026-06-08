import streamlit as st
import requests
from config import CITIES
import ui

st.set_page_config(page_title="District 1 Weather", page_icon="⛅", layout="centered")

# --- ALWAYS INJECT CSS FIRST ---
# This ensures the app looks sleek even if the API fails below
ui.apply_dynamic_css("Cloudy")

selected_city = st.selectbox("Select Municipality", list(CITIES.keys()))


def get_fallback_data():
    """Provides mock data if the API rate limit is exceeded."""
    return {
        "current": {"temperature_2m": 31, "apparent_temperature": 36, "weather_code": 3},
        "daily": {
            "time": ["2026-06-09", "2026-06-10", "2026-06-11", "2026-06-12", "2026-06-13", "2026-06-14", "2026-06-15"],
            "weather_code": [3, 61, 80, 0, 1, 3, 61],
            "temperature_2m_max": [32, 30, 29, 34, 33, 31, 30]
        }
    }


@st.cache_data(ttl=900)
def fetch_weather(city_name):
    coords = CITIES[city_name]
    url = f"https://api.open-meteo.com/v1/forecast?latitude={coords['lat']}&longitude={coords['lon']}&current=temperature_2m,apparent_temperature,weather_code&daily=weather_code,temperature_2m_max&timezone=Asia%2FManila"
    headers = {"User-Agent": "Mozilla/5.0 (Cavite Weather Widget/1.0)"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as err:
        if response.status_code == 429:
            st.warning("⚠️ API Rate Limit Exceeded. Displaying offline fallback data.")
            return get_fallback_data()
        st.error(f"API Error: {err}")
        return None
    except requests.exceptions.RequestException:
        st.warning("⚠️ Network connection failed. Displaying offline fallback data.")
        return get_fallback_data()


if selected_city:
    with st.spinner("Fetching live radar data..."):
        weather_data = fetch_weather(selected_city)

    if weather_data:
        ui.render_dashboard(weather_data)