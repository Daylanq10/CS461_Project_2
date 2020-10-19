import pygame
import pygame.freetype
import pygame_menu
import Human_V_Human
import Human_V_CPU

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


def menu():
    """
    Menu function that allows multiple choices
    """
    menu = True
    while menu:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        surface = pygame.display.set_mode((WIDTH, HEIGHT))
        menu = pygame_menu.Menu(HEIGHT, WIDTH, 'CONNECT 4', theme=pygame_menu.themes.THEME_DARK)

        menu.add_button('Human V Human', Human_V_Human.play())
        menu.add_button('Computer V Human', Human_V_CPU.play())
        menu.add_button('Quit', pygame_menu.events.EXIT)

        menu.mainloop(surface)
