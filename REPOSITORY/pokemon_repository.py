from __future__ import annotations

import json
from functools import lru_cache
from optparse import Option
from os import name
from pathlib import Path
from typing import Any, Optional, TypedDict

from POKEMON import enums


class pokemon_data(TypedDict):
    """JSON/pokemon_data.json の各ポケモンのデータ形式。"""

    name: str
    jpname: str
    types: list[int]
    abilities: list[dict[str, Any]]
    moveids: list[int]
    stats: dict[str, int]
    gender: int
    weight: int
    height: int
    mega_exsist: bool
    pass


"""JSON/pokemon_data.json の内容を保持する辞書。キーはポケモンID、値は pokemon_data 型の辞書。"""
json_pokemon_data_dict = dict[str, pokemon_data]


class PokemonRepository:
    """JSON形式のポケモンマスターデータを保持するキャッシュ付きリポジトリ。

    画面表示やドメイン生成がファイルパスや読み込みロジックを直接知る必要がないように、
    すべての取得 API をこのクラスに集約する。
    """

    _JSON_DIR = Path(__file__).resolve().parents[1] / "JSON"
    _MASTER_DATA_PATH = _JSON_DIR / "pokemon_data.json"
    _INDEX_DATA_PATH = _JSON_DIR / "pokeindex.json"

    @classmethod
    @lru_cache(maxsize=1)
    def load_master_data(cls) -> dict[str, dict[str, Any]]:
        """マスターデータを1度だけ読み込み、メモリ上にキャッシュする。"""
        with cls._MASTER_DATA_PATH.open("r", encoding="utf-8") as file:
            payload = json.load(file)

        if not isinstance(payload, dict):
            raise TypeError("pokemon_data.json の内容は辞書形式である必要があります。")

        return {str(key): value for key, value in payload.items()}

    @classmethod
    def clear_cache(cls) -> None:
        """JSONキャッシュを破棄する。データ更新後に呼び出す。"""
        cls.load_master_data.cache_clear()
        cls.load_index_data.cache_clear()

    @classmethod
    @lru_cache(maxsize=1)
    def load_index_data(cls) -> list[int]:
        """ポケモン図鑑のインデックスデータを1度だけ読み込み、メモリ上にキャッシュする。"""
        with cls._INDEX_DATA_PATH.open("r", encoding="utf-8") as file:
            payload = json.load(file)
        return [int(key) for key in list(payload) if isinstance(key, (int, str))]

    @classmethod
    def _get_pokemon_by_id(cls, pokemon_id: int | str) -> dict[str, Any] | None:
        """指定したIDのポケモンデータを返す。"""
        pokemon_data = cls.load_master_data()
        key = str(pokemon_id)
        value = pokemon_data.get(key)
        if value is None:
            return None
        if not isinstance(value, dict):
            raise TypeError(f"pokemon_id={pokemon_id} のデータ形式が不正です。")
        return value

    @classmethod
    def get_master_pokemon_ids_names(cls) -> list[tuple[int, str]]:
        """マスターデータのポケモンIDと名前の一覧を返す。"""
        pokemon_data = cls.load_master_data()
        return [
            (int(key), value.get("name", "") or value.get("jpname", ""))
            for key, value in pokemon_data.items()
        ]

    @classmethod
    def get_selectable_pokemon_map(cls) -> dict[int, str]:
        """選択UI向けにIDと表示名のマップを返す。

        Returns:
            キーがポケモンID、値が表示名の辞書。
        """
        return {
            pokemon_id: name for pokemon_id, name in cls.get_master_pokemon_ids_names()
        }

    @classmethod
    def get_pokemon_ids(cls) -> list[int]:
        """マスターデータのポケモンIDの一覧を返す。"""
        return cls.load_index_data()


class NatureRepository:
    @classmethod
    @lru_cache(maxsize=1)
    def _load_nature_data(cls) -> dict[str, Any]:
        """自然のデータを1度だけ読み込み、メモリ上にキャッシュする。"""
        natures_path = Path(__file__).resolve().parents[1] / "JSON" / "stat_change.json"
        with open(natures_path, "r") as j:
            return json.load(j)

    @classmethod
    def nature_change_rate(cls, stat_name: str, nature_ID: int) -> float:
        """Return the nature-based multiplier for the specified stat.

        Args:
            stat_name: Name of the stat to check.
            nature_ID: Numeric ID of the Pokémon's nature.

        Returns:
            1.1 if the nature raises the stat, 0.9 if it lowers it,
            otherwise 1.0.
        """
        natures_rate_file = cls._load_nature_data()
        if nature_ID in natures_rate_file["natures"][stat_name]["rate_up"]:
            return 1.1
        elif nature_ID in natures_rate_file["natures"][stat_name]["rate_dw"]:
            return 0.9
        else:
            return 1.0
