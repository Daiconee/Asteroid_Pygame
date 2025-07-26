from player import *
from playermouse import PlayerMouse
from sys import exit 
from asteroid import Asteroid
from asteroidfield import AsteroidField
from particle import Particle

from random import randint

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
    particles = pygame.sprite.Group()

    Shot.containers = (updatable, killable, drawable, shots)
    #Player.containers = (updatable, drawable, wrapable)
    PlayerMouse.containers = (updatable, drawable, wrapable)
    Asteroid.containers = (updatable, killable, drawable, asteroids)
    AsteroidField.containers = (updatable)
    Particle.containers = (particles)
    

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

            if game_state == "game_over":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    for asteroid in asteroids:
                        asteroid.kill()
                    player.position = pygame.Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
                    score = 0   
                    game_state = "running"
                    
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
            font_score = font.render(f"Score: {score}", True, "white")
            screen.blit(font_score, (50,50))
            score += shotCollisionScoreSpawn(shots, asteroids, asteroidfield)

            keys = pygame.key.get_pressed()
            if(pygame.mouse.get_pressed()[0]):
                particle = Particle(pygame.mouse.get_pos())
                particle.color = "yellow"
            particles.draw(screen)

            for asteroid in asteroids:     
                if player.collisionAsteroid(asteroid):
                    game_state = "game_over"
                    print("Game Over")
        
        elif game_state == "game_over":
            screen.fill((0,0,0))
            if score > high_score:
                high_score = score
            font_currscore = font.render(f"Your Score: {score}", True, "white")
            font_highscore = font.render(f"Your High Score: {high_score}", True, "cyan")
            screen.blit(font_game_name, (SCREEN_WIDTH/8, SCREEN_HEIGHT/4))
            screen.blit(font_start_text, (SCREEN_WIDTH/8, 3*SCREEN_HEIGHT/4))   
            screen.blit(font_currscore, (SCREEN_WIDTH/8, SCREEN_HEIGHT/2))   
            screen.blit(font_highscore, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
                    
        pygame.display.flip()


def shotCollisionScoreSpawn(shots, asteroids, asteroidfield):
    score = 0
    for shot in shots:
        for asteroid in asteroids:
            if shot.collision(asteroid):
                shot.kill()
                asteroid.kill()
                score += asteroidfield.spawnAfterShot(asteroid)
    return score

if __name__ == "__main__":
    main()