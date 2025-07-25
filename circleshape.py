import pygame
from constants import *

# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        # we will be using this later
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen):
        # sub-classes must override
        pass

    def update(self, dt):
        # sub-classes must override
        pass

    def collision(self, otherCircle):
        if self.radius + otherCircle.radius > self.position.distance_to(otherCircle.position):
            return True
        return False
    
    def killFromGroups(self):
        if (self.position.y > SCREEN_HEIGHT + ASTEROID_MAX_RADIUS
            or self.position.y < -ASTEROID_MAX_RADIUS
            or self.position.x > SCREEN_WIDTH + ASTEROID_MAX_RADIUS
            or self.position.x < -ASTEROID_MAX_RADIUS):
            self.kill()