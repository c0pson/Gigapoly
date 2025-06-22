from misc import EFFECT, GOOD_EFFECT, BAD_EFFECT, NEUTRAL_EFFECT
from abc import ABC, abstractmethod
from random import shuffle
from typing import TypeVar, Generic

T = TypeVar("T", bound=EFFECT)

class Cards(ABC, Generic[T]):
    """
    Abstract base class representing a generic deck of cards.
    Provides a template for creating, shuffling, and using cards from a deck.
    """
    def __init__(self) -> None:
        self.deck: list[T] = self.create_deck()

    @abstractmethod
    def create_deck(self) -> list[T]:
        """Abstract method for creating shuffled deck of cards.

        Returns:
            list[T]: Shuffled deck of cards.
        """
        pass

    def shuffle_deck(self, deck: list[T]) -> list[T]:
        """Shuffles the deck of cards.

        Args:
            deck (list[T]): Deck of cards

        Returns:
            list[T]: Shuffled deck of cards.
        """
        shuffle(deck)
        return deck

    def use_card(self) -> T:
        """Returns the card from the deck of cards if not empty. Creates a new one if empty and returns the card.

        Returns:
            T: Card.
        """
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
