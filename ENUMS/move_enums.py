from .basic_enums import DescribedEnum


class MoveAttribute(DescribedEnum):
    """Move attributes and flags (PokeAPI specification)"""

    # Description of the attribute
    CONTACT = (1, "Makes contact with the target", "CONTACT")
    CHARGE = (2, "Requires a turn to charge before attacking", "CHARGE")
    RECHARGE = (3, "Requires a turn to recharge after attacking", "RECHARGE")
    PROTECT = (4, "Can be blocked by Protect and similar moves", "PROTECT")
    REFLECTABLE = (
        5,
        "Can be bounced back by Magic Coat or Magic Bounce",
        "REFLECTABLE",
    )
    SNATCH = (6, "Can be stolen by Snatch", "SNATCH")
    MIRROR = (7, "Can be copied by Mirror Move", "MIRROR")
    PUNCH = (8, "Punching move, boosted by Iron Fist", "PUNCH")
    SOUND = (
        9,
        "Sound-based move, bypasses Substitute and blocked by Soundproof",
        "SOUND",
    )
    GRAVITY = (10, "Cannot be used during Gravity", "GRAVITY")
    DEFROST = (11, "Thaws the user upon execution if frozen", "DEFROST")
    DISTANCE = (12, "Can target non-adjacent opponents in Triple Battles", "DISTANCE")
    HEAL = (13, "Healing move, blocked by Heal Block", "HEAL")
    AUTHENTIC = (14, "Bypasses Substitute", "AUTHENTIC")
    POWDER = (
        15,
        "Powder move, ineffective against Grass-types, Overcoat, or Safety Goggles",
        "POWDER",
    )
    BITE = (16, "Biting move, boosted by Strong Jaw", "BITE")
    PULSE = (17, "Pulse move, boosted by Mega Launcher", "PULSE")
    BALLISTICS = (18, "Bullet or bomb move, blocked by Bulletproof", "BALLISTICS")
    MENTAL = (19, "Mental move, affected by Mental Herb or Oblivious", "MENTAL")
    NON_SKY_BATTLE = (20, "Cannot be used in Sky Battles", "NON_SKY_BATTLE")
    DANCE = (21, "Dance move, triggers Dancer", "DANCE")


class MoveTarget(DescribedEnum):
    """技の対象範囲（PokeAPI / データ定義準拠）"""

    description: str
    jpname: str  # Japanese name of the enum value

    SPECIFIC_MOVE = (
        1,
        (
            "One specific move. How this move is chosen depends upon on the"
            " move being used."
        ),
        "SPECIFIC_MOVE",
    )
    SELECTED_POKEMON_ME_FIRST = (
        2,
        "One other Pokémon on the field, selected by the trainer. Stolen moves reuse the same target.",
        "SELECTED_POKEMON_ME_FIRST",
    )
    ALLY = (3, "The user’s ally (if any).", "ALLY")
    USERS_FIELD = (
        4,
        "The user’s side of the field. Affects the user and its ally (if any).",
        "USERS_FIELD",
    )
    USER_OR_ALLY = (
        5,
        "Either the user or its ally, selected by the trainer.",
        "USER_OR_ALLY",
    )
    OPPONENTS_FIELD = (
        6,
        "The opposing side of the field. Affects opposing Pokémon.",
        "OPPONENTS_FIELD",
    )
    USER = (7, "The user.", "USER")
    RANDOM_OPPONENT = (
        8,
        "One opposing Pokémon, selected at random.",
        "RANDOM_OPPONENT",
    )
    ALL_OTHER_POKEMON = (9, "Every other Pokémon on the field.", "ALL_OTHER_POKEMON")
    SELECTED_POKEMON = (
        10,
        "One other Pokémon on the field, selected by the trainer.",
        "SELECTED_POKEMON",
    )
    ALL_OPPONENTS = (11, "All opposing Pokémon.", "ALL_OPPONENTS")
    ENTIRE_FIELD = (12, "The entire field. Affects all Pokémon.", "ENTIRE_FIELD")
    USER_AND_ALLIES = (13, "The user and its allies.", "USER_AND_ALLIES")
    ALL_POKEMON = (14, "Every Pokémon on the field.", "ALL_POKEMON")
    ALL_ALLIES = (15, "All of the user’s allies.", "ALL_ALLIES")


class MoveMetaCategory(DescribedEnum):
    """技のメタカテゴリ（PokeAPI / データ定義準拠）"""

    description: str
    DAMAGE = (0, "Inflicts damage", "DAMAGE")
    AILMENT = (1, "No damage; inflicts status ailment", "AILMENT")
    NET_GOOD_STATS = (
        2,
        "No damage; lowers target’s stats or raises user’s stats",
        "NET_GOOD_STATS",
    )
    HEAL = (3, "No damage; heals the user", "HEAL")
    DAMAGE_AILMENT = (4, "Inflicts damage; inflicts status ailment", "DAMAGE_AILMENT")
    SWAGGER = (
        5,
        "No damage; inflicts status ailment; raises target’s stats",
        "SWAGGER",
    )
    DAMAGE_LOWER = (6, "Inflicts damage; lowers target’s stats", "DAMAGE_LOWER")
    DAMAGE_RAISE = (7, "Inflicts damage; raises user’s stats", "DAMAGE_RAISE")
    DAMAGE_HEAL = (
        8,
        "Inflicts damage; absorbs damage done to heal the user",
        "DAMAGE_HEAL",
    )
    OHKO = (9, "One-hit KO", "OHKO")
    WHOLE_FIELD_EFFECT = (10, "Effect on the whole field", "WHOLE_FIELD_EFFECT")
    FIELD_EFFECT = (11, "Effect on one side of the field", "FIELD_EFFECT")
    FORCE_SWITCH = (12, "Forces target to switch out", "FORCE_SWITCH")
    UNIQUE = (13, "Unique effect", "UNIQUE")


class MoveMetaAilment(DescribedEnum):
    """技が付与する状態異常・特殊状態（PokeAPI / データ定義準拠）"""

    description: str
    UNKNOWN = (-1, "Unknown or unclassified status effect", "UNKNOWN")
    NONE = (0, "No status ailment", "NONE")
    PARALYSIS = (1, "Paralysis (reduces Speed and may prevent action)", "PARALYSIS")
    SLEEP = (2, "Sleep (prevents action for a few turns)", "SLEEP")
    FREEZE = (3, "Freeze (prevents action until thawed)", "FREEZE")
    BURN = (
        4,
        ("Burn (reduces Physical Attack damage and deals damage each turn)"),
        "BURN",
    )
    POISON = (5, "Poison (deals damage each turn)", "POISON")
    CONFUSION = (6, "Confusion (may cause the Pokémon to damage itself)", "CONFUSION")
    INFATUATION = (
        7,
        ("Infatuation (50% chance to prevent action against opposite gender)"),
        "INFATUATION",
    )
    TRAP = (8, "Trapped (prevents switching out and deals damage each turn)", "TRAP")
    NIGHTMARE = (9, "Nightmare (deals damage each turn while sleeping)", "NIGHTMARE")
    TORMENT = (12, "Torment (prevents using the same move twice in a row)", "TORMENT")
    DISABLE = (
        13,
        "Disable (prevents the target from using its last used move)",
        "DISABLE",
    )
    YAWN = (14, "Yawn (causes the target to fall asleep next turn)", "YAWN")
    HEAL_BLOCK = (
        15,
        "Heal Block (prevents HP recovery for several turns)",
        "HEAL_BLOCK",
    )
    NO_TYPE_IMMUNITY = (
        17,
        "Ignores type immunities (e.g., Foresight or Odor Sleuth effect)",
        "NO_TYPE_IMMUNITY",
    )
    LEECH_SEED = (
        18,
        "Leech Seed (drains HP each turn to heal the opponent)",
        "LEEF_SEED",
    )
    EMBARGO = (19, "Embargo (prevents the use of held items)", "EMBARGO")
    PERISH_SONG = (
        20,
        "Perish Song (causes affected Pokémon to faint in 3 turns)",
        "PERISH_SONG",
    )
    INGRAIN = (21, "Ingrain (restores HP each turn but prevents switching)", "INGRAIN")
    SILENCE = (
        24,
        "Silence / Throat Chop effect (prevents sound-based moves)",
        "SILENCE",
    )
    TAR_SHOT = (
        42,
        "Tar Shot (lowers Speed and makes target weak to Fire moves)",
        "TAR_SHOT",
    )


class MoveDamageClass(DescribedEnum):
    """技の分類(物理、特殊、変化)（PokeAPI / データ定義準拠）"""

    description: str
    STATUS = (1, "Status move (no direct damage)", "STATUS")
    PHYSICAL = (2, "Physical move (uses Attack and Defense)", "PHYSICAL")
    SPECIAL = (3, "Special move (uses Special Attack and Special Defense)", "SPECIAL")
