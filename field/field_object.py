from dataclasses import dataclass, field

# 実際のリモートモジュール構造に合わせてインポートしてください
from ENUMS import field_enums


@dataclass
class TimedState:
    """持続ターン数を持つ状態のデータクラス。
    Args:
        state (field_enums.FieldStateEnum): 状態の種類（フィールド効果や天候など）。
        remaining_turns (int): 残りターン数。0の場合は状態が存在しないことを示す。
        一つの状態のみを持つ。
    このクラスは、持続ターン数を持つ状態（フィールド効果や天候など）を管理するためのデータクラスです。
    """

    state: field_enums.FieldStateEnum
    """状態の種類（フィールド効果や天候など）。"""

    remaining_turns: int = field(default=0, metadata={"min": 0})
    """残りターン数。0の場合は状態が存在しないことを示す。"""

    @property
    def is_active(self) -> bool:
        """状態が有効かどうか（残りターン数が1以上かつNONEではない）"""
        none_value = getattr(self.state.__class__, "NONE", None)
        return self.remaining_turns > 0 and self.state != none_value

    def can_set_state(self, new_state: field_enums.FieldStateEnum) -> bool:
        """新しい状態を設定できるかどうかを判定する。いまのstateと同じの時もFalseを返す。
        すでに状態が有効な場合、同じ状態を再設定することはできません。新しい状態がNONEの場合も設定できません。

        Args:
            new_state (field_enums.FieldStateEnum): 設定しようとする新しい状態。

        Returns:
            bool: 新しい状態を設定できる場合は True、それ以外は False。
        """
        none_value = getattr(new_state.__class__, "NONE", None)
        return (
            self.state != new_state
            and new_state != none_value
            and self.is_active is False
        )

    def set_state(
        self, new_state: field_enums.FieldStateEnum, turns: int | None = None
    ) -> None:
        """新しい状態を設定する。すでに状態が有効な場合、同じ状態を再設定することはできません。
        新しい状態がNONEの場合も設定できません。

        Args:
            new_state (field_enums.FieldStateEnum): 設定しようとする新しい状態。
            turns (int | None): 新しい状態の持続ターン数。Noneの場合はデフォルトターン数を使用する。
        """
        if not self.can_set_state(new_state):
            raise ValueError(
                f"Cannot set state to {new_state}. Either the state is already active or the new state is NONE."
            )

        if turns is None:
            turns = new_state.default_turn

        if turns <= 0:
            raise ValueError("持続ターン数は1以上である必要があります。")

        self.state = new_state
        self.remaining_turns = turns

    def step_turn(self) -> bool:
        """ターンを進め、残りターン数を減少させる。

        Returns:
            bool: ちょうどこのターンで効果が終了した場合は True、それ以外は False
        """
        if not self.is_active:
            return False

        self.remaining_turns -= 1

        # カウントが0になったら効果終了処理を行う
        if self.remaining_turns == 0:
            none_value = getattr(self.state.__class__, "NONE", None)
            if none_value is not None:
                self.state = none_value  # NONE 状態に安全に初期化
            return True  # 「今ターンで終了した」ことを通知

        return False


@dataclass
class TerrainState(TimedState):
    """フィールドオブジェクトの状態を管理するデータクラス。"""

    state: field_enums.Terrain = field_enums.Terrain.NONE


class WeatherState(TimedState):
    """天候の状態を管理するデータクラス。"""

    state: field_enums.Weather = field_enums.Weather.NONE


class RoomState(TimedState):
    """バトルルームの状態を管理するデータクラス。"""

    state: field_enums.Room = field_enums.Room.NONE


@dataclass
class OtherEffectsContainer:
    """複数の『その他の効果』をまとめて管理するコンテナ"""

    # キー: 効果の種類(Enum) / 値: 残りターン数(int)
    active_effects: dict[field_enums.OtherEffect, int] = field(default_factory=dict)

    def add_effect(
        self, effect: field_enums.OtherEffect, turns: int | None = None
    ) -> bool:
        """効果を発動する（すでに発動中なら False）"""
        if effect in self.active_effects:
            return False  # 重複防止

        # 残りターン数だけを保存
        self.active_effects[effect] = (
            turns if turns is not None else effect.default_turn
        )
        return True

    def has_effect(self, effect: field_enums.OtherEffect) -> bool:
        """指定した効果が発動中か判定（O(1)で高速）"""
        return effect in self.active_effects

    def on_turn_end(self) -> list[str]:
        """ターン経過処理（1減らして0になったら削除）"""
        expired_messages = []

        # ループ中に辞書を書き換えるため list() でキーをコピーして回す
        for effect in list(self.active_effects.keys()):
            self.active_effects[effect] -= 1

            if self.active_effects[effect] <= 0:
                expired_messages.append(f"{effect.jpname} の効果が切れた！")
                del self.active_effects[effect]

        return expired_messages
