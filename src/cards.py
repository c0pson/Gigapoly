from misc import EFFECT, GOOD_EFFECT, BAD_EFFECT, NEUTRAL_EFFECT
from abc import ABC, abstractmethod
from random import shuffle
from typing import TypeVar, Generic

T = TypeVar("T", bound=EFFECT)

class Cards(ABC, Generic[T]):
    def __init__(self) -> None:
        self.deck: list[T] = self.create_deck()

    @abstractmethod
    def create_deck(self) -> list[T]:
        pass

    def shuffle_deck(self, deck: list[T]) -> list[T]:
        shuffle(deck)
        return deck

    def use_card(self) -> T:
        if not len(self.deck):
            self.deck = self.create_deck()
        return self.deck.pop()

class RiskCards(Cards[EFFECT]):
    def create_deck(self) -> list[EFFECT]:
        return self.shuffle_deck(
            [e for e in GOOD_EFFECT] + [e for e in BAD_EFFECT] + [e for e in NEUTRAL_EFFECT]
        )

class ChanceCards(Cards[GOOD_EFFECT]):
    def create_deck(self) -> list[GOOD_EFFECT]:
        return self.shuffle_deck(list(GOOD_EFFECT))
