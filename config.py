from PyQt5.QtGui import QColor

# --- LIVE DATA CONFIGURATION ---
CITIES = {
    "Tanza": {"lat": 14.3396, "lon": 120.8524},
    "Trece Martires": {"lat": 14.2818, "lon": 120.8679},
    "Amadeo": {"lat": 14.1706, "lon": 120.9250},
    "Indang": {"lat": 14.1952, "lon": 120.8758}
}

COLORS = {
    "Sunny": (QColor(255, 140, 0, 220), QColor(255, 200, 50, 220)),
    "Cloudy": (QColor(90, 100, 110, 220), QColor(160, 170, 180, 220)),
    "Rainy": (QColor(20, 50, 90, 220), QColor(60, 110, 160, 220))
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


def get_bg_category(desc):
    if desc in ["Sunny", "Partly Cloudy"]: return "Sunny"
    if desc in ["Rainy", "Drizzle", "Showers", "Thunderstorm"]: return "Rainy"
    return "Cloudy"


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
        advice.append("☀️ Great weather! Apply sunscreen if you're heading out.")

    if heat_index_status in ["Caution", "Extreme Caution", "Danger", "Extreme Danger"]:
        advice.append("💧 Hydrate! The heat index is reaching dangerous levels.")

    if not advice:
        advice.append("☁️ Normal conditions today. Have a great day!")

    return "\n".join(advice)