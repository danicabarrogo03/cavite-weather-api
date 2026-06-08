from flask import Flask, jsonify, render_template
import requests
from datetime import datetime

app = Flask(__name__)

# --- DISTRICT 1 CAVITE COORDINATES ---
CITIES = {
    "Cavite City": {"lat": 14.4791, "lon": 120.8976},
    "Kawit": {"lat": 14.4444, "lon": 120.9038},
    "Noveleta": {"lat": 14.4283, "lon": 120.8809},
    "Rosario": {"lat": 14.4150, "lon": 120.8550}
}


def get_weather_info(code):
    if code == 0: return "Sunny", "☀️"
    if code in [1, 2, 3]: return "Partly Cloudy", "⛅"
    if code in [45, 48]: return "Foggy", "🌫️"
    if code in [51, 53, 55, 56, 57]: return "Drizzle", "🌦️"
    if code in [61, 63, 65, 66, 67]: return "Rainy", "🌧️"
    if code in [80, 81, 82]: return "Showers", "☔"
    if code in [95, 96, 99]: return "Thunderstorm", "⛈️"
    return "Cloudy", "☁️"


def get_heat_index_status(temp):
    if temp < 27: return "Safe"
    if 27 <= temp <= 32: return "Caution"
    if 33 <= temp <= 41: return "Extreme Caution"
    if 42 <= temp <= 51: return "Danger"
    return "Extreme Danger"


def get_weather_advice(condition, heat_index_status):
    advice = []
    if condition in ["Rainy", "Drizzle", "Showers", "Thunderstorm"]:
        advice.append("🌧️ It's wet outside! Don't forget your umbrella.")
    elif condition == "Sunny":
        advice.append("☀️ Great weather! Apply sunscreen if heading out.")
    if heat_index_status in ["Caution", "Extreme Caution", "Danger", "Extreme Danger"]:
        advice.append("💧 Hydrate! The heat index is reaching dangerous levels.")
    if not advice:
        advice.append("☁️ Normal conditions today. Have a great day!")
    return " ".join(advice)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/weather/<city>')
def weather(city):
    if city not in CITIES:
        return jsonify({"error": "City not found"}), 404

    coords = CITIES[city]
    url = f"https://api.open-meteo.com/v1/forecast?latitude={coords['lat']}&longitude={coords['lon']}&current=temperature_2m,apparent_temperature,weather_code&daily=weather_code,temperature_2m_max&timezone=Asia%2FManila"

    try:
        res = requests.get(url, timeout=5).json()
        current = res.get("current", {})
        daily = res.get("daily", {})

        temp = round(current.get("temperature_2m", 0))
        feels_like = round(current.get("apparent_temperature", 0))
        code = current.get("weather_code", 0)

        desc, icon = get_weather_info(code)
        status = get_heat_index_status(feels_like)
        advice = get_weather_advice(desc, status)

        forecast = []
        days = daily.get("time", [])
        codes = daily.get("weather_code", [])
        max_temps = daily.get("temperature_2m_max", [])

        for i in range(min(7, len(days))):
            date_obj = datetime.strptime(days[i], "%Y-%m-%d")
            day_name = date_obj.strftime("%a")
            d_desc, d_icon = get_weather_info(codes[i])
            forecast.append({
                "day": day_name,
                "icon": d_icon,
                "desc": d_desc,
                "temp": round(max_temps[i])
            })

        return jsonify({
            "temp": temp,
            "condition": desc,
            "icon": icon,
            "heat_index": feels_like,
            "heat_status": status,
            "advice": advice,
            "forecast": forecast
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    # Swapped to port 5001 to bypass Windows socket restrictions
    app.run(debug=True, host='0.0.0.0', port=5001)