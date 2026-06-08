import requests
from PyQt5.QtCore import QThread, pyqtSignal
from config import CITIES

class WeatherWorker(QThread):
    result = pyqtSignal(dict)

    def __init__(self, city):
        super().__init__()
        self.city = city

    def run(self):
        coords = CITIES[self.city]
        url = f"https://api.open-meteo.com/v1/forecast?latitude={coords['lat']}&longitude={coords['lon']}&current=temperature_2m,apparent_temperature,weather_code&daily=weather_code,temperature_2m_max&timezone=Asia%2FManila"
        try:
            res = requests.get(url, timeout=5)
            self.result.emit(res.json())
        except Exception:
            self.result.emit({})