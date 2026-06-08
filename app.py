import streamlit as st
import requests
from config import CITIES
import ui

# 1. Page Configuration
st.set_page_config(page_title="District 1 Weather", page_icon="⛅", layout="centered")
ui.apply_custom_css()

st.title("📍 District 1 Cavite Weather")

# 2. City Selection
selected_city = st.selectbox("Select Municipality", list(CITIES.keys()))


# 3. Data Fetching (Cached for 15 minutes to prevent API limits)
@st.cache_data(ttl=900)
def fetch_weather(city_name):
    coords = CITIES[city_name]
    url = f"https://api.open-meteo.com/v1/forecast?latitude={coords['lat']}&longitude={coords['lon']}&current=temperature_2m,apparent_temperature,weather_code&daily=weather_code,temperature_2m_max&timezone=Asia%2FManila"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return None


# 4. Main Execution
if selected_city:
    with st.spinner("Fetching live radar data..."):
        weather_data = fetch_weather(selected_city)

    if weather_data:
        ui.render_dashboard(weather_data)
    else:
        st.error("⚠️ Network Error: Unable to fetch live weather data. Please try again later.")