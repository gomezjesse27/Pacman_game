
import pygame
import sys
from maze import maze_layout, draw_maze, get_nodes, TILE_SIZE
from pacman import PacMan

SCREEN_WIDTH = len(maze_layout[0]) * TILE_SIZE
SCREEN_HEIGHT = len(maze_layout[1]) * TILE_SIZE


def game_loop():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # Create PacMan instance
    pacman_instance = PacMan(screen, get_nodes(), maze_layout)
    
    # Store the current direction of Pac-Man
    current_direction = None
    
    # Timer for delay
    move_timer = 0
    move_delay = 50  # 200 milliseconds
    
    running = True
    while running:
        screen.fill((0, 0, 0))  # Clear the screen
        
        # Draw the maze
        draw_maze(screen, maze_layout)
        pacman_instance.draw()  # Draw Pac-Man on the screen
        
        # Move Pac-Man in the current direction (if any) with a delay
        if current_direction:
            current_time = pygame.time.get_ticks()
            if current_time - move_timer > move_delay:
                pacman_instance.move(current_direction)
                move_timer = current_time
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    current_direction = 'UP'
                elif event.key == pygame.K_DOWN:
                    current_direction = 'DOWN'
                elif event.key == pygame.K_LEFT:
                    current_direction = 'LEFT'
                elif event.key == pygame.K_RIGHT:
                    current_direction = 'RIGHT'
            if event.type == pygame.KEYUP:  # Reset direction when the key is released
                if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    current_direction = None
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
                
        pygame.display.flip()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # Create PacMan instance
    pacman_instance = PacMan(screen, get_nodes(), maze_layout)
    
    running = True
    while running:
        screen.fill((0, 0, 0))  # Clear the screen
        
        # Draw the maze
        draw_maze(screen, maze_layout)
        pacman_instance.draw()  # Draw Pac-Man on the screen
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    pacman_instance.move('UP')
                elif event.key == pygame.K_DOWN:
                    pacman_instance.move('DOWN')
                elif event.key == pygame.K_LEFT:
                    pacman_instance.move('LEFT')
                elif event.key == pygame.K_RIGHT:
                    pacman_instance.move('RIGHT')
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
                
        pygame.display.flip()