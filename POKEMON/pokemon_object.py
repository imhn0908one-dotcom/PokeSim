import json
from dataclasses import dataclass, field
from enum import Enum, IntEnum
from typing import Dict, List

from enums import Stats
from requests import get

from POKEMON import enums
from REPOSITORY.pokemon_repository import PokemonRepository


class VolatileCondition(Enum):
    """状態変化の種類、バトンタッチによって移動するか"""

    CONFUSION = ("こんらん", True)
    FLINCH = ("ひるみ", True)
    CURSE = ("のろい", True)
    CANT_ESCAPE = ("にげられない", True)
    LEECH_SEED = ("やどりぎのタネ", True)
    SUBSTITUTE = ("みがわり", True)
    THROAT_CHOP = ("じごくづき", True)
    SALT_CURE = ("しおづけ", True)
    AQUA_RING = ("アクアリング", True)
    INGRAIN = ("ねをはる", True)
    NO_ABILITY = ("いえきによって特性の効果が消えた", True)
    TAR_SHOT = ("タールショット", True)
    SMACK_DOWN = ("うちおとす", True)
    FLASH_FIRE = ("もらいび", True)
    DESTINY_BOND = ("みちづれ", True)
    GRUDGE = ("おんねん", True)
    UPROAR = ("さわぐ", True)
    STOCKPILE = ("たくわえる", True)

    TRANSFORM = ("へんしん", False)
    TORMENT = ("いちゃもん", False)
    IMPRISON = ("ふういん", False)
    ATTRACT = ("めろめろ", False)
    DROWSY = ("ねむけ", False)
    BOUND = ("バインド", False)
    DEFENCE_CURL = ("まるくなる", False)


@dataclass(slots=True)
class VolatileInstance:
    """基本状態異常クラス
    TODO: if volatile have Special function, overload this dataclass
    """

    Volatile_stat: VolatileCondition
    turn: int = field(metadata={"description": "-1 は無制限"})

    def __str__(self):
        return f"{self.Volatile_stat.name}"


# =======================================================
# 特殊状態異常の子クラス
# =======================================================
# @dataclass
class SubstituteEffect(VolatileInstance):
    """身代わり用。hp要素をふくむ。"""

    Volatile_stat: VolatileCondition = VolatileCondition.SUBSTITUTE
    hp: int = 0


# ======================================================
# ベーシックデータのデータクラス（マスターデータ）
# ======================================================
@dataclass
class MasterPokemonData:
    id: int = field(metadata={"description": "pokemon ID"})
    name: str = field(metadata={"description": "pokemon name"})
    jpname: str = field(metadata={"description": "Japanese pokemon name"})

    selectable_genders: enums.Genders = field(
        metadata={"description": "pokemon gender"}
    )
    weight: int = field(metadata={"description": "pokemon weight"})
    height: int = field(metadata={"description": "pokemon height"})
    types: enums.Typeslist = field(metadata={"description": "pokemon types"})
    base_stats: Dict[Stats, int] = field(
        metadata={"description": "種族値"},
    )
    abilities: List[int] = field(
        metadata={"description": "selective abilities id"}, default_factory=list
    )

    learnt_moves: List[int] = field(
        metadata={"description": "selective moves id"}, default_factory=list
    )

    @staticmethod
    def get_selectable_genders(gender_rate: int | None) -> enums.Genders:
        """マスターデータの gender 値から選択可能な性別種別を返す。

        Args:
            gender_rate: JSONマスターに定義された gender 値。

        Returns:
            選択可能な性別種別。
        """
        if gender_rate == -1:
            return enums.Genders.GENDERLESS
        if gender_rate == 0:
            return enums.Genders.MALE
        if gender_rate == 8:
            return enums.Genders.FEMALE
        return enums.Genders.BOTH

    @classmethod
    def from_dict(cls, data: dict, id: int) -> "MasterPokemonData":
        def convert_enum(enum_type, value):
            if isinstance(value, enum_type):
                return value
            try:
                return enum_type(value)
            except (TypeError, ValueError):
                return enum_type[value]

        base_stats = {
            convert_enum(Stats, stat): int(value)
            for stat, value in data.get("base_stats", {}).items()
        }
        raw_types = data.get("types", [])
        types = (
            raw_types
            if isinstance(raw_types, enums.Typeslist)
            else enums.Typeslist([
                convert_enum(enums.TypeID, type_id) for type_id in raw_types
            ])
        )

        return cls(
            id=id,
            name=str(data["name"]),
            jpname=str(data["jpname"]),
            selectable_genders=cls.get_selectable_genders(data.get("gender_rate")),
            weight=int(data["weight"]),
            height=int(data["height"]),
            types=types,
            base_stats=base_stats,
            abilities=[ability["ability_id"] for ability in data.get("abilities", [])],
            learnt_moves=[int(move) for move in data.get("learnt_moves", [])],
        )

    @classmethod
    def create_from_id(cls, pokemon_id: int) -> "MasterPokemonData":
        """指定したIDのポケモンのマスターデータを返す。"""
        pokemon_data_dict = PokemonRepository._get_pokemon_by_id(pokemon_id)
        if pokemon_data_dict is None:
            raise ValueError(f"pokemon_id={pokemon_id} のデータが見つかりません。")
        return cls.from_dict(pokemon_data_dict, id=pokemon_id)

    @classmethod
    def get_all_pokemon(cls) -> dict[int, "MasterPokemonData"]:
        """全ポケモンのMasterPokemonDataを返す。

        Returns:
            マスターデータの全件リスト。
        """
        result: dict[int, MasterPokemonData] = {}
        for pokemon_id in PokemonRepository.get_pokemon_ids():
            pokemon_data_dict = PokemonRepository._get_pokemon_by_id(pokemon_id)
            if pokemon_data_dict is not None:
                pokemon_data = cls.from_dict(pokemon_data_dict, id=pokemon_id)
                result[pokemon_id] = pokemon_data
        return result

    def __str__(self):
        return f"{self.name} (ID: {self.id}) object"


print(
    MasterPokemonData.create_from_id(3)
)  # Example usage to create a MasterPokemonData instance for Pokémon ID 3


# =======================================================
# 構築後のポケモンクラス（インスタンスごとに違うもの）
# =======================================================
@dataclass(slots=True)
class BuiltPokemon:
    gender: enums.Genders = field(metadata={"description": "pokemon gender"})
    nature: enums.Natures = field(metadata={"description": "pokemon nature"})
    itemid: int = field(metadata={"description": "selected item id"})
    abilityid: int = field(metadata={"description": "selected ability id"})
    id: int = field(metadata={"description": "pokemon ID"})

    evs: Dict[Stats, int] = field(
        metadata={"description": "努力値"},
        default_factory=lambda: {
            Stats.HP: 0,
            Stats.ATTACK: 0,
            Stats.DEFENSE: 0,
            Stats.SPECIAL_ATTACK: 0,
            Stats.SPECIAL_DEFENSE: 0,
            Stats.SPEED: 0,
        },
    )
    movelist: List[int] = field(
        metadata={"description": "selected moves id"}, default_factory=list
    )


# =======================================================
# チームクラス
# =======================================================
@dataclass(slots=True)
class Team:
    """チームクラス"""

    teamname: str = field(metadata={"description": "team name"})
    pokemons: List[BuiltPokemon] = field(
        metadata={"description": "selected pokemons"}, default_factory=list
    )

    def __str__(self):
        return f"{self.teamname}"

    def to_dict(self) -> dict:
        """Convert this team and its Pokémon to a serializable dictionary.

        ``dataclasses.asdict`` recursively converts the ``Team`` instance and
        each nested ``BuiltPokemon`` instance into dictionaries.  The returned
        value can therefore be used when saving team data or preparing it for
        JSON serialization without modifying the original team object.

        Returns:
            dict: A dictionary containing the team's name and Pokémon data.
        """
        import dataclasses

        return dataclasses.asdict(self)


# =======================================================
# 戦闘用ポケモンクラス (BattlePokemon)
# =======================================================


@dataclass(slots=True)
class BattlePokemon:
    basic_data: MasterPokemonData
    built_data: BuiltPokemon
    real_stats: Dict[Stats, int] = field(
        metadata={"description": "実数値"},
        default_factory=lambda: {
            Stats.HP: 0,
            Stats.ATTACK: 0,
            Stats.DEFENSE: 0,
            Stats.SPECIAL_ATTACK: 0,
            Stats.SPECIAL_DEFENSE: 0,
            Stats.SPEED: 0,
        },
    )
    rank: Dict[Stats, int] = field(
        metadata={"description": "ランク"},
        default_factory=lambda: {
            Stats.HP: 0,
            Stats.ATTACK: 0,
            Stats.DEFENSE: 0,
            Stats.SPECIAL_ATTACK: 0,
            Stats.SPECIAL_DEFENSE: 0,
            Stats.SPEED: 0,
        },
    )

    def nature_change_rate(self, stat_name: str, ID: int) -> float:
        """Return the nature-based multiplier for the specified stat.

        Args:
            stat_name: Name of the stat to check.
            ID: Numeric ID of the Pokémon's nature.

        Returns:
            1.1 if the nature raises the stat, 0.9 if it lowers it,
            otherwise 1.0.
        """

        natures_path = "JSON/stat_change.json"
        with open(natures_path, "r") as j:
            natures_rate_file = json.load(j)
        if ID in natures_rate_file["natures"][stat_name]["rate_up"]:
            return 1.1
        elif ID in natures_rate_file["natures"][stat_name]["rate_dw"]:
            return 0.9
        else:
            return 1

    def calculate_real_stat(self, stat_name: str) -> int:
        """目的ステータス名を引数に実数値を返す

        Args:
            stat_name (str): 目的ステータス名

        Returns:
            int: 実数値
        """
        if stat_name == "HP":
            return self.base_stat[Stats.HP] + self.evs[Stats.HP] + 75
        else:
            change_rate = self.nature_change_rate(stat_name, self.built_data.nature)
            return int(
                (self.base_stat[Stats[stat_name]] + self.evs[Stats[stat_name]] + 20)
                * change_rate
            )

    def reset_ranks(self) -> None:
        """交代時や戦闘終了時にランクをすべて0に戻す"""
        for key in self.rank:
            self.rank[key] = 0

    def set_move(self, slot_index: int, move_id: int) -> None:
        """技スロット（0〜3）に技をセットする"""
        if 0 <= slot_index < 4:
            if move_id in self.basic_data.learnt_moves:
                self.built_data.movelist[slot_index] = move_id

    def to_dict(self) -> dict:
        """JSON化や保存用にデータクラスを辞書化する"""
        import dataclasses

        return dataclasses.asdict(self)

    @property
    def base_stat(self) -> Dict[Stats, int]:
        return self.basic_data.base_stats

    @property
    def evs(self) -> Dict[Stats, int]:
        return self.built_data.evs

    @property
    def nature(self) -> enums.Natures:
        return self.built_data.nature


# =======================================================
# battleteamクラス
# =======================================================


@dataclass(slots=True)
class BattleTeam:
    """バトル用のチームクラス"""

    teamname: str = field(metadata={"description": "team name"})
    pokemons: List[BattlePokemon] = field(
        metadata={"description": "selected pokemons"}, default_factory=list
    )
