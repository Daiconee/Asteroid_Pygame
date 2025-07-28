import pygame
import random
from asteroid import Asteroid
from asteroid_strong import Asteroid_Strong
from constants import *


class AsteroidField(pygame.sprite.Sprite):
    edges = [
        [
            pygame.Vector2(1, 0),
            lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
        ],
        [
            pygame.Vector2(-1, 0),
            lambda y: pygame.Vector2(
                SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT
            ),
        ],
        [
            pygame.Vector2(0, 1),
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS),
        ],
        [
            pygame.Vector2(0, -1),
            lambda x: pygame.Vector2(
                x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS
            ),
        ],
    ]

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.reset()
        

    def spawn(self, radius, position, velocity):
        if self.game_level > 2:
            asteroid = self.chooseSpawn()(position.x, position.y, radius)
        else:
            asteroid = Asteroid(position.x, position.y, radius)
        asteroid.velocity = velocity
    
    def chooseSpawn(self):
        return Asteroid if random.random() > self.strong_spawn_rate else Asteroid_Strong

    def spawnAfterShot(self, asteroid):
        score = 0
        if asteroid.radius == ASTEROID_MIN_RADIUS:
            score += 15
        angle = random.randint(20,100)
        if asteroid.radius == 3*ASTEROID_MIN_RADIUS:
            score += 5
            self.spawn(2*ASTEROID_MIN_RADIUS, asteroid.position, asteroid.velocity.rotate(angle)*1.4)
            self.spawn(2*ASTEROID_MIN_RADIUS, asteroid.position, asteroid.velocity.rotate(-angle)*1.4)
        elif asteroid.radius == 2*ASTEROID_MIN_RADIUS:
            score += 10
            self.spawn(ASTEROID_MIN_RADIUS, asteroid.position, asteroid.velocity.rotate(angle)*1.6)
            self.spawn(ASTEROID_MIN_RADIUS, asteroid.position, asteroid.velocity.rotate(-angle)*1.6)
        return score 
    
    def update(self, dt):
        self.spawn_timer += dt
        if self.spawn_timer > self.spawn_rate:
            self.spawn_timer = 0

            # spawn a new asteroid at a random edge
            edge = random.choice(self.edges)
            speed = random.randint(40, 100)
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))
            position = edge[1](random.uniform(0, 1))
            kind = random.randint(1, ASTEROID_KINDS)
            self.spawn(ASTEROID_MIN_RADIUS * kind, position, velocity)

    def reset(self):
        self.spawn_timer = 0.0
        self.spawn_rate = ASTEROID_SPAWN_RATE
        self.strong_spawn_rate = 0.5
        self.game_level = 1