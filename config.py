# --- DISTRICT 1 CAVITE COORDINATES ---
CITIES = {
    "Cavite City": {"lat": 14.4791, "lon": 120.8976},
    "Kawit": {"lat": 14.4444, "lon": 120.9038},
    "Noveleta": {"lat": 14.4283, "lon": 120.8809},
    "Rosario": {"lat": 14.4150, "lon": 120.8550}
}


def get_weather_info(code):
    # Basic WeatherAPI code mapping
    if code in [1000]: return "Sunny", "☀️"
    if code in [1003, 1006, 1009]: return "Cloudy", "☁️"
    if code in [1063, 1180, 1183]: return "Rainy", "🌧️"
    if code in [1087, 1273]: return "Thunderstorm", "⛈️"
    return "Partly Cloudy", "⛅"

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