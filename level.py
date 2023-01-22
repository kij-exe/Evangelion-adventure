import pygame
from player import Player
from sprites import Generic_sprite, Object
from config import *
from pytmx.util_pygame import load_pygame
import sys

class Level:
    def __init__(self):

        self.display_surface = pygame.display.get_surface()
        self.debug_mode_active = False

        self.all_sprites = CameraGroup()
        self.collision_sprites = CollisionGroup()

        self.setup()

    def setup(self):
        main_map = load_pygame("tiled/tmx/main_map.tmx")

        #   ground
        for x, y, surf in main_map.get_layer_by_name("ground").tiles():
            Generic_sprite(
                pos=(x * 64, (y+1) * 64),
                surf=surf,
                groups=self.all_sprites,
                z=LAYERS["ground"])

        #   buildings
        for x, y, surf in main_map.get_layer_by_name("tile_buildings").tiles():
            Generic_sprite(
                pos=(x * 64, (y+1) * 64),
                surf=surf,
                groups=self.all_sprites,
                z=LAYERS["main"])

        #   player
        for obj in main_map.get_layer_by_name("player"):
            if obj.name == "start":
                self.player = Player(
                    pos=(obj.x, obj.y), 
                    group=self.all_sprites, 
                    collision_sprites=self.collision_sprites,
                    toggle_debug_mode=self.toggle_debug_mode)

        #   objects
        for obj in main_map.get_layer_by_name("objects"):
            Object(
                pos=(obj.x, obj.y + 64),
                surf=obj.image,
                groups=(self.all_sprites, self.collision_sprites))

        #   collisions
        for x, y, surf in main_map.get_layer_by_name("collisions").tiles():
            Generic_sprite(
                pos=(x * 64, (y+1) * 64),
                surf=pygame.Surface((64, 64)),
                groups=self.collision_sprites)

        self.font = pygame.font.SysFont("comicsansms", 24)

    def show_fps(self, dt):
        fps = round(1 / dt) if dt else -1
        fps_surf = self.font.render(str(fps), True, "White")
        fps_rect = fps_surf.get_rect(topleft=(10, 10))
        pygame.draw.rect(self.display_surface, "Black", fps_rect)
        self.display_surface.blit(fps_surf, fps_rect)

    def toggle_debug_mode(self):
        self.debug_mode_active = not self.debug_mode_active

    def run(self, dt):
        #   self.display_surface.fill("#80a7fb")
        self.display_surface.fill("white")
        self.all_sprites.custom_draw(self.player)
        self.all_sprites.update(dt)
        if self.debug_mode_active:
            self.show_fps(dt)
            self.collision_sprites.custom_draw(self.player)


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - SCREEN_WIDTH // 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT // 2
        for layer in LAYERS.values():
            for sprite in sorted(self.sprites(), key=lambda x: x.rect.centery):
                if sprite.z == layer:
                    offset_pos = sprite.rect.topleft - self.offset
                    self.display_surface.blit(sprite.image, offset_pos)

class CollisionGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - SCREEN_WIDTH // 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT // 2
        for sprite in self.sprites():
            offset_rect = sprite.hitbox.move(-self.offset.x, -self.offset.y)
            pygame.draw.rect(self.display_surface, "Black", offset_rect)
        pygame.draw.rect(self.display_surface, "Black", player.hitbox.move(-self.offset.x, -self.offset.y))
