import pygame
from support import import_folder
from config import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, characters, collision_sprites, toggle_debug_mode, obj_name):
        super().__init__(group, characters)

        #   general setup
        self.obj_name = obj_name
        self.import_assets(obj_name)
        self.status = "down"
        self.frame_index = 0

        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.z = LAYERS["main"]
        self.toggle_debug_mode = toggle_debug_mode
        self.keys = pygame.key.get_pressed()

        #   movement direction
        self.direction = pygame.math.Vector2(0, 0)
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200

        #   collisions
        self.hitbox = self.rect.copy().inflate((-self.rect.width * 0.3, -self.rect.height * 0.6))
        self.collision_sprites = collision_sprites
        self.characters = characters

    def import_assets(self, obj_name):
        self.animations = {"up": [], "down": [], "right": [], "left": [],
                           "up_idle": [], "down_idle": [], "left_idle": [], "right_idle": []}
        for animation in self.animations.keys():
            path = f"../graphics/characters/{obj_name}/" + animation
            self.animations[animation] = import_folder(path)

    def animate(self, dt):
        self.frame_index += 5 * dt
        self.get_status()
        if self.frame_index >= len(self.animations[self.status]): self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index)]

    def get_status(self):
        if not self.direction.magnitude():
            self.status = self.status.split("_")[0] + "_idle"

    def input(self):
        self.prev_keys = self.keys
        self.keys = pygame.key.get_pressed()

        #   vertical movemment
        if self.keys[pygame.K_w]:
            self.direction.y = -1
            self.status = "up"
        elif self.keys[pygame.K_s]:
            self.direction.y = 1
            self.status = "down"
        else:
            self.direction.y = 0

        #   horizontal movement
        if self.keys[pygame.K_d]:
            self.direction.x = 1
            self.status = "right"
        elif self.keys[pygame.K_a]:
            self.direction.x = -1
            self.status = "left"
        else:
            self.direction.x = 0

        #   toggling debug mode
        if self.keys[pygame.K_y] and not self.prev_keys[pygame.K_y]:
            self.toggle_debug_mode()


    def collision(self, direction):
        collidabale_chars = [a for a in self.characters.sprites() if a.obj_name != self.obj_name]
        for sprite in self.collision_sprites.sprites() + collidabale_chars:
            if sprite.hitbox.colliderect(self.hitbox):
                if direction == "horizontal":
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
                    self.rect.centerx = self.hitbox.centerx
                    self.pos.x = self.hitbox.centerx

                if direction == "vertical":
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
                    self.rect.centery = self.hitbox.centery
                    self.pos.y = self.hitbox.centery
    def move(self, dt):

        #   normalizing the vector to maintain the same speed in any directions
        if self.direction.magnitude(): self.direction.normalize_ip()

        #   horizontal movement
        self.pos.x += self.speed * self.direction.x * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        self.collision("horizontal")

        #   vertical movement
        self.pos.y += self.speed * self.direction.y * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        self.collision("vertical")

    def update(self, dt):
        #   self.input()
        self.move(dt)
        self.animate(dt)