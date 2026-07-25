from dataclasses import dataclass, field
from enum import Enum, auto
from pickle import NONE
from typing import Dict, List

from flask.cli import F


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
    """状態変化の種類"""

    NONE = "なし"
    CONFUSION = "こんらん"
    FLINCH = "ひるみ"
    ATTRACT = "めろめろ"
    DROWSY = "ねむけ"
    BOUND = "バインド"
    CURSE = "のろい"
    CANT_ESCAPE = "にげられない"
    LEECH_SEED = "やどりぎのタネ"
    SUBSTITUTE = "みがわり"
    TORMENT = "いちゃもん"
    IMPRISON = "ふういん"
    THROAT_CHOP = "じごくづき"
    SALT_CURE = "しおづけ"
    AQUA_RING = "アクアリング"
    INGRAIN = "ねをはる"
    NO_ABILITY = "いえきによって特性の効果が消えた"
    TAR_SHOT = "タールショット"
    SMACK_DOWN = "うちおとす"
    FLASH_FIRE = "もらいび"
    DESTINY_BOND = "みちづれ"
    GRUDGE = "おんねん"
    TRANSFORM = "へんしん"
    UPROAR = "さわぐ"
    STOCKPILE = "たくわえる"


@dataclass(slots=True)
class PokemonInstance:
    id: int = field(metadata={"description": "pokemon ID"})  # pokemon ID
    name: str = field(metadata={"description": "pokemon name"})
    level: int
    types: List[str] = field(
        default_factory=list, metadata={"description": "length 1~4"}
    )
    base_stats: Dict[str, int] = field(
        metadata={"description": "種族値"},
        default_factory=lambda: {
            "HP": 0,
            "Atk": 0,
            "Def": 0,
            "SpA": 0,
            "SpD": 0,
            "Spe": 0,
        },
    )
    evs: Dict[str, int] = field(
        metadata={"description": "努力値"},
        default_factory=lambda: {
            "HP": 0,
            "Atk": 0,
            "Def": 0,
            "SpA": 0,
            "SpD": 0,
            "Spe": 0,
        },
    )
    rank: Dict[str, int] = field(
        metadata={"description": "ランク"},
        default_factory=lambda: {
            "Atk": 0,
            "Def": 0,
            "SpA": 0,
            "SpD": 0,
            "Spe": 0,
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

    def calculate_real_stat(self, stat_name: str) -> int:
        """目的ステータス名を引数に実数値を返す
            ランク変化も考慮
        Args:
            stat_name (str): 目的ステータス名

        Returns:
            int: 実数値
        """
        if stat_name == "HP":
            return self.base_stats["HP"]
        else:
            return self.base_stats[stat_name]

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
