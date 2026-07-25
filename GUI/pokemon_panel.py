# Pokemon Panel for the GUI select pokemon and show its details
# makingGUI with python and Pyside6
import signal
from dataclasses import dataclass, fields
from typing import Dict, List, Tuple

from PySide6.QtCore import QSize, Qt, QTimer, Signal, Slot
from PySide6.QtGui import (
    QAction,
    QFont,
    QIcon,
    QKeySequence,
    QPixmap,
)
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
    QVBoxLayout,
    QWidget,
)

from FIELD.state import BattleField
from GUI import field_panel, panel_logic
from POKEMON import factory, instance, manager

from .field_panel import FieldPanel


class PokemonPanel(QFrame):
    def __init__(self, panel_name, battle_manager):
        super().__init__()
        self.setWindowTitle(f"{panel_name} Panel")
        self.battle_manager = battle_manager
        self.instance_atk_or_def = panel_name
        # window size
        self.setMinimumSize(200, 300)
        self.side_state_widget = {}
        # layout
        self.field_selection_layout = QVBoxLayout()
        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel(f"{panel_name} Selection"))
        self.pokemon_combo = panel_logic.SelectionComboBox(
            items=manager.get_selectable_pokemon_map(),
            placeholder="Select a Pokemon",
            objectName="pokemon_selection",
        )
        self.pokemon_combo.currentIndexChanged.connect(
            self.emit_updated_pokemon_instance
        )

        main_layout.addWidget(self.pokemon_combo)
        print(self.styleSheet())
        self.setLayout(main_layout)

    # if pokemon is selected, emit pokemon instance
    @Slot()
    def emit_updated_pokemon_instance(self):
        id = self.pokemon_combo.currentData()
        if self.instance_atk_or_def == "attacker":
            print(self.battle_manager.attacker, id)
        elif self.instance_atk_or_def == "defender":
            print(f"defender{id}")


# pokemon view(details)
class PokemonViewPanel(QWidget):
    def __init__(self, panel_name, battle_manager):
        super().__init__()
        self.setWindowTitle("Pokemon View Panel")
        self.battle_manager = battle_manager
        self.setObjectName(panel_name)

    pass
