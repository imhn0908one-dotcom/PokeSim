import math
import stat
from dataclasses import dataclass
from email.mime import base

from numpy import power

from CALC.calculate_context import CalculateContext
from CALC.calculate_manager import CalculateResult
from ENUMS import basic_enums, move_enums, pokemon_enums


@dataclass
class CalculationState:
    """計算の状態を管理するクラス。"""

    base_power: int
    move_stats_type: pokemon_enums.Stats
    effective_attack_stat: int
    effective_deffense_stat: int
    power_modifier: float
    damage_modifier: float


class DamageCalculater:
    """ダメージ計算を行うクラス。"""

    def __init__(self) -> None:
        self.power_calculator = PowerCalculator()

    def damage_calculate(self, context: CalculateContext) -> CalculateResult:
        """ダメージ計算を行うメソッド。

        Args:
            context (CalculateContext): 計算のコンテキスト。

        Returns:
            CalculateResult: 計算結果を格納したオブジェクト。
        """
        state = CalculationState(
            base_power=self.power_calculator.calc_move_base_power(context),
            move_stats_type=self._move_calc_stat_type(context),
            effective_attack_stat=self.calc_modified_attack_stat(context),
            effective_deffense_stat=self.calc_modified_difend_stat(context),
            power_modifier=self.power_calculator._power_modifier_calculate(context), #calc_flow.md(l36)
            damage_modifier=1.0,  # TODO: ダメージ補正の計算を実装する #calc_flow.md (l120)
        )
        if context.move.power is None:
            return CalculateResult(
                damage_range=(0, 0),
                damage_list=[],
                critical_damage_range=(0, 0),
                critical_damage_list=[],
                meta_data={},
            )
        return CalculateResult(
            damage_range=(0, 0),
            damage_list=[],
            critical_damage_range=(0, 0),
            critical_damage_list=[],
            meta_data={},
        )

    @classmethod
    def calc_modified_attack_stat(cls, context: CalculateContext) -> int:
        """攻撃側のステータスを補正するメソッド。

        Args:
            context (CalculateContext): 計算のコンテキスト。

        Returns:
            int: 補正後の攻撃側のステータス。
        """
        move_calc_stat_type = cls._move_calc_stat_type(context)
        attack_stat = context.attacker.real_stats[move_calc_stat_type]
        # ここに攻撃側のステータス補正の計算ロジックを実装する
        return attack_stat

    @classmethod
    def calc_modified_difend_stat(cls, context: CalculateContext) -> int:
        """防御側のステータスを補正するメソッド。

        Args:
            context (calculateContext): 計算のコンテキスト。
        
        Returns:
            int: 補正後の防御側のステータス。
        """
        move_cald_state_type = cls._move_calc_stat_type(context)
        if move_cald_state_type == pokemon_enums.Stats.ATTACK:
            difend_stat = context.defender.real_stats[pokemon_enums.Stats.DEFENSE]
        else:
            difend_stat = context.defender.real_stats[pokemon_enums.Stats.SPECIAL_DEFENSE]
        return difend_stat



    @classmethod
    def _move_calc_stat_type(cls, context: CalculateContext) -> pokemon_enums.Stats:
        """技の計算に使用するステータスを決定するメソッド。

        Args:
            context (CalculateContext): 計算のコンテキスト。

        Returns:
            pokemon_enums.Stats: 計算に使用するステータス。
        """
        if context.move.damage_class_id == move_enums.MoveDamageClass.PHYSICAL:
            return pokemon_enums.Stats.ATTACK
        else:
            return pokemon_enums.Stats.SPECIAL_ATTACK


class PowerCalculator:
    """技の威力を計算するクラス。"""

    @classmethod
    def _power_modifier_calculate(cls, context: CalculateContext) -> float:
        """技の威力補正を計算するメソッド。

        Args:
            context (CalculateContext): 計算のコンテキスト。

        Returns:
            float: 技の威力補正値。
        """
        # ここに威力補正の計算ロジックを実装する
        field_modifier = cls._calc_field_modifier(context)
        return 4096

    @classmethod
    def _calc_field_modifier(cls, context: CalculateContext) -> float:
        """フィールド補正を計算するメソッド。

        Args:
            context (CalculateContext): 計算のコンテキスト。

        Returns:
            float: フィールド補正値。
        """
        # ここにフィールド補正の計算ロジックを実装する
        return 4096

    @classmethod
    def calc_modified_power(cls, context: CalculateContext) -> int:
        """技の威力を補正するメソッド。

        Args:
            context (CalculateContext): 計算のコンテキスト。

        Returns:
            int: 補正後の技の威力。
        """
        if context.move.power is None:
            return 0
        power_modifier = cls._power_modifier_calculate(context)
        finaly_power = rounding_half_down(
            cls.calc_move_base_power(context) * power_modifier / 4096
        )
        return finaly_power

    @classmethod
    def calc_move_base_power(cls, context: CalculateContext) -> int:
        """特定の技の威力を計算するメソッド。"""
        if context.move.power is None:
            return 0
        if context.move.id == 360:
            return cls._calc_gyro_ball_power(context)
        if context.move.id == 486:
            return cls._calc_electro_ball_power(context)
        if context.move.id in (323, 284):
            return cls._calc_hp_depended_power(context)
        if context.move.id in (179, 175):
            return cls._calc_hp_reversal_power(context)
        if context.move.id in (447, 67):
            return cls._calc_weight_depended_power(context)
        return context.move.power

    @classmethod
    def _calc_gyro_ball_power(cls, context: CalculateContext) -> int:
        """ジャイロボールの威力を計算するメソッド。"""
        attacker_speed = context.attacker.real_stats[pokemon_enums.Stats.SPEED]
        defender_speed = context.defender.real_stats[pokemon_enums.Stats.SPEED]
        if attacker_speed <= 0:
            return 150
        return min(150, 25 * defender_speed // attacker_speed + 1)

    @classmethod
    def _calc_electro_ball_power(cls, context: CalculateContext) -> int:
        """エレキボールの威力を計算するメソッド。"""
        attacker_speed = context.attacker.real_stats[pokemon_enums.Stats.SPEED]
        defender_speed = context.defender.real_stats[pokemon_enums.Stats.SPEED]
        if defender_speed <= 0:
            return 150
        speed_ratio = attacker_speed // defender_speed
        return min(150, 30 * speed_ratio + 10 * abs(speed_ratio - 2) + 20)

    @classmethod
    def _calc_hp_depended_power(cls, context: CalculateContext) -> int:
        """しおふき・ふんかの威力を計算するメソッド。"""
        defender = context.defender
        current_hp = getattr(defender, "current_hp", None)
        max_hp = defender.real_stats[pokemon_enums.Stats.HP]
        if current_hp is None:
            current_hp = getattr(
                getattr(defender, "built_data", None), "current_hp", max_hp
            )
        if max_hp <= 0:
            return 1
        return max(1, int(150 * current_hp / max_hp))

    @classmethod
    def _calc_hp_reversal_power(cls, context: CalculateContext) -> int:
        """きしかいせい・じたばたの威力を計算するメソッド。"""
        defender = context.defender
        max_hp = defender.real_stats[pokemon_enums.Stats.HP]
        current_hp = getattr(defender, "current_hp", None)
        if current_hp is None:
            current_hp = getattr(
                getattr(defender, "built_data", None), "current_hp", max_hp
            )
        if max_hp <= 0:
            return 20
        hp_ratio = current_hp / max_hp
        if hp_ratio < 1 / 48:
            return 200
        if hp_ratio < 1 / 12:
            return 150
        if hp_ratio < 9 / 48:
            return 100
        if hp_ratio < 16 / 48:
            return 80
        if hp_ratio < 31 / 48:
            return 40
        return 20

    @classmethod
    def _calc_weight_depended_power(cls, context: CalculateContext) -> int:
        """くさむすび・けたぐりの威力を計算するメソッド。"""
        weight = context.defender.master_data.weight
        if weight < 10:
            return 20
        if weight < 25:
            return 40
        if weight < 50:
            return 60
        if weight < 100:
            return 80
        if weight < 200:
            return 100
        return 120

    


def rounding_half_down(value: float) -> int:
    """半分を下に丸める。

    Args:
        value (float): 丸める値。

    Returns:
        int: 丸められた値。
    """
    return math.ceil(value - 0.5)
