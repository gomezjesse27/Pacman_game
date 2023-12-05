
import pygame
import random


TILE_SIZE = 20  # Size of each tile in pixels
SPEED = 5  # Pixels per frame



class ImageManager:
    def __init__(self, image_path, sheet=True, pos_offsets=None, resize=None, reversible=False, animation_delay=100, repeat=True):
        self.image = pygame.image.load(image_path)
        self.sheet = sheet
        self.pos_offsets = pos_offsets
        self.resize = resize
        self.reversible = reversible
        self.animation_delay = animation_delay
        self.repeat = repeat
        self.image_index = 0
        self.last_update = pygame.time.get_ticks()
        self.images = self.load_images()
        self.ai_frame_counter = 0
        
        
    def load_images(self):
        images = []
        for offset in self.pos_offsets:
            sub_image = self.image.subsurface(pygame.Rect(offset))
            if self.resize:
                sub_image = pygame.transform.scale(sub_image, self.resize)
            images.append(sub_image)
        if self.reversible:
            reversed_images = [pygame.transform.flip(img, True, False) for img in images]
            images.extend(reversed_images)
        return images
        
    def next_image(self, direction=None):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_delay:
            self.last_update = now
            self.image_index += 1
            if self.image_index >= len(self.images): 
                if self.repeat:
                    self.image_index = 0
                else:
                    self.image_index = len(self.images) - 1
                    


            return self.images[self.image_index], None 

            return self.images[self.image_index], None 

        return self.images[self.image_index], None



class PacMan:
    def __init__(self, screen, nodes, maze_layout):
        self.screen = screen
        self.nodes = nodes
        self.image = pygame.image.load('pacman.png')
        self.score = 0
        self.layout = maze_layout
        self.powered_up = False
        self.powered_up_duration = 5000
        self.power_up_timer = None
        self.lives = 100
        self.is_dying = False
        self.death_start = None  # This will store the time when scatter mode starts
        self.death_duration = 5000  # Scatter mode duration, 5 seconds in milliseconds
        self.can_move = True
        self.ai_move_frame_counter = 0
        self.ai_move_frame_threshold = 10  # Adjust this value to control AI speed
        self.last_successful_move = None
        self.speed = 0
        
        # Load the vertical and horizontal animation sprites
        self.image_horiz = pygame.transform.scale(pygame.image.load('pacman-horiz.png'), (TILE_SIZE, TILE_SIZE))
        self.image_vert = pygame.transform.scale(pygame.image.load('pacman-vert.png'), (TILE_SIZE, TILE_SIZE))
        self.image_death = pygame.transform.scale(pygame.image.load('pacman-death.png'), (TILE_SIZE, TILE_SIZE))
        
        # Resize the default image to fit within a tile
        
        self.image_horiz = ImageManager('pacman-horiz.png', sheet=True, pos_offsets=[(0, 0, 32, 32),
                                                                                               (32, 0, 32, 32),
                                                                                               (0, 32, 32, 32),
                                                                                               (32, 32, 32, 32),
                                                                                               (0, 64, 32, 32)],
                                          resize=(TILE_SIZE, TILE_SIZE))
        self.image_left = ImageManager('pacman-left.png', sheet=True, pos_offsets=[(0, 0, 32, 32),
                                                                                               (32, 0, 32, 32),
                                                                                               (0, 32, 32, 32),
                                                                                               (32, 32, 32, 32),
                                                                                               (0, 64, 32, 32)],
                                          resize=(TILE_SIZE, TILE_SIZE))
        
        self.image_vert = ImageManager('pacman-vert.png', sheet=True, pos_offsets=[(0, 0, 32, 32),
                                                                                               (32, 0, 32, 32),
                                                                                               (0, 32, 32, 32),
                                                                                               (32, 32, 32, 32),
                                                                                               (0, 64, 32, 32)],
                                          resize=(TILE_SIZE, TILE_SIZE))
        self.image_down = ImageManager('pacman-down.png', sheet=True, pos_offsets=[(0, 0, 32, 32),
                                                                                            (32, 0, 32, 32),
                                                                                            (0, 32, 32, 32),
                                                                                            (32, 32, 32, 32),
                                                                                            (0, 64, 32, 32)],
                                        resize=(TILE_SIZE, TILE_SIZE))
        self.image_death = ImageManager('pacman-death.png', sheet=True, pos_offsets=[(0, 0, 32, 32),
                                                                                            (32, 0, 32, 32),
                                                                                            (0, 32, 32, 32),
                                                                                            (32, 32, 32, 32),
                                                                                            (0, 64, 32, 32)],
                                        resize=(TILE_SIZE, TILE_SIZE))
        
        self.image, _ = self.image_horiz.next_image()
    
        
        self.rect = self.image.get_rect()
        self.target = None  # Target node to move towards
        
        # Setting PacMan's initial position to the player spawn point
        for y, row in enumerate(maze_layout):
            for x, tile in enumerate(row):
                if tile == "p":
                    self.rect.topleft = (x * TILE_SIZE, y * TILE_SIZE)
                    break
    #def eat (self):
        self.starting_position = self.rect.topleft

    def draw(self):
        self.screen.blit(self.image, self.rect.topleft)

    def die(self):
        if not self.is_dying:  # Ensure we only start the death process once
            self.is_dying = True
            self.can_move = False  # Disable movement
            self.death_start = pygame.time.get_ticks()
            self.rect.topleft = self.starting_position  # Reset position immediately



    def move(self, direction):
        
        if not self.target:  # If not already moving towards a target
            if direction == 'UP':
                target_pos = (self.rect.centerx, self.rect.centery - TILE_SIZE)
                if target_pos in self.nodes:
                    self.target = target_pos
                    self.image, _ = self.image_vert.next_image('DOWN')
            elif direction == 'DOWN':
                target_pos = (self.rect.centerx, self.rect.centery + TILE_SIZE)
                if target_pos in self.nodes:
                    self.target = target_pos
                    self.image, _ = self.image_down.next_image('DOWN')
            elif direction == 'LEFT':
                target_pos = (self.rect.centerx - TILE_SIZE, self.rect.centery)
                if target_pos in self.nodes:
                    self.target = target_pos
                    self.image, _ = self.image_left.next_image('LEFT')
            elif direction == 'RIGHT':
                target_pos = (self.rect.centerx + TILE_SIZE, self.rect.centery)
                if target_pos in self.nodes:
                    self.target = target_pos
                    self.image, _ = self.image_horiz.next_image('LEFT')
        
        # Move Pac-Man smoothly towards the target
        if self.target:
            if self.rect.centerx < self.target[0]:  # Move right
                self.rect.x += self.speed
                if self.rect.centerx >= self.target[0]:
                    self.rect.centerx = self.target[0]
                    self.target = None
            elif self.rect.centerx > self.target[0]:  # Move left
                self.rect.x -= self.speed
                if self.rect.centerx <= self.target[0]:
                    self.rect.centerx = self.target[0]
                    self.target = None
            elif self.rect.centery < self.target[1]:  # Move down
                self.rect.y += self.speed
                if self.rect.centery >= self.target[1]:
                    self.rect.centery = self.target[1]
                    self.target = None
            elif self.rect.centery > self.target[1]:  # Move up
                self.rect.y -= self.speed
                if self.rect.centery <= self.target[1]:
                    self.rect.centery = self.target[1]
                    self.target = None
            maze_width = len(self.layout[0]) * TILE_SIZE
            if self.rect.left < 1:
                self.rect.right = maze_width
            elif self.rect.right > maze_width - 1:
                self.rect.left = 0
        x, y = self.rect.centerx // TILE_SIZE, self.rect.centery // TILE_SIZE
        if self.layout[y][x] == "*":
            self.score += 10  # Increase the score by 10
            self.layout[y][x] = "."  # Remove the pellet from the maze layout
        if self.layout[y][x] == "@":
            self.score += 50  # Increase the score by 10
            self.layout[y][x] = "."  # Remove the pellet from the maze layout
            self.powered_up = True
            self.power_up_timer = pygame.time.get_ticks()  # Start the timer
    def ai_move(self, maze_layout, ghosts):
        self.speed = 1
        self.ai_move_frame_counter += 1
        if self.ai_move_frame_counter < self.ai_move_frame_threshold:
            return  # Skip the move if the frame threshold has not been reached

        closest_ghost, closest_dist = self.get_closest_ghost(ghosts)
        pacman_x, pacman_y = self.rect.centerx // TILE_SIZE, self.rect.centery // TILE_SIZE

        if closest_ghost:
            ghost_x, ghost_y = closest_ghost.location()
            primary_direction = self.get_primary_direction(ghost_x, ghost_y, pacman_x, pacman_y)
            reverse_direction = self.get_reverse_direction(self.last_successful_move)

            # If a ghost is very close, prioritize escaping from it
            if closest_dist < 100:  # Define a threshold for "very close"
                escape_directions = self.get_escape_directions(primary_direction, reverse_direction)
                if self.try_escape(escape_directions, pacman_x, pacman_y, maze_layout):
                    return

            # If no immediate ghost threat, try to continue in the last successful direction
            if self.last_successful_move and self.try_move(self.last_successful_move, pacman_x, pacman_y, maze_layout):
                return

            # If blocked, choose a new direction
            new_directions = self.get_new_directions(reverse_direction)
            for direction in new_directions:
                if self.try_move(direction, pacman_x, pacman_y, maze_layout):
                    self.last_successful_move = direction
                    break

        self.ai_move_frame_counter = 0


    def get_closest_ghost(self, ghosts):
        closest_ghost = None
        closest_dist = float('inf')
        for ghost in ghosts:
            ghost_pos = ghost.location()
            dist = abs(self.rect.centerx - ghost_pos[0] * TILE_SIZE) + abs(self.rect.centery - ghost_pos[1] * TILE_SIZE)
            if dist < closest_dist:
                closest_dist = dist
                closest_ghost = ghost
        return closest_ghost, closest_dist

    def get_primary_direction(self, ghost_x, ghost_y, pacman_x, pacman_y):
        if ghost_x > pacman_x:
            return 'LEFT'
        elif ghost_x < pacman_x:
            return 'RIGHT'
        elif ghost_y > pacman_y:
            return 'UP'
        elif ghost_y < pacman_y:
            return 'DOWN'
        return None

    def get_reverse_direction(self, last_move):
        if last_move == 'LEFT':
            return 'RIGHT'
        elif last_move == 'RIGHT':
            return 'LEFT'
        elif last_move == 'UP':
            return 'DOWN'
        elif last_move == 'DOWN':
            return 'UP'
        return None

    def get_escape_directions(self, primary_direction, reverse_direction):
        directions = ['LEFT', 'RIGHT', 'UP', 'DOWN']
        if reverse_direction and reverse_direction in directions:
            directions.remove(reverse_direction)
        if primary_direction and primary_direction in directions:
            directions.remove(primary_direction)
            directions.insert(0, primary_direction)
        return directions

    def try_escape(self, directions, pacman_x, pacman_y, maze_layout):
        available_directions = self.get_available_directions(pacman_x, pacman_y, maze_layout)
        for direction in directions:
            if direction in available_directions:
                self.last_successful_move = direction
                self.move(direction)
                return True
        return False
    def get_available_directions(self, pacman_x, pacman_y, maze_layout):
        available_directions = []
        if maze_layout[pacman_y][pacman_x - 1] != 'x':
            available_directions.append('LEFT')
        if maze_layout[pacman_y][pacman_x + 1] != 'x':
            available_directions.append('RIGHT')
        if maze_layout[pacman_y - 1][pacman_x] != 'x':
            available_directions.append('UP')
        if maze_layout[pacman_y + 1][pacman_x] != 'x':
            available_directions.append('DOWN')
        return available_directions
    def get_new_directions(self, reverse_direction):
        directions = ['LEFT', 'RIGHT', 'UP', 'DOWN']
        if reverse_direction and reverse_direction in directions:
            directions.remove(reverse_direction)
        return directions

    def try_move(self, direction, pacman_x, pacman_y, maze_layout):
        if direction == 'LEFT' and maze_layout[pacman_y][pacman_x - 1] != 'x':
            self.move('LEFT')
            return True
        elif direction == 'RIGHT' and maze_layout[pacman_y][pacman_x + 1] != 'x':
            self.move('RIGHT')
            return True
        elif direction == 'UP' and maze_layout[pacman_y - 1][pacman_x] != 'x':
            self.move('UP')
            return True
        elif direction == 'DOWN' and maze_layout[pacman_y + 1][pacman_x] != 'x':
            self.move('DOWN')
            return True
        return False


    def update_power_up_status(self):
        if self.powered_up and pygame.time.get_ticks() - self.power_up_timer > self.powered_up_duration:
            self.powered_up = False