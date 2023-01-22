import pygame
from config import *

class Menu:
	def __init__(self):
		self.active = True
		self.display_surface = pygame.display.get_surface()
		self.button1 = Button("aboba", 160, 40, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

	def input(self):
		keys = 6

	def switch_off(self):
		self.active = False
  
	def update(self):
		self.display_surface.fill("White")
		self.button1.draw(self.display_surface)

class Button:
	def __init__(self, text, width, height, pos):
		self.pressed = False	

		#	top rectangle
		pos = (pos[0] - width/2, pos[1] - height/2)
		self.top_rect = pygame.Rect(pos, (width, height))
		self.top_colour = "#1b647e"

		#	text
		self.font = pygame.font.SysFont("calibri", 20)
		self.text_surf = self.font.render(text, True, "White")
		self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

	def draw(self, surface):
		pygame.draw.rect(surface, self.top_colour, self.top_rect)
		surface.blit(self.text_surf, self.text_rect)
	
	def check_click(self):
		pos = pygame.mouse.get_pos()
		mouse = pygame.mouse.get_pressed()
		if mouse[0] and self.top_rect.collidepoint(pos):
			self.pressed = True
		else:
			self.pressed = False
  
