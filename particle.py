import pygame
from random import uniform
from circleshape import CircleShape
from constants import *

# Base class for game particles
class Particle(CircleShape):
    color = "yellow"
    speed = 100

    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.speed = self.__class__.speed
        self.velocity = self.speed * pygame.math.Vector2(uniform(-1,1), uniform(-1, 1)).normalize()
        self.color = self.__class__.color
        self.alpha = 255
        self.createSurf()
    
    def createSurf(self):
        self.image = pygame.Surface((4,4)).convert_alpha()
        self.image.set_colorkey("black")
        pygame.draw.circle(self.image, self.color, (2,2), self.radius)
        self.rect = self.image.get_rect(center=self.position)
    
    def update(self, dt):
        changeInPos = dt * (self.velocity)
        self.rect.center += changeInPos
        self.position += changeInPos
        self.checkAlpha(dt)
# Note: pygame.sprite.Group.draw uses the Sprite.image attribute for the source surface, and Sprite.rect for the position
    
    def fade(self, dt):
        self.alpha -= PARTICLE_FADE_SPEED * dt 
        self.image.set_alpha(self.alpha)

    def checkAlpha(self, dt):
        self.fade(dt)
        if self.alpha <= 0:
            self.kill()


class AsteroidParticle(Particle):
    color = (170, 170, 170)
    speed = 10
    def __init__(self, position, direction):
        super().__init__(position, direction)