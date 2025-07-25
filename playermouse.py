import pygame
from circleshape import CircleShape
from shot import Shot
from constants import *

class PlayerMouse(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.mouseDirNorm = pygame.math.Vector2(0,0)
        self.timer = 0

    def triangle(self):
        perpend = self.mouseDirNorm.rotate(90)
        a = self.position + 30 * self.mouseDirNorm
        b = self.position - 5 * self.mouseDirNorm + 15 * perpend 
        c = self.position - 5 * self.mouseDirNorm - 15 * perpend
        return (a,b,c)

    def draw(self, screen):
        pygame.draw.polygon(screen, "red", self.triangle(), 2)

    def update(self, dt):
        self.timer -= dt
        self.updateMouseDir()
            
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.timer < 0:
            self.timer = PLAYER_SHOOT_COOLDOWN
            self.shoot()

        if keys[pygame.K_a]:
            self.move(dt, pygame.K_a)
        if keys[pygame.K_d]:
            self.move(dt, pygame.K_d)
        if keys[pygame.K_w]:
            self.move(dt, pygame.K_w)
        if keys[pygame.K_s]:
            self.move(dt, pygame.K_s)


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