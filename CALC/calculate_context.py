from dataclasses import dataclass

from MOVE import move_object
from POKEMON import pokemon_object


@dataclass(slots=True, frozen=True)
class CalculateContext:
    """計算のコンテキストを管理するクラス。"""

    attacker: pokemon_object.BattlePokemon
    defender: pokemon_object.BattlePokemon
    move: move_object.MasterMove
