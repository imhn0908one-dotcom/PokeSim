from dataclasses import fields
from typing import Any

from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFrame,
    QSpinBox,
    QVBoxLayout,
)

from FIELD.field import BattleField


class FieldState(QObject):
    changed = Signal()

    def __init__(self):
        super().__init__()
        self.field = BattleField()

    def set_value(
        self,
        name: str,
        value,
    ) -> None:
        setattr(self.field, name, value)
        self.changed.emit()

    def update_field(self, values: dict[str, Any]) -> None:
        for name, value in values.items():
            setattr(self.field, name, value)
        self.changed.emit()


class FieldPanel(QFrame):
    """Display and edit the current battle field properties.

    The panel creates an appropriate Qt widget for each field attribute and
    updates the field state's field whenever a value changes.

    Args:
        field_state: The field state whose field is being edited.
    """

    def __init__(self, field_state: FieldState):
        super().__init__()
        self.field_state = field_state
        self.setWindowTitle("Field Panel")
        self.setObjectName("field_pannel")
        self.widgets = {}
        main_layout = QVBoxLayout()

        current_field = self.field_state.field
        field_class = current_field.__class__

        for field_info in fields(field_class):
            # 💡 現在のインスタンスから「初期値」を取り出して渡す
            current_val = getattr(current_field, field_info.name)

            self.widgets[field_info.name] = self.create_widget_by_type(
                field_info, current_val
            )
            main_layout.addWidget(self.widgets[field_info.name])

        # event connect
        for _, widget in self.widgets.items():
            if isinstance(widget, QComboBox):
                widget.currentIndexChanged.connect(self.emit_updated_battle_field)
            elif isinstance(widget, QSpinBox):
                widget.valueChanged.connect(self.emit_updated_battle_field)
            elif isinstance(widget, QCheckBox):
                widget.stateChanged.connect(self.emit_updated_battle_field)

        self.setLayout(main_layout)

    def create_widget_by_type(self, field_info, current_val):
        display_name = field_info.name.replace("_", " ").capitalize()

        if field_info.type is str:
            widget = QComboBox()
            widget.setPlaceholderText(display_name)
            widget.addItems(field_info.metadata["choices"])
            # 💡 初期値をセット
            if current_val in field_info.metadata["choices"]:
                widget.setCurrentText(current_val)
            return widget

        elif field_info.type is bool:
            widget = QCheckBox(display_name)
            # 💡 初期値をセット
            widget.setChecked(bool(current_val))
            return widget

        elif field_info.type is int:
            widget = QSpinBox()
            widget.setRange(field_info.metadata["min"], field_info.metadata["max"])
            widget.setPrefix(display_name + ": ")
            # 💡 初期値をセット
            widget.setValue(int(current_val))
            return widget

    def emit_updated_battle_field(self):
        values = {}

        for field_info in fields(self.field_state.field.__class__):
            widget = self.widgets[field_info.name]

            if isinstance(widget, QComboBox):
                val = widget.currentText()
            elif isinstance(widget, QSpinBox):
                val = widget.value()
            elif isinstance(widget, QCheckBox):
                val = widget.isChecked()

            values[field_info.name] = val

        self.field_state.update_field(values)

    def set_value(self, name: str, value: str | bool | int) -> None:
        """フィールド項目を1件更新する。

        UIウィジェットと内部状態を同時に更新し、値の整合性を保つために
        項目名・型・選択肢の妥当性を明示的に検証する。

        Args:
            name: 更新対象のフィールド名。
            value: 設定する値。

        Raises:
            KeyError: 指定フィールド名に対応するウィジェットが存在しない場合。
            TypeError: ウィジェット種別に対して値の型が不正な場合。
            ValueError: コンボボックスの選択肢に値が存在しない場合。
        """
        if name not in self.widgets:
            raise KeyError(f"Unknown field name: {name}")

        widget = self.widgets[name]

        if isinstance(widget, QComboBox):
            if not isinstance(value, str):
                raise TypeError(f"Field '{name}' requires str value.")
            if widget.findText(value) < 0:
                raise ValueError(f"Field '{name}' does not allow value: {value}")
            widget.blockSignals(True)
            widget.setCurrentText(value)
            widget.blockSignals(False)
            self.field_state.set_value(name, value)
            return

        if isinstance(widget, QSpinBox):
            if not isinstance(value, int) or isinstance(value, bool):
                raise TypeError(f"Field '{name}' requires int value.")
            widget.blockSignals(True)
            widget.setValue(value)
            widget.blockSignals(False)
            self.field_state.set_value(name, value)
            return

        if isinstance(widget, QCheckBox):
            if not isinstance(value, bool):
                raise TypeError(f"Field '{name}' requires bool value.")
            widget.blockSignals(True)
            widget.setChecked(value)
            widget.blockSignals(False)
            self.field_state.set_value(name, value)
            return

        raise TypeError(f"Unsupported widget type for field '{name}'.")
