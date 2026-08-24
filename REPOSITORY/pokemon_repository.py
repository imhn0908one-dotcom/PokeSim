from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

from POKEMON import enums
from POKEMON.pokemon_object import MasterPokemonData


class PokemonRepository:
    """JSON形式のポケモンマスターデータを保持するキャッシュ付きリポジトリ。

    画面表示やドメイン生成がファイルパスや読み込みロジックを直接知る必要がないように、
    すべての取得 API をこのクラスに集約する。
    """

    _JSON_DIR = Path(__file__).resolve().parents[1] / "JSON"
    _MASTER_DATA_PATH = _JSON_DIR / "pokemon_data.json"

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

    @classmethod
    def get_pokemon_by_id(cls, pokemon_id: int | str) -> dict[str, Any] | None:
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

    @staticmethod
    def get_selectable_genders(gender_rate: int | None) -> enums.Genders:
        """マスターデータの gender 値から選択可能な性別種別を返す。

        Args:
            gender_rate: JSONマスターに定義された gender 値。

        Returns:
            選択可能な性別種別。
        """
        if gender_rate == -1:
            return enums.Genders.GENDERLESS
        if gender_rate == 0:
            return enums.Genders.MALE
        if gender_rate == 8:
            return enums.Genders.FEMALE
        return enums.Genders.BOTH

    @classmethod
    def make_master_pokemon_instance(
        cls, pokemon_id: int | str
    ) -> MasterPokemonData | None:
        """指定したIDのMasterPokemonDataを生成して返す。

        Args:
            pokemon_id: ポケモンID。

        Returns:
            生成したマスターデータ。IDが見つからない場合はNone。
        """
        pokedata = cls.get_pokemon_by_id(pokemon_id)
        if pokedata is None:
            return None

        gender_rate = pokedata.get("gender", 0)
        selectable_genders = cls.get_selectable_genders(gender_rate)
        statlist = enums.Statslist({
            enums.Stats.HP: pokedata["stats"].get("1", 0),
            enums.Stats.ATTACK: pokedata["stats"].get("2", 0),
            enums.Stats.DEFENSE: pokedata["stats"].get("3", 0),
            enums.Stats.SPECIAL_ATTACK: pokedata["stats"].get("4", 0),
            enums.Stats.SPECIAL_DEFENSE: pokedata["stats"].get("5", 0),
            enums.Stats.SPEED: pokedata["stats"].get("6", 0),
        })
        return MasterPokemonData(
            id=int(pokemon_id),
            name=str(pokedata["name"]),
            jpname=str(pokedata["jpname"]),
            selectable_genders=selectable_genders,
            weight=pokedata["weight"],
            height=pokedata["height"],
            base_stats=statlist,
            abilities=list(pokedata["abilities"]),
            types=enums.Typeslist([
                enums.TypeID(type_id) for type_id in pokedata["types"]
            ]),
            learnt_moves=pokedata["moveids"],
        )

    @classmethod
    def get_all_pokemon(cls) -> dict[int, MasterPokemonData]:
        """全ポケモンのMasterPokemonDataを返す。

        Returns:
            マスターデータの全件リスト。
        """
        result: dict[int, MasterPokemonData] = {}
        for pokemon_id_str in cls.load_master_data():
            pokemon_id = int(pokemon_id_str)
            pokemon_data = cls.make_master_pokemon_instance(pokemon_id)
            if pokemon_data is not None:
                result[pokemon_id] = pokemon_data
        return result

    @classmethod
    def get_selectable_pokemon_map(cls) -> dict[int, str]:
        """選択UI向けにIDと表示名のマップを返す。

        Returns:
            キーがポケモンID、値が表示名の辞書。
        """
        return {
            pokemon_id: name for pokemon_id, name in cls.get_master_pokemon_ids_names()
        }
