import re
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Callable, Dict, Optional

from ENUMS import basic_enums, field_enums, move_enums, pokemon_enums

if TYPE_CHECKING:
    from CALC.calculate_context import CalculateContext
# 2. 補正関数の自動登録用レジストリとデコレータ
POWER_MODIFIERS: Dict[str, Callable[[CalculateContext], float]] = {}
DAMAGE_MODIFIERS: Dict[str, Callable[[CalculateContext], float]] = {}


def register_power(name: str):
    """威力補正関数を登録するデコレータ"""

    def decorator(func: Callable[[CalculateContext], float]):
        POWER_MODIFIERS[name] = func
        return func

    return decorator


def register_damage(name: str):
    """ダメージ補正関数を登録するデコレータ"""

    def decorator(func: Callable[[CalculateContext], float]):
        DAMAGE_MODIFIERS[name] = func
        return func

    return decorator


# ---------------------------------------------------------
# 3. 特性計算ロジックの定義（デコレータで自動登録）
# ---------------------------------------------------------


@register_power("technician")
def calc_technician(ctx: CalculateContext) -> float:
    if ctx.move.power is None:
        return 1.0
    return 6144 / 4096 if ctx.move.power <= 60 else 4096 / 4096


@register_power("rivalry")
def calc_rivalry(ctx: CalculateContext) -> float:
    if _gender_much(ctx) is None:
        return 1.0
    return 5120 / 4096 if _gender_much(ctx) else 3072 / 4096


@register_power("pixilate")
def calc_pixilate(ctx: CalculateContext) -> float:
    if ctx.move.type_id == basic_enums.TypeID.NORMAL:
        return 4915 / 4096
    return 4096 / 4096


@register_power("refrigerate")
def calc_refrigerate(ctx: CalculateContext) -> float:
    if ctx.move.type_id == basic_enums.TypeID.NORMAL:
        return 4915 / 4096
    return 4096 / 4096


@register_power("reckless")
def calc_reckless(ctx: CalculateContext) -> float:
    if ctx.move.drain < 0:
        return 4915 / 4096
    return 4096 / 4096


@register_power("iron_fist")
def calc_iron_fist(ctx: CalculateContext) -> float:
    if move_enums.MoveAttribute.PUNCH in ctx.move.attribute_ids:
        return 4915 / 4096
    return 4096 / 4096


@register_power("sand_force")
def calc_sand_force(ctx: CalculateContext) -> float:
    if ctx.battlefield.weather is field_enums.Weather.SANDSTORM:
        if ctx.move.type_id in (
            basic_enums.TypeID.ROCK,
            basic_enums.TypeID.GROUND,
            basic_enums.TypeID.STEEL,
        ):
            return 5235 / 4096
    return 4096 / 4096


@register_power("tough_claws")
def calc_tough_claws(ctx: CalculateContext) -> float:
    if move_enums.MoveAttribute.CONTACT in ctx.move.attribute_ids:
        return 5235 / 4096
    return 4096 / 4096


def _gender_much(context: CalculateContext) -> bool | None:
    """性別の一致を判定するメソッド。

    Args:
        context (CalculateContext): 計算のコンテキスト。

    Returns:
        bool|None: 性別が一致する場合は True、そうでない場合は False。不明な場合は None。
    """
    attacker_gender = context.attacker.built_data.gender
    defender_gender = context.defender.built_data.gender
    if attacker_gender is None or defender_gender is None:
        return None
    return attacker_gender == defender_gender


# ---------------------------------------------------------
# 4. Ability クラス本体
# ---------------------------------------------------------


class Ability:
    def __init__(
        self,
        ability_id: int,
        name: str,
        jpname: str,
        short_effect: str,
        effect: str,
        power_modifier: Optional[Callable[[CalculateContext], float]] = None,
        damage_modifier: Optional[Callable[[CalculateContext], float]] = None,
    ):
        self.id = ability_id
        self.name = name
        self.jpname = jpname
        self.short_effect = short_effect
        self.effect = effect
        self.power_modifier = power_modifier
        self.damage_modifier = damage_modifier

    @classmethod
    def from_dict(cls, key_id: str, data: Dict[str, Any]) -> "Ability":
        """JSONなどの辞書データから自動で補正関数を紐付けてインスタンス化"""
        eng_name = data["name"]
        return cls(
            ability_id=int(key_id),
            name=eng_name,
            jpname=data.get("jpname", ""),
            short_effect=data.get("short_effect", ""),
            effect=data.get("effect", ""),
            power_modifier=POWER_MODIFIERS.get(eng_name),
            damage_modifier=DAMAGE_MODIFIERS.get(eng_name),
        )

    def get_power_mod(self, ctx: CalculateContext) -> float:
        """威力補正を計算（補正関数が未定義の場合は1.0倍）"""
        if self.power_modifier:
            return self.power_modifier(ctx)
        return 1.0

    def get_damage_mod(self, ctx: CalculateContext) -> float:
        """最終ダメージ補正を計算（補正関数が未定義の場合は1.0倍）"""
        if self.damage_modifier:
            return self.damage_modifier(ctx)
        return 1.0

    def __repr__(self) -> str:
        return f"<Ability id={self.id} name='{self.jpname} ({self.name})'>"


# ---------------------------------------------------------
# 5. 実際の使用例
# ---------------------------------------------------------

# JSONデータ（サンプル）
json_data = {
    "100": {
        "name": "technician",
        "jpname": "テクニシャン",
        "short_effect": "Powers up weak moves.",
        "effect": "...",
    },
    "1": {
        "name": "stench",
        "jpname": "あくしゅう",
        "short_effect": "Has a 10% chance...",
        "effect": "...",
    },
}

# Ability インスタンスの生成
