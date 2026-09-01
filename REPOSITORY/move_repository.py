import json
from functools import lru_cache
from pathlib import Path
from typing import Any, TypedDict

from POKEMON import enums


class Move_data(TypedDict):
    """JSON/move_data.json の各技のデータ形式。"""

    id: int
    name: str
    jpname: str
    type_id: int
    damage_class_id: int
    pp: int
    power: int | None
    accuracy: int | None
    attribute_ids: list[int]
    target_id: int
    category_id: int
    ailment_id: int
    ailment_chance: int
    crit_rate: int
    healing: int
    drain: int
    flinch_chance: int
    min_hits: int | None
    max_hits: int | None
    min_turns: int | None
    max_turns: int | None
    stat_changes_stat: dict[enums.Stats, int] | None
    stat_chance: int
    effect_chance: int | None
    effect_id: int
    effect_docs: str


json_move_data = dict[str, Move_data]


class MoveRepository:
    _JSON_DIR = Path(__file__).resolve().parents[1] / "JSON"
    _MASTER_DATA_PATH = _JSON_DIR / "move_data.json"
    _INDEX_DATA_PATH = _JSON_DIR / "moveindex.json"

    @classmethod
    @lru_cache(maxsize=1)
    def load_master_data(cls) -> dict[str, dict[str, Any]]:
        """マスターデータを1度だけ読み込み、メモリ上にキャッシュする。"""
        with cls._MASTER_DATA_PATH.open("r", encoding="utf-8") as file:
            payload = json.load(file)

        if not isinstance(payload, dict):
            raise TypeError("move_data.json の内容は辞書形式である必要があります。")

        return {str(key): value for key, value in payload.items()}

    @classmethod
    @lru_cache(maxsize=1)
    def load_index_data(cls) -> list[int]:
        """技のインデックスデータを1度だけ読み込み、メモリ上にキャッシュする。"""
        with cls._INDEX_DATA_PATH.open("r", encoding="utf-8") as file:
            payload = json.load(file)
        return [int(key) for key in list(payload) if isinstance(key, (int, str))]

    @classmethod
    def clear_cache(cls) -> None:
        """JSONキャッシュを破棄する。データ更新後に呼び出す。"""
        cls.load_master_data.cache_clear()
        cls.load_index_data.cache_clear()

    @classmethod
    def _get_move_by_id(cls, move_id: int | str) -> dict[str, Any] | None:
        """指定したIDの技データを返す。"""
        move_data = cls.load_master_data()
        key = str(move_id)
        value = move_data.get(key)
        if value is None:
            return None
        if not isinstance(value, dict):
            raise TypeError(f"move_id={move_id} のデータ形式が不正です。")
        return value
