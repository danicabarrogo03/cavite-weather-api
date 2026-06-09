import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont
from ui import WeatherWidget

if __name__ == '__main__':
    app = QApplication(sys.argv)

    app_font = QFont("Segoe UI", 10)
    app.setFont(app_font)

    window = WeatherWidget()
    window.show()
    sys.exit(app.exec())