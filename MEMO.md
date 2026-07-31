# MEMO

このドキュメントは、ポケモンバトルシステム開発で使う主要なデータ構造・変数・データ管理方針をまとめたメモです。

## 0. 今後の優先順位

1. ダメージ計算機の実装
   - アタック側 / ディフェンス側のポケモン選択
   - 技、環境、努力値を設定
   - 最低/最大ダメージを算出
2. 計算機能を組み込んだモダンな GUI の構築
3. ダメージ計算メソッドを用いたバトルシステム開発
4. パーティ管理、バトル拡張、AI 最適化

`BATTLE/` フォルダ内の既存インスタンスメソッドは、現在の優先度に合わせて不要なら削除して構いません。


## 1. データ管理方針（最新）

### JSON（マスターデータ）
- `JSON/` 配下のファイルをマスターデータの正本として扱う。
- 主な対象:
  - `pokemon.json`
  - `move.json`
  - `ability.json`
  - `stat_change.json`
- ポケモン選択肢・基本情報・計算に必要な定義値は、原則このマスターを参照する。

### SQLite（実行ログ）
- `pokemon_champions.db` は実行時のログ保存先として扱う。
- 主な用途:
  - ダメージ計算や検証時の記録
  - 開発中の実験結果の蓄積
  - 後続分析のための履歴保存
- 重要: SQLite はマスターデータの正本としては扱わない。

## 2. 主要な変数・概念

### ポケモンの状態に関する変数
- `id`: ポケモンID
- `name`: ポケモン名
- `moves`: 所持技IDのリスト
- `level`: レベル
- `nature`: 性格ID
- `evs`: 努力値
- `ability`: 特性ID
- `hp`: 現在HP
- `hp_max`: 最大HP
- `attack`, `defense`, `sp_attack`, `sp_defense`, `speed`: 実数値ステータス
- `moves_pp`: 技ごとの現在PP
- `moves_name`: 技IDに対応する技名
- `condition`: 状態異常などの状態
- `ranks`: ランク補正

### フィールド・場に関する変数
- `weather`: 天候
- `weather_turns`: 天候の残りターン数
- `trick_room_turns`: トリックルームの残りターン数
- `side_a`, `side_b`: 両サイドの状態
- `stealth_rock`: ステルスロックの有無
- `spikes_layers`: まきびしの層数
- `toxic_spikes_layers`: どくびしの層数
- `reflect_turns`: リフレクターの残りターン数
- `light_screen_turns`: ひかりのかべの残りターン数

## 3. 主要クラスと責務

### Pokemon_Instance
- 1匹分のポケモンをインスタンス化し、戦闘に必要な基礎情報・実数値・PP管理を行う。
- 主要メソッド:
  - `__init__`: 初期化
  - `init_moves_and_pp`: 技とPPを初期化
  - `get_rank_multiplier`: ランク補正倍率を計算
  - `get_effective_stat`: 実効ステータスを計算
  - `show_status`: ステータス表示
  - `from_toml`: TOML からポケモン情報を生成

### Single_Battle_Manager
- 2体のポケモンを用いたシングルバトルの進行を管理する。
- 主要メソッド:
  - `move_basic_data`: 技データを取得
  - `move_meta_data`: 技メタデータを取得
  - `calculate_final_priority`: 優先度を計算

### PartyManagerLogic
- パーティの作成・読み込み・保存・編集を管理する。
- 主要な責務:
  - 空のパーティの生成
  - 既存パーティの読み込み
  - スロットの変更
  - 努力値・性格・特性・技の更新
  - TOML への保存

### PartyManagerCUI
- パーティ管理の CUI インターフェースを提供する。
- 主要な責務:
  - ユーザー入力の受け付け
  - パーティ表示
  - 操作メニューの表示
  - 変更処理の実行

## 4. 開発時に見ると良いポイント

- `BATTLE/` は計算フローと状態遷移の中心。UI依存を持ち込まず、純粋ロジックとして保つ。
- `POKEMON/` はデータ読み込みとインスタンス生成の中心。マスターデータ参照を集約する。
- `GUI/` は入力と表示に専念し、ロジック実装は `BATTLE/`・`POKEMON/` に寄せる。
- データアクセス実装時は、JSON（マスター）と SQLite（ログ）の責務を混同しない。

## 5. 補足

- [Poke API GraphiQL console](https://graphql.pokeapi.co/v1beta2/console) を参照しながらデータ構造を確認している。
- 今後の実装では、まずダメージ計算機を完成させ、その後 GUI とバトルフェーズへ展開していく予定。
