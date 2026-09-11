import math
from dataclasses import dataclass

from ENUMS import basic_enums, field_enums, move_enums, pokemon_enums
from FIELD import field
from MOVE import move_object
from POKEMON import pokemon_object


@dataclass
class CalculateContext:
    """計算のコンテキストを管理するクラス。"""

    attacker: pokemon_object.BattlePokemon
    """攻撃側のポケモン。"""
    defender: pokemon_object.BattlePokemon
    """防御側のポケモン。"""
    move: move_object.MasterMove
    """使用する技。"""
    battlefield: field.BattleField
    """バトルフィールドの状態。"""

    @property
    def move_type(self) -> int:
        """技のタイプを取得するプロパティ。"""

        return self.move.type_id

    @property
    def move_damage_class(self) -> int:
        """技のダメージクラスを取得するプロパティ。"""

        return self.move.damage_class_id

    @property
    def attacker_speed(self) -> int:
        """攻撃側のポケモンの素早さを取得するプロパティ。"""

        return self.attacker.rank_calced_real_stats("SPEED")

    @property
    def defender_speed(self) -> int:
        """防御側のポケモンの素早さを取得するプロパティ。"""

        return self.defender.rank_calced_real_stats("SPEED")
