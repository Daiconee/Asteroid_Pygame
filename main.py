from player import *
from sys import exit 
from asteroid_daicone import Asteroid
from asteroid import Asteroid
from asteroidfield import AsteroidField
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
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable, wrapable)
    Asteroid.containers = (updatable, drawable, asteroids)
    AsteroidField.containers = (updatable)
    Shot.containers = (updatable, drawable, shots)

    player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    #asteroid = Asteroid(0,0,0)
    asteroidfield = AsteroidField()


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
            # if spawn_timer > ASTEROID_SPAWN_RATE:
            #     spawn_timer = 0
            #     asteroid = Asteroid(0,0,0)
            screen.fill((0,0,0))
            updatable.update(dt)
            for sprite in wrapable:
                sprite.wrap()
            for sprite in drawable:
                sprite.draw(screen)
            font_score = font.render(f"Score: {score}", True, "white")
            screen.blit(font_score, (50,50))
            
            for shot in shots:
                for asteroid in asteroids:
                    if shot.collision(asteroid):
                        shot.kill()
                        asteroid.kill()
                        if asteroid.radius == ASTEROID_MIN_RADIUS:
                            score += 15
                            continue
                        angle = randint(20,50)
                        if asteroid.radius == 3*ASTEROID_MIN_RADIUS:
                            score += 5
                            asteroidfield.spawn(2*ASTEROID_MIN_RADIUS, asteroid.position, asteroid.velocity.rotate(angle)*1.2)
                            asteroidfield.spawn(2*ASTEROID_MIN_RADIUS, asteroid.position, asteroid.velocity.rotate(-angle)*1.2)
                        elif asteroid.radius == 2*ASTEROID_MIN_RADIUS:
                            score += 10
                            asteroidfield.spawn(ASTEROID_MIN_RADIUS, asteroid.position, asteroid.velocity.rotate(angle)*1.2)
                            asteroidfield.spawn(ASTEROID_MIN_RADIUS, asteroid.position, asteroid.velocity.rotate(-angle)*1.2)

            for asteroid in asteroids:
                if asteroid.collision(player):
                    game_state = "game_over"
                    print("Game Over")
                    #pygame.quit()
                    #exit()
        
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




if __name__ == "__main__":
    main()