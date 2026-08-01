import json
from typing import Any

import requests

# 指定していただいたエンドポイントURL
POKEAPI_GRAPHQL_URL = "https://graphql.pokeapi.co/v1beta2"

# IDsを配列で受け取れるようにしたクエリ
FLATTEN_MOVES_QUERY = """
query getMovesByIds($ids: [Int!]) {
  move(where: {id: {_in: $ids}}) {
    id
    name
    movenames(where: {language_id: {_eq: 11}}) {
      name
    }
    type_id
    move_damage_class_id
    pp
    power
    accuracy
    movemeta {
      crit_rate
      healing
      drain
      move_meta_category_id
      move_meta_ailment_id
      ailment_chance
      stat_chance
      flinch_chance
      max_hits
      max_turns
      min_hits
      min_turns
    }
    movemetastatchanges {
      stat_id
      change
    }
    move_effect_chance
    move_effect_id
    move_target_id
    moveeffect {
      moveeffecteffecttexts(where: {language_id: {_eq: 9}}) {
        short_effect
      }
    }
  }
}
"""


def fetch_and_flatten_moves_json(move_ids: list[int], save_file_path: str) -> None:
    """
    指定した技IDのリストを取得し、ネストを分解してフラットなJSONとして保存する
    """
    print(f"技ID {move_ids} のデータを取得中...")

    # 1. GraphQLにリクエストを投げる
    response = requests.post(
        POKEAPI_GRAPHQL_URL,
        json={"query": FLATTEN_MOVES_QUERY, "variables": {"ids": move_ids}},
        timeout=30,
    )
    response.raise_for_status()
    print(response.json())  # デバッグ用にレスポンスを表示
    # 取得した生の配列データ
    raw_moves: list[dict[str, Any]] = response.json()["data"]["move"]

    flattened_moves = []

    # 2. 階層を分解して1階層の dict に平たくする
    for raw in raw_moves:
        # --- 深い階層から必要なデータを引っ張り出す ---

        # 日本語名
        movenames = raw.get("movenames") or []
        jpname = movenames[0]["name"] if movenames else raw["name"]

        # メタ情報
        meta_list = raw.get("movemeta") or []
        meta = meta_list[0] if meta_list else {}

        # 能力変化を {stat_id: change} のシンプルな辞書に変換
        statchanges = raw.get("movemetastatchanges") or []
        stat_changes_dict = {
            s["stat_id"]: s["change"]
            for s in statchanges
            if s.get("stat_id") is not None
        }

        # エフェクト説明文
        effect_node = raw.get("moveeffect") or {}
        effect_texts = effect_node.get("moveeffecteffecttexts") or []
        effect_str = effect_texts[0].get("short_effect", "") if effect_texts else ""

        # --- すべてのデータを第1階層に並べたペッタンコの辞書を作る ---
        flat_move = {
            "id": raw["id"],
            "name": raw["name"],
            "jpname": jpname,
            "type_id": raw["type_id"],
            "damage_class_id": raw["move_damage_class_id"],
            "pp": raw["pp"],
            "power": raw["power"],
            "accuracy": raw["accuracy"],
            # メタ情報（nullの可能性があるものは default を設定）
            "target_id": raw.get("move_target_id"),
            "category_id": meta.get("move_meta_category_id", 0),
            "ailment_id": meta.get("move_meta_ailment_id", 0),
            "ailment_chance": meta.get("ailment_chance", 0),
            "crit_rate": meta.get("crit_rate", 0),
            "healing": meta.get("healing", 0),
            "drain": meta.get("drain", 0),
            "flinch_chance": meta.get("flinch_chance", 0),
            # ターン・ヒット数
            "min_hits": meta.get("min_hits"),
            "max_hits": meta.get("max_hits"),
            "min_turns": meta.get("min_turns"),
            "max_turns": meta.get("max_turns"),
            # ステータス変化の辞書
            "stat_changes": stat_changes_dict,
            "stat_chance": meta.get("stat_chance", 0),
            # ターゲットとエフェクト
            "effect_chance": raw.get("move_effect_chance"),
            "effect_id": raw.get("move_effect_id"),
            "effect": effect_str,
        }

        flattened_moves.append(flat_move)

    # 3. フラットになった辞書リストを JSON としてファイルに書き出す
    with open(save_file_path, "w", encoding="utf-8") as f:
        json.dump(flattened_moves, f, ensure_ascii=False, indent=2)

    print(
        f"✅ {len(flattened_moves)} 件の技データをペッタンコにして '{save_file_path}' に保存しました！"
    )


# ==============================
# 実行部分（テスト）
# ==============================
if __name__ == "__main__":
    # ほしい技のIDリスト（1: はたく, 2: からてチョップ）
    target_ids = [1, 2]

    # 実行してJSONファイルを作るだけ！
    fetch_and_flatten_moves_json(target_ids, "JSON/flattened_moves.json")
