import pygame
from circleshape import *
from constants import *

class PlayerMouse(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.mouseDirNorm = pygame.math.Vector2(0,0)
        self.len = 60
        self.reset()
        self.genImg()
        # self.genMask()
        self.resetInvincibilityTicker()
        
    def draw(self, screen):
        if not self.invincibilityTicker % 7:
            self.genImg()
            tri = self.triangle()
            pygame.draw.polygon(self.image, self.color, tri, 2)
            self.genMask()
            screen.blit(self.image, self.rect)
        # maskImg = self.mask.to_surface().convert_alpha()
        # maskImg.set_colorkey("black")
        # screen.blit(maskImg, (0,0)) # draw mask on screen to check 
        # pygame.draw.circle(screen, "green", self.position, 4, 2) # check self.position on screen
        # pygame.draw.rect(screen, "white", self.rect, 2) # draw rect on screen to check 
        
    
    def triangle(self):
        center = (self.len // 2, self.len // 2)
        perpend = self.mouseDirNorm.rotate(90)
        a = center + self.len * 0.4 * self.mouseDirNorm
        b = center - self.len * 0.2 * (self.mouseDirNorm + perpend)
        c = center - self.len * 0.2 * (self.mouseDirNorm - perpend)
        return (a, b, c)

    def collisionAsteroid(self, asteroid):
        p = (-self.rect.x + asteroid.rect.x, -self.rect.y + asteroid.rect.y)
        if self.mask.overlap(asteroid.mask, p):
            if not self.invincible:
                self.health -= 1
                if self.health <= 0:
                    return True 
                self.toggleInvincibility()

    def reset(self):
        self.shotTimer = 0
        self.bombTimer = 0
        self.health = PLAYER_STARTING_HEALTH
        self.invincible = False
        self.invincible_timer = PLAYER_INVINCIBILITY_DURATION
        self.color = "red"

    def genImg(self):    
        self.image = pygame.Surface((self.len,self.len)).convert_alpha()
        self.image.set_colorkey("black")
        self.rect = self.image.get_rect(center=self.position)
    
    def genMask(self):
        self.mask = pygame.mask.from_surface(self.image)
    
    def update(self, dt):
        self.shotTimer -= dt
        self.bombTimer -= dt
        self.processInvincibility(dt)
        self.updateMouseDir()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.shotTimer < 0:
            self.shotTimer = PLAYER_SHOOT_COOLDOWN
            self.shoot()
        
        if keys[pygame.K_LSHIFT] and self.bombTimer < 0:
            self.bombTimer = PLAYER_BOMB_COOLDOWN
            self.dropBomb()

        if keys[pygame.K_a]:
            self.move(dt, pygame.K_a)
        if keys[pygame.K_d]:
            self.move(dt, pygame.K_d)
        if keys[pygame.K_w]:
            self.move(dt, pygame.K_w)
        if keys[pygame.K_s]:
            self.move(dt, pygame.K_s)

        self.rect.center = self.position

    def processInvincibility(self, dt):
        if self.invincible:
            self.invincible_timer -= dt
            self.invincibilityTicker += 1
            if self.invincible_timer < 0:
                self.toggleInvincibility()
                self.resetInvincibilityTicker()

    def toggleInvincibility(self):
        self.invincible = True if not self.invincible else False
        self.color = "green" if self.invincible else "red"
        self.invincible_timer = PLAYER_INVINCIBILITY_DURATION
        
    def resetInvincibilityTicker(self):
        self.invincibilityTicker = 7

    def updateMouseDir(self):
        mouseX, mouseY = pygame.mouse.get_pos()
        mouseDir = pygame.math.Vector2(mouseX - self.position.x,
                            mouseY - self.position.y)
        self.mouseDirNorm = mouseDir.normalize()
    
    def move(self, dt, key):
        dist = dt * PLAYER_SPEED
        if key == pygame.K_a:
            self.position.x -= dist
        elif key == pygame.K_d:
            self.position.x += dist
        elif key == pygame.K_w:
            self.position.y -= dist
        else:
            self.position.y += dist
        
    def wrap(self):
        if self.position.x < 0:
            self.position.x = SCREEN_WIDTH
        elif self.position.x > SCREEN_WIDTH:
            self.position.x = 0

        if self.position.y < 0:
            self.position.y = SCREEN_HEIGHT
        elif self.position.y > SCREEN_HEIGHT:
            self.position.y = 0 
    
    def shoot(self):
        shot = Shot(self.position.x, self.position.y, SHOT_RADIUS)
        shot.velocity = PLAYER_SHOOT_SPEED * self.mouseDirNorm
    


    def dropBomb(self):
        bomb = Bomb(self.position.x, self.position.y, BOMB_RADIUS)