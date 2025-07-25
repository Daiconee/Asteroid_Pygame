import pygame
from particle import Particle

class AsteroidParticle(Particle):
    def __init__(self, position):
        super().__init__(position)
        self.color = (170,170,170)
        self.direction = 0
        self.speed = 10

        