import pygame
from player import Player
from sprites import Generic_sprite, Collision_object
from config import *
from pytmx.util_pygame import load_pygame
import sys

class Level:
    def __init__(self):

        self.display_surface = pygame.display.get_surface()
        self.debug_mode_active = False

        self.all_sprites = CameraGroup()
        self.collision_sprites = CollisionGroup()
        self.characters = pygame.sprite.Group()
        self.player_index = 0

        self.offset = pygame.Vector2()

        self.keys = pygame.key.get_pressed()

        self.setup()

    def setup(self):
        main_map = load_pygame("../tiled/tmx/main_map.tmx")

        #   ground
        for x, y, surf in main_map.get_layer_by_name("ground").tiles():
            Generic_sprite(
                pos=(x * 64, (y+1) * 64),
                surf=surf,
                groups=self.all_sprites,
                z=LAYERS["ground"])

        #   buildings
        for x, y, surf in main_map.get_layer_by_name("building_tiled").tiles():
            Generic_sprite(
                pos=(x * 64, (y+1) * 64),
                surf=surf,
                groups=self.all_sprites,
                z=LAYERS["main"])

        input_functions = {
        "toggle_debug_mode": self.toggle_debug_mode,
        "switch_player": self.switch_player
        }

        #   initialization of playable characters
        for obj in main_map.get_layer_by_name("characters"):
            match obj.name:
                case "shinji_ikari":
                    self.player1 = Player(
                        pos=(obj.x, obj.y), 
                        group=self.all_sprites,
                        characters=self.characters, 
                        collision_sprites=self.collision_sprites,
                        input_functions=input_functions,
                        obj_name=obj.name)
                    self.offset = pygame.Vector2(obj.x - SCREEN_WIDTH//2, obj.y - SCREEN_HEIGHT//2)
               
                case "ayanami_rei":
                    self.player2 = Player(
                        pos=(obj.x, obj.y), 
                        group=self.all_sprites,
                        characters=self.characters,
                        collision_sprites=self.collision_sprites,
                        input_functions=input_functions,
                        obj_name=obj.name)

        #   collisions
        for obj in main_map.get_layer_by_name("collisions"):
            Collision_object(
                pos=(obj.x, obj.y),
                dimensions=(obj.width, obj.height),
                groups=self.collision_sprites)

        self.font = pygame.font.SysFont("comicsansms", 24)

        self.current_player = self.player1

    def show_fps(self, dt):
        fps = round(1 / dt) if dt else -1
        fps_surf = self.font.render(str(fps), True, "White")
        fps_rect = fps_surf.get_rect(topleft=(10, 10))
        pygame.draw.rect(self.display_surface, "Black", fps_rect)
        self.display_surface.blit(fps_surf, fps_rect)

    def toggle_debug_mode(self):
        self.debug_mode_active = not self.debug_mode_active

    def switch_player(self):
        self.current_player.direction = pygame.math.Vector2(0, 0)
        self.player_index += 1
        self.player_index %= len(self.characters.sprites())
        self.current_player = self.characters.sprites()[self.player_index]

    def calculated_offset(self, dt):
        #   not smooth camera
        #   self.offset.x = player.rect.centerx - SCREEN_WIDTH // 2
        #   self.offset.y = player.rect.centery - SCREEN_HEIGHT // 2

        #   smooth camera
        self.offset.x += (self.current_player.rect.centerx - self.offset.x - SCREEN_WIDTH // 2) * 4  * dt
        self.offset.y += (self.current_player.rect.centery - self.offset.y - SCREEN_HEIGHT // 2) * 4 * dt

        #   getting rid of rounding effects
        int_offset = pygame.Vector2(int(self.offset.x), int(self.offset.y))

        return int_offset


    def run(self, dt):
        #   self.display_surface.fill("#80a7fb")
        self.display_surface.fill("white")

        offset = self.calculated_offset(dt)

        self.all_sprites.custom_draw(offset)

        if self.debug_mode_active:
            self.collision_sprites.custom_draw(offset, self.characters)
            self.show_fps(dt)

        self.prev_keys = self.keys
        self.keys = pygame.key.get_pressed()

        self.current_player.input(self.keys, self.prev_keys)
        self.all_sprites.update(dt)


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

    def custom_draw(self, offset):
        for layer in LAYERS.values():
            for sprite in sorted(self.sprites(), key=lambda x: x.rect.centery):
                if sprite.z == layer:
                    offset_pos = sprite.rect.topleft - offset
                    self.display_surface.blit(sprite.image, offset_pos)

class CollisionGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

    def draw_alpha_rect(self, rect, colour):
        surf = pygame.Surface((rect.width, rect.height))
        surf_rect = surf.get_rect(topleft=rect.topleft)
        surf.set_alpha(128)
        surf.fill(colour)
        self.display_surface.blit(surf, surf_rect)

    def custom_draw(self, offset, players):
        for sprite in self.sprites() + players.sprites():
            offset_rect = sprite.hitbox.move(-offset.x, -offset.y)

            self.draw_alpha_rect(offset_rect, "Green")
            #   pygame.draw.rect(self.display_surface, "Black", offset_rect)