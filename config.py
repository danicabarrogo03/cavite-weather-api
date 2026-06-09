from PyQt6.QtGui import QColor

CITIES = {
    "Cavite City": {"lat": 14.4833, "lon": 120.9000},
    "Kawit": {"lat": 14.4455, "lon": 120.9045},
    "Noveleta": {"lat": 14.4290, "lon": 120.8785},
    "Rosario": {"lat": 14.4135, "lon": 120.8595}
}

COLORS = {
    "Sunny": (QColor(255, 140, 0, 220), QColor(255, 200, 50, 220)),
    "Cloudy": (QColor(90, 100, 110, 220), QColor(160, 170, 180, 220)),
    "Rainy": (QColor(20, 50, 90, 220), QColor(60, 110, 160, 220))
}

def get_weather_info(code):
    if code == 1000: return "Sunny", "☀️"
    if code in [1003, 1006, 1009]: return "Partly Cloudy", "⛅"
    if code in [1030, 1135, 1147]: return "Foggy", "🌫️"
    if code in [1063, 1150, 1153, 1180, 1183]: return "Drizzle", "🌦️"
    if code in [1186, 1189, 1192, 1195, 1240, 1243]: return "Rainy", "🌧️"
    if code in [1246, 1249, 1252]: return "Showers", "☔"
    if code in [1087, 1273, 1276, 1279, 1282]: return "Thunderstorm", "⛈️"
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

def get_humidity_status(humidity):
    if humidity < 30: return "Dry"
    if humidity <= 60: return "Comfortable"
    return "Muggy"

def get_wind_status(wind_speed):
    if wind_speed < 10: return "Calm"
    if wind_speed <= 24: return "Breezy"
    return "Windy"

def get_uv_status(uv):
    if uv <= 2: return "Low"
    if uv <= 5: return "Moderate"
    if uv <= 7: return "High"
    if uv <= 10: return "Very High"
    return "Extreme"

def get_pressure_status(pressure):
    if pressure < 1009: return "Low"
    if pressure <= 1020: return "Normal"
    return "High"