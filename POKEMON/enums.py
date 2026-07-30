from enum import IntEnum
from typing import Literal, TypeAlias


class TypeID(IntEnum):
    NONE = 0
    NORMAL = 1
    FIRE = 2
    WATER = 3
    GRASS = 4
    ELECTRIC = 5
    ICE = 6
    FIGHTING = 7
    POISON = 8
    GROUND = 9
    FLYING = 10
    PSYCHIC = 11
    BUG = 12
    ROCK = 13
    GHOST = 14
    DRAGON = 15
    DARK = 16
    STEEL = 17
    FAIRY = 18


# 「TypeID 単体」または「数字(int)」
TypeArg: TypeAlias = TypeID | int

# 「TypeID または 数字(int)」が入った可変リスト
Typeslist: TypeAlias = list[TypeArg]

TYPE_CHART: list[list[float]] = [[]]


class Genders(IntEnum):
    MALE = 0
    FEMALE = 1
    GENDERLESS = 2
    BOTH = 3


class Stats(IntEnum):
    """基本ステータスの種類"""

    HP = 1
    Atk = 2
    Def = 3
    SpA = 4
    SpD = 5
    Spe = 6


class Natures(IntEnum):
    Hardy = 1
    Bold = 2
    Modest = 3
    Calm = 4
    Timid = 5
    Lonely = 6
    Docile = 7
    Mild = 8
    Gentle = 9
    Hasty = 10
    Adamant = 11
    Impish = 12
    Bashful = 13
    Careful = 14
    Rash = 15
    Jolly = 16
    Naughty = 17
    Lax = 18
    Quirky = 19
    Naive = 20
    Brave = 21
    Relaxed = 22
    Quiet = 23
    Sassy = 24
    Serious = 25
