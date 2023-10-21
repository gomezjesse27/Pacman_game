import pygame
from start import start_screen
from game import game_loop

if __name__ == "__main__":
    pygame.init()
    start_screen()
    game_loop()
    pygame.quit()
