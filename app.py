import streamlit as st
import requests
from config import CITIES
import ui

st.set_page_config(page_title="District 1 Weather", page_icon="⛅", layout="centered")

# --- ADD YOUR API KEY HERE ---
API_KEY = "db2bbb06ef9c44a0a65223312260806"

ui.apply_dynamic_css("Cloudy")

selected_city = st.selectbox("Select Municipality", list(CITIES.keys()))


@st.cache_data(ttl=900)
def fetch_weather(city_name):
    # WeatherAPI structure
    url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city_name}&days=7"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Transform WeatherAPI data into the format our ui.py expects
        return {
            "current": {
                "temperature_2m": data['current']['temp_c'],
                "apparent_temperature": data['current']['feelslike_c'],
                "weather_code": data['current']['condition']['code'],
                "text": data['current']['condition']['text']
            },
            "daily": {
                "time": [f["date"] for f in data['forecast']['forecastday']],
                "weather_code": [f["day"]["condition"]["code"] for f in data['forecast']['forecastday']],
                "temperature_2m_max": [f["day"]["maxtemp_c"] for f in data['forecast']['forecastday']]
            }
        }
    except Exception as e:
        st.error(f"API Error: {e}")
        return None


if selected_city:
    with st.spinner("Fetching data from WeatherAPI..."):
        weather_data = fetch_weather(selected_city)

    if weather_data:
        ui.render_dashboard(weather_data)