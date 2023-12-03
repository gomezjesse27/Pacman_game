
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

# New Constants for Algorithm Selection Buttons
ALGORITHM_BUTTON_WIDTH = 200
ALGORITHM_BUTTON_HEIGHT = 50
ALGORITHM_BUTTON_COLOR = (50, 50, 205)  # A different color for differentiation
ALGORITHM_BUTTON_HOVER_COLOR = (34, 34, 139)
ALGORITHM_LABELS = ["Random", "Bfs", "A*", "Dijkstra's", "Greedy"]
ALGORITHM_BUTTON_SPACING = 60  # Vertical spacing between buttons

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

# Function to create and handle algorithm selection buttons
def create_algorithm_buttons(screen):
    selected_algorithm = None
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # Adjust button layout: 2 rows, 2 columns, moved down to avoid blocking the title
    button_x_start = (SCREEN_WIDTH - (ALGORITHM_BUTTON_WIDTH * 2 + ALGORITHM_BUTTON_SPACING)) // 2
    # Moving buttons down, adjust the vertical start position as needed
    button_y_start = (SCREEN_HEIGHT - (ALGORITHM_BUTTON_HEIGHT * 2 + ALGORITHM_BUTTON_SPACING)) // 2 + 100 

    for i, label in enumerate(ALGORITHM_LABELS):
        row = i // 2
        col = i % 2

        button_x = button_x_start + col * (ALGORITHM_BUTTON_WIDTH + ALGORITHM_BUTTON_SPACING)
        button_y = button_y_start + row * (ALGORITHM_BUTTON_HEIGHT + ALGORITHM_BUTTON_SPACING)

        button_rect = pygame.Rect(button_x, button_y, ALGORITHM_BUTTON_WIDTH, ALGORITHM_BUTTON_HEIGHT)

        # Button hover effect
        if button_rect.collidepoint(mouse):
            pygame.draw.rect(screen, ALGORITHM_BUTTON_HOVER_COLOR, button_rect)
            if click[0] == 1:
                selected_algorithm = label
        else:
            pygame.draw.rect(screen, ALGORITHM_BUTTON_COLOR, button_rect)

        # Button text
        font = pygame.font.SysFont(None, 35)
        text = font.render(label, True, (255, 255, 255))
        screen.blit(text, (button_x + (ALGORITHM_BUTTON_WIDTH - text.get_width()) // 2, 
                           button_y + (ALGORITHM_BUTTON_HEIGHT - text.get_height()) // 2))

    return selected_algorithm




# Main function
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Pacman')

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                selected_algorithm = create_algorithm_buttons(screen)
                if selected_algorithm:
                    game_loop(selected_algorithm)

        screen.fill((0, 0, 0))  # Clear screen

        # Draw title image
        screen.blit(title_image, (SCREEN_WIDTH//2 - title_image.get_width()//2, 50))

        # Draw algorithm selection buttons
        selected_algorithm = create_algorithm_buttons(screen)

        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
