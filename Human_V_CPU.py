import pygame
import pygame.freetype
import time
import random
import copy
import math


class Player:
    def __init__(self, name, symbol, turn, moves=0, win=False):
        self.name = name
        self.symbol = symbol
        self.turn = turn
        self.moves = moves
        self.win = win

    def inc_moves(self):
        self.moves += 1

    def swap_turn(self):
        if self.turn:
            self.turn = False
        else:
            self.turn = True


class Board:
    def __init__(self, sim_count=1, complete=False, full=False):
        self.possible = [[5, 0], [5, 1], [5, 2], [5, 3], [5, 4], [5, 5], [5, 6]]
        self.grid = create_grid()
        self.complete = complete
        self.full = full
        self.sim_count = sim_count
        self.useful_positions = {}

    def display(self):
        for x in self.grid:
            print(x)

    def update_grid(self, player: Player, location: int):
        if location in [1, 2, 3, 4, 5, 6, 7]:
            for row in range(len(self.grid) - 1, -1, -1):
                if self.grid[row][location - 1] == '0':
                    if player.name == "Player_1":
                        self.grid[row][location - 1] = '1'
                        player.moves += 1
                    else:
                        self.grid[row][location - 1] = '2'
                        player.moves += 1
                    break

    def check_full(self):
        count = 0
        for row in self.grid:
            if len(set(row)) <= 1:
                count += 1
        if count == 6:
            self.full = True

    def possible_drops(self):
        for item in self.possible:
            x = item[1]
            y = item[0]
            if y > 0:
                if (self.grid[y][x] != '0') and (self.grid[y - 1][x] == '0'):
                    self.possible.remove([y, x])
                    self.possible.append([y - 1, x])
                    break

            else:
                self.possible.remove([y, x])

    def check_grid(self):
        for row in range(6):
            for index in range(4):
                if (self.grid[row][index] == '1') and (self.grid[row][index + 1] == '1') and (
                        self.grid[row][index + 2] == '1') and (self.grid[row][index + 3] == '1'):
                    self.complete = True
                if (self.grid[row][index] == '2') and (self.grid[row][index + 1] == '2') and (
                        self.grid[row][index + 2] == '2') and (self.grid[row][index + 3] == '2'):
                    self.complete = True
        for row in range(3):
            for index in range(7):
                if (self.grid[row][index] == '1') and (self.grid[row + 1][index] == '1') and (
                        self.grid[row + 2][index] == '1') and (self.grid[row + 3][index] == '1'):
                    self.complete = True
                if (self.grid[row][index] == '2') and (self.grid[row + 1][index] == '2') and (
                        self.grid[row + 2][index] == '2') and (self.grid[row + 3][index] == '2'):
                    self.complete = True

        for row in range(3):
            for index in range(4):
                if (self.grid[row][index] == '1') and (self.grid[row + 1][index + 1] == '1') and (
                        self.grid[row + 2][index + 2] == '1') and (self.grid[row + 3][index + 3] == '1'):
                    self.complete = True
                if (self.grid[row][index] == '2') and (self.grid[row + 1][index + 1] == '2') and (
                        self.grid[row + 2][index + 2] == '2') and (self.grid[row + 3][index + 3] == '2'):
                    self.complete = True

        for row in range(3, 6):
            for index in range(4):
                if (self.grid[row][index] == '1') and (self.grid[row - 1][index + 1] == '1') and (
                        self.grid[row - 2][index + 2] == '1') and (self.grid[row - 3][index + 3] == '1'):
                    self.complete = True
                if (self.grid[row][index] == '2') and (self.grid[row - 1][index + 1] == '2') and (
                        self.grid[row - 2][index + 2] == '2') and (self.grid[row - 3][index + 3] == '2'):
                    self.complete = True


def create_grid() -> list:
    """
    Creates a 7x6 grid filled with 0's
    """
    grid = []
    for x in range(6):
        grid.append([])
        for y in range(7):
            grid[x].append('0')

    return grid


def scoring(chain: int) -> int:
    if chain == 1:
        return 0
    elif chain == 2:
        return 5
    elif chain == 3:
        return 15
    else:
        return 0

    # chain for 4 should not exist as that would be game over


def check_chains(board: Board, drop: list, player: Player) -> int:
    """
    This checks the chaining placements of a player and returns how many placements touch in all
    playable directions for scoring purposes
    """
    total = 0

    drop_y = drop[0]
    drop_x = drop[1]

    # This checks horizontal chains
    cont_left = True
    cont_right = True
    horizontal_total = 1
    for spot in range(1, 5):
        try:
            if (drop_x + spot <= 6) and (cont_right == True):
                if board.grid[drop_y][drop_x + spot] == player.symbol:
                    horizontal_total += 1
                else:
                    cont_right = False
            if drop_x - spot >= 0 and (cont_left == True):
                if board.grid[drop_y][drop_x - spot] == player.symbol:
                    horizontal_total += 1
                else:
                    cont_left = False
        except:
            pass

    total += scoring(horizontal_total)

    # This checks vertical chains
    cont_down = True
    vert_total = 1
    for spot in range(1, 5):
        try:
            if (drop_y + spot >= 0) and (cont_down == True):
                if board.grid[drop_y + spot][drop_x] == player.symbol:
                    vert_total += 1
                else:
                    cont_down = False
        except:
            pass

    total += scoring(vert_total)

    # This checks diagonal with positive slope
    cont_diag_pos_right = True
    cont_diag_pos_left = True
    diag_pos_total = 1
    for spot in range(1, 5):
        try:
            if (drop_y - spot >= 0) and (drop_x + spot <= 6) and (cont_diag_pos_right == True):
                if board.grid[drop_y - spot][drop_x + spot] == player.symbol:
                    diag_pos_total += 1
                else:
                    cont_diag_pos_right = False

            if (drop_y + spot <= 5) and (drop_x - spot >= 0) and (cont_diag_pos_left == True):
                if board.grid[drop_y + spot][drop_x - spot] == player.symbol:
                    diag_pos_total += 1
                else:
                    cont_diag_pos_left = False
        except:
            pass

    total += scoring(diag_pos_total)

    # This checks diagonal with negative slope
    cont_diag_neg_left = True
    cont_diag_neg_right = True
    diag_neg_total = 1
    for spot in range(1, 5):
        try:
            if (drop_y + spot <= 5) and (drop_x + spot <= 6) and (cont_diag_neg_right == True):
                if board.grid[drop_y + spot][drop_x + spot] == player.symbol:
                    diag_neg_total += 1
                else:
                    cont_diag_neg_right = False

            if (drop_y - spot >= 0) and (drop_x - spot >= 0) and (cont_diag_neg_left == True):
                if board.grid[drop_y - spot][drop_x - spot] == player.symbol:
                    diag_neg_total += 1
                else:
                    cont_diag_neg_left = False
        except:
            pass

    total += scoring(diag_neg_total)

    return total


def possible_totals(board: Board, player) -> dict:
    children_dicts = {}
    for item in board.possible:
        value = (check_chains(board, item, player))
        item = tuple(item)
        children_dicts[item] = value

    return children_dicts


def children_output(children: dict):
    for item in children:
        print(item, ":", children[item])


def monte_carlo_bounds(children: dict, results: list, board: Board) -> dict:
    """
    S =  x + C * sqrt((ln(t)/n)
    S = value
    x = mean value
    C = some constant
    t = number of simulations
    n = number of visits to node
    """
    if not results:
        pass
    else:
        outcome = results[0]
        if outcome:
            winning_multiplier = 2
        else:
            winning_multiplier = 1

        path = results[1]
        for item in path:
            if item not in board.useful_positions:
                board.useful_positions[item] = (1 * winning_multiplier)
            if item in board.useful_positions:
                temp = board.useful_positions[item]
                temp += (1 * winning_multiplier)
                board.useful_positions[item] = temp

    depth_size = len(children)
    for item in children:

        if item not in board.useful_positions:
            visited = 1
        else:
            visited = board.useful_positions[item]

        current = children[item]
        total = (current / depth_size) + random.uniform(0, 1) * math.sqrt((math.log(board.sim_count) / visited))
        children[item] = [current, total]

    return children


def AI_place(children: dict, board: Board, player: Player):
    winner = 0
    spot = 0
    for item in children:
        if children[item][1] > winner:
            winner = children[item][1]
            spot = item

    board.update_grid(player, spot[1] + 1)


def AI_moves(children: dict) -> tuple:
    winner = 0
    spot = 0
    for item in children:
        if children[item][1] > winner:
            winner = children[item][1]
            spot = item

    return spot


def simulation(board: Board, AI: Player, Player_1: Player, current=None) -> list:
    board.sim_count += 1
    sim_board = copy.deepcopy(board)
    AI_2 = copy.deepcopy(Player_1)
    AI_sim = copy.deepcopy(AI)

    AI_sim_moves = []

    while (sim_board.complete == False) and (sim_board.full == False):

        if AI_2.turn & (AI_2.moves == AI_sim.moves):
            current = AI_2

        if AI_sim.turn & (AI_2.moves != AI_sim.moves):
            current = AI_sim

        AI_2.swap_turn()
        AI_sim.swap_turn()

        if current == AI_sim:
            dictionary = possible_totals(sim_board, AI_sim)
            dictionary = monte_carlo_bounds(dictionary, [], board)
            AI_place(dictionary, sim_board, AI_sim)
            AI_sim_moves.append(AI_moves(dictionary))
            sim_board.possible_drops()
            sim_board.check_grid()
            sim_board.check_full()
            if sim_board.complete:
                AI_sim.win = True

        if current == AI_2:
            dictionary = possible_totals(sim_board, AI_2)
            dictionary = monte_carlo_bounds(dictionary, [], board)
            AI_place(dictionary, sim_board, AI_2)
            sim_board.possible_drops()
            sim_board.check_grid()
            sim_board.check_full()
            if sim_board.complete:
                AI_2.win = True

    """
    print("AI_sim win =", AI_sim.win)
    print("AI_2 win =", AI_2.win)
    print("Board complete ->", sim_board.complete)
    print("Board full ->", sim_board.full)
    sim_board.display()
    """

    contents = [AI_sim.win, AI_sim_moves]

    return contents


def drop_location(location: tuple) -> int:
    """
    This takes the clicked location and assigns an integer value collaborated with a column slot
    Also allows for the menu button to be clicked
    """
    x = location[0]
    y = location[1]
    if (x > 300) and (x < 350) and (y > 175) and (y < 225):
        return 1
    elif (x > 355) and (x < 405) and (y > 175) and (y < 225):
        return 2
    elif (x > 410) and (x < 460) and (y > 175) and (y < 225):
        return 3
    elif (x > 465) and (x < 520) and (y > 175) and (y < 225):
        return 4
    elif (x > 525) and (x < 575) and (y > 175) and (y < 225):
        return 5
    elif (x > 580) and (x < 630) and (y > 175) and (y < 225):
        return 6
    elif (x > 635) and (x < 685) and (y > 175) and (y < 225):
        return 7
    elif (x > 35) and (x < 115) and (y > 390) and (y < 430):
        return 8
    # made for menu
    else:
        return 0


def play():
    pygame.init()

    # VARIABLES FOR COLOR CONSISTENCY
    white = (255, 255, 255)
    red = (200, 0, 0)
    green = (0, 200, 0)
    black = (0, 0, 0)

    # DISTANCES FOR CONSISTENCY
    WIDTH = 1000
    HEIGHT = 800
    MARGIN = 5
    LEFT_D = 300
    BLOCK_SIZE = 50

    GAME_FONT = pygame.freetype.Font(None, 24)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    Player_1 = Player("Player_1", '1', True)
    AI = Player("Player_2", '2', False)
    board = Board()

    # Run until the user asks to quit
    running = True
    while running:

        if Player_1.turn & (Player_1.moves == AI.moves):
            current = Player_1

        if AI.turn & (Player_1.moves != AI.moves):
            current = AI

        Player_1.swap_turn()
        AI.swap_turn()

        if current == Player_1:
            # Did the user click the window close button?
            for event in pygame.event.get():  # User did something
                if event.type == pygame.QUIT:  # If user clicked close
                    running = False  # Flag that we are done so we exit this loop
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # User clicks the mouse. Get the position
                    pos = pygame.mouse.get_pos()
                    board.update_grid(current, drop_location(pos))
                    board.possible_drops()
                    board.check_grid()
                    board.check_full()
                    if board.complete:
                        Player_1.win = True

        if current == AI:
            sim_results = simulation(board, AI, Player_1)
            dictionary = possible_totals(board, AI)
            dictionary = monte_carlo_bounds(dictionary, sim_results, board)
            AI_place(dictionary, board, AI)
            board.possible_drops()
            board.check_grid()
            board.check_full()
            if board.complete:
                AI.win = True

        # Fill the background with black
        screen.fill(black)

        for x in range(7):

            rect = pygame.Rect(x * (BLOCK_SIZE + MARGIN) + LEFT_D, 175, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, white, rect)
            GAME_FONT.render_to(screen, (x * (BLOCK_SIZE + MARGIN) + LEFT_D, 175), str(x + 1), black)

            for y in range(6):
                rect = pygame.Rect(x * (BLOCK_SIZE + MARGIN) + LEFT_D, y * (BLOCK_SIZE + MARGIN) + LEFT_D, BLOCK_SIZE,
                                   BLOCK_SIZE)
                pygame.draw.rect(screen, white, rect)
                if board.grid[y][x] == '1':
                    pygame.draw.circle(screen, green, [x * (BLOCK_SIZE + MARGIN) + (LEFT_D + 25),
                                                       y * (BLOCK_SIZE + MARGIN) + (LEFT_D + 25)], BLOCK_SIZE - 25)
                if board.grid[y][x] == '2':
                    pygame.draw.circle(screen, red, [x * (BLOCK_SIZE + MARGIN) + (LEFT_D + 25),
                                                     y * (BLOCK_SIZE + MARGIN) + (LEFT_D + 25)], BLOCK_SIZE - 25)

        if current == Player_1:
            player_turn = "Player 1's Turn"
            player_won = "Player 1 has won"
            GAME_FONT.render_to(screen, (40, 350), player_turn, (100, 100, 100))
            if Player_1.win:
                GAME_FONT.render_to(screen, (40, 450), player_won, green)

        if current == AI:
            player_turn = "AI's Turn"
            player_won = "AI has won"
            GAME_FONT.render_to(screen, (40, 350), player_turn, (100, 100, 100))
            if AI.win:
                GAME_FONT.render_to(screen, (40, 450), player_won, red)

        if board.full:
            GAME_FONT.render_to(screen, (40, 450), "DRAW", red)

        pygame.draw.rect(screen, white, (35, 390, 80, 40))
        GAME_FONT.render_to(screen, (40, 400), "Menu", (100, 100, 100))

        pygame.display.flip()

        if board.complete or board.full:
            time.sleep(3)
            pygame.quit()
            quit()

play()
