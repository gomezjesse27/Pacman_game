
import pygame
import sys
from maze import maze_layout, draw_maze, get_nodes, TILE_SIZE
from pacman import PacMan
from ghosts import Blinky, Pinky, Inky, Clyde

SCREEN_WIDTH = len(maze_layout[0]) * TILE_SIZE +150
SCREEN_HEIGHT = len(maze_layout[1]) * TILE_SIZE +100


def game_loop():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # Create PacMan instance
    pacman_instance = PacMan(screen, get_nodes(), maze_layout)
    Inky_instance = Inky(screen, get_nodes(), maze_layout, (11,11))
    Pinky_instance = Pinky(screen, get_nodes(), maze_layout, (10,11))
    Blinky_instance = Blinky(screen, get_nodes(), maze_layout, (9,11))
    Clyde_instance = Clyde(screen, get_nodes(), maze_layout, (12,11))
    # Store the current direction of Pac-Man
    current_direction = None
    numericdirection = (0,0)
    
    # Timer for delay
    move_timer = 0
    move_delay = 50  # 200 milliseconds
    
    running = True
    while running:
        screen.fill((0, 0, 0))  # Clear the screen
        
        # Draw the maze
        draw_maze(screen, maze_layout)
        pacman_instance.draw()  # Draw Pac-Man on the screen
        Inky_instance.draw()
        Pinky_instance.draw()
        Blinky_instance.draw()
        Clyde_instance.draw()
        Inky_instance.move()
        Pinky_instance.move()
        Blinky_instance.move()
        Clyde_instance.move()

        if not pacman_instance.is_dying:
            Inky_instance.target = Inky_instance.get_target(pacman_instance.rect.topleft, numericdirection)
            
            Pinky_instance.target = Pinky_instance.get_target(pacman_instance.rect.topleft, current_direction)
            
            Blinky_instance.target = Blinky_instance.get_target(pacman_instance.rect.topleft)
            
            Clyde_instance.target = Clyde_instance.get_target(pacman_instance.rect.topleft)
        


        if pacman_instance.is_dying:
            elapsed_time = pygame.time.get_ticks() - pacman_instance.death_start
            if elapsed_time > pacman_instance.death_duration:
                pacman_instance.lives -= 1
                print(pacman_instance.lives)
                pacman_instance.is_dying = False
                pacman_instance.can_move = True  # Enable movement once the timer is up

        if pacman_instance.is_dying == False:

            if (pacman_instance.rect.topleft[0] // TILE_SIZE, pacman_instance.rect.topleft[1] // TILE_SIZE) == Inky_instance.location():
                pacman_instance.die()
            if (pacman_instance.rect.topleft[0] // TILE_SIZE, pacman_instance.rect.topleft[1] // TILE_SIZE) == Clyde_instance.location():
                pacman_instance.die()
            if (pacman_instance.rect.topleft[0] // TILE_SIZE, pacman_instance.rect.topleft[1] // TILE_SIZE) == Pinky_instance.location():
                pacman_instance.die()
            if (pacman_instance.rect.topleft[0] // TILE_SIZE, pacman_instance.rect.topleft[1] // TILE_SIZE) == Blinky_instance.location():
                pacman_instance.die()
        if pacman_instance.is_dying == True:
            Inky_instance.target = (220, 220)
            Inky_instance.move()
            Pinky_instance.target = (220, 220)
            Pinky_instance.move()
            Blinky_instance.target = (220, 220)
            Blinky_instance.move()
            Clyde_instance.target = (220, 220)
            Clyde_instance.move()
        
        # Move Pac-Man in the current direction (if any) with a delay
        if current_direction and pacman_instance.can_move:
            current_time = pygame.time.get_ticks()
            if current_time - move_timer > move_delay:
                
                pacman_instance.move(current_direction)
                move_timer = current_time
        # Update the power-up status of Pac-Man
        pacman_instance.update_power_up_status()
        score_text = pygame.font.SysFont(None, 36).render(f"Score: {pacman_instance.score}", True, (255, 255, 255))
        screen.blit(score_text, (460, 10))  # Display the score at the top left corner
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    current_direction = 'UP'
                    numericdirection = (0, 1)
                elif event.key == pygame.K_DOWN:
                    current_direction = 'DOWN'
                    numericdirection = (0, -1)
                elif event.key == pygame.K_LEFT:
                    current_direction = 'LEFT'
                    numericdirection = (-1, 0)
                elif event.key == pygame.K_RIGHT:
                    current_direction = 'RIGHT'
                    numericdirection = (1, 0)
            if event.type == pygame.KEYUP:  # Reset direction when the key is released
                if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    current_direction = None
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
                
        pygame.display.flip()
        
