from enum import IntEnum, StrEnum
from typing import Union
import os

class COMPONENT_TILE(IntEnum):
    GPU = 2000
    CPU = 1500
    MEM = 600
    RAM = 700
    NIC = 500  # network internet protocol (NIC)
    SERVICE = 800

class SPECIAL_TILE(StrEnum):
    START = "start"
    CHANCE = "chance"
    RISK = "risk"
    TRAVEL = "travel"

TILE = Union[SPECIAL_TILE, COMPONENT_TILE]

class GOOD_EFFECT(StrEnum):
    RAISE = "raise"
    MOVE = "move"
    BONUS = "bonus"
    ADVANCE = "advance"

class BAD_EFFECT(StrEnum):
    LOOSE = "loose"

class NEUTRAL_EFFECT(StrEnum):
    NOTHING = "nothing"

EFFECT = Union[GOOD_EFFECT, BAD_EFFECT, NEUTRAL_EFFECT]

def clear_screen() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')
