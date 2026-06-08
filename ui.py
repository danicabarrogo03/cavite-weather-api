import streamlit as st
from datetime import datetime
from config import get_weather_info, get_heat_index_status, get_weather_advice


def apply_dynamic_css(condition_desc, feels_like):
    """Injects Glassmorphism CSS with dynamic background based on weather and heat."""

    # 1. Base Gradient based on Weather
    if "Sunny" in condition_desc or "Clear" in condition_desc:
        base_grad = "#ff8c00, #ffc832"
    elif "Rain" in condition_desc or "Drizzle" in condition_desc:
        base_grad = "#14325a, #3c6ea0"
    else:
        base_grad = "#5a646e, #a0aab4"

    # 2. Temperature Tint
    tint = "rgba(255, 0, 0, 0.3)" if feels_like > 35 else "rgba(0,0,0,0)"

    st.markdown(f"""
        <style>
        /* Force background on the main app wrapper */
        .stApp {{
            background: linear-gradient(135deg, {base_grad});
            background-blend-mode: overlay;
            background-color: {tint};
            background-attachment: fixed !important;
        }}

        /* Glassmorphism Main Container */
        [data-testid="stMainBlockContainer"] {{
            background: rgba(255, 255, 255, 0.15) !important;
            backdrop-filter: blur(20px) !important;
            -webkit-backdrop-filter: blur(20px) !important;
            border: 1px solid rgba(255, 255, 255, 0.3) !important;
            border-radius: 24px !important;
            padding: 40px !important;
            max-width: 450px !important;
            margin-top: 40px !important;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3) !important;
        }}

        /* Typography overrides */
        h1, h2, h3, h4, p, span, div, label {{ color: white !important; font-family: 'Segoe UI', sans-serif; }}

        /* Metric Styling */
        [data-testid="stMetricValue"] {{ font-size: 4.5rem !important; font-weight: 800 !important; text-align: center; }}
        [data-testid="stMetricLabel"] {{ font-size: 1.5rem !important; text-align: center; }}
        [data-testid="stMetric"] {{ display: flex; flex-direction: column; align-items: center; justify-content: center; }}

        /* Heat Box */
        .heat-box {{
            background-color: rgba(0, 0, 0, 0.3); border: 1px solid rgba(255, 215, 0, 0.4);
            padding: 12px; border-radius: 12px; margin-bottom: 20px; text-align: center;
        }}

        .advice-text {{ font-style: italic; text-align: center; margin-bottom: 30px; font-size: 14px; opacity: 0.9; }}

        /* Forecast Rows */
        .forecast-row {{
            display: flex; justify-content: space-between; padding: 12px 15px;
            border-radius: 10px; background: rgba(255, 255, 255, 0.1); margin-bottom: 8px;
        }}
        </style>
    """, unsafe_allow_html=True)


def render_dashboard(data):
    current = data.get("current", {})
    daily = data.get("daily", {})

    temp = round(current.get("temperature_2m", 0))
    feels_like = round(current.get("apparent_temperature", 0))
    code = current.get("weather_code", 0)

    desc, icon = get_weather_info(code)
    status = get_heat_index_status(feels_like)
    advice = get_weather_advice(desc, status)

    apply_dynamic_css(desc, feels_like)

    # 1. Main Weather Section
    st.metric(label=f"{icon} {desc}", value=f"{temp}°C")

    # 2. Heat Index
    st.markdown(f"""
        <div class='heat-box'>
            <h4 style='margin:0; color: #FFD700 !important; font-size: 16px;'>Heat Index: {feels_like}°C ({status})</h4>
        </div>
    """, unsafe_allow_html=True)

    with st.popover("ℹ️ Heat Index Guide", use_container_width=True):
        st.markdown("""
        **Perceived Danger Levels:**
        * 🟢 **Safe:** Below 27°C
        * 🟡 **Caution:** 27°C - 32°C
        * 🟠 **Extreme Caution:** 33°C - 41°C
        * 🔴 **Danger:** 42°C - 51°C
        * 🟤 **Extreme Danger:** 52°C and above
        """)

    st.markdown(f"<div class='advice-text'>{advice}</div>", unsafe_allow_html=True)

    # 3. 7-Day Forecast
    st.markdown(
        "<h4 style='text-transform: uppercase; font-size: 15px; letter-spacing: 1px; margin-top: 15px;'>7-Day Forecast</h4>",
        unsafe_allow_html=True)

    days = daily.get("time", [])
    codes = daily.get("weather_code", [])
    max_temps = daily.get("temperature_2m_max", [])

    for i in range(min(7, len(days))):
        try:
            date_obj = datetime.strptime(days[i], "%Y-%m-%d")
            day_name = date_obj.strftime("%A")
        except:
            day_name = "Day"

        d_desc, d_icon = get_weather_info(codes[i])
        d_temp = round(max_temps[i])

        st.markdown(f"""
            <div class='forecast-row'>
                <strong style='width: 90px;'>{day_name}</strong>
                <span style='flex: 1; text-align: center;'>{d_icon} {d_desc}</span>
                <strong>{d_temp}°C</strong>
            </div>
        """, unsafe_allow_html=True)