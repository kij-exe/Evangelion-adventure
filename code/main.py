import sys
import subprocess

try:
    import pygame, pytmx
except ModuleNotFoundError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pytmx"])

import pygame, time
from level import Level
from menu import Menu
from config import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Evangelion adventure")
        self.clock = pygame.time.Clock()
        self.level = Level()
        self.menu = Menu()
        

    def run(self):
        previous_time = time.time() - 1
        while True:
            dt = time.time() - previous_time
            previous_time = time.time()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.menu.switch_off()

            if self.menu.active:
                self.menu.run(dt)
            else:
                 self.level.run(dt)

            #   self.clock.tick(120)
            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
