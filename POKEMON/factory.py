import functools
import json
import time
from email.mime import base
from functools import lru_cache

import enums
import pokemon_object as pokemon

POKEMON_DATABASE = "JSON/pokemon_data.json"


# 計測用デコレータの定義
def timer(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)  # 本体の関数を実行
        end = time.perf_counter()
        print(f"⏱️ [{func.__name__}] 実行時間: {end - start:.6f} 秒")
        return result

    return wrapper


# 💡 jsonファイル全体を1回だけ読み込んで保持する関数を作る
@lru_cache(maxsize=1)
def load_all_pokemon_data() -> dict:
    with open(POKEMON_DATABASE, "r", encoding="utf-8") as f:
        return json.load(f)


def fetch_pokedata_by_id(id: int) -> dict | None:
    all_pokemon = load_all_pokemon_data()
    if str(id) in all_pokemon:
        return all_pokemon[str(id)]
    else:
        return None


def get_celectable_genders(gender_rate: int) -> enums.Genders:
    """Determine selectable genders based on the gender rate from the master data."""
    if gender_rate == -1:
        selectable_genders = enums.Genders.GENDERLESS
    elif gender_rate == 0:
        selectable_genders = enums.Genders.MALE
    elif gender_rate == 8:
        selectable_genders = enums.Genders.FEMALE
    else:
        selectable_genders = enums.Genders.BOTH
    return selectable_genders


def make_master_pokemon_instance(id: int) -> pokemon.MasterPokemonData | None:
    """Create a MasterPokemonData instance from the master data using the given ID."""
    pokedata = fetch_pokedata_by_id(id)
    if pokedata is None:
        return None
    gender_rate = pokedata.get("gender", 0)
    selectable_genders = get_celectable_genders(gender_rate)
    statlist = enums.Statslist({
        enums.Stats.HP: pokedata["stats"].get("1", 0),
        enums.Stats.ATTACK: pokedata["stats"].get("2", 0),
        enums.Stats.DEFENSE: pokedata["stats"].get("3", 0),
        enums.Stats.SPECIAL_ATTACK: pokedata["stats"].get("4", 0),
        enums.Stats.SPECIAL_DEFENSE: pokedata["stats"].get("5", 0),
        enums.Stats.SPEED: pokedata["stats"].get("6", 0),
    })
    return pokemon.MasterPokemonData(
        id=id,
        name=pokedata["name"],
        jpname=pokedata["jpname"],
        selectable_genders=selectable_genders,
        weight=pokedata["weight"],
        height=pokedata["height"],
        base_stats=statlist,
        abilities=pokedata["abilities"],
        types=enums.Typeslist([enums.TypeID(type_id) for type_id in pokedata["types"]]),
        learnt_moves=pokedata["moveids"],
    )


print(make_master_pokemon_instance(128))
