import streamlit as st
from datetime import datetime
from config import get_weather_info, get_heat_index_status, get_weather_advice


def apply_custom_css():
    """Injects custom CSS to make Streamlit look sleeker."""
    st.markdown("""
        <style>
        div[data-testid="stMetricValue"] { font-size: 4rem !important; font-weight: 800; }
        .heat-box {
            background-color: rgba(255, 215, 0, 0.1); border-left: 5px solid #FFD700;
            padding: 15px; border-radius: 5px; margin-bottom: 20px;
        }
        .advice-text { font-style: italic; color: #555; text-align: center; margin-bottom: 30px; }
        .forecast-row {
            display: flex; justify-content: space-between; padding: 10px;
            border-bottom: 1px solid rgba(128,128,128,0.2);
        }
        </style>
    """, unsafe_allow_html=True)


@st.dialog("PAGASA Heat Index Guide")
def show_heat_index_guide():
    """Streamlit's native modal popup for the Heat Index Guide."""
    st.markdown("""
    **Perceived Danger Levels:**
    * 🟢 **Safe:** Below 27°C
    * 🟡 **Caution:** 27°C - 32°C
    * 🟠 **Extreme Caution:** 33°C - 41°C
    * 🔴 **Danger:** 42°C - 51°C
    * 🟤 **Extreme Danger:** 52°C and above
    """)


def render_dashboard(data):
    """Renders the entire weather UI based on provided data."""
    current = data.get("current", {})
    daily = data.get("daily", {})

    temp = round(current.get("temperature_2m", 0))
    feels_like = round(current.get("apparent_temperature", 0))
    code = current.get("weather_code", 0)

    desc, icon = get_weather_info(code)
    status = get_heat_index_status(feels_like)
    advice = get_weather_advice(desc, status)

    # 1. Main Weather Section
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.metric(label=f"{icon} {desc}", value=f"{temp}°C")

    # 2. Heat Index & Advice
    st.markdown(f"""
        <div class='heat-box'>
            <h4 style='margin:0; color: #b8860b;'>Heat Index: {feels_like}°C ({status})</h4>
        </div>
    """, unsafe_allow_html=True)

    if st.button("ℹ️ What does this Heat Index mean?"):
        show_heat_index_guide()

    st.markdown(f"<div class='advice-text'>{advice}</div>", unsafe_allow_html=True)

    # 3. 7-Day Forecast
    st.subheader("7-Day Forecast")
    days = daily.get("time", [])
    codes = daily.get("weather_code", [])
    max_temps = daily.get("temperature_2m_max", [])

    for i in range(min(7, len(days))):
        date_obj = datetime.strptime(days[i], "%Y-%m-%d")
        day_name = date_obj.strftime("%A")
        d_desc, d_icon = get_weather_info(codes[i])
        d_temp = round(max_temps[i])

        # HTML injection for clean, responsive rows
        st.markdown(f"""
            <div class='forecast-row'>
                <strong>{day_name}</strong>
                <span>{d_icon} {d_desc}</span>
                <strong>{d_temp}°C</strong>
            </div>
        """, unsafe_allow_html=True)