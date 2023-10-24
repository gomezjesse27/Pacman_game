import pygame
import random

# Constants from the maze.py file
GHOST_SPAWN = "g"
TILE_SIZE = 20
SPEED = 5

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
ALL_DIRECTIONS = [UP, DOWN, LEFT, RIGHT]


class Ghost:
    def __init__(self, screen, nodes, maze_layout, spawn_tile, color):
        self.screen = screen
        self.nodes = nodes
        self.maze_layout = maze_layout
        self.spawn_tile = spawn_tile
        self.color = color
        self.rect = pygame.Rect(spawn_tile[0] * TILE_SIZE, spawn_tile[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        self.target = None
        self.direction = random.choice(ALL_DIRECTIONS)
        self.frightened = False

    def draw(self):
        if self.frightened:
            pygame.draw.circle(self.screen, (0, 0, 255), self.rect.center, TILE_SIZE // 2)
        else:
            pygame.draw.circle(self.screen, self.color, self.rect.center, TILE_SIZE // 2)
    def move(self):
        possible_moves = []
        x, y = self.rect.topleft

        # Check possible moves based on the current direction
        if self.direction != DOWN and self.maze_layout[y-1][x] != '#':
            possible_moves.append(UP)
        if self.direction != UP and self.maze_layout[y+1][x] != '#':
            possible_moves.append(DOWN)
        if self.direction != RIGHT and self.maze_layout[y][x-1] != '#':
            possible_moves.append(LEFT)
        if self.direction != LEFT and self.maze_layout[y][x+1] != '#':
            possible_moves.append(RIGHT)

        # Choose the direction that minimizes the distance to the target
        min_dist = float('inf')
        for move in possible_moves:
            new_x, new_y = x + move[0]*TILE_SIZE, y + move[1]*TILE_SIZE
            dist = (self.target[0] - new_x)**2 + (self.target[1] - new_y)**2
            if dist < min_dist:
                min_dist = dist
                self.direction = move

        # Update position based on the chosen direction
        self.rect.x += self.direction[0] * SPEED
        self.rect.y += self.direction[1] * SPEED

    

    def update(self, pacman_pos, pacman_direction, blinky_pos=None):
        if self.frightened:
            self.target = random.choice(self.nodes)
        else:
            self.target = self.get_target(pacman_pos, pacman_direction, blinky_pos)

        self.move()

    def get_target(self, pacman_pos, pacman_direction, blinky_pos):
        pass

    def set_frightened(self, frightened=True):
        self.frightened = frightened


class Blinky(Ghost):
    def __init__(self, screen, nodes, maze_layout, spawn_tile):
        super().__init__(screen, nodes, maze_layout, spawn_tile, (255, 0, 0))

    def get_target(self, pacman_pos, pacman_direction, blinky_pos=None):
        return pacman_pos  # Directly targets Pac-Man's position


class Pinky(Ghost):
    def __init__(self, screen, nodes, maze_layout, spawn_tile):
        super().__init__(screen, nodes, maze_layout, spawn_tile, (255, 105, 180))

    def get_target(self, pacman_pos, pacman_direction, blinky_pos=None):
        # Targets 4 tiles ahead of Pac-Man in its current direction
        return (pacman_pos[0] + 4 * pacman_direction[0], pacman_pos[1] + 4 * pacman_direction[1])


class Inky(Ghost):
    def __init__(self, screen, nodes, maze_layout, spawn_tile):
        super().__init__(screen, nodes, maze_layout, spawn_tile, (0, 255, 255))

    def get_target(self, pacman_pos, pacman_direction, blinky_pos):
        # Calculate a reference point 2 tiles ahead of Pac-Man in its current direction
        ref_point = (pacman_pos[0] + 2 * pacman_direction[0], pacman_pos[1] + 2 * pacman_direction[1])
        # Use the vector from Blinky to this reference point and double it
        return (2 * ref_point[0] - blinky_pos[0], 2 * ref_point[1] - blinky_pos[1])


class Clyde(Ghost):
    def __init__(self, screen, nodes, maze_layout, spawn_tile):
        super().__init__(screen, nodes, maze_layout, spawn_tile, (255, 165, 0))

    def get_target(self, pacman_pos, pacman_direction, blinky_pos=None):
        # If more than 8 tiles away from Pac-Man, targets him directly
        if abs(self.rect.x - pacman_pos[0]) + abs(self.rect.y - pacman_pos[1]) > 8 * TILE_SIZE:
            return pacman_pos
        # If within 8 tiles, targets its scatter point (bottom-left corner)
        else:
            return (2, len(self.maze_layout) - 3)  # Just above the bottom-left corner

# This is the base ghost implementation. Next, we'll integrate them into the game loop.