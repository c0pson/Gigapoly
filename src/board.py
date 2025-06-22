from misc import (
    SPECIAL_TILE,
    COMPONENT_TILE,
    TILE,
    GOOD_EFFECT,
    BAD_EFFECT,
    NEUTRAL_EFFECT,
    clear_screen
)
from random import shuffle, randrange
from typing import cast, TYPE_CHECKING
from cards import RiskCards, ChanceCards

if TYPE_CHECKING:
    from player import Player

class Node:
    """Represents a node in a circular graph structure for the game board.

    Each Node contains a reference to a tile, an optional owner, a list of players currently on the node,
    and links to the previous and next nodes, forming a circular doubly-linked list.
    """
    def __init__(self, tile: TILE) -> None:
        self.tile = tile
        self.owner: 'Player' | None = None
        self.current_players: list['Player'] = []
        self.prev: Node | None = None
        self.next: Node | None = None

class CircularGraph:
    """Represents the circular graph structure for the game board.

    The CircularGraph class manages a circular doubly-linked list of Node objects,
    where each Node represents a tile on the board.
    """
    def __init__(self) -> None:
        self.head: Node | None = None

    def add(self, tile: TILE) -> None:
        new_node = Node(tile)
        if not self.head:
            self.head = new_node
            self.head.next = new_node
            self.head.prev = new_node
        elif self.head.prev:
            tail = self.head.prev
            tail.next = new_node
            new_node.prev = tail
            new_node.next = self.head
            self.head.prev = new_node

class Board:
    """Represents the circular graph structure for the game board.

    The Board class manages all actions taken by players,
    and creates visual representation of the current state of the board.
    """
    def __init__(self) -> None:
        self.board: CircularGraph = self.create_board()
        self.chance_cards = ChanceCards()
        self.risk_cards = RiskCards()

    def create_board(self) -> CircularGraph:
        """Creates randomly generated board.

        Returns:
            CircularGraph: Circular graph representing the board.
        """
        tiles: list[TILE] = cast(list[TILE], list(SPECIAL_TILE) + list(COMPONENT_TILE) * 2)
        tiles.remove(SPECIAL_TILE.START)
        shuffle(tiles)
        cg = CircularGraph()
        cg.add(SPECIAL_TILE.START)
        for tile in tiles:
            cg.add(tile)
        return cg

    def move_player(self, player: 'Player', steps: int) -> None:
        """Moves player by specified amount of steps.

        Args:
            player (Player): Player to move.
            steps (int): Amount of steps the player is taking.
        """
        if not player.current_position:
            return
        if player in player.current_position.current_players:
            player.current_position.current_players.remove(player)
        new_position = player.current_position
        for _ in range(steps):
            if new_position.next:
                new_position = new_position.next
                if new_position == self.board.head:
                    player.add_start_money()
        new_position.current_players.append(player)
        player.current_position = new_position

    def move_player_to_position(self, player: 'Player', position_number: int) -> None:
        """Moves player to specific position on board.

        Args:
            player (Player): Player to move.
            position_number (int): Number on the tile to which player is being moved.
        """
        if position_number < 1 or position_number > 16:
            return
        if player.current_position and player in player.current_position.current_players:
            player.current_position.current_players.remove(player)
        current = self.board.head
        if current and current.next:
            for _ in range(position_number - 1):
                current = current.next
            current.current_players.append(player)
        player.current_position = current

    def get_chance(self, player: 'Player', other_player: 'Player') -> None:
        """Handles the effect of a Chance card for the player.

        Args:
            player (Player): Player drawing the Chance card.
            other_player (Player): Other player in the game.
        """
        effect = self.chance_cards.use_card()
        match effect:
            case GOOD_EFFECT.RAISE:
                input("Claim 500$")
                player.money += 500
            case GOOD_EFFECT.BONUS:
                input("Claim 400$")
                player.money += 400
            case GOOD_EFFECT.ADVANCE:
                input("Move by 3 tiles")
                self.move_player(player, 3)
                clear_screen()
                print(f"P1 money: {player.money} | P2 money: {other_player.money}")
                print()
                print(f"Current player: {player.name}")
                self.display()
                self.buy_part(player, player, other_player, player, None)
            case GOOD_EFFECT.MOVE:
                input("Roll the dice")
                dice_roll = randrange(1, 7)
                self.move_player(player, dice_roll)
                clear_screen()
                player.move(dice_roll)
                print(f"P1 money: {player.money} | P2 money: {other_player.money}")
                print(f"{player.name} rolled: {dice_roll}")
                print(f"Current player: {player.name}")
                self.display()
                self.buy_part(player, player, other_player, player, dice_roll)
            case _:
                pass

    def get_risk(self, player: 'Player', other_player: 'Player') -> None:
        """Handles the effect of a Risk card for the player.

        Args:
            player (Player): Player drawing the Risk card.
            other_player (Player): Other player in the game.
        """
        effect = self.risk_cards.use_card()
        match effect:
            case GOOD_EFFECT.RAISE:
                input("Claim 500$")
                player.money += 500
            case GOOD_EFFECT.BONUS:
                input("Claim 400$")
                player.money += 400
            case GOOD_EFFECT.ADVANCE:
                input("Move by 3 tiles")
                clear_screen()
                self.move_player(player, 3)
                print(f"P1 money: {player.money} | P2 money: {other_player.money}")
                print()
                print(f"Current player: {player.name}")
                self.display()
                self.buy_part(player, player, other_player, player, None)
            case GOOD_EFFECT.MOVE:
                input("Roll the dice")
                dice_roll = randrange(1, 7)
                self.move_player(player, dice_roll)
                clear_screen()
                print(f"P1 money: {player.money} | P2 money: {other_player.money}")
                print(f"{player.name} rolled: {dice_roll}")
                print(f"Current player: {player.name}")
                self.display()
                self.buy_part(player, player, other_player, player, dice_roll)
            case BAD_EFFECT.LOOSE:
                input("You are loosing 300$ ")
                player.money -= 300
            case NEUTRAL_EFFECT.NOTHING:
                input("Nothing ever happens")
            case _:
                pass

    def handle_buying(self, player: 'Player', other_player: 'Player') -> None:
        """Handles the logic for a player buying a component tile or paying rent to another player.

        Args:
            player (Player): Player taking the action.
            other_player (Player): Other player in the game.
        """
        if player.current_position and player.current_position.owner:
                if player.current_position.owner == player:
                    return
                elif isinstance(player.current_position.tile, COMPONENT_TILE):
                    player.money -= player.current_position.tile.value
                    other_player.money += player.current_position.tile.value
        elif player.current_position and isinstance(player.current_position.tile, COMPONENT_TILE) and player.money >= player.current_position.tile.value:
            user_input = ""
            while user_input not in {"yes", "no"}:
                user_input = input("Are you willing to buy this part [yes | no]: ")
                if user_input == "yes":
                    player.current_position.owner = player
                    player.money -= player.current_position.tile.value
                    player.add_owned_part(player.current_position.tile)

    def buy_part(self, player: 'Player', player_1, player_2, current_player, dice_roll) -> None:
        """Handles the logic for a player attempting to buy a part or triggering special tile actions.

        Args:
            player (Player): Player taking the action.
            player_1 (Player): First player in the game.
            player_2 (Player): Second player in the game.
            current_player (Player): Player whose turn it currently is.
            dice_roll (int | None): The value of the dice roll, if applicable.
        """
        if player.current_position and player.current_position.owner:
            self.handle_buying(player, player_1 if player_1 != current_player else player_2)
        self.handle_buying(player, player_2)
        if player.current_position and isinstance(player.current_position.tile, SPECIAL_TILE):
            user_input_: int = -1
            match player.current_position.tile:
                case SPECIAL_TILE.CHANCE:
                    self.get_chance(player, player_1 if current_player != player_1 else player_2)
                case SPECIAL_TILE.RISK:
                    self.get_risk(player, player_1 if current_player != player_1 else player_2)
                case SPECIAL_TILE.TRAVEL:
                    while user_input_ < 1 or user_input_ > 16:
                        try:
                            user_input_ = int(input("Enter tile number u want to travel to [1 - 16]: "))
                        except ValueError:
                            user_input_ = 0
                    self.move_player_to_position(player, user_input_)
                    clear_screen()
                    print(f"P1 money: {player_1.money} | P2 money: {player_2.money}")
                    print(f"{current_player.name} rolled: {dice_roll}") if dice_roll else print()
                    print(f"Current player: {current_player.name}")
                    self.display()
                    self.buy_part(player, player_2, player_2, current_player, dice_roll)
                case _:
                    pass

    @staticmethod
    def draw_separator(row_idx: int) -> None:
        """Prints a separator line for a board display based on the given row index.

        Args:
            row_idx (int): The index of the row for which the separator should be drawn.
        """
        if row_idx == 0:
            print("┌────────" + "┬────────" * 4 + "┐")
        elif row_idx == 1:
            print("├────────" + "┼────────" + "┴────────" * 2 + "┼────────" + "┤")
        elif row_idx == 4:
            print("├────────" + "┼────────" + "┬────────" * 2 + "┼────────" + "┤")
        elif row_idx == 5:
            print("└────────" + "┴────────" * 4 + "┘")
        elif row_idx == 3:
            print("├────────┤ " + " " * 9 + "c0pson" + " " * 9 + " ├────────┤")
        else:
            print("├────────┤ " + " " * 8 + "GIGAPOLY" + " " * 8 + " ├────────┤")

    @staticmethod
    def get_position_number(row_idx: int, col_idx: int) -> int:
        """Returns the board position number for a given row and column index.

        Args:
            row_idx (int): Row index on the board grid.
            col_idx (int): Column index on the board grid.

        Returns:
            int: The position number on the board corresponding to the given indices.
        """
        border_pos_map = {
            (0, 0): 1,  (0, 1): 2,
            (0, 2): 3,  (0, 3): 4,
            (0, 4): 5,  (1, 4): 6,
            (2, 4): 7,  (3, 4): 8,
            (4, 4): 9,  (4, 3): 10,
            (4, 2): 11, (4, 1): 12,
            (4, 0): 13, (3, 0): 14,
            (2, 0): 15, (1, 0): 16
        }
        return border_pos_map.get((row_idx, col_idx), 0)

    @staticmethod
    def get_owner_display(node: Node) -> str:
        """Returns a string representation of the owner of a given node.

        Args:
            node (Node): Object representing a node on the board.

        Returns:
            str: The name of the owner if the node and its owner exist, otherwise '--'.
        """
        if not node or not node.owner:
            return "--"
        return node.owner.name

    @staticmethod
    def get_players_display(node: Node) -> str:
        """Returns a formatted string displaying the names of the current players at a given node,
        with color coding based on player name (yellow for names containing "1", green otherwise).

        Args:
            node (Node): Object representing a node on the board.

        Returns:
            str: A formatted string of player names with ANSI color codes.
        """
        if not node or not node.current_players:
            return ""
        player_names = [f"{"\033[33m" if "1" in player.name else "\033[32m"}{player.name}\033[0m" for player in node.current_players]
        return " ".join(player_names) + "  " * (int(2 / len(player_names))) + " " * (int(2 / len(player_names)))

    def draw_cell_lines(self, row: list[TILE], row_idx: int, temp_nodes: list[list[Node]]) -> None:
        """Draws the content lines for each cell in a board row.

        Args:
            row (list[TILE]): The row of tiles to draw.
            row_idx (int): The index of the row.
            temp_nodes (list[list[Node]]): Temporary node data for the board.
        """
        for line in range(4):
            if row_idx in {0, 4}:
                out = ""
                for col_idx, cell in enumerate(row):
                    content = ""
                    node = temp_nodes[row_idx][col_idx]
                    pos_num = self.get_position_number(row_idx, col_idx)
                    if line == 0:
                        players_str = self.get_players_display(node)
                        content = players_str.center(8)
                    elif line == 1 and cell != 0:
                        content = str(cell.name).center(8)
                    elif line == 2:
                        if node:
                            owner_str = self.get_owner_display(node)
                            content = owner_str.center(8)
                        else:
                            content = " " * 8
                    elif line == 3:
                        if pos_num > 0:
                            content = f"{pos_num:<8}"
                        else:
                            content = " " * 8
                    else:
                        content = " " * 8
                    out += "│" + content
                out += "│"
                print(out)
            else:
                left_cell = row[0]
                right_cell = row[4]
                left_node = temp_nodes[row_idx][0]
                right_node = temp_nodes[row_idx][4]
                left_content = ""
                right_content = ""
                left_pos = self.get_position_number(row_idx, 0)
                right_pos = self.get_position_number(row_idx, 4)
                if line == 0:
                    left_players = self.get_players_display(left_node)
                    right_players = self.get_players_display(right_node)
                    left_content = left_players.center(8)
                    right_content = right_players.center(8)
                elif line == 1:
                    if left_cell != 0:
                        left_content = str(left_cell.name).center(8)
                    else:
                        left_content = " " * 8
                    if right_cell != 0:
                        right_content = str(right_cell.name).center(8)
                    else:
                        right_content = " " * 8
                elif line == 2:
                    left_owner = self.get_owner_display(left_node)
                    right_owner = self.get_owner_display(right_node)
                    left_content = left_owner.center(8)
                    right_content = right_owner.center(8)
                elif line == 3:
                    if left_pos > 0:
                        left_content = f"{left_pos:<8}"
                    else:
                        left_content = " " * 8
                    if right_pos > 0:
                        right_content = f"{right_pos:<8}"
                    else:
                        right_content = " " * 8
                else:
                    left_content = " " * 8
                    right_content = " " * 8
                print("│" + left_content + "│" + " " * 26 + "│" + right_content + "│")

    def display(self) -> None:
        """Displays the current state of the board by mapping tiles and nodes to a 5x5 grid.
        """
        temp_board: list[list[TILE]] = cast(list[list[TILE]], [[0 for _ in range(5)] for _ in range(5)])
        temp_nodes: list[list[Node]] = cast(list[list[Node]], [[None for _ in range(5)] for _ in range(5)])
        border_positions: list[tuple[int, int]] = [
            (0, 0), (0, 1), (0, 2), (0, 3),
            (0, 4), (1, 4), (2, 4), (3, 4),
            (4, 4), (4, 3), (4, 2), (4, 1),
            (4, 0), (3, 0), (2, 0), (1, 0)
        ]
        current = self.board.head
        for row, col in border_positions:
            if current:
                temp_board[row][col] = current.tile
                temp_nodes[row][col] = current
                current = current.next
        for i, row_ in enumerate(temp_board):
            self.draw_separator(i)
            self.draw_cell_lines(row_, i, temp_nodes)
        self.draw_separator(5)
