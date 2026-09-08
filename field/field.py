from dataclasses import dataclass, field, fields

from ENUMS.field_enums import OtherEffect
from FIELD.field_object import (
    OtherEffectsContainer,
    RoomState,
    TerrainState,
    WeatherState,
)


@dataclass
class SideField:
    """個人の陣地状態を管理するデータクラス。

    このクラスは、攻撃側/防御側のそれぞれのサイドで
    ダメージ計算に影響する設置技や壁、フィールド効果を保持します。
    """

    reflector: bool = False
    """リフレクター状態。

    物理ダメージを受ける際に、ダメージ計算の最終段階で物理防御への補正を適用する。
    物理技に対するダメージ削減を計算する際に参照される。
    """

    light_screen: bool = False
    """ひかりのかべ状態。

    特殊ダメージを受ける際に、ダメージ計算の最終段階で特殊防御への補正を適用する。
    特殊技に対するダメージ削減を計算する際に参照される。
    """

    aurora_veil: bool = False
    """オーロラベール状態。

    物理・特殊ダメージの両方を一定割合軽減する。
    条件が成立する場合、最終防御補正で `reflector`/`light_screen` と同時に扱う。"""

    stealth_rock: bool = False
    """ステルスロックの設置有無。

    交代時に岩タイプのポケモンは無効化され、それ以外のタイプは
    最大HP割合ダメージを受ける。ダメージ計算では交代ダメージ処理に使用する。
    """

    spikes: int = field(default=0, metadata={"min": 0, "max": 3})
    """まきびしの設置枚数（0〜3）。

    交代時に、枚数に応じたダメージを与える。
    計算時には交代ターンの追加ダメージとして参照される。"""

    toxic_spikes: int = field(default=0, metadata={"min": 0, "max": 2})
    """どくびしの設置枚数（0〜2）。

    交代時に相手のポケモンに毒/猛毒状態を付与する。
    ダメージ計算時には毒ダメージを間接的に扱うための状態として参照される。"""

    sticky_web: bool = False
    """ねばねばネット状態。

    交代時に相手の素早さランクを1段階下げる。
    ダメージ計算時には実質的に速度影響を与えるため、素早さ判定・行動順に関連する。
    """

    tailwind: bool = False
    """おいかぜ状態。

    陣地内のポケモンの最終素早さを2倍として扱う。
    ダメージ計算では、行動順や素早さ依存の効果を判定する際に参照される。
    """


@dataclass
class BattleField:
    """戦場状態を管理するデータクラス。

    このクラスは、戦場全体の状態を保持し、ダメージ計算に影響するフィールド効果を管理します。
    """

    terrain: TerrainState
    weather: WeatherState
    room: RoomState
    other: OtherEffectsContainer

    def turn_step(self):
        """ターンを進め、各状態の残りターン数を減少させる。

        Returns:
            dict: 各状態の終了状況を示す辞書。
                例: {'terrain': True, 'weather': False, 'room': True}
        """
        return {
            "terrain": self.terrain.step_turn(),
            "weather": self.weather.step_turn(),
            "room": self.room.step_turn(),
            "other": {
                effect: (turns - 1 == 0)
                for effect, turns in self.other.active_effects.items()
            },
        }
