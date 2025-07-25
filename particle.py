import pygame

# Base class for game particles

class Particle(pygame.sprite.Sprite):
    def __init__(self, position:pygame.math.Vector2):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = position
        self.createSurf()
        self.color = self.__class__.color
        self.direction = self.__class__.direction
        self.speed = self.__class__.speed
    
    def createSurf(self):
        self.image = pygame.Surface((4,4)).convert_alpha()
        self.image.set_colorkey("black")
        pygame.draw.circle(self.image, self.color, (2,2), 2)
        self.rect = self.image.get_rect(center=self.position)
# Note: pygame.sprite.Group.draw uses the Sprite.image attribute for the source surface, and Sprite.rect for the position


