import pygame
from playermouse import *
from sys import exit 
from asteroid import Asteroid
from asteroidfield import AsteroidField
from particle import Particle

def main():
    pygame.init()
    pygame.display.set_caption("Asteroids")
    

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    score = 0
    high_score = 0
    spawn_timer = 0
    game_state = "running"
    game_level = 1
    levelup_score = LEVEL_UP_SCORE
    font = pygame.font.SysFont(None, 30)

    font_game_name = font.render("Asteroids", True, "white")
    font_start_text = font.render("Press 'r' to start", True, "white")
    
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    wrapable = pygame.sprite.Group()
    killable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    bombs = pygame.sprite.Group()
    particles = pygame.sprite.Group()

    Shot.containers = (updatable, killable, drawable, shots)
    PlayerMouse.containers = (updatable, drawable, wrapable)
    Asteroid.containers = (updatable, killable, drawable, asteroids)
    AsteroidField.containers = (updatable)
    Particle.containers = (particles, updatable, killable)
    Bomb.containers = (updatable, drawable, killable, bombs)
    

    player = PlayerMouse(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    asteroidfield = AsteroidField()

    bg_images =[0]
    for i in range(4):
        new_image = pygame.image.load(f"assets/level{i+1}BG.png")
        bg_images.append(new_image)

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

            # -------------- update level and spawning ---------------
            if score > levelup_score and game_level < 4: # increase spawn rate at every level
                game_level += 1
                asteroidfield.spawn_rate /= 1.5
                levelup_score *= 2 # increase new score hit to level up 
                if game_level > 2:
                    asteroidfield.game_level = game_level  
            # --------------------------------------------------------

            spawn_timer += dt
            screen.blit(bg_images[game_level], (0, 0))
            screen.blit(dark_overlay, (0,0))
            updatable.update(dt)
            for sprite in wrapable:
                sprite.wrap()
            for sprite in drawable:
                sprite.draw(screen)
            for sprite in killable:
                sprite.killFromGroups()
            particles.draw(screen)

            # -------------- score and level text --------------------
            font_score = font.render(f"Score: {score}", True, "white")
            level_display = font.render(f"Level: {game_level}", True, "white")
            screen.blit(font_score, (50,50))
            screen.blit(level_display, (SCREEN_WIDTH - 150,50))
            # spawn_rate = font.render(f"Spawn rate: {asteroidfield.spawn_rate}", True, "white")
            # screen.blit(spawn_rate, (SCREEN_WIDTH - 300,100))
            # --------------------------------------------------------

            # -------------- handle shot asteroid collision ------------------
            score += shotCollisionScoreSpawn(shots, bombs, asteroids, asteroidfield)
            # ----------------------------------------------------------------

            # -------------- asteroid player collision check ---------
            for asteroid in asteroids:     
                if player.collisionAsteroid(asteroid):
                    player.reset()
                    asteroidfield.reset()
                    game_level = 1
                    game_state = "game_over"
            # --------------------------------------------------------
        
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


def shotCollisionScoreSpawn(shots, bombs, asteroids, asteroidfield):
    score = 0
    for shot in shots:
        for asteroid in asteroids:
            score = handleObjectCollision(shot, asteroid, asteroidfield, score)
    for bomb in bombs:
        for asteroid in asteroids:
            score = handleObjectCollision(bomb, asteroid, asteroidfield, score)
    return score

def handleObjectCollision(obj, asteroid, asteroidfield, score):
    if obj.collision(asteroid):
        if isinstance(obj, Shot):
            obj.kill()
        if asteroid.health == 1:
            asteroid.kill()
            spawnParticles(asteroid)
            score += asteroidfield.spawnAfterShot(asteroid)
        else:
            asteroid.health -= 1
    return score

def spawnParticles(asteroid):
    for i in range(3):
        particle = Particle(asteroid.position.x, asteroid.position.y, 2)

if __name__ == "__main__":
    main()