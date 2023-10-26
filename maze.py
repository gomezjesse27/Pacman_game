
import pygame


# Maze symbols
WALL = "x"
EMPTY = "."
PELLET = "*"
POWER_PELLET = "@"
PLAYER_SPAWN = "p"
GHOST_SPAWN = "g"
GHOST_HOME = "s"
GHOST_HOME_ENTRANCE = "t"

TILE_SIZE = 20  # Size of each tile in pixels
PELLET_SIZE = 5  # Size of a pellet in pixels

# Maze layout
maze_layout = [['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'], ['x', '@', '.', '*', '.', '*', '.', '*', '.', '*', '.', 'x', '.', '*', '.', '*', '.', '*', '.', '*', '.', '@', 'x'], ['x', '.', 'x', 'x', 'x', '.', 'x', 'x', 'x', 'x', '*', 'x', '*', 'x', 'x', 'x', 'x', '.', 'x', 'x', 'x', '.', 'x'], ['x', '*', 'x', 'x', 'x', '*', 'x', 'x', 'x', 'x', '.', 'x', '.', 'x', 'x', 'x', 'x', '*', 'x', 'x', 'x', '*', 'x'], ['x', '.', '*', '.', '*', '.', '*', '.', '*', '.', '*', '.', '*', '.', '*', '.', '*', '.', '*', '.', '*', '.', 'x'], ['x', '*', 'x', 'x', 'x', '.', 'x', '*', 'x', 'x', 'x', 'x', 'x', 'x', 'x', '*', 'x', '*', 'x', 'x', 'x', '.', 'x'], ['x', '.', '*', '.', '*', '.', 'x', '.', 'x', 'x', 'x', 'x', 'x', 'x', 'x', '.', 'x', '.', '*', '.', '*', '.', 'x'], ['x', 'x', 'x', 'x', 'x', '@', 'x', '*', '.', '*', '.', 'x', '.', '*', '.', '*', 'x', '@', 'x', 'x', 'x', 'x', 'x'], ['.', '.', '.', '.', 'x', '.', 'x', 'x', 'x', 'x', '*', 'x', '*', 'x', 'x', 'x', 'x', '.', 'x', '.', '.', '.', '.'], ['.', '.', '.', '.', 'x', '*', 'x', '.', '.', '.', '.', 'g', '.', '.', '.', '.', 'x', '*', 'x', '.', '.', '.', '.'], ['x', 'x', 'x', 'x', 'x', '.', 'x', '.', 'x', 'x', 'x', 's', 'x', 'x', 'x', '.', 'x', '.', 'x', 'x', 'x', 'x', 'x'], ['t', '*', '.', '*', '.', '*', '.', '.', 'x', 'g', '.', 'g', '.', 'g', 'x', '.', '.', '*', '.', '*', '.', '*', 't'], ['x', 'x', 'x', 'x', 'x', '.', 'x', '.', 'x', 'x', 'x', 'x', 'x', 'x', 'x', '.', 'x', '.', 'x', 'x', 'x', 'x', 'x'], ['.', '.', '.', '.', 'x', '*', 'x', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'x', '*', 'x', '.', '.', '.', '.'], ['.', '.', '.', '.', 'x', '.', 'x', '.', 'x', 'x', 'x', 'x', 'x', 'x', 'x', '.', 'x', '.', 'x', '.', '.', '.', '.'], ['x', 'x', 'x', 'x', 'x', '*', 'x', '.', 'x', 'x', 'x', 'x', 'x', 'x', 'x', '.', 'x', '*', 'x', 'x', 'x', 'x', 'x'], ['x', '.', '*', '.', '*', '.', '*', '.', '*', '.', '*', 'x', '*', '.', '*', '.', '*', '.', '*', '.', '*', '.', 'x'], ['x', '*', 'x', 'x', 'x', '@', 'x', 'x', 'x', 'x', '.', 'x', '.', 'x', 'x', 'x', 'x', '@', 'x', 'x', 'x', '*', 'x'], ['x', '.', '*', '.', 'x', '.', '.', '*', '.', '*', '.', 'p', '.', '*', '.', '*', '.', '.', 'x', '.', '*', '.', 'x'], ['x', 'x', 'x', '.', 'x', '*', 'x', '.', 'x', 'x', 'x', 'x', 'x', 'x', 'x', '.', 'x', '*', 'x', '*', 'x', 'x', 'x'], ['x', '.', '*', '.', '*', '.', 'x', '.', '.', '.', '.', 'x', '.', '*', '.', '*', 'x', '.', '*', '.', '*', '.', 'x'], ['x', '*', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', '.', 'x', '*', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', '*', 'x'], ['x', '.', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', '.', 'x', '.', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', '.', 'x'], ['x', '@', '.', '*', '.', '*', '.', '*', '.', '*', '.', '*', '.', '*', '.', '*', '.', '*', '.', '*', '.', '@', 'x'], ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x']]

def draw_maze(screen, layout):
    # Define colors
    WALL_COLOR = (255, 255, 255)  # White
    PELLET_COLOR = (255, 255, 0)  # Yellow
    POWER_PELLET_COLOR = (255, 0, 0)  # Red
    EMPTY_COLOR = (0, 0, 0)  # Black
    
    # Loop through each tile in the layout
    for y, row in enumerate(layout):
        for x, tile in enumerate(row):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if tile == WALL:  # Wall
                pygame.draw.rect(screen, WALL_COLOR, rect)
            elif tile == PELLET:  # Pellet
                pellet_pos = (x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2)
                pygame.draw.circle(screen, PELLET_COLOR, pellet_pos, PELLET_SIZE)
            elif tile == POWER_PELLET:  # Power Pellet
                pellet_pos = (x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2)
                pygame.draw.circle(screen, POWER_PELLET_COLOR, pellet_pos, 2 * PELLET_SIZE)
            elif tile in [EMPTY, PLAYER_SPAWN, GHOST_SPAWN, GHOST_HOME, GHOST_HOME_ENTRANCE]:  # Empty space, Player spawn, Ghost spawn, Ghost home, and entrance
                pygame.draw.rect(screen, EMPTY_COLOR, rect)
    # Debug: Draw grid
    for x in range(0, len(row) * TILE_SIZE, TILE_SIZE):
        pygame.draw.line(screen, (50, 50, 50), (x, 0), (x, len(layout) * TILE_SIZE))
    for y in range(0, len(layout) * TILE_SIZE, TILE_SIZE):
        pygame.draw.line(screen, (50, 50, 50), (0, y), (len(row) * TILE_SIZE, y))


def get_nodes():
    nodes = []
    for y, row in enumerate(maze_layout):
        for x, tile in enumerate(row):
            # If the tile is not a wall, it's a potential node
            if tile != "x":
                nodes.append((x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2))  # Taking center of the tile
    return nodes
