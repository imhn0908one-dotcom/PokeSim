from __future__ import annotations

from typing import TypedDict

from REPOSITORY.pokemon_repository import PokemonRepository


class PokemonOptionData(TypedDict):
    """ポケモン選択肢の表示データ。"""

    id: int
    name: str


def get_pokemon_list() -> list[PokemonOptionData]:
    """選択UI向けにポケモン一覧を返す。

    Returns:
        ポケモンIDと表示名を持つ選択肢一覧。
    """
    return [
        PokemonOptionData(id=id, name=name)
        for id, name in PokemonRepository.get_master_pokemon_ids_names()
    ]
