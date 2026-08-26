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
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from POKEMON import enums, move


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

    move: move.MasterMove | None = None

    @classmethod
    def from_master(
        cls, move: move.MasterMove, icon_path: str = "", used_rate: float | None = None
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
        self.setMinimumSize(200, 50)
        self.setMaximumSize(200, 50)
        self._apply_selection_style()

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
        self.title_label = QLabel(select_option.title, self)
        self.subtitle_label = QLabel(select_option.subtitle, self)
        self.title_label.setWordWrap(True)
        self.subtitle_label.setWordWrap(True)
        text_layout.addWidget(self.title_label)
        text_layout.addWidget(self.subtitle_label)

        if select_option.description:
            description = " / ".join(
                f"{key}: {value}" for key, value in select_option.description.items()
            )
            self.description_label = QLabel(description, self)
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
        self.clicked.emit(self.select_option)
        super().mousePressEvent(event)


class SelectPanel(QFrame):
    """1件だけ選択できる選択肢一覧パネル。"""

    selection_changed = Signal(object)
    option_selected = Signal(SelectOption)

    def __init__(self, options: Sequence[SelectOption] | None = None):
        super().__init__()
        self._options: Sequence[SelectOption] = []
        self._widgets: dict[int, SelectOptionWidget] = {}
        self._selected_option: SelectOption | None = None
        self._selected_widget: SelectOptionWidget | None = None
        self._filter_widget: FilterWidget | None = None
        self._active_filters: dict[type[Enum], set[Enum]] = {}
        self._search_text = ""
        self._header_selection_text = "{}"
        self._expanded = False

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

        self._header_button = QPushButton(self)
        self._header_button.setIconSize(QSize(24, 24))
        self._header_button.clicked.connect(self.toggle_expand)
        self._header_button.hide()
        self._layout.addWidget(self._header_button)

        self._control_layout = QHBoxLayout()
        self._control_layout.setContentsMargins(0, 0, 0, 0)
        self._control_layout.setSpacing(6)
        self._search_bar = QLineEdit(self)
        self._search_bar.setPlaceholderText("検索")
        self._search_bar.textChanged.connect(self._filter_options_by_text)
        self._filter_button = QPushButton("絞り込み", self)
        self._control_layout.addWidget(self._search_bar)
        self._control_layout.addWidget(self._filter_button)
        self._layout.addLayout(self._control_layout)

        self._scroll_area = QScrollArea(self)
        self._scroll_area.setWidgetResizable(True)
        self._scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self._scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        self._content_widget = QWidget(self)
        self._content_layout = QVBoxLayout(self._content_widget)
        self._content_layout.setContentsMargins(0, 0, 0, 0)
        self._content_layout.setSpacing(6)
        self._scroll_area.setWidget(self._content_widget)
        self._layout.addWidget(self._scroll_area)
        self._update_header_text()

        if options is not None:
            self.set_options(options)

    def set_options(self, options: Sequence[SelectOption]) -> None:
        """選択肢一覧を差し替える。"""
        self.clear_selection()
        self._options = list(options)
        self._widgets.clear()

        for widget in self._content_widget.findChildren(SelectOptionWidget):
            widget.deleteLater()

        for option in self._options:
            widget = SelectOptionWidget(option)
            widget.clicked.connect(self.on_option_clicked)
            self._widgets[option.id] = widget
            self._content_layout.addWidget(widget)

        self._apply_filters()

    def on_option_clicked(self, select_option: SelectOption) -> None:
        """ユーザーのクリックを受け取り、単一選択状態を更新する。"""
        if (
            self._selected_option is not None
            and self._selected_option.id == select_option.id
        ):
            self.clear_selection()
            return

        if self._selected_widget is not None:
            self._selected_widget.set_selected(False)

        self._selected_option = select_option
        self._selected_widget = self._widgets.get(select_option.id)
        if self._selected_widget is not None:
            self._selected_widget.set_selected(True)
        self._update_header_text()
        self.set_scroll_area_visible(False)

        self.selection_changed.emit(select_option)
        self.option_selected.emit(select_option)

    def selected_option(self) -> SelectOption | None:
        """現在選択中の選択肢を返す。"""
        return self._selected_option

    def selected_id(self) -> int | None:
        """現在選択中の選択肢IDを返す。"""
        if self._selected_option is None:
            return None
        return self._selected_option.id

    def select_by_id(self, option_id: int) -> bool:
        """IDを指定して選択肢を選択する。"""
        widget = self._widgets.get(option_id)
        if widget is None:
            return False

        if self._selected_option is not None and self._selected_option.id == option_id:
            return True

        if self._selected_widget is not None:
            self._selected_widget.set_selected(False)

        self._selected_option = widget.select_option
        self._selected_widget = widget
        self._selected_widget.set_selected(True)
        self._update_header_text()
        self.set_scroll_area_visible(False)

        self.selection_changed.emit(self._selected_option)
        self.option_selected.emit(self._selected_option)
        return True

    def clear_selection(self) -> None:
        """選択を解除する。"""
        had_selection = self._selected_option is not None
        if self._selected_widget is not None:
            self._selected_widget.set_selected(False)
        self._selected_option = None
        self._selected_widget = None
        self._update_header_text()
        if had_selection:
            self.selection_changed.emit(None)

    def set_scroll_area_visible(self, visible: bool) -> None:
        """スクロール領域の表示状態を切り替える。"""
        self._expanded = visible
        self._scroll_area.setVisible(visible)
        self._search_bar.setVisible(visible)
        self._filter_button.setVisible(visible)
        self._header_button.setVisible(not visible)
        if visible:
            self._apply_filters()

    def toggle_expand(self) -> None:
        """展開状態を切り替える。"""
        self.set_scroll_area_visible(not self._expanded)

    def set_header_selection_text(self, text: str) -> None:
        """ヘッダーに表示する選択対象テキストを更新する。"""
        self._header_selection_text = text
        self._update_header_text()

    def search_bar_widget(self) -> QLineEdit:
        """検索バーを返す。"""
        return self._search_bar

    def filter_button_widget(self) -> QPushButton:
        """フィルターボタンを返す。"""
        return self._filter_button

    def attach_filter_widget(self, filter_widget: FilterWidget) -> None:
        """Enumフィルターウィジェットを接続する。

        Args:
            filter_widget: 連動させるフィルターウィジェット。
        """
        self._filter_widget = filter_widget
        self._filter_widget.filter_changed.connect(self._on_filter_changed)
        self._active_filters = self._filter_widget.get_active_filters()
        self._apply_filters()

    def _filter_options_by_text(self, search_text: str) -> None:
        """検索語に一致しない選択肢ウィジェットを非表示にする。

        Args:
            search_text: 検索バーに入力された文字列。
        """
        self._search_text = search_text
        self._apply_filters()

    def _on_filter_changed(self, filters: dict[type[Enum], set[Enum]]) -> None:
        """Enumフィルターの変更を受け取り、表示状態を更新する。

        Args:
            filters: フィルター対象のEnumごとの選択値。
        """
        self._active_filters = filters
        self._apply_filters()

    def _apply_filters(self) -> None:
        """検索文字列とEnumフィルターをまとめて反映する。"""
        normalized_query = self._search_text.strip().casefold()
        for widget in self._widgets.values():
            option = widget.select_option
            is_visible = self._matches_search_query(option, normalized_query)
            if is_visible:
                is_visible = self._matches_enum_filters(option)
            widget.setVisible(is_visible)

    def _matches_search_query(
        self, option: SelectOption, normalized_query: str
    ) -> bool:
        """検索語と選択肢の一致可否を返す。

        Args:
            option: 一致判定対象の選択肢。
            normalized_query: 前処理済み検索語（前後空白除去 + casefold）。

        Returns:
            検索語に一致すれば True。
        """
        if normalized_query == "":
            return True

        searchable_fields: list[str] = [option.title, option.subtitle]
        if option.description is not None:
            searchable_fields.extend(option.description.keys())
        if option.used_rate is not None:
            searchable_fields.append(str(option.used_rate))

        normalized_fields = " ".join(searchable_fields).casefold()
        return normalized_query in normalized_fields

    def _matches_enum_filters(self, option: SelectOption) -> bool:
        """Enumフィルターに一致するかを判定する。

        Args:
            option: 判定対象の選択肢。

        Returns:
            全フィルター条件に一致する場合は True。
        """
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
            if not any(isinstance(tag, enum_cls) and tag in selected_tags for tag in option_tags):
                return False
        return True

    def _update_header_text(self) -> None:
        """ヘッダーテキストを現在の設定値から再構築する。"""
        if self._selected_option is None:
            self._header_button.setText(f"{self._header_selection_text}を選択")
            self._header_button.setIcon(QIcon())
            return

        self._header_button.setText(
            f"{self._selected_option.title} / {self._selected_option.subtitle}"
        )

        icon_path = self._selected_option.icon_path
        icon = QIcon(icon_path) if icon_path else QIcon()
        self._header_button.setIcon(icon)


class FilterWidget(QWidget):
    """Enumカテゴリごとにドロップダウンを並べるフィルターウィジェット。"""

    filter_changed = Signal(object)

    def __init__(
        self,
        target_enums: Sequence[tuple[str, type[Enum]]],
        parent: QWidget | None = None,
    ):
        """
        Args:
            target_enums: (表示名, Enumクラス) のリスト
                例: [("タイプ", TypeID), ("分類", MoveDamageClass)]
        """
        super().__init__(parent)
        self._combos: dict[type[Enum], QComboBox] = {}

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        for label_text, enum_cls in target_enums:
            layout.addWidget(QLabel(f"{label_text}:", self))

            combo = QComboBox(self)
            combo.addItem("すべて", userData=None)

            # Enumの要素をドロップダウンに追加
            for member in enum_cls:
                # NONE 項目や未定義のスキップ（必要に応じて調整）
                if getattr(member, "name", "") == "NONE":
                    continue

                display_name = getattr(member, "description", member.name)
                combo.addItem(display_name, userData=member)

            combo.currentIndexChanged.connect(self._on_filter_changed)
            self._combos[enum_cls] = combo
            layout.addWidget(combo)

    def _on_filter_changed(self) -> None:
        """現在の全コンボボックスの選択状態を集約してシグナルを送る。"""
        filters: dict[type[Enum], set[Enum]] = {}

        for enum_cls, combo in self._combos.items():
            selected_enum = combo.currentData()
            if selected_enum is not None:
                filters[enum_cls] = {selected_enum}
            else:
                filters[enum_cls] = set()

        self.filter_changed.emit(filters)

    def get_active_filters(self) -> dict[type[Enum], set[Enum]]:
        """現在のフィルター選択状態を取得する。"""
        filters: dict[type[Enum], set[Enum]] = {}
        for enum_cls, combo in self._combos.items():
            selected_enum = combo.currentData()
            filters[enum_cls] = {selected_enum} if selected_enum is not None else set()
        return filters
