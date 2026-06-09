from datetime import datetime
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QLabel, QComboBox, QFrame, QSpacerItem, QSizePolicy, QDialog, QPushButton)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QLinearGradient
# --- FIX: Import the new status functions ---
from config import (CITIES, COLORS, get_weather_info, get_bg_category, get_heat_index_status,
                    get_weather_advice, get_humidity_status, get_wind_status,
                    get_visibility_status, get_pressure_status)
from worker import WeatherWorker


class HeatIndexDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(360, 440)
        self.setStyleSheet("* { font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif; }")

        self.container = QFrame(self)
        self.container.setFixedSize(360, 440)
        self.container.setStyleSheet("""
            QFrame { background-color: rgba(25, 25, 25, 0.95); border-radius: 18px; border: 1px solid rgba(255, 215, 0, 0.4); }
        """)

        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(12)

        title = QLabel("PAGASA Heat Index")
        title.setStyleSheet("color: #FFD700; font-size: 22px; font-weight: 800; border: none; background: transparent;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        desc = QLabel("Perceived Danger Levels")
        desc.setStyleSheet(
            "color: rgba(255, 255, 255, 0.6); font-size: 13px; font-weight: 500; border: none; background: transparent; margin-bottom: 10px;")
        desc.setAlignment(Qt.AlignCenter)
        layout.addWidget(desc)

        levels = [
            ("Safe", "Below 27°C", "#4CAF50"),
            ("Caution", "27°C - 32°C", "#FFEB3B"),
            ("Extreme Caution", "33°C - 41°C", "#FF9800"),
            ("Danger", "42°C - 51°C", "#F44336"),
            ("Extreme Danger", "52°C +", "#B71C1C")
        ]

        for status, temp, color in levels:
            row = QHBoxLayout()
            row.setContentsMargins(15, 8, 15, 8)

            lbl_status = QLabel(status)
            lbl_status.setStyleSheet(
                f"color: {color}; font-size: 15px; font-weight: bold; border: none; background: transparent;")
            lbl_temp = QLabel(temp)
            lbl_temp.setStyleSheet(
                "color: white; font-size: 15px; font-weight: 500; border: none; background: transparent;")
            lbl_temp.setAlignment(Qt.AlignRight)

            row.addWidget(lbl_status)
            row.addWidget(lbl_temp)

            card = QFrame()
            card.setStyleSheet(
                "QFrame { background-color: rgba(255, 255, 255, 0.05); border-radius: 10px; border: none; } QFrame:hover { background-color: rgba(255, 255, 255, 0.12); }")
            card.setLayout(row)
            layout.addWidget(card)

        layout.addStretch()

        close_btn = QPushButton("Got it")
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.setStyleSheet("""
            QPushButton { background-color: rgba(255, 215, 0, 0.15); color: #FFD700; font-size: 15px; font-weight: bold; padding: 10px; border-radius: 10px; border: 1px solid rgba(255, 215, 0, 0.3); }
            QPushButton:hover { background-color: rgba(255, 215, 0, 0.3); border: 1px solid rgba(255, 215, 0, 0.8); }
        """)
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)


class ClickableFrame(QFrame):
    clicked = pyqtSignal()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)


class WeatherWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.current_condition = "Sunny"
        self.worker = None
        self.initUI()
        self.setup_auto_refresh()

    def create_detail_card(self, title, initial_val, initial_status="--"):
        """Helper function to generate the glassmorphism grid cards WITH context indicator."""
        card = QFrame()
        card.setStyleSheet("""
            QFrame { background-color: rgba(0, 0, 0, 0.2); border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.15); }
        """)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(2)  # Keep items tight together

        lbl_title = QLabel(title)
        lbl_title.setStyleSheet(
            "color: rgba(255, 255, 255, 0.7); font-size: 12px; border: none; background: transparent;")
        lbl_title.setAlignment(Qt.AlignCenter)

        lbl_val = QLabel(initial_val)
        lbl_val.setStyleSheet(
            "color: white; font-size: 16px; font-weight: bold; border: none; background: transparent;")
        lbl_val.setAlignment(Qt.AlignCenter)

        # --- FIX: Add the new Indicator/Status label ---
        lbl_status = QLabel(initial_status)
        lbl_status.setStyleSheet(
            "color: rgba(255, 255, 255, 0.9); font-size: 11px; font-weight: 500; border: none; background: transparent;")
        lbl_status.setAlignment(Qt.AlignCenter)

        layout.addWidget(lbl_title)
        layout.addWidget(lbl_val)
        layout.addWidget(lbl_status)
        return card, lbl_val, lbl_status

    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(450, 840)  # Slightly taller to fit the 3rd row of text
        self.setStyleSheet("* { font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif; }")

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(35, 35, 35, 35)
        main_layout.setSpacing(18)
        city_names = list(CITIES.keys())

        self.city_selector = QComboBox()
        self.city_selector.addItems(city_names)
        self.city_selector.setStyleSheet("""
            QComboBox { background-color: rgba(255, 255, 255, 0.15); color: white; font-size: 18px; font-weight: 500; padding: 10px 15px; border: 1px solid rgba(255, 255, 255, 0.3); border-radius: 10px; }
            QComboBox:hover { background-color: rgba(255, 255, 255, 0.25); border: 1px solid rgba(255, 255, 255, 0.6); }
            QComboBox::drop-down { border: none; }
            QComboBox QAbstractItemView { background-color: #2b2b2b; color: white; border-radius: 5px; }
        """)

        self.city_selector.currentTextChanged.connect(self.fetch_weather)
        main_layout.addWidget(self.city_selector)

        weather_container = QVBoxLayout()
        weather_container.setSpacing(0)

        self.temp_label = QLabel("--°C")
        self.temp_label.setStyleSheet("color: white; font-size: 90px; font-weight: 800; letter-spacing: -2px;")
        self.temp_label.setAlignment(Qt.AlignCenter)
        weather_container.addWidget(self.temp_label)

        self.cond_label = QLabel("Initializing...")
        self.cond_label.setStyleSheet(
            "color: rgba(255, 255, 255, 0.9); font-size: 22px; font-weight: 500; margin-bottom: 15px;")
        self.cond_label.setAlignment(Qt.AlignCenter)
        weather_container.addWidget(self.cond_label)

        main_layout.addLayout(weather_container)

        # --- 2x2 Details Grid Setup ---
        self.details_layout = QGridLayout()
        self.details_layout.setSpacing(10)

        self.card_hum, self.val_hum, self.stat_hum = self.create_detail_card("💦 Humidity", "--%")
        self.card_wind, self.val_wind, self.stat_wind = self.create_detail_card("💨 Wind", "-- km/h")
        self.card_vis, self.val_vis, self.stat_vis = self.create_detail_card("👁️ Visibility", "-- km")
        self.card_pres, self.val_pres, self.stat_pres = self.create_detail_card("🌡️ Pressure", "-- mb")

        self.details_layout.addWidget(self.card_hum, 0, 0)
        self.details_layout.addWidget(self.card_wind, 0, 1)
        self.details_layout.addWidget(self.card_vis, 1, 0)
        self.details_layout.addWidget(self.card_pres, 1, 1)

        main_layout.addLayout(self.details_layout)
        # ------------------------------

        self.heat_index_frame = ClickableFrame()
        self.heat_index_frame.setCursor(Qt.PointingHandCursor)
        self.heat_index_frame.setStyleSheet("""
            QFrame { background-color: rgba(0, 0, 0, 0.25); border-radius: 12px; border: 1px solid rgba(255, 215, 0, 0.3); }
            QFrame:hover { background-color: rgba(0, 0, 0, 0.5); border: 1px solid rgba(255, 215, 0, 0.8); }
        """)
        self.heat_index_frame.clicked.connect(self.show_heat_info_popup)

        heat_layout = QVBoxLayout()
        heat_layout.setContentsMargins(15, 10, 15, 10)
        self.heat_index_label = QLabel("Heat Index: --°C")
        self.heat_index_label.setStyleSheet(
            "color: #FFD700; font-size: 16px; font-weight: bold; background: transparent;")
        self.heat_index_label.setAlignment(Qt.AlignCenter)

        heat_layout.addWidget(self.heat_index_label)
        self.heat_index_frame.setLayout(heat_layout)
        main_layout.addWidget(self.heat_index_frame)

        self.advice_label = QLabel("Fetching local conditions...")
        self.advice_label.setStyleSheet(
            "color: rgba(255, 255, 255, 0.95); font-size: 14px; font-weight: 500; font-style: italic;")
        self.advice_label.setAlignment(Qt.AlignCenter)
        self.advice_label.setWordWrap(True)
        main_layout.addWidget(self.advice_label)

        main_layout.addSpacerItem(QSpacerItem(20, 15, QSizePolicy.Minimum, QSizePolicy.Fixed))

        forecast_title = QLabel("7-Day Forecast")
        forecast_title.setStyleSheet(
            "color: white; font-size: 15px; font-weight: bold; letter-spacing: 1px; text-transform: uppercase;")
        main_layout.addWidget(forecast_title)

        self.forecast_layout = QVBoxLayout()
        self.forecast_layout.setSpacing(10)
        main_layout.addLayout(self.forecast_layout)

        self.setLayout(main_layout)
        self.fetch_weather(city_names[0])

    def show_heat_info_popup(self):
        dialog = HeatIndexDialog(self)
        dialog.exec_()

    def setup_auto_refresh(self):
        self.refresh_timer = QTimer(self)
        self.refresh_timer.setInterval(15 * 60 * 1000)
        self.refresh_timer.timeout.connect(self.auto_update)
        self.refresh_timer.start()

    def auto_update(self):
        current_city = self.city_selector.currentText()
        self.fetch_weather(current_city)

    def fetch_weather(self, city):
        self.cond_label.setText("Fetching Live Data...")

        if self.worker is not None and self.worker.isRunning():
            self.worker.quit()
            self.worker.wait()

        self.worker = WeatherWorker(city)
        self.worker.result.connect(self.update_ui)
        self.worker.start()

    def update_ui(self, data):
        if not data:
            self.cond_label.setText("⚠️ Network Error")
            return

        current = data.get("current", {})
        daily = data.get("daily", {})

        temp = round(current.get("temperature_2m", 0))
        feels_like = round(current.get("apparent_temperature", 0))
        code = current.get("weather_code", 0)

        # --- UPDATE EXTRA DETAILS GRID & INDICATORS ---
        humidity = current.get("relative_humidity_2m", 0)
        wind = current.get("wind_speed_10m", 0)
        vis_m = current.get("visibility", 0)
        pressure = current.get("surface_pressure", 0)

        vis_km = round(vis_m / 1000, 1)

        # Set Numeric Values
        self.val_hum.setText(f"{humidity}%")
        self.val_wind.setText(f"{wind} km/h")
        self.val_vis.setText(f"{vis_km} km")
        self.val_pres.setText(f"{round(pressure)} mb")

        # Set Qualitative Indicators
        self.stat_hum.setText(get_humidity_status(humidity))
        self.stat_wind.setText(get_wind_status(wind))
        self.stat_vis.setText(get_visibility_status(vis_km))
        self.stat_pres.setText(get_pressure_status(pressure))
        # ----------------------------------

        desc, icon = get_weather_info(code)
        self.current_condition = desc

        self.temp_label.setText(f"{temp}°C")
        self.cond_label.setText(f"{icon} {desc}")

        status = get_heat_index_status(feels_like)
        self.heat_index_label.setText(f"Heat Index: {feels_like}°C ({status})")

        advice_text = get_weather_advice(desc, status)
        self.advice_label.setText(advice_text)

        for i in reversed(range(self.forecast_layout.count())):
            widget = self.forecast_layout.itemAt(i).widget()
            if widget: widget.setParent(None)

        days = daily.get("time", [])
        codes = daily.get("weather_code", [])
        max_temps = daily.get("temperature_2m_max", [])

        for i in range(min(7, len(days))):
            date_obj = datetime.strptime(days[i], "%Y-%m-%d")
            day_name = date_obj.strftime("%a")
            day_desc, day_icon = get_weather_info(codes[i])
            day_temp = round(max_temps[i])

            row = QHBoxLayout()
            row.setContentsMargins(15, 8, 15, 8)

            lbl_day = QLabel(day_name)
            lbl_day.setStyleSheet(
                "color: white; font-size: 15px; font-weight: bold; width: 45px; background: transparent;")
            lbl_cond = QLabel(f"{day_icon} {day_desc}")
            lbl_cond.setStyleSheet("color: rgba(255, 255, 255, 0.85); font-size: 14px; background: transparent;")
            lbl_cond.setAlignment(Qt.AlignCenter)
            lbl_temp = QLabel(f"{day_temp}°C")
            lbl_temp.setStyleSheet("color: white; font-size: 15px; font-weight: bold; background: transparent;")
            lbl_temp.setAlignment(Qt.AlignRight)

            row.addWidget(lbl_day)
            row.addWidget(lbl_cond)
            row.addWidget(lbl_temp)

            card = QFrame()
            card.setStyleSheet(
                "QFrame { background-color: rgba(255, 255, 255, 0.08); border-radius: 10px; border: 1px solid transparent;} QFrame:hover { background-color: rgba(255, 255, 255, 0.2); border: 1px solid rgba(255, 255, 255, 0.5); }")
            card.setLayout(row)
            self.forecast_layout.addWidget(card)

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        bg_category = get_bg_category(self.current_condition)
        grad_colors = COLORS.get(bg_category, COLORS["Sunny"])

        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, grad_colors[0])
        gradient.setColorAt(1.0, grad_colors[1])

        painter.setBrush(gradient)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), 24, 24)