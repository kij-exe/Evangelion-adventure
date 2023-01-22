import pygame
from config import *

class Menu:
	def __init__(self):
		#	general setup
		self.active = True
		self.display_surface = pygame.display.get_surface()
		self.background = pygame.image.load("../smth.png").convert_alpha()
		self.background = pygame.transform.rotozoom(self.background, 0, SCREEN_WIDTH/1920)
		
		self.buttons = [
		Button("Singleplayer", 450, 50, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 120),
			self.switch_off),
		Button("Multiplayer", 450, 50, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50),
			print, "not finished yet")
		]

	def switch_off(self):
		self.active = False

	def run(self):
		self.display_surface.blit(self.background, (0,0))
		for button in self.buttons:
			button.update(self.display_surface)

class Button:
	def __init__(self, text, width, height, pos, func, *args):
		#	general setup
		self.pressed = False	
		self.func = func
		self.args = args
		self.shift = 6
		self.actual_shift = 6

		#	top rectangle
		pos = (pos[0] - width/2, pos[1] - height/2)
		self.pos = pos
		self.top_rect = pygame.Rect(pos, (width, height))
		self.top_colour = "#14293e"

		#	bottom rectangle
		self.bottom_rect = pygame.Rect(pos, (width, height))
		self.bottom_colour = "Black"

		#	text
		self.font = pygame.font.Font("../fonts/brokenled-2.ttf", 25)
		self.text_surf = self.font.render(text, True, "White")
		self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

		#	keys
		self.keys = pygame.mouse.get_pressed()
		
	def update(self, surface):
		self.top_rect.y = self.pos[1] - self.actual_shift
		self.text_rect.center = self.top_rect.center

		pygame.draw.rect(surface, self.bottom_colour, self.bottom_rect, border_radius=10)
		pygame.draw.rect(surface, self.top_colour, self.top_rect, border_radius=10)
		surface.blit(self.text_surf, self.text_rect)
		self.check_click()

	def check_click(self):
		pos = pygame.mouse.get_pos()
		self.prev_keys = self.keys
		self.keys = pygame.mouse.get_pressed()
		if self.top_rect.collidepoint(pos):
			self.top_colour = "#234432"
			if self.keys[0]:
				self.actual_shift = 0
				if not self.prev_keys[0]:
					self.func(self.args[0]) if self.args else self.func()
			else:
				self.actual_shift = self.shift				
		else:
			self.actual_shift = self.shift
			self.top_colour = "#222228"
