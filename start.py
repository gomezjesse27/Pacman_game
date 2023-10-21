import pygame
import sys
from game import game_loop


# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_COLOR = (50, 205, 50)
BUTTON_HOVER_COLOR = (34, 139, 34)

# Load images
title_image = pygame.image.load("pacmanTitle.png")
pacman_image = pygame.image.load("pacman.png")
pink_ghost_image = pygame.image.load("pinkGhost.png")
orange_ghost_image = pygame.image.load("orangeGhost.png")
blue_ghost_image = pygame.image.load("blueGhost.png")
red_ghost_image = pygame.image.load("redGhost.png")

# Scale images
title_image = pygame.transform.scale(title_image, (500, 200))
pacman_image = pygame.transform.scale(pacman_image, (50, 50))
pink_ghost_image = pygame.transform.scale(pink_ghost_image, (50, 50))
orange_ghost_image = pygame.transform.scale(orange_ghost_image, (50, 50))
blue_ghost_image = pygame.transform.scale(blue_ghost_image, (50, 50))
red_ghost_image = pygame.transform.scale(red_ghost_image, (50, 50))

def start_screen():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pac-Man Game")
    font = pygame.font.Font(None, 36)
    
    # Define initial positions for Pac-Man and ghosts
    pacman_pos = [SCREEN_WIDTH // 2 - 400, 330]  # Adjusted horizontal position
    
    pink_ghost_pos = [SCREEN_WIDTH // 2 - 350, 330]
    orange_ghost_pos = [SCREEN_WIDTH // 2 - 250, 330]
    blue_ghost_pos = [SCREEN_WIDTH // 2 - 150, 330]
    red_ghost_pos = [SCREEN_WIDTH // 2 - 50, 330]
    
    ghost_speed = 0.5  # Further reduced speed
    pacman_speed = 0.5  # Further reduced speed
    
    running = True
    while running:
        screen.fill((0, 0, 0))
        
        # Move ghosts to the right
        pink_ghost_pos[0] += ghost_speed
        orange_ghost_pos[0] += ghost_speed
        blue_ghost_pos[0] += ghost_speed
        red_ghost_pos[0] += ghost_speed
        
        # Move Pac-Man to the right
        pacman_pos[0] += pacman_speed
        
        # Wrap-around movement for ghosts and Pac-Man
        pink_ghost_pos[0] %= SCREEN_WIDTH
        orange_ghost_pos[0] %= SCREEN_WIDTH
        blue_ghost_pos[0] %= SCREEN_WIDTH
        red_ghost_pos[0] %= SCREEN_WIDTH
        pacman_pos[0] %= SCREEN_WIDTH
        
        # Draw title image
        screen.blit(title_image, (SCREEN_WIDTH // 2 - title_image.get_width() // 2, 50))
        
        # Draw Pac-Man and ghosts
        screen.blit(pacman_image, pacman_pos)
        screen.blit(pink_ghost_image, pink_ghost_pos)
        screen.blit(orange_ghost_image, orange_ghost_pos)
        screen.blit(blue_ghost_image, blue_ghost_pos)
        screen.blit(red_ghost_image, red_ghost_pos)
        
        # Draw button
        mouse = pygame.mouse.get_pos()
        if SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2 < mouse[0] < SCREEN_WIDTH // 2 + BUTTON_WIDTH // 2 and \
           450 < mouse[1] < 450 + BUTTON_HEIGHT:
            pygame.draw.rect(screen, BUTTON_HOVER_COLOR, (SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, 450, BUTTON_WIDTH, BUTTON_HEIGHT))
            if pygame.mouse.get_pressed()[0]:
                game_loop()

        else:
            pygame.draw.rect(screen, BUTTON_COLOR, (SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, 450, BUTTON_WIDTH, BUTTON_HEIGHT))
        
        text = font.render("Start Game", True, (255, 255, 255))
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 457))
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        pygame.display.flip()

# This is the adjusted function with Pac-Man to the left of the ghosts and even slower movement speed.



# Run start screen function
start_screen()
