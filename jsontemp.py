import json

import requests

POKEAPI_GRAPHQL_URL = "https://graphql.pokeapi.co/v1beta2"

EFFECTQUERY = """
query samplePokeAPIquery {
  moveeffecteffecttext(where: {language_id: {_eq: 9}}) {
    id
    effect
  }
}
"""
response = requests.post(
    POKEAPI_GRAPHQL_URL,
    json={"query": EFFECTQUERY},
    timeout=30,
)
filename = "JSON/move_effectdescriptions.json"

with open(filename, "w", encoding="utf-8") as f:
    json.dump(
        response.json()["data"]["moveeffecteffecttext"], f, ensure_ascii=False, indent=4
    )

print(f"finish {filename}")
