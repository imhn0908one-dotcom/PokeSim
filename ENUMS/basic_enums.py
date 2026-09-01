from enum import IntEnum
from typing import Any, TypeAlias, TypedDict


class DescribedEnum(IntEnum):
    """Base class for enums with descriptions and optional Japanese names."""

    description: str
    jpname: str  # Japanese name of the enum value

    def __new__(cls, value: int, description: str, jpname: str = ""):
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj.description = description
        obj.jpname = jpname
        return obj


class TypeID(IntEnum):
    """ポケモンのタイプID（PokeAPI準拠 / 日本語説明付き）"""

    description: str
    NONE = (0, "なし")
    NORMAL = (1, "ノーマル")
    FIRE = (2, "ほのお")
    WATER = (3, "みず")
    GRASS = (4, "くさ")
    ELECTRIC = (5, "でんき")
    ICE = (6, "こおり")
    FIGHTING = (7, "かくとう")
    POISON = (8, "どく")
    GROUND = (9, "じめん")
    FLYING = (10, "ひこう")
    PSYCHIC = (11, "エスパー")
    BUG = (12, "むし")
    ROCK = (13, "いわ")
    GHOST = (14, "ゴースト")
    DRAGON = (15, "ドラゴン")
    DARK = (16, "あく")
    STEEL = (17, "はがね")
    FAIRY = (18, "フェアリー")

    def __new__(cls, value: int, description: str):
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj.description = description
        return obj


# 「TypeID 単体」または「数字(int)」
TypeArg: TypeAlias = TypeID | int


# 「TypeID または 数字(int)」が入った可変リスト
class Typeslist(list[TypeArg]):
    def __str__(self) -> str:
        return ", ".join(TypeID(type_id).name for type_id in self)


TYPE_CHART: list[list[float]] = [[]]


def convert_enum(enum_type, value):
    """Convert an enum member, value, or member name to an enum member."""
    if isinstance(value, enum_type):
        return value
    try:
        return enum_type(value)
    except (TypeError, ValueError):
        return enum_type[value]
