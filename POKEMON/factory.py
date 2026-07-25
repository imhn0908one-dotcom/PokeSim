import functools
import json
import sqlite3
import sys
import time
from contextlib import contextmanager
from functools import lru_cache
from typing import Optional

from memory_profiler import profile

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


# 💡 jsonファイル全体を1回だけ読み込んで保持する関数を作る
@lru_cache(maxsize=1)
def load_all_pokemon_data() -> dict:
    with open("JSON/pokemon.json", "r", encoding="utf-8") as f:
        return json.load(f)


@profile(stream=sys.stdout)
def fetch_pokedata_by_id(id: int) -> dict | None:
    all_pokemon = load_all_pokemon_data()
    if str(id) in all_pokemon:
        return all_pokemon[str(id)]
    else:
        return None


def fetch_pokedata_fromDB(id: int) -> dict | None:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    sql = "SELECT * FROM pokemon WHERE id = ?"
    cursor.execute(sql, (id,))
    result = cursor.fetchone()
    conn.close()
    return result
