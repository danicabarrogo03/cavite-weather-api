import requests
from PyQt5.QtCore import QThread, pyqtSignal
from config import CITIES

class WeatherWorker(QThread):
    result = pyqtSignal(dict)

    def __init__(self, city):
        super().__init__()
        self.city = city

    def run(self):
        coords = CITIES.get(self.city)
        if not coords:
            self.result.emit({})
            return

        url = f"https://api.open-meteo.com/v1/forecast?latitude={coords['lat']}&longitude={coords['lon']}&current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,surface_pressure,wind_speed_10m,visibility&daily=weather_code,temperature_2m_max&timezone=Asia%2FManila"

        headers = {"User-Agent": "Mozilla/5.0 (Cavite Weather Widget/1.0)"}

        try:
            res = requests.get(url, headers=headers, timeout=5)
            res.raise_for_status()
            self.result.emit(res.json())
        except Exception as e:
            print(f"Network Worker Error: {e}")
            self.result.emit({})