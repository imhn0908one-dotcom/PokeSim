from __future__ import annotations

from typing import TypedDict

from REPOSITORY.pokemon_repository import PokemonRepository


class PokemonOption(TypedDict):
    """ポケモン選択肢の表示データ。"""

    id: int
    name: str


def get_pokemon_list() -> list[PokemonOption]:
    """選択UI向けにポケモン一覧を返す。

    Returns:
        ポケモンIDと表示名を持つ選択肢一覧。
    """
    return [
        PokemonOption(id=master_data.id, name=master_data.jpname)
        for master_data in PokemonRepository.all_get()
    ]
