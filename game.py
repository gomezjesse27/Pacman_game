import pygame
import sys
from maze import maze_layout, draw_maze, get_nodes, TILE_SIZE
from pacman import PacMan
from ghosts import Blinky, Pinky, Inky, Clyde

SCREEN_WIDTH = len(maze_layout[0]) * TILE_SIZE + 150
SCREEN_HEIGHT = len(maze_layout[1]) * TILE_SIZE + 100

def game_loop():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    pacman_instance = PacMan(screen, get_nodes(), maze_layout)
    ghosts = [
        Inky(screen, get_nodes(), maze_layout, (11,11)),
        Pinky(screen, get_nodes(), maze_layout, (10,11)),
        Blinky(screen, get_nodes(), maze_layout, (9,11)),
        Clyde(screen, get_nodes(), maze_layout, (12,11))
    ]
    
    current_direction = None
    numericdirection = (0,0)
    
    move_timer = 0
    move_delay = 50  # milliseconds

    running = True
    while running:
        screen.fill((0, 0, 0))
        draw_maze(screen, maze_layout)
        
        for ghost in ghosts:
            ghost.draw()
            ghost.move()

        pacman_instance.draw()

        if pacman_instance.powered_up:
            handle_powered_up_state(pacman_instance, ghosts)
        else:
            handle_normal_state(pacman_instance, ghosts, current_direction, numericdirection)
        
        if current_direction and pacman_instance.can_move:
            current_time = pygame.time.get_ticks()
            if current_time - move_timer > move_delay:
                pacman_instance.move(current_direction)
                move_timer = current_time
        
        pacman_instance.update_power_up_status()
        
        score_text = pygame.font.SysFont(None, 36).render(f"Score: {pacman_instance.score}", True, (255, 255, 255))
        screen.blit(score_text, (460, 10))

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                current_direction, numericdirection = handle_keydown(event)
            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    current_direction = None
            elif event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

        pygame.display.flip()

def handle_powered_up_state(pacman, ghosts):
    elapsed_time = pygame.time.get_ticks() - pacman.power_up_timer
    if elapsed_time > pacman.powered_up_duration:
        pacman.powered_up = False
        for ghost in ghosts:
            ghost.frightened = False
    else:
        for ghost in ghosts:
            ghost.frightened = True
            if not ghost.is_dying:
                ghost.target = ghost.get_frightened_target(pacman.rect.topleft)

            pacman_pos = (pacman.rect.topleft[0] // TILE_SIZE, pacman.rect.topleft[1] // TILE_SIZE)
            if pacman_pos == ghost.location() and not ghost.is_dying:
                ghost.is_dying = True
                ghost.death_start = pygame.time.get_ticks()
                pacman.score += 100

            if ghost.is_dying:
                elapsed_time = pygame.time.get_ticks() - ghost.death_start
                if elapsed_time > ghost.death_duration:
                    ghost.is_dying = False
                else:
                    ghost.target = (220, 220)
                    ghost.move()

def handle_normal_state(pacman, ghosts, current_direction, numericdirection):
    if pacman.is_dying:
        elapsed_time = pygame.time.get_ticks() - pacman.death_start
        if elapsed_time > pacman.death_duration:
            pacman.lives -= 1
            print(pacman.lives)
            pacman.is_dying = False
            pacman.can_move = True
    else:
        pacman_pos = (pacman.rect.topleft[0] // TILE_SIZE, pacman.rect.topleft[1] // TILE_SIZE)
        for ghost in ghosts:
            if not ghost.is_dying:
                if isinstance(ghost, Inky):
                    ghost.target = ghost.get_target(pacman.rect.topleft, numericdirection)
                elif isinstance(ghost, Pinky):
                    ghost.target = ghost.get_target(pacman.rect.topleft, current_direction)
                else:
                    ghost.target = ghost.get_target(pacman.rect.topleft)

            if pacman_pos == ghost.location():
                pacman.die()

    if pacman.is_dying:
        for ghost in ghosts:
            ghost.target = (220, 220)
            ghost.move()

def handle_keydown(event):
    numericdirection = (0,0)
    if event.key == pygame.K_UP:
        return 'UP', (0, 1)
    elif event.key == pygame.K_DOWN:
        return 'DOWN', (0, -1)
    elif event.key == pygame.K_LEFT:
        return 'LEFT', (-1, 0)
    elif event.key == pygame.K_RIGHT:
        return 'RIGHT', (1, 0)
    return None, numericdirection