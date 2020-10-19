import pygame
import pygame.freetype
import time


class Human:
    def __init__(self, name, turn, moves=0, win=False):
        self.name = name
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
    def __init__(self, complete=False):
        self.grid = create_grid()
        self.complete = complete

    def display(self):
        for x in self.grid:
            print(x)

    def update_grid(self, player: Human, location: int):
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
    else:
        return 0


def play():

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    Player_1 = Human("Player_1", True)
    Player_2 = Human("Player_2", False)
    board = Board()

    # Run until the user asks to quit
    running = True
    while running:

        if Player_1.turn & (Player_1.moves == Player_2.moves):
            current = Player_1

        if Player_2.turn & (Player_1.moves != Player_2.moves):
            current = Player_2

        Player_1.swap_turn()
        Player_2.swap_turn()

        # Did the user click the window close button?
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                running = False  # Flag that we are done so we exit this loop
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # User clicks the mouse. Get the position
                pos = pygame.mouse.get_pos()
                board.update_grid(current, drop_location(pos))
                board.check_grid()

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
            player_won = "Player 2 has won"
            GAME_FONT.render_to(screen, (40, 350), player_turn, (100, 100, 100))
            if board.complete:
                GAME_FONT.render_to(screen, (40, 450), player_won, red)
                Player_2.win = True

        if current == Player_2:
            player_turn = "Player 2's Turn"
            player_won = "Player 1 has won"
            GAME_FONT.render_to(screen, (40, 350), player_turn, (100, 100, 100))
            if board.complete:
                GAME_FONT.render_to(screen, (40, 450), player_won, green)
                Player_1.win = True

        pygame.draw.rect(screen, white, (35, 390, 80, 40))
        GAME_FONT.render_to(screen, (40, 400), "Menu", (100, 100, 100))

        pygame.display.flip()

        if board.complete:
            time.sleep(3)
            pygame.quit()
            quit()


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

play()