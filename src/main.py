from player import Player
from board import Board
import random
from misc import clear_screen
from typing import Generator, Literal, Any, NoReturn

class Game:
    """Main Game class for managing the game loop, players, and board.
    """
    def __init__(self) -> None:
        self.running = True
        self.board = Board()
        self.player_1 = Player(self.board, "P1")
        self.player_2 = Player(self.board, "P2")
        self.players = [self.player_1, self.player_2]
        if self.board.board.head:
            self.board.board.head.current_players = [self.player_1, self.player_2]
        self.current_turn = self.turn()

    def turn(self) -> Generator[Literal[0, 1], Any, NoReturn]:
        """Generator for alternating turns between two players.

        Yields:
            Literal[0, 1]: Index of the current player.
        """
        while True:
            yield 0
            yield 1

    def mainloop(self) -> None:
        """Main loop for running the game until an end condition is met.
        """
        while self.running:
            current_player_index = next(self.current_turn)
            current_player = self.players[current_player_index]
            clear_screen()
            print(f"P1 money: {self.player_1.money} | P2 money: {self.player_2.money}")
            print()
            print(f"Current player: {current_player.name}")
            self.board.display()
            input("Roll the dice")
            dice_roll = random.randint(1, 6)
            clear_screen()
            current_player.move(dice_roll)
            print(f"P1 money: {self.player_1.money} | P2 money: {self.player_2.money}")
            print(f"{current_player.name} rolled: {dice_roll}")
            print(f"Current player: {current_player.name}")
            self.board.display()
            self.board.buy_part(current_player, self.player_1, self.player_2, current_player, dice_roll)
            if self.player_1.check_end_game(self.player_2) or self.player_2.check_end_game(self.player_1):
                clear_screen()
                self.running = False
                print(f"P1 money: {self.player_1.money} | P2 money: {self.player_2.money}")
                print()
                print(f"Current player: {current_player.name}")
                self.board.display()
                self.player_1.check_end_game(self.player_2)
                self.player_2.check_end_game(self.player_1)

if __name__ == "__main__":
    game = Game()
    game.mainloop()
