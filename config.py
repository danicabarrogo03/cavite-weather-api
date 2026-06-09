from PyQt5.QtGui import QColor

# --- LIVE DATA CONFIGURATION (District 1 Cavite) ---
CITIES = {
    "Cavite City": {"lat": 14.4791, "lon": 120.8976},
    "Kawit": {"lat": 14.4444, "lon": 120.9038},
    "Noveleta": {"lat": 14.4283, "lon": 120.8809},
    "Rosario": {"lat": 14.4150, "lon": 120.8550}
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

def get_humidity_status(humidity):
    if humidity < 30: return "Dry"
    if humidity <= 60: return "Comfortable"
    return "Muggy"

def get_wind_status(wind_speed):
    if wind_speed < 10: return "Calm"
    if wind_speed <= 24: return "Breezy"
    return "Windy"

def get_visibility_status(vis_km):
    if vis_km < 2: return "Poor"
    if vis_km <= 5: return "Moderate"
    return "Good"

def get_pressure_status(pressure):
    if pressure < 1000: return "Low"
    if pressure <= 1020: return "Normal"
    return "High"