# makingGUI with python and Pyside6
import os
import sqlite3
import sys
from datetime import datetime
from typing import Dict, List, Tuple

from PySide6.QtCore import (
    QSize,
    Qt,
    QTimer,
    Slot,
)
from PySide6.QtGui import QAction, QFont, QIcon, QImage, QKeySequence, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDial,
    QDoubleSpinBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSlider,
    QSpinBox,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from BATTLE import battle_manager
from GUI.field_panel import FieldPanel
from GUI.pokemon_panel import PokemonPanel
from GUI.result_panel import ResultPanel
from POKEMON.manager import learnt_move_names_to_dict

# pannel import
from POKEMON.pokemon_object import PokemonInstance


class MainWindow(QMainWindow):
    """Main window for the Pokemon GUI application.
    This class represents the main window of the application, which contains
    various panels for selecting Pokemon, displaying results, and configuring the field."""

    def __init__(self):
        super().__init__()
        self.battle_manager = battle_manager.BattleManager()
        self.setWindowTitle("Main Window")
        # pannel
        self.left_pannel = PokemonPanel("attacker", self.battle_manager)
        self.right_pannel = PokemonPanel("defender", self.battle_manager)
        self.result_pannel = ResultPanel()
        self.bottom_pannel = FieldPanel(battle_manager=self.battle_manager)
        # object name
        self.left_pannel.setObjectName("left_pannel")
        self.right_pannel.setObjectName("right_pannel")
        self.result_pannel.setObjectName("result_pannel")
        self.bottom_pannel.setObjectName("bottom_pannel")

        # window size
        screen = QApplication.primaryScreen()
        geometry = screen.availableGeometry()
        H_size = geometry.height() * 0.7
        W_size = H_size * 1.5

        self.resize(int(W_size), int(H_size))

        self.setMinimumSize(750, 500)

        # layout by splitter
        self.sep1 = QSplitter(Qt.Orientation.Vertical)
        self.sep1.addWidget(self.result_pannel)
        self.sep1.addWidget(self.bottom_pannel)

        # main layout
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.left_pannel)
        main_layout.addWidget(self.sep1)
        main_layout.addWidget(self.right_pannel)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # main widget
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # style sheet
        self.load_stylesheet("GUI/style.qss")

    @Slot(str)
    def load_stylesheet(self, stylesheet_path: str):
        """Load a stylesheet from a file and apply it to the main window."""
        if os.path.exists(stylesheet_path):
            with open(stylesheet_path, "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())
        else:
            print(f"Stylesheet file not found: {stylesheet_path}")
