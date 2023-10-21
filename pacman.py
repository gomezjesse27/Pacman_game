
import pygame

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
        
        # Load the vertical and horizontal animation sprites
        self.image_horiz = pygame.transform.scale(pygame.image.load('pacman-horiz.png'), (TILE_SIZE, TILE_SIZE))
        self.image_vert = pygame.transform.scale(pygame.image.load('pacman-vert.png'), (TILE_SIZE, TILE_SIZE))
        
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
        
        self.image, _ = self.image_horiz.next_image()
    
        
        self.rect = self.image.get_rect()
        self.target = None  # Target node to move towards
        
        # Setting PacMan's initial position to the player spawn point
        for y, row in enumerate(maze_layout):
            for x, tile in enumerate(row):
                if tile == "p":
                    self.rect.topleft = (x * TILE_SIZE, y * TILE_SIZE)
                    break

    def draw(self):
        self.screen.blit(self.image, self.rect.topleft)

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
                self.rect.x += SPEED
                if self.rect.centerx >= self.target[0]:
                    self.rect.centerx = self.target[0]
                    self.target = None
            elif self.rect.centerx > self.target[0]:  # Move left
                self.rect.x -= SPEED
                if self.rect.centerx <= self.target[0]:
                    self.rect.centerx = self.target[0]
                    self.target = None
            elif self.rect.centery < self.target[1]:  # Move down
                self.rect.y += SPEED
                if self.rect.centery >= self.target[1]:
                    self.rect.centery = self.target[1]
                    self.target = None
            elif self.rect.centery > self.target[1]:  # Move up
                self.rect.y -= SPEED
                if self.rect.centery <= self.target[1]:
                    self.rect.centery = self.target[1]
                    self.target = None
