import math

from CALC.calculate_context import CalculateContext
from CALC.calculate_manager import CalculateResult
from ENUMS import basic_enums, move_enums, pokemon_enums


class DamageCalculater:
    """ダメージ計算を行うクラス。"""

    @classmethod
    def damage_calculate(cls, context: CalculateContext) -> CalculateResult:
        """ダメージ計算を行うメソッド。

        Args:
            context (CalculateContext): 計算のコンテキスト。

        Returns:
            CalculateResult: 計算結果を格納したオブジェクト。
        """
        if context.move.power is None:
            return CalculateResult(
                damage_range=(0, 0),
                damage_list=[],
                critical_damage_range=(0, 0),
                critical_damage_list=[],
                meta_data={},
            )

        modified_attack_stat = cls.calc_modified_attack_stat(context)
        atl = context.attacker.built_data.level
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
        finaly_power = rounding_half_down(context.move.power * power_modifier / 4096)
        return finaly_power


def rounding_half_down(value: float) -> int:
    """半分を下に丸める。

    Args:
        value (float): 丸める値。

    Returns:
        int: 丸められた値。
    """
    return math.ceil(value - 0.5)
