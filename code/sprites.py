import pygame
from config import *

class Generic_sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups,  z=LAYERS["main"]):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(bottomleft=pos)
        self.z = z
        self.hitbox = self.rect.copy().inflate((-self.rect.width * 0, -self.rect.height * 0))

class Object(Generic_sprite):
    def __init__(self, pos, surf, groups, z=LAYERS["main"]):
        super().__init__(
            pos=pos,
            surf=surf,
            groups=groups,
            z=z)
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.copy().inflate((-self.rect.width * 0.3, -self.rect.height * 0.6))