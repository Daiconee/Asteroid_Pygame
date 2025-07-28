from asteroid import *

class Asteroid_Strong(Asteroid):
    starting_health = 2

    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        
    def draw(self, screen):
        super().draw(screen)
        if self.health > 1:
            pygame.draw.circle(screen, "red", self.rect.center, 4, 2)
    
    def genImg(self):
        super().genImg()
        