from settings import *
from sprites import Sprite, MovingSprite, AnimatedSprite, Spike, Item, ParticleEffectSprite
from player import Player
from groups import AllSprites
from enemies import Zombies, Wizard, Pearl
from random import uniform

class Level:
	def __init__(self, tmx_map, level_frames, audio_files, data, switch_stage):
		self.display_surface = pygame.display.get_surface()
		self.data = data
		self.switch_stage = switch_stage

		self.level_width = tmx_map.width * TILE_SIZE
		self.level_bottom = tmx_map.height * TILE_SIZE
		tmx_level_properties = tmx_map.get_layer_by_name('Data')[0].properties
		self.level_unlock = tmx_level_properties['level_unlock']
		if tmx_level_properties['bg']:
			bg_tile = level_frames['bg_tiles'][tmx_level_properties['bg']]
		else:
			bg_tile = None

		self.all_sprites = AllSprites(
			width = tmx_map.width, 
			height = tmx_map.height,
			bg_tile = bg_tile, 
			top_limit = tmx_level_properties['top_limit'],
			horizon_line = tmx_level_properties['horizon_line'])
		self.collision_sprites = pygame.sprite.Group()
		self.semi_collision_sprites = pygame.sprite.Group()
		self.damage_sprites = pygame.sprite.Group()
		self.zombies_sprites = pygame.sprite.Group()
		self.pearl_sprites = pygame.sprite.Group()
		self.item_sprites = pygame.sprite.Group()

		self.setup(tmx_map, level_frames, audio_files)

		self.pearl_surf = level_frames['pearl']
		self.particle_frames = level_frames['particle']

		# audio
		self.coin_sound = audio_files['coin']
		self.coin_sound.set_volume(0.4)
		self.damage_sound = audio_files['damage']
		self.damage_sound.set_volume(0.5)
		self.pearl_sound = audio_files['pearl']
