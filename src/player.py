from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from board import Board
    from board import Node

class Player:
    def __init__(self, board: 'Board', name: str) -> None:
        self.board: 'Board' = board
        self.name: str = name
        self.money: int = 10_000
        self.current_position: 'Node' | None = board.board.head
    
    def move(self, steps: int) -> None:
        self.board.move_player(self, steps)
    
    def move_to(self, position: int) -> None:
        self.board.move_player_to_position(self, position)

    def add_start_money(self) -> None:
        self.money += 1000
