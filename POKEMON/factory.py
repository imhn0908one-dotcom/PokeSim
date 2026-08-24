import enums
import pokemon_object as pokemon

import REPOSITORY.pokemon_repository as repository


def fetch_pokedata_by_id(id: int) -> dict | None:
    """IDからマスターデータを取得する。

    Args:
        id: ポケモンID。

    Returns:
        該当するポケモンの辞書データ。見つからない場合はNone。
    """
    return repository.PokemonRepository.get_pokemon_by_id(id)


def get_celectable_genders(gender_rate: int) -> enums.Genders:
    """マスターの gender 値から選択可能性別を返す。

    Args:
        gender_rate: JSONマスターの gender 値。

    Returns:
        選択可能な性別種別。
    """
    return repository.PokemonRepository.get_selectable_genders(gender_rate)


def make_master_pokemon_instance(id: int) -> pokemon.MasterPokemonData | None:
    """IDをもとにMasterPokemonDataを生成する。

    Args:
        id: ポケモンID。

    Returns:
        生成したマスターデータ。IDが見つからない場合はNone。
    """
    return repository.PokemonRepository.make_master_pokemon_instance(id)
