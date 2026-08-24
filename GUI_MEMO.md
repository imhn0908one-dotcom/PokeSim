## GUIフォルダ現状メモ

### 1. ファイルとクラスの対応

| ファイル | クラス | 役割 |
|---|---|---|
| `GUI/main_window.py` | `MainWindow` | 画面全体のレイアウト構築、各パネルの生成、QSS適用 |
| `GUI/panel_logic.py` | `SelectionComboBox` | 画像付き選択コンボボックスの共通UI部品 |
| `GUI/pokemon_panel.py` | `PokemonPanel` / `PokemonViewPanel` | 攻撃側・防御側ポケモン選択パネル（`PokemonViewPanel`は現状未実装） |
| `GUI/field_panel.py` | `FieldPanel` | フィールド状態入力UIを動的生成し、`BattleManager.field`へ反映 |
| `GUI/result_panel.py` | `ResultPanel` | 結果表示領域（現状は枠のみ） |
| `GUI/style.qss` | - | オブジェクト名ベースの見た目定義 |

---

### 2. クラスごとの「表示インプット形式」

## `MainWindow`（`GUI/main_window.py`）
- **生成時インプット**
  - `battle_manager.BattleManager()` を内部生成。
  - `PokemonPanel("attacker", battle_manager)` / `PokemonPanel("defender", battle_manager)` を生成。
  - `FieldPanel(battle_manager=battle_manager)` を生成。
- **表示上の重要点**
  - パネルの `objectName` を以下に設定し、`GUI/style.qss` のセレクタと対応。
    - `left_pannel`, `right_pannel`, `result_pannel`, `bottom_pannel`
  - レイアウトは `QHBoxLayout` + `QSplitter(Vertical)`。

## `SelectionComboBox`（`GUI/panel_logic.py`）
- **生成時インプット形式**
  - `items: Dict[int, str]`
    - `key`: 内部ID（`currentData()`で取得される値）
    - `value`: 表示名（ドロップダウン表示テキスト）
  - `placeholder: str`
  - `objectName: str`
- **表示データ化ルール**
  - 各要素は `addItem(icon, value, key)` で追加される。
  - アイコンパス形式: `IMAGES/{objectName}/{value}.png`
  - つまり「表示」は `value`、「内部値」は `key`。

## `PokemonPanel`（`GUI/pokemon_panel.py`）
- **生成時インプット**
  - `panel_name`（`"attacker"` or `"defender"` 想定）
  - `battle_manager`
- **表示インプットの実体**
  - `manager.get_selectable_pokemon_map()` を `SelectionComboBox.items` に渡す。
  - `get_selectable_pokemon_map()` は `JSON/pokemon.json` を読み込み、`Dict[int, str]` に変換して返す。
    - 形式: `{ポケモンID(int): ポケモン名(str)}`
- **現状**
  - ラベルとポケモン選択コンボのみ実装。
  - `PokemonViewPanel` はクラス定義のみで表示ロジック未実装。

## `FieldPanel`（`GUI/field_panel.py`）
- **生成時インプット**
  - `battle_manager`
  - 実際には `battle_manager.field`（`FIELD/state.py` の `BattleField` データクラス）を参照してUIを組み立てる。
- **表示インプット形式（動的生成）**
  - `dataclasses.fields(BattleField)` を走査し、フィールド型ごとにウィジェット生成:
    - `str` -> `QComboBox`（`metadata["choices"]` を選択肢として利用）
    - `bool` -> `QCheckBox`
    - `int` -> `QSpinBox`（`metadata["min"]`, `metadata["max"]` を範囲として利用）
  - 初期値は `battle_manager.field` の現在値を反映。
- **依存する入力定義の場所**
  - `FIELD/state.py` の `BattleField`:
    - `weather: str`（choicesあり）
    - `terrain: str`（choicesあり）
    - `trick_room`, `magic_room`, `wonder_room`, `gravity`（bool）

## `ResultPanel`（`GUI/result_panel.py`）
- **生成時インプット**
  - なし（コンストラクタ引数なし）
- **現状**
  - 最低サイズ・`objectName` 設定のみ。結果表示コンテンツや計算トリガは未実装。

---

### 3. 発火システム（イベント接続）現状

## A. ポケモン選択イベント
- 対象: `PokemonPanel.pokemon_combo`
- 接続:
  - `currentIndexChanged` -> `emit_updated_pokemon_instance`
- 現状ハンドラ挙動:
  - `currentData()` で選択IDを取得
  - 攻撃側/防御側判定で `print` 出力のみ
  - `battle_manager.set_attacker` / `set_defender` 呼び出しは未接続

## B. フィールド入力イベント
- 対象: `FieldPanel` 内で生成した各ウィジェット
- 接続:
  - `QComboBox.currentIndexChanged`
  - `QSpinBox.valueChanged`
  - `QCheckBox.stateChanged`
  - すべて `emit_updated_battle_field` へ接続
- ハンドラ挙動:
  - `BattleField` の全項目を再走査
  - 各ウィジェット値を読み取り
  - `setattr(current_field, field_name, value)` で `battle_manager.field` に即時反映

## C. 画面スタイル反映
- 対象: `MainWindow.load_stylesheet("GUI/style.qss")`
- 発火:
  - `MainWindow` 初期化時に1回実行
- 内容:
  - パネル枠線、`QSplitter::handle`、`#pokemon_selection` の見た目を適用

---

### 4. 実装場所の早見（入力元とGUIの接続）

- ポケモン選択肢の入力元:
  - `POKEMON/manager.py` の `get_selectable_pokemon_map()`
  - `JSON/pokemon.json` を読み込み `Dict[int, str]` 化
- フィールド選択肢/範囲の入力元:
  - `FIELD/state.py` の `BattleField` フィールド定義（`metadata["choices"]`, `metadata["min"]`, `metadata["max"]`）
- GUI状態保存先（反映先）:
  - `BATTLE/battle_manager.py` の `BattleManager.field`
  - （ポケモン側は現状、`attacker/defender` への代入処理が未配線）