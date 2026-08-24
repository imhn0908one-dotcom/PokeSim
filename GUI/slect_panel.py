from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtGui import QIcon, QMouseEvent, QPixmap
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)


@dataclass
class SelectOption:
    """1件分の選択肢を表すクラス。

    title は表示名、subtitle は補足情報、description は詳細情報を表す。
    """

    id: int
    title: str
    subtitle: str
    description: dict[str, int] | None
    icon_path: str
    used_rate: float | None


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

    def __init__(self, options: list[SelectOption] | None = None):
        super().__init__()
        self._options: list[SelectOption] = []
        self._widgets: dict[int, SelectOptionWidget] = {}
        self._selected_option: SelectOption | None = None
        self._selected_widget: SelectOptionWidget | None = None
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
        self._search_bar.setPlaceholderText("検索（後で実装）")
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

    def set_options(self, options: list[SelectOption]) -> None:
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

    def _update_header_text(self) -> None:
        """ヘッダーテキストを現在の設定値から再構築する。"""
        if self._selected_option is None:
            self._header_button.setText(f"{self._header_selection_text}を選択")
            self._header_button.setIcon(QIcon())
            return

        self._header_button.setText(
            f"{self._selected_option.title} / {self._selected_option.subtitle}"
        )

        icon = QIcon(self._selected_option.icon_path)
        self._header_button.setIcon(icon)
