from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Sequence

from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtGui import QIcon, QMouseEvent, QPixmap
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from MOVE import move_object
from POKEMON import enums


@dataclass
class SelectOption:
    """1件分の選択肢を表すクラス。

    title は表示名、subtitle は補足情報、description は詳細情報を表す。
    """

    id: int
    title: str
    subtitle: str
    description: dict[str, int] | None
    icon_path: str | None
    used_rate: float | None


@dataclass
class MoveSelectOption(SelectOption):
    """MasterMove を保持し、SelectPanel / UI 用に最適化した選択肢データ"""

    move: move_object.MasterMove | None = None

    @classmethod
    def from_master(
        cls,
        move: move_object.MasterMove,
        icon_path: str = "",
        used_rate: float | None = None,
    ) -> MoveSelectOption:
        """MasterMove から UI 表示用の MoveSelectOption を生成する"""

        # サブタイトル例: 「ほのお / 物理 (威力: 90 / 命中: 100)」
        power_str = f"威力:{move.power}" if move.power is not None else "威力:-"
        acc_str = f"命中:{move.accuracy}" if move.accuracy is not None else "命中:-"
        subtitle = (
            f"{move.type_id.name} / {move.damage_class_id.description} "
            f"({power_str} {acc_str})"
        )

        return cls(
            id=move.id,
            title=move.jpname,
            subtitle=subtitle,
            description=None,
            icon_path=icon_path,
            used_rate=used_rate,
            move=move,
        )

    def get_tags(self) -> set[Enum]:
        """enums.py で定義された Enum 群をフィルター用のタグとして取り出す"""
        if self.move is None:
            return set()

        tags = {
            self.move.type_id,
            self.move.damage_class_id,
            self.move.target_id,
            self.move.category_id,
            self.move.ailment_id,
        }
        if self.move.stat_changes_stat is not None:
            tags.update(self.move.stat_changes_stat.keys())

        enum_types = tuple(
            value
            for value in vars(enums).values()
            if isinstance(value, type) and issubclass(value, Enum)
        )
        return {tag for tag in tags if isinstance(tag, enum_types)}


class SelectOptionWidget(QFrame):
    """1件の選択肢を描画するウィジェット。"""

    clicked = Signal(SelectOption)

    def __init__(self, select_option: SelectOption):
        super().__init__()
        self.select_option = select_option
        self._is_selected = False
        self.setObjectName("select_option_label")
        self.setMaximumSize(100, 25)
        self._apply_selection_style()
        self.setStyleSheet(
            """
            QFrame#select_option_label {
                border: 2px solid #ccc;
                border-radius: 6px;
                background-color: #f9f9f9;
            }
            QFrame#select_option_label:hover {
                border: 2px solid #3b82f6;
                background-color: #dbeafe;
            }
            """
        )
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(8)

        icon_label = QLabel(self)
        icon_label.setFixedSize(32, 32)
        if select_option.icon_path:
            pixmap = QPixmap(select_option.icon_path)
            if not pixmap.isNull():
                icon_label.setPixmap(
                    pixmap.scaled(
                        QSize(32, 32),
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation,
                    )
                )
        layout.addWidget(icon_label)

        text_layout = QVBoxLayout()
        self.title_label = QLabel(text=select_option.title)
        self.subtitle_label = QLabel(text=select_option.subtitle)
        self.title_label.setWordWrap(True)
        self.subtitle_label.setWordWrap(True)
        text_layout.addWidget(self.title_label)
        text_layout.addWidget(self.subtitle_label)

        if select_option.description:
            description = " / ".join(
                f"{key}: {value}" for key, value in select_option.description.items()
            )
            self.description_label = QLabel(text=description)
            self.description_label.setWordWrap(True)
            text_layout.addWidget(self.description_label)

        layout.addLayout(text_layout)

    def set_selected(self, selected: bool) -> None:
        """選択状態を更新し、見た目を切り替える。"""
        self._is_selected = selected
        self._apply_selection_style()

    def _apply_selection_style(self) -> None:
        """選択状態に応じて枠線と背景色を切り替える。"""
        border_color = "#3b82f6" if self._is_selected else "#ccc"
        background_color = "#dbeafe" if self._is_selected else "#f9f9f9"
        self.setStyleSheet(
            f"""
            QFrame#select_option_label {{
                border: 2px solid {border_color};
                border-radius: 6px;
                background-color: {background_color};
            }}
            """
        )

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """if mouse click, emit clicked signal with the select_option object."""
        self.clicked.emit(self.select_option)
        super().mousePressEvent(event)


class PopupList(QListWidget):
    """ポップアップ表示用のリストウィジェット。"""

    item_selected = Signal(SelectOption)

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.Popup)
        self.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self.itemClicked.connect(self._on_item_clicked)

    def set_options(self, options: Sequence[SelectOption]) -> None:
        """選択肢を QListWidgetItem としてセットする。"""
        self.clear()
        for option in options:
            # 表示テキスト（タイトル ＋ サブタイトル）
            display_text = f"{option.title}  ({option.subtitle})"
            item = QListWidgetItem(display_text)

            # 裏データとして SelectOption オブジェクトを保持
            item.setData(Qt.ItemDataRole.UserRole, option)
            self.addItem(item)

    def _on_item_clicked(self, item: QListWidgetItem) -> None:
        """アイテム選択時にオブジェクトを伝播し、ポップアップを閉じる。"""
        option = item.data(Qt.ItemDataRole.UserRole)
        if isinstance(option, SelectOption):
            self.item_selected.emit(option)
            self.hide()


class FilterWidget(QWidget):
    """Enumカテゴリごとにドロップダウンを並べるフィルターウィジェット。"""

    filter_changed = Signal(dict)

    def __init__(
        self,
        target_enums: Sequence[tuple[str, type[Enum]]],
        parent: QWidget | None = None,
    ):
        super().__init__(parent)
        self._combos: dict[type[Enum], QComboBox] = {}

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        for label_text, enum_cls in target_enums:
            layout.addWidget(QLabel(f"{label_text}:", self))

            combo = QComboBox(self)
            combo.addItem("すべて", userData=None)

            for member in enum_cls:
                if getattr(member, "name", "") == "NONE":
                    continue
                display_name = getattr(member, "description", member.name)
                combo.addItem(display_name, userData=member)

            combo.currentIndexChanged.connect(self._on_filter_changed)
            self._combos[enum_cls] = combo
            layout.addWidget(combo)

    def _on_filter_changed(self) -> None:
        filters: dict[type[Enum], set[Enum]] = {}
        for enum_cls, combo in self._combos.items():
            selected_enum = combo.currentData()
            filters[enum_cls] = {selected_enum} if selected_enum is not None else set()
        self.filter_changed.emit(filters)

    def get_active_filters(self) -> dict[type[Enum], set[Enum]]:
        filters: dict[type[Enum], set[Enum]] = {}
        for enum_cls, combo in self._combos.items():
            selected_enum = combo.currentData()
            filters[enum_cls] = {selected_enum} if selected_enum is not None else set()
        return filters


class SelectPanel(QFrame):
    """FilterWidget と PopupList を統合管理する親パネル。"""

    selection_changed = Signal(object)
    option_selected = Signal(SelectOption)

    def __init__(self, options: Sequence[SelectOption] | None = None):
        super().__init__()
        self._options: list[SelectOption] = []
        self._selected_option: SelectOption | None = None
        self._filter_widget: FilterWidget | None = None
        self._active_filters: dict[type[Enum], set[Enum]] = {}
        self._search_text = ""
        self._header_selection_text = "選択肢"

        self.setObjectName("select_panel")
        self.setStyleSheet(
            """
            QFrame#select_panel {
                border: 1px solid #d0d0d0;
                border-radius: 6px;
                background-color: #f9f9f9;
            }
            """
        )

        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(8, 8, 8, 8)
        self._layout.setSpacing(6)

        # 検索バー
        self._search_bar = QLineEdit(self)
        self._search_bar.setPlaceholderText("検索...")
        self._search_bar.setClearButtonEnabled(True)
        self._search_bar.textChanged.connect(self._filter_options_by_text)
        self._layout.addWidget(self._search_bar)

        # メイン選択ボタン（クリックでポップアップ表示）
        self._header_button = QPushButton(self)
        self._header_button.setIconSize(QSize(24, 24))
        self._header_button.setStyleSheet("text-align: left; padding: 6px;")
        self._header_button.clicked.connect(self.show_popup)
        self._layout.addWidget(self._header_button)

        # ポップアップリストの生成
        self._popup_list = PopupList(self)
        self._popup_list.item_selected.connect(self.on_option_selected)

        self._update_header_text()

        if options is not None:
            self.set_options(options)

    def attach_filter_widget(self, filter_widget: FilterWidget) -> None:
        """FilterWidget を SelectPanel のレイアウト上部へ挿入・接続する。"""
        self._filter_widget = filter_widget
        self._filter_widget.filter_changed.connect(self._on_filter_changed)
        self._active_filters = self._filter_widget.get_active_filters()

        # レイアウトの一番上（検索バーの上）に追加
        self._layout.insertWidget(0, self._filter_widget)
        self._apply_filters()

    def set_options(self, options: Sequence[SelectOption]) -> None:
        """選択肢一覧を更新し PopupList にセットする。"""
        self.clear_selection()
        self._options = list(options)
        self._popup_list.set_options(self._options)
        self._apply_filters()

    def show_popup(self) -> None:
        """ヘッダーボタンの直下に PopupList を展開する。"""
        pos = self._header_button.mapToGlobal(self._header_button.rect().bottomLeft())
        self._popup_list.move(pos)
        self._popup_list.setFixedWidth(max(self._header_button.width(), 280))
        self._popup_list.setFixedHeight(250)
        self._apply_filters()
        self._popup_list.show()

    def on_option_selected(self, select_option: SelectOption) -> None:
        """PopupList で選択されたアイテムを受け取る。"""
        self._selected_option = select_option
        self._update_header_text()
        self.selection_changed.emit(select_option)
        self.option_selected.emit(select_option)

    def clear_selection(self) -> None:
        had_selection = self._selected_option is not None
        self._selected_option = None
        self._update_header_text()
        if had_selection:
            self.selection_changed.emit(None)

    def _filter_options_by_text(self, search_text: str) -> None:
        self._search_text = search_text
        self._apply_filters()

    def _on_filter_changed(self, filters: dict[type[Enum], set[Enum]]) -> None:
        self._active_filters = filters
        self._apply_filters()

    def _apply_filters(self) -> None:
        """QListWidgetItem の UserRole からデータを取り出し setHidden で絞り込む。"""
        normalized_query = self._search_text.strip().casefold()

        for i in range(self._popup_list.count()):
            item = self._popup_list.item(i)
            option: SelectOption | None = item.data(Qt.ItemDataRole.UserRole)
            if option is None:
                continue

            is_visible = self._matches_search_query(
                option, normalized_query
            ) and self._matches_enum_filters(option)
            item.setHidden(not is_visible)

    def _matches_search_query(
        self, option: SelectOption, normalized_query: str
    ) -> bool:
        if normalized_query == "":
            return True
        searchable_fields: list[str] = [option.title, option.subtitle]
        if option.description is not None:
            searchable_fields.extend(option.description.keys())
        if option.used_rate is not None:
            searchable_fields.append(str(option.used_rate))

        return normalized_query in " ".join(searchable_fields).casefold()

    def _matches_enum_filters(self, option: SelectOption) -> bool:
        if self._filter_widget is None:
            return True
        get_tags = getattr(option, "get_tags", None)
        if not callable(get_tags):
            return True

        option_tags = get_tags()
        if not isinstance(option_tags, set):
            return True

        for enum_cls, selected_tags in self._active_filters.items():
            if not selected_tags:
                continue
            if not any(
                isinstance(tag, enum_cls) and tag in selected_tags
                for tag in option_tags
            ):
                return False
        return True

    def _update_header_text(self) -> None:
        if self._selected_option is None:
            self._header_button.setText(f"{self._header_selection_text}を選択")
            self._header_button.setIcon(QIcon())
            return

        self._header_button.setText(
            f"{self._selected_option.title} / {self._selected_option.subtitle}"
        )
        icon_path = self._selected_option.icon_path
        self._header_button.setIcon(QIcon(icon_path) if icon_path else QIcon())
