from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtGui import QIcon, QMouseEvent, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

# noqa: E402 - import を実行する前にプロジェクトルートを追加する必要がある
from MOVE import move_object
from POKEMON import enums

# これで読み込めるようになります
# 修正前
# from .slect_panel import FilterWidget, MoveSelectOption, SelectOption, SelectPanel
# 修正後
from .slect_panel import FilterWidget, MoveSelectOption, SelectOption, SelectPanel

# プロジェクトルート (Pokemonフォルダ) を sys.path に追加
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))


def _build_sample_options() -> list[MoveSelectOption]:
    """テスト表示用の技データを組み立てる。

    Returns:
        enum フィルターの挙動を確認できるサンプル選択肢一覧。
    """
    sample_moves: list[move_object.MasterMove] = [
        move_object.MasterMove(
            id=1,
            name="ember",
            jpname="ほのおのうず",
            type_id=enums.TypeID.FIRE,
            damage_class_id=enums.MoveDamageClass.SPECIAL,
            pp=15,
            power=35,
            accuracy=100,
            target_id=enums.MoveTarget.RANDOM_OPPONENT,
            category_id=enums.MoveMetaCategory.DAMAGE_AILMENT,
            ailment_id=enums.MoveMetaAilment.BURN,
            ailment_chance=10,
            crit_rate=0,
            healing=0,
            drain=0,
            flinch_chance=0,
        ),
        move_object.MasterMove(
            id=2,
            name="thunderbolt",
            jpname="10まんボルト",
            type_id=enums.TypeID.ELECTRIC,
            damage_class_id=enums.MoveDamageClass.SPECIAL,
            pp=15,
            power=90,
            accuracy=100,
            target_id=enums.MoveTarget.RANDOM_OPPONENT,
            category_id=enums.MoveMetaCategory.DAMAGE,
            ailment_id=enums.MoveMetaAilment.NONE,
            ailment_chance=0,
            crit_rate=0,
            healing=0,
            drain=0,
            flinch_chance=0,
        ),
        move_object.MasterMove(
            id=3,
            name="swords-dance",
            jpname="つるぎのまい",
            type_id=enums.TypeID.NORMAL,
            damage_class_id=enums.MoveDamageClass.STATUS,
            pp=20,
            power=None,
            accuracy=None,
            target_id=enums.MoveTarget.USER,
            category_id=enums.MoveMetaCategory.NET_GOOD_STATS,
            ailment_id=enums.MoveMetaAilment.NONE,
            ailment_chance=0,
            crit_rate=0,
            healing=0,
            drain=0,
            flinch_chance=0,
            stat_changes_stat={enums.Stats.ATTACK: 2},
        ),
    ]
    return [
        MoveSelectOption.from_master(sample_move, used_rate=index / 10)
        for index, sample_move in enumerate(sample_moves, start=1)
    ]


class TempWindow(QMainWindow):
    """SelectPanel と enum フィルターの動作確認用ウィンドウ。"""

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.setWindowTitle("SelectPanel テスト")
        self.resize(800, 560)

        main_widget = QWidget(self)
        layout = QVBoxLayout(main_widget)

        self.filter_widget = FilterWidget([
            ("タイプ", enums.TypeID),
            ("分類", enums.MoveDamageClass),
        ])
        layout.addWidget(self.filter_widget)

        self.select_panel = SelectPanel()
        self.select_panel.attach_filter_widget(self.filter_widget)
        self.select_panel.set_options(_build_sample_options())
        self.select_panel.option_selected.connect(self._on_option_selected)

        self.result_label = QLabel("選択結果: 未選択", self)

        layout.addWidget(self.select_panel)
        layout.addWidget(self.result_label)
        self.setCentralWidget(main_widget)

    def _on_option_selected(self, select_option: SelectOption) -> None:
        """選択結果をラベルに反映する。

        Args:
            select_option: 選択された選択肢。
        """
        self.result_label.setText(
            f"選択結果: {select_option.title} / {select_option.subtitle}"
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TempWindow()
    window.show()
    sys.exit(app.exec())
