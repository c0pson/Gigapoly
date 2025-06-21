from enum import IntEnum, StrEnum
from typing import Union

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
