import pygame
from sys import exit 
from constants import *
from player import Player

def main():
    pygame.init()
    pygame.display.set_caption("Asteroids")
    
    WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        dt = clock.tick(60) / 1000
        #print(dt)
        WIN.fill((0,0,0))
        player.update(dt)
        player.wrap()
        player.draw(WIN)

        pygame.display.flip()

if __name__ == "__main__":
    main()