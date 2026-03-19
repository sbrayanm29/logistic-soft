import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer

from ui.splash import SplashScreen
from ui.ventana_principal import VentanaPrincipal
from utils.recursos import resource_path

app = QApplication(sys.argv)

css_file = resource_path("styles.css")

if os.path.exists(css_file):
    with open(css_file, "r", encoding="utf-8") as f:
        app.setStyleSheet(f.read())

splash = SplashScreen()
splash.show()

ventana = VentanaPrincipal()

def iniciar_app():
    splash.close()
    ventana.show()

QTimer.singleShot(3000, iniciar_app)

sys.exit(app.exec())