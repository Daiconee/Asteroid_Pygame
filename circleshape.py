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

class Shot(CircleShape):

    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        
    def draw(self, screen):
        pygame.draw.circle(screen, "red", self.position, self.radius, 2)

    def update(self, dt):
        self.position += self.velocity * dt
        self.killFromGroups()


class Bomb(CircleShape):

    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.timer = BOMB_TIMER
        

    def draw(self, screen):
        if self.timer < 0:
            self.radius += 1
            pygame.draw.circle(screen, "red", self.position, self.radius, 2)
        else:
            pygame.draw.circle(screen, "red", self.position, self.radius, 2)
            pygame.draw.circle(screen, "red", self.position, self.radius*2, 2)
            

    
    def update(self, dt):
        self.timer -= dt
        self.checkMaxRadius()
    
    def checkMaxRadius(self):
        if self.radius >= MAX_BOMB_RADIUS:
            self.kill()
    
    def collision(self, otherCircle):
        if self.timer > 0:
            return False
        return super().collision(otherCircle)