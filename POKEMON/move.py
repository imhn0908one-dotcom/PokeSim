from dataclasses import dataclass, field
from multiprocessing import current_process
from typing import Optional

from POKEMON import enums


@dataclass(slots=True, frozen=True)
class MasterMove:
    """技のマスターデータ（IDベース・Enum連携型）"""

    # --- 基本情報 ---
    id: int
    name: str
    jpname: str
    type_id: enums.TypeID
    damage_class_id: enums.MoveDamageClass
    pp: int  # e.g., 15
    power: Optional[int]  # e.g., None
    accuracy: Optional[int]  # e.g., 100

    # --- メタ情報 & 状態異常 ---
    target_id: enums.MoveTarget
    category_id: enums.MoveMetaCategory
    ailment_id: enums.MoveMetaAilment
    ailment_chance: int
    crit_rate: int
    healing: int
    drain: int
    flinch_chance: int

    # --- ターン・ヒット数 ---
    min_hits: Optional[int] = None
    max_hits: Optional[int] = None
    min_turns: Optional[int] = None
    max_turns: Optional[int] = None

    # --- 能力変化 ---
    stat_changes_stat: Optional[dict[enums.Stats, int]] = None
    stat_chance: int = 0

    # --- エフェクト関連 ---
    effect_chance: Optional[int] = None
    effect_id: int = 0
    effect: str = ""


@dataclass(slots=True, frozen=True)
class BattleMove:
    MasterMove: MasterMove
    current_pp: int
