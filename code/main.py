from settings import * 
from level import Level
from pytmx.util_pygame import load_pygame
from os.path import join
from support import * 
from data import Data
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
