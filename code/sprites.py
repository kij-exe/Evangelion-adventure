import pygame
from config import *

class Generic_sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups,  z=LAYERS["main"]):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(bottomleft=pos)
        self.z = z
        self.hitbox = self.rect.copy().inflate((-self.rect.width * 0, -self.rect.height * 0))

class Collision_object(pygame.sprite.Sprite):
    def __init__(self, pos, dimensions, groups):
        super().__init__(groups)
        self.image = pygame.Surface(dimensions)
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.copy()