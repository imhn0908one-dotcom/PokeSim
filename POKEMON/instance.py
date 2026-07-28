from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List
from dataclasses import dataclass


class stats(Enum):
    """基本ステータスの種類"""

    HP = "HP"
    Atk = "Attack"
    Def = "Defense"
    SpA = "Special Attack"
    SpD = "Special Defense"
    Spe = "Speed"


class Condition(Enum):
    """状態異常の種類"""

    NONE = "なし"
    SLEEP = "ねむり"
    POISON = "どく"
    BAD_POISON = "もうどく"
    PARALYSIS = "まひ"
    BURN = "やけど"
    FROZEN = "こおり"


class VolatileCondition(Enum):
    """状態変化の種類、バトンタッチによって移動するか"""

    CONFUSION = ("こんらん", True)
    FLINCH = ("ひるみ", True)
    CURSE = ("のろい", True)
    CANT_ESCAPE = ("にげられない", True)
    LEECH_SEED = ("やどりぎのタネ", True)
    SUBSTITUTE = ("みがわり", True)
    THROAT_CHOP = ("じごくづき", True)
    SALT_CURE = ("しおづけ", True)
    AQUA_RING = ("アクアリング", True)
    INGRAIN = ("ねをはる", True)
    NO_ABILITY = ("いえきによって特性の効果が消えた", True)
    TAR_SHOT = ("タールショット", True)
    SMACK_DOWN = ("うちおとす", True)
    FLASH_FIRE = ("もらいび", True)
    DESTINY_BOND = ("みちづれ", True)
    GRUDGE = ("おんねん", True)
    UPROAR = ("さわぐ", True)
    STOCKPILE = ("たくわえる", True)

    TRANSFORM = ("へんしん", False)
    TORMENT = ("いちゃもん", False)
    IMPRISON = ("ふういん", False)
    ATTRACT = ("めろめろ", False)
    DROWSY = ("ねむけ", False)
    BOUND = ("バインド", False)
    DEFENCE_CURL = ("まるくなる", False)


@dataclass(slots=True)
class VolatileInstance:
    """基本状態異常クラス
    TODO: if volatile have Special function, overload this dataclass
    """

    Volatile_stat: VolatileCondition
    turn: int = field(metadata={"description": "-1 は無制限"})

    def __str__(self):
        return f"{self.Volatile_stat.name}"


# =======================================================
# 特殊状態異常の子クラス
# =======================================================
#@dataclass
class SubstituteEffect(VolatileInstance):
    """身代わり用。hp要素をふくむ。"""

    Volatile_stat: VolatileCondition = VolatileCondition.SUBSTITUTE
    hp: int = 0



# =======================================================
# ポケモンインスタンスのデータクラス
# =======================================================


@dataclass(slots=True)
class PokemonInstance:
    id: int = field(metadata={"description": "pokemon ID"})
    name: str = field(metadata={"description": "pokemon name"})
    level: int = field(default=50, metadata={"description": "pokemon level"})
    types: List[str] = field(
        default_factory=list, metadata={"description": "length 1~4"}
    )

    base_stats: Dict[stats, int] = field(
        metadata={"description": "種族値"},
        default_factory=lambda: {
            stats.HP: 0,
            stats.Atk: 0,
            stats.Def: 0,
            stats.Spe: 0,
            stats.SpA: 0,
            stats.SpD: 0,
        },
    )
    evs: Dict[stats, int] = field(
        metadata={"description": "努力値"},
        default_factory=lambda: {
            stats.HP: 0,
            stats.Atk: 0,
            stats.Def: 0,
            stats.Spe: 0,
            stats.SpA: 0,
            stats.SpD: 0,
        },
    )
    rank: Dict[stats | str, int] = field(
        metadata={"description": "ランク"},
        default_factory=lambda: {
            stats.Atk: 0,
            stats.Def: 0,
            stats.Spe: 0,
            stats.SpA: 0,
            stats.SpD: 0,
            "Accuracy_rate": 0,
            "Evasion_rate": 0,
        },
    )
    gender_Id: int = 0
    nature_Id: int = 0
    stat_change: Dict[str, float] = field(
        default_factory=dict,
        metadata={"description": "性格によるステート変化, float = 0.9 or 1.1"},
    )
    item_Id: int = 0

    # moves
    learnt_move_ids: List[int] = field(default_factory=list)
    selected_move_ids: List[int] = field(default_factory=lambda: [0, 0, 0, 0])
    # Conditions
    condition: Condition = Condition.NONE

    def calculate_real_stat(self, stat_name: str) -> int:
        """目的ステータス名を引数に実数値を返す
            ランク変化も考慮
        Args:
            stat_name (str): 目的ステータス名

        Returns:
            int: 実数値
        """
        if stat_name == "HP":
            return self.base_stats[stats.HP]
        else:
            return self.base_stats[stats[stat_name]]

    def reset_ranks(self) -> None:
        """交代時や戦闘終了時にランクをすべて0に戻す"""
        for key in self.rank:
            self.rank[key] = 0

    def set_move(self, slot_index: int, move_id: int) -> None:
        """技スロット（0〜3）に技をセットする"""
        if 0 <= slot_index < 4:
            if move_id in self.learnt_move_ids:
                self.selected_move_ids[slot_index] = move_id

    def to_dict(self) -> dict:
        """JSON化や保存用にデータクラスを辞書化する"""
        import dataclasses

        return dataclasses.asdict(self)
