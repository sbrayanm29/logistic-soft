import pandas as pd
import openpyxl as px
import sys
import os
import unicodedata
import numpy as np
import itertools

from PySide6.QtWidgets import QWidget, QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices

from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill
from itertools import combinations



class DescargaChrome(QWidget):

    def __init__(self, ruta):
        super().__init__()

        self.ruta = ruta
        nombre = os.path.basename(ruta)

        frame = QFrame()
        frame.setStyleSheet("""
        QFrame{
            border:1px solid #e0e0e0;
            border-radius:8px;
            padding:8px;
            background:white;
        }
        QPushButton{
            border:none;
            color:#1a73e8;
            font-weight:bold;
        }
        QPushButton:hover{
            text-decoration:underline;
        }
        """)

        layout = QVBoxLayout(frame)

        titulo = QLabel(nombre)
        titulo.setStyleSheet("font-weight:bold;font-size:13px")

        ruta_label = QLabel(self.ruta)
        ruta_label.setStyleSheet("color:gray;font-size:11px")

        botones = QHBoxLayout()

        abrir = QPushButton("Abrir")
        carpeta = QPushButton("Mostrar en carpeta")
        borrar = QPushButton("Eliminar")

        abrir.clicked.connect(self.abrir_archivo)
        carpeta.clicked.connect(self.abrir_carpeta)
        borrar.clicked.connect(self.eliminar)

        botones.addWidget(abrir)
        botones.addWidget(carpeta)
        botones.addWidget(borrar)

        layout.addWidget(titulo)
        layout.addWidget(ruta_label)
        layout.addLayout(botones)

        main = QVBoxLayout()
        main.addWidget(frame)

        self.setLayout(main)

    def abrir_archivo(self):
        QDesktopServices.openUrl(QUrl.fromLocalFile(self.ruta))

    def abrir_carpeta(self):
        carpeta = os.path.dirname(self.ruta)
        QDesktopServices.openUrl(QUrl.fromLocalFile(carpeta))

    def eliminar(self):
        self.setParent(None)