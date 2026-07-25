import functools
import json
import sqlite3
import time
from calendar import c
from contextlib import contextmanager
from typing import Optional

DB_PATH = "pokemon_champions.db"
STAT_KEYS = ["HP", "Atk", "Def", "SpA", "SpD", "Spe"]
DB_STAT_COLUMNS = [
    "hp",
    "attack",
    "defense",
    "special_attack",
    "special_defense",
    "speed",
]


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


@timer
def fetch_pokedata_by_id(id: int) -> dict | None:
    filename = "JSON/pokemon.json"
    with open(filename, "r", encoding="utf-8") as f:
        all_pokemon = json.load(f)
        print(len(all_pokemon))
    if str(id) in all_pokemon:
        return all_pokemon[str(id)]
    else:
        return None


@timer
def fetch_pokedata_fromDB(id: int) -> dict | None:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    sql = "SELECT * FROM pokemon WHERE id = ?"
    cursor.execute(sql, (id,))
    result = cursor.fetchone()
    conn.close()
    return result


print(fetch_pokedata_fromDB(3))
print(fetch_pokedata_by_id(3))
