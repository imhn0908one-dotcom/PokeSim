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
    def attacker_speed(self) -> int:
        """攻撃側のポケモンの素早さを取得するプロパティ。"""

        return self.attacker.real_stats[pokemon_enums.Stats.SPEED]

    @property
    def defender_speed(self) -> int:
        """防御側のポケモンの素早さを取得するプロパティ。"""

        return self.defender.real_stats[pokemon_enums.Stats.SPEED]

    @property
    def move_power(self) -> int:
        """技の威力を取得するプロパティ。"""
        if self.move.power is None:
            return 0
        """ここに特定の技の威力を補正する関数を呼び出す"""
        if self.move.id == 360:
            # ジャイロボール
            return self._calc_gyro_ball_power()
        if self.move.id == 486:
            # エレキボール
            return self._calc_electro_ball_power()
        if self.move.id in (323, 284):
            # しおふき、ふんか
            return self._calc_HP_depended_power()
        if self.move.id in (179, 175):
            # きしかいせい、じたばた
            return self._calc_HP_reversal_power()
        if self.move.id in (447, 67):
            # くさむすび、けたぐり
            return self._calc_Weight_depended_power()
        return self.move.power

    def _calc_gyro_ball_power(self) -> int:
        """ジャイロボールの威力を計算するメソッド。

        Args:
            context (CalculateContext): 計算のコンテキスト。

        Returns:
            int: ジャイロボールの威力。
        """
        if self.move.id != 360:  # ジャイロボールの技IDを確認
            return self.move.power if self.move.power is not None else 0
        return min(
            150,
            25 * self.defender_speed // self.attacker_speed + 1,
        )

    def _calc_electro_ball_power(self) -> int:
        """エレキボールの威力を計算するメソッド。

        Returns:
            int: エレキボールの威力。
        """
        if self.move.id != 486:  # エレキボールの技IDを確認
            return self.move.power if self.move.power is not None else 0
        speed_ratio = math.floor(self.attacker_speed / self.defender_speed)
        return 30 * speed_ratio + 10 * (abs(speed_ratio - 2)) + 20

    def _calc_HP_depended_power(self) -> int:
        """HP依存の技の威力を計算するメソッド。

        Returns:
            int: HP依存の技の威力。
        """
        hp_ratio = (
            self.defender.real_stats[pokemon_enums.Stats.HP]
            / self.defender.real_stats[pokemon_enums.Stats.HP]
        )
        return max(1, int(150 * hp_ratio))

    def _calc_HP_reversal_power(self) -> int:
        """HP逆転の技の威力を計算するメソッド。

        Returns:
            int: HP逆転の技の威力。
        """
        hp_ratio = (
            self.defender.real_stats[pokemon_enums.Stats.HP]
            / self.defender.real_stats[pokemon_enums.Stats.HP]
        )
        if hp_ratio < 1 / 48:
            return 200
        elif hp_ratio < 1 / 12:
            return 150
        elif hp_ratio < 9 / 48:
            return 100
        elif hp_ratio < 16 / 48:
            return 80
        elif hp_ratio < 31 / 48:
            return 40
        else:
            return 20

    def _calc_Weight_depended_power(self) -> int:
        """重さ依存の技の威力を計算するメソッド。

        Returns:
            int: 重さ依存の技の威力。
        """
        weight = self.defender.master_data.weight
        if weight < 10:
            return 20
        elif weight < 25:
            return 40
        elif weight < 50:
            return 60
        elif weight < 100:
            return 80
        elif weight < 200:
            return 100
        else:
            return 120
