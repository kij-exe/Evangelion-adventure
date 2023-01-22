import pygame
from sys import exit
import time
from pytmx.util_pygame import load_pygame

class Button:
    def __init__(self, text, pos, width, height):
        self.


all_sprites = pygame.sprite.Group()

w, h = 1280, 720
c = 0
pygame.init()
screen_surf = pygame.display.set_mode((w, h))
screen_surf.fill("White")
pygame.display.set_caption("Game")
clock = pygame.time.Clock()

font = pygame.font.SysFont("calibri light", 40)

ground_surf = pygame.Surface((1500, 125))
ground_rect = ground_surf.get_rect(bottom=h)
ground_surf.fill("brown")

text_surf = font.render("Bruh moment", False, "Black")
text_rect = text_surf.get_rect(center=(w/2, 150))

test_surface = pygame.Surface((100, 100))
test_rect = test_surface.get_rect(center=(100,100))
hitbox = test_rect.copy().inflate((-test_rect.x * 0.2, -test_rect.y * 1))
print(hitbox.colliderect(test_rect))


previous_time = time.time()
while True:
    dt = time.time() - previous_time
    previous_time = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen_surf.fill("White")
    screen_surf.blit(ground_surf, (0,0))
    pygame.draw.rect(screen_surf, "Light blue", text_rect, 8, 15)
    screen_surf.blit(text_surf, text_rect)

    pygame.draw.rect(screen_surf, "Black", test_rect)
    pygame.draw.rect(screen_surf, "Light blue", hitbox)

    all_sprites.draw(screen_surf)
    

    pygame.display.update()
