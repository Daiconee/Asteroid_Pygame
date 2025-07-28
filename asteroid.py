import pygame
from circleshape import CircleShape
from constants import *
import random

class Asteroid(CircleShape):
    numPoints = 8
    rotationAngle = 360 / numPoints
    starting_health = 1

    def __init__(self, x, y, radius):  
        super().__init__(x, y, radius)
        self.health = self.__class__.starting_health
        self.points = []
        self.imgCenter = pygame.math.Vector2(radius, radius) # center on self.image
        self.genPoints()
        self.genImg()
        self.genMask()
        

    def draw(self, screen):
        self.rect.center = self.position
        screen.blit(self.image, self.rect)
        #pygame.draw.rect(screen, "white", self.rect, 2)
        #pygame.draw.circle(screen, "green", self.position, 4, 2) # check self.position on screen
        
        # -------- another way to blit on screen without using rect - don't know if performance differs
        # correctedPos = self.position - self.imgCenter
        # screen.blit(self.image, correctedPos)
        # pygame.draw.circle(screen, "green", self.position, 4, 2) # check self.position on screen

    def genPoints(self):
        for i in range(self.numPoints):
            pointFromCenter = pygame.math.Vector2(self.radius, 0).rotate(i * Asteroid.rotationAngle)
            pointFromCenter *= random.uniform(0.5, 1.0)
            self.points.append((self.radius,self.radius) + pointFromCenter)
    
    def genImg(self):
        self.image = pygame.Surface((2*self.radius,2*self.radius)).convert_alpha()
        self.image.set_colorkey("black")
        self.rect = self.image.get_rect(center=self.position)
        pygame.draw.polygon(self.image, "white", self.points, 2)
        #pygame.draw.circle(self.image, "red", self.imgCenter, 4, 2)

    def genMask(self):
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        self.position += self.velocity * dt
        # somehow putting `self.rect.center = self.position` here results in a bug
        # where the asteroid appears in the top left when spawning
        self.killFromGroups()