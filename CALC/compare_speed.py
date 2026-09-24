from .calculate_context import CalculateContext, CalculateResult


class SpeedCalculator:
    """素早さ計算を行うクラス。"""

    @staticmethod
    def calculate_speed(context: CalculateContext) -> float:
        """素早さを計算するメソッド。"""
        base_speed = context.attacker_speed
        speed_modifier = 1.0

        # 特性による補正を適用
        if context.attacker.ability and context.attacker.ability.speed_modifier:
            speed_modifier *= context.attacker.ability.speed_modifier(context)

        return base_speed * speed_modifier
