import threading
from dataclasses import dataclass, field
from re import M
from typing import Dict, List


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
    stat_change: Dict[str, int] = field(
        default_factory=dict,
        metadata={"description": "性格によるステート変化, int = 0.9 or 1.1"},
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
