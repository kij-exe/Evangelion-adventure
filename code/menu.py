import pygame
from config import *
from support import import_folder

class Menu:
	def __init__(self):
		#	general setup
		self.active = True
		self.display_surface = pygame.display.get_surface()
		self.background = pygame.image.load("../menu_pic.png").convert_alpha()
		scale = SCREEN_WIDTH/1920
		self.background = pygame.transform.rotozoom(self.background, 0, scale)

		self.sound = pygame.mixer.Sound("../audio/Cicada_menu_sound.mp3")
		self.sound.set_volume(0.1)
		self.sound.play(loops=-1)

		self.buttons = [
		Button("Singleplayer", 450, 50, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 120),
			self.switch_off),
		Button("Multiplayer", 450, 50, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50),
			self.toggle_tree)
		]

		self.tree = EasterEgg(536, 186, scale)
		self.group_single = pygame.sprite.GroupSingle(self.tree)
		self.tree_active = True

	def switch_off(self):
		self.active = False
		self.sound.stop()

	def toggle_tree(self):
		self.tree_active = not self.tree_active

	def run(self, dt):
		self.display_surface.blit(self.background, (0,0))
		for button in self.buttons:
			button.update(self.display_surface)

		if self.tree_active:
			self.group_single.update(dt)
			self.group_single.draw(self.display_surface)

class Button:
	def __init__(self, text, width, height, pos, func, *args):
		#	general setup
		self.pressed = False	
		self.func = func
		self.args = args
		self.shift = 6
		self.actual_shift = 6

		#	click sound
		self.click_sound = pygame.mixer.Sound("../audio/dota_2_meep_merp.mp3")
		self.click_sound.set_volume(0.5)

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
					self.click_sound.play()
					self.func(self.args[0]) if self.args else self.func()
			else:
				self.actual_shift = self.shift				
		else:
			self.actual_shift = self.shift
			self.top_colour = "#222228"

class EasterEgg(pygame.sprite.Sprite):
	def __init__(self, x, y, scale):
		super().__init__()
		self.frame_index = 0

	
		self.frames = []
		path = "../graphics/easter_egg"
		self.frames = import_folder(path)
		for index, frame in enumerate(self.frames):
			self.frames[index] = pygame.transform.rotozoom(frame, 0, 0.35 * scale)

		self.image = self.frames[self.frame_index]
		self.rect = self.image.get_rect(center=(x * scale, y * scale))

	def animate(self, dt):
		self.frame_index += 25 * dt
		if self.frame_index >= len(self.frames): self.frame_index = 0
		self.image = self.frames[int(self.frame_index)]

	def update(self, dt):
		self.animate(dt)

