from player import *
from sys import exit 
#from asteroid_anuj import Asteroid
from asteroid import Asteroid
from asteroidfield import AsteroidField

def main():
    pygame.init()
    pygame.display.set_caption("Asteroids")
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    wrapable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable, wrapable)
    Asteroid.containers = (updatable, drawable, asteroids)
    AsteroidField.containers = (updatable)
    Shot.containers = (updatable, drawable)

    player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    #asteroid = Asteroid(0,0,0)
    asteroidfield = AsteroidField()
    spawn_timer = 0 

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        dt = clock.tick(60) / 1000
        spawn_timer += dt
        # if spawn_timer > ASTEROID_SPAWN_RATE:
        #     spawn_timer = 0
        #     asteroid = Asteroid(0,0,0)
        screen.fill((0,0,0))
        updatable.update(dt)
        for sprite in wrapable:
            sprite.wrap()
        for sprite in drawable:
            sprite.draw(screen)

        for asteroid in asteroids:
            if asteroid.collision(player):
                print("Game Over")
                pygame.quit()
                exit()

        pygame.display.flip()

if __name__ == "__main__":
    main()