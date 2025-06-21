from misc import SPECIAL_TILE, COMPONENT_TILE, TILE
from random import shuffle
from typing import cast, TYPE_CHECKING
import os

if TYPE_CHECKING:
    from player import Player

class Node:
    def __init__(self, tile: TILE) -> None:
        self.tile = tile
        self.owner: 'Player' | None = None
        self.current_players: list['Player'] = []
        self.prev: Node | None = None
        self.next: Node | None = None

class CircularGraph:
    def __init__(self) -> None:
        self.head: Node | None = None

    def add(self, tile: TILE) -> None:
        new_node = Node(tile)
        if not self.head:
            self.head = new_node
            self.head.next = new_node
            self.head.prev = new_node
        else:
            tail = self.head.prev
            tail.next = new_node                    # type: ignore
            new_node.prev = tail
            new_node.next = self.head
            self.head.prev = new_node

class Board:
    def __init__(self) -> None:
        self.board: CircularGraph = self.create_board()

    def create_board(self) -> CircularGraph:
        tiles: list[TILE] = cast(list[TILE], list(SPECIAL_TILE) + list(COMPONENT_TILE) * 2)
        tiles.remove(SPECIAL_TILE.START)
        shuffle(tiles)
        cg = CircularGraph()
        cg.add(SPECIAL_TILE.START)
        for tile in tiles:
            cg.add(tile)
        return cg

    def move_player(self, player: 'Player', steps: int) -> None:
        if not player.current_position:
            return
        if player in player.current_position.current_players:
            player.current_position.current_players.remove(player)
        new_position = player.current_position
        for _ in range(steps):
            new_position = new_position.next        # type: ignore
        new_position.current_players.append(player)
        player.current_position = new_position
    
    def move_player_to_position(self, player: 'Player', position_number: int) -> None:
        if position_number < 1 or position_number > 16:
            return
        if player.current_position and player in player.current_position.current_players:
            player.current_position.current_players.remove(player)
        current = self.board.head
        for _ in range(position_number - 1):
            current = current.next                  # type: ignore
        current.current_players.append(player)      # type: ignore
        player.current_position = current

    def get_chance(self, player: 'Player') -> None:
        pass

    def get_risk(self, player: 'Player') -> None:
        pass

    def handle_buying(self, player: 'Player') -> None:
        if player.current_position.owner:                               # type: ignore
            return
        if isinstance(player.current_position.tile, COMPONENT_TILE) and player.money >= player.current_position.tile.value:  # type: ignore
            user_input = ""
            while user_input not in {"yes", "no"}:
                user_input = input("Are you willing to buy this part [yes | no]: ")
                if user_input == "yes":
                    player.current_position.owner = player              # type: ignore
                    player.money -= player.current_position.tile.value  # type: ignore

    def buy_part(self, player: 'Player', player_1, player_2, current_player, dice_roll) -> None:
        if player.current_position.owner:                               # type: ignore
            return
        self.handle_buying(player)
        if isinstance(player.current_position.tile, SPECIAL_TILE):      # type: ignore
            user_input_: int = -1
            match player.current_position.tile:                         # type: ignore
                case SPECIAL_TILE.CHANCE:
                    self.get_chance(player)
                case SPECIAL_TILE.RISK:
                    self.get_risk(player)
                case SPECIAL_TILE.TRAVEL:
                    while user_input_ < 1 or user_input_ > 16:
                        try:
                            user_input_ = int(input("Enter tile number u want to travel to [1 - 16]: "))
                        except ValueError:
                            user_input_ = 0
                    self.move_player_to_position(player, user_input_)
                    os.system("cls")
                    print(f"P1 money: {player_1.money} | P2 money: {player_2.money}")
                    print(f"{current_player.name} rolled: {dice_roll}")
                    print(f"Current player: {current_player.name}")
                    self.display()
                    self.handle_buying(player)
                case _:
                    pass

    def display(self) -> None:
        temp_board = [[0 for _ in range(5)] for _ in range(5)]
        temp_nodes = [[None for _ in range(5)] for _ in range(5)]
        border_positions = [
            (0, 0), (0, 1), (0, 2), (0, 3),
            (0, 4), (1, 4), (2, 4), (3, 4),
            (4, 4), (4, 3), (4, 2), (4, 1),
            (4, 0), (3, 0), (2, 0), (1, 0)
        ]
        current = self.board.head
        for row, col in border_positions:
            temp_board[row][col] = current.tile     # type: ignore
            temp_nodes[row][col] = current          # type: ignore
            current = current.next                  # type: ignore

        def draw_separator(row_idx: int) -> None:
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

        def get_players_display(node) -> str:
            if not node or not node.current_players:
                return ""
            player_names = [f"{"\033[33m" if "1" in player.name else "\033[32m"}{player.name}\033[0m" for player in node.current_players]
            return " ".join(player_names) + "  " * (int(2 / len(player_names))) + " " * (int(2 / len(player_names)))

        def get_position_number(row_idx: int, col_idx: int) -> int:
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

        def get_owner_display(node) -> str:
            if not node or not node.owner:
                return "--"
            return node.owner.name

        def draw_cell_lines(row: list, row_idx: int) -> None:
            for line in range(4):
                if row_idx in {0, 4}:
                    out = ""
                    for col_idx, cell in enumerate(row):
                        content = ""
                        node = temp_nodes[row_idx][col_idx]
                        pos_num = get_position_number(row_idx, col_idx)
                        if line == 0:
                            players_str = get_players_display(node)
                            content = players_str.center(8)
                        elif line == 1 and cell != 0:
                            content = str(cell.name).center(8)
                        elif line == 2:
                            if node:
                                owner_str = get_owner_display(node)
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
                    left_pos = get_position_number(row_idx, 0)
                    right_pos = get_position_number(row_idx, 4)
                    if line == 0:
                        left_players = get_players_display(left_node)
                        right_players = get_players_display(right_node)
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
                        left_owner = get_owner_display(left_node)
                        right_owner = get_owner_display(right_node)
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
        for i, row in enumerate(temp_board):    # type: ignore
            draw_separator(i)
            draw_cell_lines(row, i)             # type: ignore
        draw_separator(5)
