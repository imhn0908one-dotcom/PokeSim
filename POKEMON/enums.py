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


class MoveAttribute(IntEnum):
    """Move attributes and flags (PokeAPI specification)"""

    __slots__ = ("description",)
    CONTACT = (1, "Makes contact with the target")
    CHARGE = (2, "Requires a turn to charge before attacking")
    RECHARGE = (3, "Requires a turn to recharge after attacking")
    PROTECT = (4, "Can be blocked by Protect and similar moves")
    REFLECTABLE = (5, "Can be bounced back by Magic Coat or Magic Bounce")
    SNATCH = (6, "Can be stolen by Snatch")
    MIRROR = (7, "Can be copied by Mirror Move")
    PUNCH = (8, "Punching move, boosted by Iron Fist")
    SOUND = (
        9,
        "Sound-based move, bypasses Substitute and blocked by Soundproof",
    )
    GRAVITY = (10, "Cannot be used during Gravity")
    DEFROST = (11, "Thaws the user upon execution if frozen")
    DISTANCE = (12, "Can target non-adjacent opponents in Triple Battles")
    HEAL = (13, "Healing move, blocked by Heal Block")
    AUTHENTIC = (14, "Bypasses Substitute")
    POWDER = (
        15,
        "Powder move, ineffective against Grass-types, Overcoat, or Safety Goggles",
    )
    BITE = (16, "Biting move, boosted by Strong Jaw")
    PULSE = (17, "Pulse move, boosted by Mega Launcher")
    BALLISTICS = (18, "Bullet or bomb move, blocked by Bulletproof")
    MENTAL = (19, "Mental move, affected by Mental Herb or Oblivious")
    NON_SKY_BATTLE = (20, "Cannot be used in Sky Battles")
    DANCE = (21, "Dance move, triggers Dancer")

    def __new__(cls, value: int, description: str):
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj.description = description
        return obj


class MoveTarget(IntEnum):
    """技の対象範囲（PokeAPI / データ定義準拠）"""

    # ★ これを入れることで 'description' 属性の追加エラーを防ぎます
    __slots__ = ("description",)

    SPECIFIC_MOVE = (
        1,
        (
            "One specific move. How this move is chosen depends upon on the"
            " move being used."
        ),
    )
    SELECTED_POKEMON_ME_FIRST = (
        2,
        (
            "One other Pokémon on the field, selected by the trainer. Stolen"
            " moves reuse the same target."
        ),
    )
    ALLY = (3, "The user’s ally (if any).")
    USERS_FIELD = (
        4,
        "The user’s side of the field. Affects the user and its ally (if any).",
    )
    USER_OR_ALLY = (5, "Either the user or its ally, selected by the trainer.")
    OPPONENTS_FIELD = (
        6,
        "The opposing side of the field. Affects opposing Pokémon.",
    )
    USER = (7, "The user.")
    RANDOM_OPPONENT = (8, "One opposing Pokémon, selected at random.")
    ALL_OTHER_POKEMON = (9, "Every other Pokémon on the field.")
    SELECTED_POKEMON = (
        10,
        "One other Pokémon on the field, selected by the trainer.",
    )
    ALL_OPPONENTS = (11, "All opposing Pokémon.")
    ENTIRE_FIELD = (12, "The entire field. Affects all Pokémon.")
    USER_AND_ALLIES = (13, "The user and its allies.")
    ALL_POKEMON = (14, "Every Pokémon on the field.")
    ALL_ALLIES = (15, "All of the user’s allies.")

    def __new__(cls, value: int, description: str):
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj.description = description
        return obj


class MoveMetaCategory(IntEnum):
    """技のメタカテゴリ（PokeAPI / データ定義準拠）"""

    __slots__ = ("description",)

    DAMAGE = (0, "Inflicts damage")
    AILMENT = (1, "No damage; inflicts status ailment")
    NET_GOOD_STATS = (
        2,
        "No damage; lowers target’s stats or raises user’s stats",
    )
    HEAL = (3, "No damage; heals the user")
    DAMAGE_AILMENT = (4, "Inflicts damage; inflicts status ailment")
    SWAGGER = (5, "No damage; inflicts status ailment; raises target’s stats")
    DAMAGE_LOWER = (6, "Inflicts damage; lowers target’s stats")
    DAMAGE_RAISE = (7, "Inflicts damage; raises user’s stats")
    DAMAGE_HEAL = (8, "Inflicts damage; absorbs damage done to heal the user")
    OHKO = (9, "One-hit KO")
    WHOLE_FIELD_EFFECT = (10, "Effect on the whole field")
    FIELD_EFFECT = (11, "Effect on one side of the field")
    FORCE_SWITCH = (12, "Forces target to switch out")
    UNIQUE = (13, "Unique effect")

    def __new__(cls, value: int, description: str):
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj.description = description
        return obj


class MoveMetaAilment(IntEnum):
    """技が付与する状態異常・特殊状態（PokeAPI / データ定義準拠）"""

    __slots__ = ("description",)

    UNKNOWN = (-1, "Unknown or unclassified status effect")
    NONE = (0, "No status ailment")
    PARALYSIS = (1, "Paralysis (reduces Speed and may prevent action)")
    SLEEP = (2, "Sleep (prevents action for a few turns)")
    FREEZE = (3, "Freeze (prevents action until thawed)")
    BURN = (
        4,
        ("Burn (reduces Physical Attack damage and deals damage each turn)"),
    )
    POISON = (5, "Poison (deals damage each turn)")
    CONFUSION = (6, "Confusion (may cause the Pokémon to damage itself)")
    INFATUATION = (
        7,
        ("Infatuation (50% chance to prevent action against opposite gender)"),
    )
    TRAP = (8, "Trapped (prevents switching out and deals damage each turn)")
    NIGHTMARE = (9, "Nightmare (deals damage each turn while sleeping)")
    TORMENT = (12, "Torment (prevents using the same move twice in a row)")
    DISABLE = (13, "Disable (prevents the target from using its last used move)")
    YAWN = (14, "Yawn (causes the target to fall asleep next turn)")
    HEAL_BLOCK = (15, "Heal Block (prevents HP recovery for several turns)")
    NO_TYPE_IMMUNITY = (
        17,
        "Ignores type immunities (e.g., Foresight or Odor Sleuth effect)",
    )
    LEECH_SEED = (
        18,
        "Leech Seed (drains HP each turn to heal the opponent)",
    )
    EMBARGO = (19, "Embargo (prevents the use of held items)")
    PERISH_SONG = (
        20,
        "Perish Song (causes affected Pokémon to faint in 3 turns)",
    )
    INGRAIN = (21, "Ingrain (restores HP each turn but prevents switching)")
    SILENCE = (
        24,
        "Silence / Throat Chop effect (prevents sound-based moves)",
    )
    TAR_SHOT = (
        42,
        "Tar Shot (lowers Speed and makes target weak to Fire moves)",
    )

    def __new__(cls, value: int, description: str):
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj.description = description
        return obj


class MoveDamageClass(IntEnum):
    """技の分類(物理、特殊、変化)（PokeAPI / データ定義準拠）"""

    __slots__ = ("description",)

    STATUS = (1, "Status move (no direct damage)")
    PHYSICAL = (2, "Physical move (uses Attack and Defense)")
    SPECIAL = (3, "Special move (uses Special Attack and Special Defense)")

    def __new__(cls, value: int, description: str):

        obj = int.__new__(cls, value)
        obj._value_ = value
        obj.description = description
        return obj
