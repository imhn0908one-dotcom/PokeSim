from dataclasses import dataclass
from typing import Any


@dataclass
class CalculateResult:
    """計算結果を管理するクラス。"""

    damage_range: tuple[int, int]
    """ダメージの範囲を表すタプル。最小ダメージと最大ダメージを含む。"""
    damage_list: list[int]
    """ダメージのリスト。各ダメージ値を含む。"""
    critical_damage_range: tuple[int, int]
    """クリティカルヒット時のダメージの範囲を表すタプル。最小ダメージと最大ダメージを含む。"""
    critical_damage_list: list[int]
    """クリティカルヒット時のダメージのリスト。各ダメージ値を含む。"""
    meta_data: dict[str, Any]
    """計算に関連するメタデータを格納する辞書。"""

    def __str__(self):
        return (
            f"CalculateResult(damage_range={self.damage_range}, "
            f"damage_list={self.damage_list}, "
            f"critical_damage_range={self.critical_damage_range}, "
            f"critical_damage_list={self.critical_damage_list}, "
            f"meta_data={self.meta_data})"
        )
