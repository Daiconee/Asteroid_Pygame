from player import *
from playermouse import PlayerMouse
from sys import exit 
from asteroid import Asteroid
from asteroidfield import AsteroidField
import random

def main():
    pygame.init()
    pygame.display.set_caption("Asteroids")
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    score = 0
    high_score = 0
    spawn_timer = 0
    game_state = "running"
    font = pygame.font.SysFont(None, 50)

    font_game_name = font.render("Asteroids", True, "white")
    font_start_text = font.render("Press 'r' to start", True, "white")
    
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    wrapable = pygame.sprite.Group()
    killable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Shot.containers = (updatable, killable, drawable, shots)
    Player.containers = (updatable, drawable, wrapable)
    PlayerMouse.containers = (updatable, drawable, wrapable)
    Asteroid.containers = (updatable, killable, drawable, asteroids)
    AsteroidField.containers = (updatable)

    player = PlayerMouse(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    asteroidfield = AsteroidField()

    background_image = pygame.image.load("assets/Space_Background.png")

    alpha_value = 120  # Adjust this value for desired darkness (0-255)
    dark_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    dark_overlay.fill((0, 0, 0, alpha_value))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()        

        dt = clock.tick(60) / 1000

        if game_state == "running":
            spawn_timer += dt
            screen.blit(background_image, (0, 0))
            screen.blit(dark_overlay, (0,0))
            updatable.update(dt)
            for sprite in wrapable:
                sprite.wrap()
            for sprite in drawable:
                sprite.draw(screen)
            for sprite in killable:
                sprite.killFromGroups()

            for shot in shots:
                for asteroid in asteroids:
                    if shot.collision(asteroid):
                        shot.kill()
                        asteroid.kill()
                        if asteroid.radius == ASTEROID_MIN_RADIUS:
                            score += 15
                            continue
                        angle = random.randint(20,100)
                        if asteroid.radius == 3*ASTEROID_MIN_RADIUS:
                            score += 5
                            asteroidfield.spawn(2*ASTEROID_MIN_RADIUS, asteroid.position, asteroid.velocity.rotate(angle)*1.4)
                            asteroidfield.spawn(2*ASTEROID_MIN_RADIUS, asteroid.position, asteroid.velocity.rotate(-angle)*1.4)
                        elif asteroid.radius == 2*ASTEROID_MIN_RADIUS:
                            score += 10
                            asteroidfield.spawn(ASTEROID_MIN_RADIUS, asteroid.position, asteroid.velocity.rotate(angle)*1.6)
                            asteroidfield.spawn(ASTEROID_MIN_RADIUS, asteroid.position, asteroid.velocity.rotate(-angle)*1.6)
                      
        pygame.display.flip()


if __name__ == "__main__":
    main()