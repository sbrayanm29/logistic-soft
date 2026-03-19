import pandas as pd
import openpyxl as px
import sys
import os
import unicodedata
import numpy as np
import itertools

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QHBoxLayout, QVBoxLayout,
    QPushButton, QLabel, QFileDialog,
    QListWidget, QTableWidget, QTableWidgetItem,
    QLineEdit, QComboBox, QProgressBar,
    QStackedWidget, QGraphicsOpacityEffect, QListWidgetItem, QFrame
)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QCoreApplication, QTimer, QUrl
from PySide6.QtGui import QAction, QDesktopServices
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill
from itertools import combinations

class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedSize(500,300)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet("background-color:#0f172a;")

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        titulo = QLabel()
        titulo.setAlignment(Qt.AlignCenter)

        titulo.setText(
            '<span style="font-size:80px; font-weight:bold; color:#38bdf8;">L</span>'
            '<span style="font-size:50px; font-weight:bold; color:white;">ogistic</span>'
            '<span style="font-size:18px; color:#94a3b8;"> SOFT</span>'
        )

        layout.addWidget(titulo)

        self.loading = QProgressBar()
        self.loading.setRange(0,0)
        self.loading.setFixedWidth(200)

        self.loading.setStyleSheet("""
        QProgressBar{
            border: none;
            background-color: #1e293b;
            height:8px;
            border-radius:4px;
        }
        QProgressBar::chunk{
            background-color:#38bdf8;
            border-radius:4px;
        }
        """)

        layout.addSpacing(40)
        layout.addWidget(self.loading, alignment=Qt.AlignCenter)

        self.setLayout(layout)