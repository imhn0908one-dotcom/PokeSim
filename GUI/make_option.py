from __future__ import annotations

from REPOSITORY import pokemon_repository

from .slect_panel import SelectOption


def make_pokemon_select_options() -> list[SelectOption]:
    """ポケモンの選択肢リストを作成する。"""
    options: list[SelectOption] = []
    all_pokemon = pokemon_repository.PokemonRepository.all_get()
    for pokemon_id, master_data in all_pokemon.items():
        icon_path = f"IMAGES/pokemon_selection/{master_data.id}.png"
        option = SelectOption(
            id=pokemon_id,
            title=master_data.jpname,
            subtitle="/".join(type_id.name for type_id in master_data.types),
            description={
                stat.name: value for stat, value in master_data.base_stats.items()
            },
            icon_path=icon_path,
            used_rate=None,
        )
        options.append(option)
    return options
