from calendar import c
from dataclasses import dataclass, field
from multiprocessing import current_process
from typing import Optional

from ENUMS import basic_enums, field_enums, move_enums, pokemon_enums
from REPOSITORY.move_repository import MoveRepository


@dataclass(slots=True, frozen=True)
class MasterMove:
    """技のマスターデータ（IDベース・Enum連携型）"""

    # --- 基本情報 ---
    id: int
    name: str
    jpname: str
    type_id: basic_enums.TypeID
    damage_class_id: move_enums.MoveDamageClass
    pp: int  # e.g., 15
    power: Optional[int]  # e.g., None
    accuracy: Optional[int]  # e.g., 100

    # --- メタ情報 & 状態異常 ---
    target_id: move_enums.MoveTarget
    category_id: move_enums.MoveMetaCategory
    ailment_id: move_enums.MoveMetaAilment
    attribute_ids: list[int]
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
    stat_changes_stat: Optional[dict[pokemon_enums.Stats, int]] = None
    stat_chance: int = 0

    # --- エフェクト関連 ---
    effect_chance: Optional[int] = None
    effect_id: int = 0
    effect: str = ""

    @classmethod
    def _create_from_dict(cls, data: dict) -> "MasterMove":
        """辞書データから MasterMove インスタンスを生成する。

        Args:
            data: JSON 形式の技データを表す辞書。
        Returns:
            MasterMove インスタンス。
        """
        stat_changes_stat = None
        if "stat_changes_stat" in data and data["stat_changes_stat"] is not None:
            stat_changes_stat = {
                basic_enums.convert_enum(pokemon_enums.Stats, stat): int(value)
                for stat, value in data["stat_changes_stat"].items()
            }

        return cls(
            id=int(data["id"]),
            name=data["name"],
            jpname=data["jpname"],
            type_id=basic_enums.convert_enum(basic_enums.TypeID, data["type_id"]),
            damage_class_id=basic_enums.convert_enum(
                move_enums.MoveDamageClass, data["damage_class_id"]
            ),
            pp=int(data["pp"]),
            power=int(data["power"]) if data.get("power") is not None else None,
            accuracy=int(data["accuracy"])
            if data.get("accuracy") is not None
            else None,
            target_id=basic_enums.convert_enum(
                move_enums.MoveTarget, data["target_id"]
            ),
            category_id=basic_enums.convert_enum(
                move_enums.MoveMetaCategory, data["category_id"]
            ),
            ailment_id=basic_enums.convert_enum(
                move_enums.MoveMetaAilment, data["ailment_id"]
            ),
            ailment_chance=int(data.get("ailment_chance", 0)),
            crit_rate=int(data.get("crit_rate", 0)),
            healing=int(data.get("healing", 0)),
            drain=int(data.get("drain", 0)),
            flinch_chance=int(data.get("flinch_chance", 0)),
            min_hits=int(data["min_hits"])
            if data.get("min_hits") is not None
            else None,
            max_hits=int(data["max_hits"])
            if data.get("max_hits") is not None
            else None,
            min_turns=int(data["min_turns"])
            if data.get("min_turns") is not None
            else None,
            max_turns=int(data["max_turns"])
            if data.get("max_turns") is not None
            else None,
            stat_changes_stat=stat_changes_stat,
            stat_chance=int(data.get("stat_chance", 0)),
            effect_chance=int(data["effect_chance"])
            if data.get("effect_chance") is not None
            else None,
            effect_id=int(data.get("effect_id", 0)),
            effect=data.get("effect_docs", ""),
        )

    @classmethod
    def create_from_id(cls, move_id: int) -> "MasterMove":
        """指定したIDの技のマスターデータを返す。

        Args:
            move_id: 取得したい技のID。
        Returns:
            指定したIDの技のマスターデータ。
        """
        move_data_dict = MoveRepository._get_move_by_id(move_id)
        if move_data_dict is None:
            raise ValueError(f"move_id={move_id} のデータが見つかりません。")
        return cls._create_from_dict(move_data_dict)


@dataclass(slots=True, frozen=True)
class BattleMove:
    """バトル中に使用する技の状態（マスターデータと現在PP）。"""

    MasterMove: MasterMove
    current_pp: int
