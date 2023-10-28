
from queue import PriorityQueue



class Node():
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0  # Distance to start node
        self.h = 0  # Distance to end node
        self.f = 0  # Total cost

    def __eq__(self, other):
        return self.position == other.position

def a_star_search(start, goal, maze):
    
    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, goal)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until the end is reached
    while len(open_list) > 0:
        # Get the current node (node with the lowest f)
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current node from open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # If the goal is reached
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]  # Return reversed path

        # Generate children nodes
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:  # Adjacent squares (up, down, left, right)

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Check if within the maze boundaries
            if node_position[0] < 0 or node_position[0] >= len(maze[0]) or node_position[1] < 0 or node_position[1] >= len(maze):
                continue


            # Check if walkable
            if maze[node_position[1]][node_position[0]] == "x":
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:
            # Check if child is in the closed list
            if child in closed_list:
                continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Check if child is in the open list and if it has a lower f value
            if len([open_node for open_node in open_list if child == open_node and child.g > open_node.g]) > 0:
                continue

            # Add the child to the open list
            open_list.append(child)

    return None

import pygame
import random

# Constants from the maze.py file
GHOST_SPAWN = "g"
TILE_SIZE = 20
SPEED = 1

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
        self.move_counter = 0
        self.moving_to_tile = False
        self.frightened_timer = 0
        self.frightened_direction_change_interval = random.randint(500, 1500)  # Random interval between 0.5 and 1.5 seconds
        self.death_start = None  # This will store the time when scatter mode starts
        self.death_duration = 5000  # Scatter mode duration, 5 seconds in milliseconds
        self.is_dying = False

    def draw(self):
        if self.frightened:
            pygame.draw.circle(self.screen, (0, 0, 255), self.rect.center, TILE_SIZE // 2)
        else:
            pygame.draw.circle(self.screen, self.color, self.rect.center, TILE_SIZE // 2)
        next_tile_pixel = ((self.rect.topleft[0] // TILE_SIZE + self.direction[0]) * TILE_SIZE, 
                   (self.rect.topleft[1] // TILE_SIZE + self.direction[1]) * TILE_SIZE)
        pygame.draw.rect(self.screen, (255, 0, 255), 
                 (next_tile_pixel[0], next_tile_pixel[1], TILE_SIZE, TILE_SIZE), 2)

    def get_frightened_target(self, pacman_pos):
        """Determine target tile while in frightened mode."""
        possible_directions = list(ALL_DIRECTIONS)
        
        # Remove the opposite direction
        if (-self.direction[0], -self.direction[1]) in possible_directions:
            possible_directions.remove((-self.direction[0], -self.direction[1]))  
        
        # Filter out invalid directions based on the maze layout
        valid_directions = [dir for dir in possible_directions if self.is_valid_direction(dir)]
        
        # Compute possible tiles and their distances from Pac-Man
        distances = []
        for dir in valid_directions:
            next_tile = (self.rect.topleft[0] + dir[0] * TILE_SIZE, 
                        self.rect.topleft[1] + dir[1] * TILE_SIZE)
            distance = abs(next_tile[0] - pacman_pos[0]) + abs(next_tile[1] - pacman_pos[1])
            distances.append((distance, next_tile))
        
        if distances:
            target_tile = max(distances, key=lambda x: x[0])[1]
            return target_tile
        else:
            # Return the current position if no valid direction is found
            return self.rect.topleft
    def is_valid_direction(self, direction):
        """Check if a given direction is valid (no walls and within maze bounds)."""
        next_tile_pixel = ((self.rect.topleft[0] + direction[0] * TILE_SIZE) // TILE_SIZE,
                        (self.rect.topleft[1] + direction[1] * TILE_SIZE) // TILE_SIZE)
        if (next_tile_pixel[0] < 0 or next_tile_pixel[0] >= len(self.maze_layout[0]) or
            next_tile_pixel[1] < 0 or next_tile_pixel[1] >= len(self.maze_layout)):
            return False
        if self.maze_layout[next_tile_pixel[1]][next_tile_pixel[0]] == "x":
            return False
        return True


    
    def move(self):
        # Increment the move counter and check if it'st time to move
        self.move_counter += 1
        if self.move_counter < 5:  # Adjust this number for different speeds
            return
        self.move_counter = 0  # Reset the counter
        
        # If the ghost is currently moving to a tile, continue in the current direction
        if self.moving_to_tile:
            self.rect.move_ip(self.direction[0]*SPEED, self.direction[1]*SPEED)
            # Check if the ghost has reached a tile boundary
            if self.rect.topleft[0] % TILE_SIZE == 0 and self.rect.topleft[1] % TILE_SIZE == 0:
                self.moving_to_tile = False
            return

        # If no target, don't move
        if not self.target:
            return

        # Get current tile position
        x, y = self.rect.topleft[0] // TILE_SIZE, self.rect.topleft[1] // TILE_SIZE
        current_tile = (x, y)

        # If we're already at a target, don't recompute path
        if current_tile == (self.target[0] // TILE_SIZE, self.target[1] // TILE_SIZE):
            return

        # If we don't have a path or the next tile in the path is our current tile, compute a new path
        if not hasattr(self, 'path') or not self.path or self.path[0] == current_tile:
            # Get target tile position
            target_x, target_y = self.target[0] // TILE_SIZE, self.target[1] // TILE_SIZE
            goal = (target_x, target_y)

            # Use A* to find the path
            self.path = a_star_search(current_tile, goal, self.maze_layout)
            if not self.path:
                return

            # Remove the current tile from the path
            self.path = self.path[1:]

        # Take the next step in the path
        next_tile = self.path[0]
        if next_tile[0] > x:  # Move right
            self.direction = RIGHT
        elif next_tile[0] < x:  # Move left
            self.direction = LEFT
        elif next_tile[1] > y:  # Move down
            self.direction = DOWN
        elif next_tile[1] < y:  # Move up
            self.direction = UP

        # Move the ghost in the chosen direction
        self.rect.move_ip(self.direction[0]*SPEED, self.direction[1]*SPEED)
        self.moving_to_tile = True

    def location(self):
        return self.rect.topleft[0] // TILE_SIZE, self.rect.topleft[1] // TILE_SIZE
        

    def kill():
        pass
        

    def update(self, pacman_pos, pacman_direction):
        if self.frightened:
            self.target = random.choice(self.nodes)
        else:
            self.target = self.get_target(pacman_pos, pacman_direction)
        x, y = self.rect.topleft[0] // TILE_SIZE, self.rect.topleft[1] // TILE_SIZE
        current_tile2 = (x, y)
        if current_tile2 == (pacman_pos[0] // TILE_SIZE, pacman_pos[1] // TILE_SIZE):
            self.kill()
        self.move()

    def get_target(self, pacman_pos, pacman_direction, blinky_pos):
        pass

    def set_frightened(self, frightened=True):
        self.frightened = frightened


class Blinky(Ghost):
    def __init__(self, screen, nodes, maze_layout, spawn_tile):
        super().__init__(screen, nodes, maze_layout, spawn_tile, (255, 0, 0))

    def get_target(self, pacman_pos):
        #pacman_direction = pacman_direction or (0, 0)
        
        return pacman_pos  # Directly targets Pac-Man's position


class Pinky(Ghost):
    def __init__(self, screen, nodes, maze_layout, spawn_tile):
        super().__init__(screen, nodes, maze_layout, spawn_tile, (255, 105, 180))
        self.scatter_start_time = None  # This will store the time when scatter mode starts
        self.scatter_duration = 5000  # Scatter mode duration, 5 seconds in milliseconds
        self.reached = False

    def get_target(self, pacman_pos, pacman_direction=None, blinky_pos=None):
        pacman_direction = pacman_direction or (0, 0)
        
        # If scatter_start_time is set, check how much time has passed
        if self.scatter_start_time:
            elapsed_time = pygame.time.get_ticks() - self.scatter_start_time
            if elapsed_time < self.scatter_duration:
                x, y = self.rect.topleft[0] // 20, self.rect.topleft[1] // 20
                current_tile2 = (x, y)

                if current_tile2 == (1, 1):
                    self.reached = False

                if current_tile2 == (5, 4):
                    self.reached = True

                if self.reached:
                    return (20, 20)
                
                if not self.reached:
                    return (100, 80)
            else:
                # Reset scatter_start_time if scatter duration has passed
                self.scatter_start_time = None

        # If more than 4 tiles away from Pac-Man, targets him directly
        if abs(self.rect.x - pacman_pos[0]) + abs(self.rect.y - pacman_pos[1]) > 4 * TILE_SIZE:
            return pacman_pos

        # If within 4 tiles and scatter timer is not active, start scatter timer
        elif abs(self.rect.x - pacman_pos[0]) + abs(self.rect.y - pacman_pos[1]) <= 4 * TILE_SIZE:
            if not self.scatter_start_time:
                self.scatter_start_time = pygame.time.get_ticks()


class Inky(Ghost):
    def __init__(self, screen, nodes, maze_layout, spawn_tile):
        super().__init__(screen, nodes, maze_layout, spawn_tile, (0, 255, 255))

    def get_target(self, pacman_pos, pacman_direction, blinky_pos = None):
        # Calculate a reference point 2 tiles ahead of Pac-Man in its current direction
        ref_point = (pacman_pos[0] + 40 * pacman_direction[0], pacman_pos[1] + 40 * pacman_direction[1])
        # Use the vector from Blinky to this reference point and double it
        return ref_point


class Clyde(Ghost):
    def __init__(self, screen, nodes, maze_layout, spawn_tile):
        super().__init__(screen, nodes, maze_layout, spawn_tile, (255, 165, 0))
        self.current_target = None
        self.reached = False
        self.scatter_start_time = None  # This will store the time when scatter mode starts
        self.scatter_duration = 5000  # Scatter mode duration, 5 seconds in milliseconds

    def get_target(self, pacman_pos, pacman_direction=None, blinky_pos=None):
        pacman_direction = pacman_direction or (0, 0)
        
        # If scatter_start_time is set, check how much time has passed
        if self.scatter_start_time:
            elapsed_time = pygame.time.get_ticks() - self.scatter_start_time
            if elapsed_time < self.scatter_duration:
                x, y = self.rect.topleft[0] // TILE_SIZE, self.rect.topleft[1] // TILE_SIZE
                current_tile2 = (x, y)

                if current_tile2 == (6, 18):
                    self.reached = False

                if current_tile2 == (4, 23):
                    self.reached = True

                if self.reached:
                    return (125, 360)
                
                if not self.reached:
                    return (80, 460)
            else:
                # Reset scatter_start_time if scatter duration has passed
                self.scatter_start_time = None

        # If more than 8 tiles away from Pac-Man, targets him directly
        if abs(self.rect.x - pacman_pos[0]) + abs(self.rect.y - pacman_pos[1]) > 8 * TILE_SIZE:
            self.current_target = pacman_pos
            return pacman_pos

        # If within 8 tiles and scatter timer is not active, start scatter timer
        elif abs(self.rect.x - pacman_pos[0]) + abs(self.rect.y - pacman_pos[1]) <= 8 * TILE_SIZE:
            if not self.scatter_start_time:
                self.scatter_start_time = pygame.time.get_ticks()

            


