from settings import * 
from level import Level
from pytmx.util_pygame import load_pygame
from os.path import join
from support import * 
from data import Data
from debug import debug
from ui import UI
from overworld import Overworld

class Game:
	def __init__(self):
		pygame.init()
		self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
		pygame.display.set_caption('Forest of The Undead')
		self.clock = pygame.time.Clock()
		self.import_assets()

		self.ui = UI(self.font, self.ui_frames)
		self.data = Data(self.ui)
		self.tmx_maps = {
			0: load_pygame(join('..', 'data', 'levels', '1.tmx')),
			1: load_pygame(join('..', 'data', 'levels', '2.tmx')),
			2: load_pygame(join('..', 'data', 'levels', '3.tmx')),
			}
		self.tmx_overworld = load_pygame(join('..', 'data', 'overworld', 'overworld.tmx'))
		self.current_stage = Overworld(self.tmx_overworld, self.data, self.overworld_frames, self.switch_stage)
		self.bg_music.play(-1)

	def switch_stage(self, target, unlock = 0):
		if target == 'level':
			if unlock > 3:
				self.current_stage = Overworld(self.tmx_overworld, self.data, self.overworld_frames, )
			self.current_stage = Level(self.tmx_maps[self.data.current_level], self.level_frames, self.audio_files, self.data, self.switch_stage)
			
		else: # overworld 
			if unlock > 0:
				self.data.unlocked_level = 1
			else:
				self.data.health -= 1
			self.current_stage = Overworld(self.tmx_overworld, self.data, self.overworld_frames, self.switch_stage)

	def import_assets(self):
		self.level_frames = {
			'flag': import_folder('..', 'asset', 'level', 'flag'),
			'saw': import_folder('..', 'asset', 'enemies', 'saw', 'animation'),
			'floor_spike': import_folder('..', 'asset','enemies', 'floor_spikes'),
			'palms': import_sub_folders('..', 'asset', 'level', 'palms'),
			'candle': import_folder('..', 'asset','level', 'candle'),
			'window': import_folder('..', 'asset','level', 'window'),
			'big_chain': import_folder('..', 'asset','level', 'big_chains'),
			'small_chain': import_folder('..', 'asset','level', 'small_chains'),
			'candle_light': import_folder('..', 'asset','level', 'candle light'),
			'player': import_sub_folders('..', 'asset','player'),
			'saw': import_folder('..', 'asset', 'enemies', 'saw', 'animation'),
			'saw_chain': import_image('..',  'asset', 'enemies', 'saw', 'saw_chain'),
			'helicopter': import_folder('..', 'asset', 'level', 'helicopter'),
			'boat': import_folder('..',  'asset', 'objects', 'boat'),
			'spike': import_image('..',  'asset', 'enemies', 'spike_ball', 'Spiked Ball'),
			'spike_chain': import_image('..',  'asset', 'enemies', 'spike_ball', 'spiked_chain'),
			'zombies': import_folder('..', 'asset','enemies', 'zombies', 'run'),
			'wizard': import_sub_folders('..', 'asset','enemies', 'wizard'),
			'pearl': import_image('..',  'asset', 'enemies', 'bullets', 'pearl'),
			'items': import_sub_folders('..', 'asset', 'items'),
			'particle': import_folder('..', 'asset', 'effects', 'particle'),
			'water_top': import_folder('..', 'asset', 'level', 'water', 'top'),
			'water_body': import_image('..', 'asset', 'level', 'water', 'body'),
			'bg_tiles': import_folder_dict('..', 'asset', 'level', 'bg', 'tiles'),
		}
		self.font = pygame.font.Font(join('..', 'asset', 'ui', 'runescape_uf.ttf'), 40)
		self.ui_frames = {
			'heart': import_folder('..', 'asset', 'ui', 'heart'), 
			'coin':import_image('..', 'asset', 'ui', 'coin')
		}
		self.overworld_frames = {
			'palms': import_folder('..', 'asset', 'overworld', 'palm'),
			'water': import_folder('..', 'asset', 'overworld', 'water'),
			'path': import_folder_dict('..', 'asset', 'overworld', 'path'),
			'icon': import_sub_folders('..', 'asset', 'overworld', 'icon'),
		}

		self.audio_files = {
			'coin': pygame.mixer.Sound(join('..', 'audio', 'coin.wav')),
			'attack': pygame.mixer.Sound(join('..', 'audio', 'attack.wav')),
			'jump': pygame.mixer.Sound(join('..', 'audio', 'jump.wav')), 
			'damage': pygame.mixer.Sound(join('..', 'audio', 'damage.wav')),
			'pearl': pygame.mixer.Sound(join('..', 'audio', 'pearl.wav')),
		}
		self.bg_music = pygame.mixer.Sound(join('..', 'audio', 'starlight_city.mp3'))
		self.bg_music.set_volume(0.5)

	def check_game_over(self):
		if self.data.health <= 0:
			self.ui.game_over = True
			self.current_stage = Overworld(self.tmx_overworld, self.data, self.overworld_frames, self.switch_stage)
			self.bg_music.stop()

	def run(self):
		while True:
			dt = self.clock.tick() / 1000
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
				if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
					if self.ui.game_over:
						action = self.ui.check_buttons(event.pos)
						if action == "quit":
							pygame.quit()
							exit()
						elif action == "restart":
							self.ui.game_over = False
							self.data.health = 3
							self.data.current_level = 0
							self.bg_music.play(-1)
							
			self.check_game_over()
			self.current_stage.run(dt)
			self.ui.update(dt)
			
			pygame.display.update()

if __name__ == '__main__':
	game = Game()
	game.run()
