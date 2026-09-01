from enum import IntEnum

from traitlets import default


class FieldStateEnum(IntEnum):
    """"""

    jpname: str
    default_turn: int
    description: str

    def __new__(cls, value: int, description: str, jpname: str, default_turn: int):
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj.description = description
        obj.jpname = jpname
        obj.default_turn = default_turn
        return obj


class Terrain(FieldStateEnum):
    """フィールドの種類（PokeAPI / データ定義準拠）"""

    NONE = (0, "なし", "なし", 0)
    ELECTRIC = (1, "エレキフィールド", "エレキフィールド", 5)
    GRASSY = (2, "グラスフィールド", "グラスフィールド", 5)
    MISTY = (3, "ミストフィールド", "ミストフィールド", 5)
    PSYCHIC = (4, "サイコフィールド", "サイコフィールド", 5)


class Weather(FieldStateEnum):
    """天候の種類（PokeAPI / データ定義準拠）"""

    description: str
    NONE = (0, "なし", "なし", 0)
    SUNNY = (1, "はれ", "はれ", 5)
    RAINY = (2, "あめ", "あめ", 5)
    SANDSTORM = (3, "すなあらし", "すなあらし", 5)
    SNOW = (4, "ゆき", "ゆき", 5)


class Room(FieldStateEnum):
    """バトルルームの種類（PokeAPI / データ定義準拠）"""

    description: str
    NONE = (0, "なし", "なし", 0)
    TRICK_ROOM = (1, "トリックルーム", "トリックルーム", 5)
    MAGIC_ROOM = (2, "マジックルーム", "マジックルーム", 5)
    WONDER_ROOM = (3, "ワンダールーム", "ワンダールーム", 5)


class Screen(FieldStateEnum):
    """スクリーンの種類（PokeAPI / データ定義準拠）"""

    description: str
    NONE = (0, "なし", "なし", 0)
    LIGHT_SCREEN = (1, "ひかりのかべ", "ひかりのかべ", 5)
    REFLECT = (2, "リフレクター", "リフレクター", 5)
    AURORA_VEIL = (3, "オーロラベール", "オーロラベール", 5)


class Combination(FieldStateEnum):
    """技の組み合わせの種類（PokeAPI / データ定義準拠）"""

    description: str
    INFERNO = (1, "ひのうみ", "ひのうみ", 5)
    RAINBOW = (2, "にじ", "にじ", 5)
    WETLAND = (3, "しつげん", "しつげん", 5)


class Obstacle(FieldStateEnum):
    """障害物の種類（PokeAPI / データ定義準拠）"""

    description: str
    NONE = (0, "なし", "なし", 0)
    SPIKES = (1, "まきびし", "まきびし", 5)
    TOXIC_SPIKES = (2, "どくびし", "どくびし", 5)
    STEALTH_ROCK = (3, "ステルスロック", "ステルスロック", 5)
    STICKY_WEB = (4, "ねばねばネット", "ねばねばネット", 5)


class OtherEffect(FieldStateEnum):
    """その他の効果の種類（PokeAPI / データ定義準拠）"""

    description: str
    NONE = (0, "なし", "なし", 0)
    GRAVITY = (1, "じゅうりょく", "じゅうりょく", 5)
    FAIRY_LOCK = (2, "フェアリーロック", "フェアリーロック", 2)
    PLASMA_SHOWER = (3, "プラズマシャワー", "プラズマシャワー", 1)
