from enum import IntEnum
from typing import TypeAlias

from .basic_enums import DescribedEnum


class Genders(IntEnum):
    MALE = 0
    FEMALE = 1
    GENDERLESS = 2
    BOTH = 3


class Stats(IntEnum):
    """基本ステータスの種類"""

    HP = 1
    ATTACK = 2
    DEFENSE = 3
    SPECIAL_ATTACK = 4
    SPECIAL_DEFENSE = 5
    SPEED = 6


Statslist: TypeAlias = dict[Stats, int]  # Statsをキー、intを値とする辞書型のエイリアス


class Acc_Eva(IntEnum):
    """命中・回避ランクの種類"""

    ACCURACY = 1
    EVASION = 2


Acc_Eva_rank: TypeAlias = dict[Acc_Eva, int]


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


class Condition(DescribedEnum):
    """状態異常の種類"""

    description: str
    NONE = (0, "なし", "NONE")
    SLEEP = (1, "ねむり", "SLEEP")
    POISON = (2, "どく", "POISON")
    BAD_POISON = (3, "もうどく", "BAD_POISON")
    PARALYSIS = (4, "まひ", "PARALYSIS")
    BURN = (5, "やけど", "BURN")
    FROZEN = (6, "こおり", "FROZEN")
