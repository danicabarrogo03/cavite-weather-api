import requests
from PyQt6.QtCore import QThread, pyqtSignal


class WeatherWorker(QThread):
    result = pyqtSignal(dict)

    def __init__(self, city):
        super().__init__()
        self.city = city

    def run(self):
        API_KEY = "db2bbb06ef9c44a0a65223312260806"

        # We target the city inside Cavite explicitly for extreme accuracy
        url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={self.city},Cavite&days=7&aqi=no"

        try:
            res = requests.get(url, timeout=5)
            res.raise_for_status()
            data = res.json()

            mapped_data = {
                "current": {
                    "temperature_2m": data["current"]["temp_c"],
                    "apparent_temperature": data["current"]["feelslike_c"],
                    "weather_code": data["current"]["condition"]["code"],
                    "text": data["current"]["condition"]["text"],
                    "relative_humidity_2m": data["current"]["humidity"],
                    "wind_speed_10m": data["current"]["wind_kph"],
                    "uv": data["current"]["uv"],
                    "surface_pressure": data["current"]["pressure_mb"]
                },
                "daily": {
                    # Loop through the 7-day forecast array
                    "time": [day["date"] for day in data["forecast"]["forecastday"]],
                    "weather_code": [day["day"]["condition"]["code"] for day in data["forecast"]["forecastday"]],
                    "temperature_2m_max": [day["day"]["maxtemp_c"] for day in data["forecast"]["forecastday"]]
                }
            }
            self.result.emit(mapped_data)

        except Exception as e:
            print(f"WeatherAPI Worker Error: {e}")
            self.result.emit({})