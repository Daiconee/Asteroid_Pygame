import pygame
from circleshape import CircleShape
from constants import *
import random


class Asteroid(CircleShape):

    def __init__(self, x, y, radius):
        
        super().__init__(x, y, radius)
        self.position = self.get_spawn_position()
        self.radius = self.get_asteroid_radius()
        self.velocity = self.get_asteroid_velocity()

    def get_spawn_position(self):
        spawn_position = ["N","S","E","W"]
        spawn_dir = spawn_position[random.randint(0, 3)]
        spawn = pygame.Vector2(0,0)
        if spawn_dir == "N" or spawn_dir == "S":
            spawn.x = random.randint(0, SCREEN_WIDTH)
            if spawn_dir == "S":
                spawn.y = SCREEN_HEIGHT

        if spawn_dir == "E" or spawn_dir == "W":
            spawn.y = random.randint(0, SCREEN_HEIGHT)
            if spawn_dir == "W":
                spawn.x = SCREEN_WIDTH
        print(spawn_dir, spawn)
        return spawn

    def get_asteroid_radius(self):
        return random.randint(1, ASTEROID_KINDS) * ASTEROID_MIN_RADIUS

    def get_asteroid_velocity(self):
        direction = pygame.Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT/2) - self.position
        direction.x = direction.x +  random.randint(-ASTEROID_SPREAD, ASTEROID_SPREAD)
        direction.y = direction.y +  random.randint(-ASTEROID_SPREAD, ASTEROID_SPREAD)
        return direction.normalize() * random.randint(1, ASTEROID_KINDS) * ASTEROID_SPEED


    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)
    
    def out_of_bounds(self):
        x = self.position.x + self.velocity.normalize.x 
        y = self.position.y + self.velocity.normalize.y  
        if x < 0 or x > SCREEN_WIDTH or y < 0 or y > SCREEN_HEIGHT:
            return True
        return False

    def update(self, dt):
        self.position += self.velocity * dt
