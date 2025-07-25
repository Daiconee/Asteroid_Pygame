import pygame
from circleshape import CircleShape
from constants import *
import random

class Asteroid(CircleShape):
    numPoints = 8
    rotationAngle = 360 / numPoints

    def __init__(self, x, y, radius):  
        super().__init__(x, y, radius)
        self.points = []
        self.generatePoints()

    def draw(self, screen):
        points = [(self.position + point) for point in self.points]
        pygame.draw.polygon(screen, "white", points, 2)
        pygame.draw.circle(screen, "red", self.position, 4, 2)

    def generatePoints(self):
        for i in range(Asteroid.numPoints):
            pointFromCenter = pygame.math.Vector2(self.radius, 0).rotate(i * Asteroid.rotationAngle)
            pointFromCenter *= random.uniform(0.8, 1.0)
            self.points.append(pointFromCenter)


    def update(self, dt):
        self.position += self.velocity * dt
        self.killFromGroups()