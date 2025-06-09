import pygame
from sys import exit 
from constants import *
from player import Player

def main():
    pygame.init()
    pygame.display.set_caption("Asteroids")
    
    WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    wrapable = pygame.sprite.Group()

    Player.containers = (updatable, drawable, wrapable)
    player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        dt = clock.tick(60) / 1000
        WIN.fill((0,0,0))

        updatable.update(dt)
        for sprite in wrapable:
            sprite.wrap()
        for sprite in drawable:
            sprite.draw(WIN)

        pygame.display.flip()

if __name__ == "__main__":
    main()