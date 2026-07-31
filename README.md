# Pokemon battle systems

ポケモンの戦闘システムを、ダメージ計算・パーティ管理・バトルシミュレーションへ展開するための Python プロジェクトです。CUI で試作しながら、将来的には GUI や AI 学習環境へスケールできる構成を目指しています。

This project is a Python-based implementation of Pokémon battle systems, designed to facilitate damage calculation, party management, and battle simulation. It starts with a command-line interface (CUI) prototype and aims to scale towards a graphical user interface (GUI) and AI learning environment in the future.

## 🌟 プロジェクトの概要

このプロジェクトは、ポケモンの戦闘ロジックを段階的に実装していくための基盤です。まずは独立したダメージ計算機を完成させ、アタック側とディフェンス側のポケモンを選択し、技・環境・努力値を設定して最低/最大ダメージを算出できるようにします。その後、その計算メソッドを利用したモダンな GUI を構築し、さらにバトルシステムへと展開していきます。

This project is a basis of implementing Pokémon battle logic in stages. The immediate focus is to build a standalone damage calculator that chooses attacker and defender Pokémon, configures moves, environment, and EVs, and computes minimum and maximum damage. After that, the plan is to build a modern GUI and then expand into a battle system using the same calculation engine.

## ✅ 現在の実装状況

現在のリポジトリには、以下の内容が実装されています。

- GUI の土台（PySide6）
  - 攻撃側/防御側のポケモン選択パネル
  - フィールド状態設定パネル
  - 結果表示パネル
- バトルロジック用の基本クラス群
  - `BattleManager`
  - `BattleField` / `SideField`
- ポケモン・技・性格・特性を扱うためのデータアクセス層（`POKEMON/`）

## 🔭 これからの展望

今後の開発は、次の優先順位で進めます。

- F1: 独立ダメージ計算機の完成
  - アタック側 / ディフェンス側を選択
  - 技、環境、努力値を設定
  - 最低ダメージと最大ダメージを算出
- F2: モダンな GUI の実装
  - ダメージ計算機を使った操作性の高い UI
- F3: 計算メソッドを活用したバトル実装
  - ダメージ計算ロジックを Battle フローへ統合する
- F4: パーティ管理とバトル拡張
- F5: AI / 機械学習による最適化

現在の `BATTLE/` フォルダにある既存のインスタンスメソッドは、ダメージ計算機と新規バトル実装に合わせて整理・削除して構いません。

## 🧠 設計思想

- UI 層とロジック層を分離し、CUI から GUI への移行を容易にする
- データ駆動型の構成で、パーティ・技・性格・特性を柔軟に扱えるようにする
- 高速なシミュレーションを前提とした、保守しやすい構造を意識する

## 🗃️ データ管理方針（SQLite / JSON）

- JSON（`JSON/`）:
  - ポケモン・技・特性などの**マスターデータ**を保持する正本データ
  - アプリケーションはこのマスターデータを参照して選択肢や基本情報を構成する
- SQLite（`pokemon_champions.db`）:
  - バトル計算・検証時の**実行ログ**を保持する
  - マスターデータの正本としては扱わない


## 🧰 必要な環境

- Python 3.13 以上
- uv（Astral 製の Python パッケージ管理ツール）

## 🚀 セットアップ手順（uv 前提）

### 1. uv をインストールする

macOS / Homebrew を使う場合:

```bash
brew install uv
```

または公式インストーラーを使う場合:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. リポジトリをクローンする

```bash
git clone <your-repository-url>
cd Pokemon
```

### 3. 仮想環境を作成し、依存関係をインストールする

このプロジェクトでは、依存関係の管理に uv を使用します。次のコマンドを実行すると、仮想環境が作成され、必要なパッケージが自動で入ります。

```bash
uv sync
```

### 4. 実行する

現在の実装は GUI エントリーポイントから起動します。必要に応じて、対象スクリプトを `uv run python ...` で実行してください。

```bash
uv run python main.py
```

## Recomend Extension

- [vscode-pokemon](https://marketplace.visualstudio.com/items?itemName=jakobhoeg.vscode-pokemon)
- [SQLite Viewer](https://marketplace.visualstudio.com/items?itemName=qwtel.sqlite-viewer)

## 📁 プロジェクト構成

- `BATTLE/` : 戦闘ロジック（マネージャー、ダメージ計算）
- `FIELD/` : フィールド/サイド状態のデータ構造
- `GUI/` : PySide6 ベースの UI
- `POKEMON/` : ポケモン関連のドメイン・データアクセス
- `JSON/` : マスターデータ（正本）
- `buildDB/` : データ構築・取得スクリプト
- `log/` : 実行ログ・構築ログ
- `pokemon_champions.db` : SQLite 実行ログ

## 🗂️ 開発メモ
- MEMO.mdを確認すると開発に必要なことがまとめられている。
- データ方針は「JSON=マスターデータ」「SQLite=実行ログ」。

## 📄 ライセンス

このプロジェクトは MIT License のもとで公開されています。