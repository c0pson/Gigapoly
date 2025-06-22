from typing import TYPE_CHECKING
from misc import COMPONENT_TILE

if TYPE_CHECKING:
    from board import Board
    from board import Node

class Player:
    """Represents a player in the game."""
    def __init__(self, board: 'Board', name: str) -> None:
        self.board: 'Board' = board
        self.name: str = name
        self.money: int = 10_000
        self.current_position: 'Node' | None = board.board.head
        self.owned_parts: list[COMPONENT_TILE] = []
        self.all_parts = [e for e in COMPONENT_TILE if e != COMPONENT_TILE.SERVICE]

    def move(self, steps: int) -> None:
        """Moves player by the amount of steps.

        Args:
            steps (int): Number of steps.
        """
        self.board.move_player(self, steps)

    def move_to(self, position: int) -> None:
        """Moves player to specific position on board.

        Args:
            position (int): Number on the tile to which player is being moved.
        """
        self.board.move_player_to_position(self, position)

    def add_start_money(self) -> None:
        """Adds funds to the player.
        """
        self.money += 1000

    def check_end_game(self, other: 'Player') -> bool:
        """Checks if player passes wining or loosing condition.

        Args:
            other (Player): Other player in the game.

        Returns:
            bool: True if conditions are passed False otherwise.
        """
        if self.money <= 0:
            print(f"{self.name} bankrupted. {other.name} wins the game")
            return True
        else:
            if len(set(self.owned_parts)) == len(self.all_parts):
                print(f"{self.name} won the game")
                return True
        return False

    def add_owned_part(self, part: COMPONENT_TILE) -> None:
        """Appends list of owned PC parts to list of items owned by player.

        Args:
            part (COMPONENT_TILE): Component to add to list.
        """
        if part == COMPONENT_TILE.SERVICE:
            return
        self.owned_parts.append(part)
