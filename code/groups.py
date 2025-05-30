from settings import * 
from sprites import Sprite
from support import import_image
from random import choice, randint
from timer import Timer

class WorldSprites(pygame.sprite.Group):
	def __init__(self, data):
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.data = data
		self.offset = vector()

	def draw(self, target_pos):
		self.offset.x = -(target_pos[0] - WINDOW_WIDTH / 2)
		self.offset.y = -(target_pos[1] - WINDOW_HEIGHT / 2)

		for sprite in sorted(self, key = lambda sprite: sprite.z):
			if sprite.z < Z_LAYERS['main']:
				if sprite.z == Z_LAYERS['path']:
					if sprite.level <= self.data.unlocked_level:
						self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset)
				else:
					self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset)
		
		for sprite in sorted(self, key = lambda sprite: sprite.rect.centery):
			if sprite.z == Z_LAYERS['main']:
				if hasattr(sprite, 'icon'):
					self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset + vector(0,-28))
				else:
					self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset)

		

class AllSprites(pygame.sprite.Group):
	def __init__(self, width, height, horizon_line, bg_tile = None, top_limit = 0):
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.offset = vector()
		self.width, self.height = width * TILE_SIZE, height * TILE_SIZE
		self.borders = {
			'left': 0,
			'right': -self.width + WINDOW_WIDTH,
			'bottom': -self.height + WINDOW_HEIGHT,
			'top': top_limit}
		self.sky = not bg_tile
		self.horizon_line = horizon_line
		self.bg_image = import_image('..', 'asset', 'level', 'bg', 'tiles', 'Background')
		self.bg_image = pygame.transform.scale(self.bg_image, (WINDOW_WIDTH, WINDOW_HEIGHT))  # optional scaling


		if bg_tile:
			for col in range(width):
				for row in range(-int(top_limit / TILE_SIZE) - 1, height):
					x, y = col * TILE_SIZE, row * TILE_SIZE
					Sprite((x,y), bg_tile, self, -1)

	def camera_constraint(self):
		self.offset.x = self.offset.x if self.offset.x < self.borders['left'] else self.borders['left']
		self.offset.x = self.offset.x if self.offset.x > self.borders['right'] else self.borders['right'] 
		self.offset.y = self.offset.y if self.offset.y > self.borders['bottom'] else self.borders['bottom']
		self.offset.y = self.offset.y if self.offset.y < self.borders['top'] else self.borders['top']

	def background(self):
		self.display_surface.blit(self.bg_image, (0, 0))

	def draw(self, target_pos, dt):
		self.offset.x = -(target_pos[0] - WINDOW_WIDTH / 2)
		self.offset.y = -(target_pos[1] - WINDOW_HEIGHT / 2)
		self.camera_constraint()

		if self.sky:
			self.background()

		for sprite in sorted(self, key = lambda sprite: sprite.z):
			offset_pos = sprite.rect.topleft + self.offset
			self.display_surface.blit(sprite.image, offset_pos)
