import json

import requests

mainurl = "https://pokeapi.co/api/v2/"
filename = "JSON/pokemon.json"
with open(filename, "r", encoding="utf-8") as f:
    all_pokemon: dict = json.load(f)

# .items() を使って (ID, ポケモンデータ) を同時に取り出す
for _, poke_data in all_pokemon.items():
    # poke_data["types"] からリストを取り出して int に変換
    poke_data["types"] = [int(t) for t in poke_data["types"]]

# ファイルへ保存
with open(filename, "w", encoding="utf-8") as f:
    json.dump(all_pokemon, f, indent=4, ensure_ascii=False)
