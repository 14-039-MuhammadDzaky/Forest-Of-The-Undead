from settings import * 
from random import choice

class Zombie(pygame.sprite.Sprite):
	def _init_(self, pos, frames, groups, collision_sprites):
		super()._init_(groups)
		self.frames, self.frame_index = frames, 0
		self.image = self.frames[self.frame_index]
		self.rect = self.image.get_rect(topleft = pos)
		self.z = Z_LAYERS['main']

		self.direction = choice((-1,1))
		self.speed = 200
		
	def die(self):
	        self.is_alive = False
	        self.death_timer.activate()
	        self.kill()

	def reverse(self):
		if not self.hit_timer.active:
			self.direction *= -1
			self.hit_timer.activate()

	def update(self, dt):
		self.hit_timer.update()
