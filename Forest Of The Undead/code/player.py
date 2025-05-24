from settings import * 
from timer import Timer
from os.path import join
from math import sin

class Player(pygame.sprite.Sprite):
	def __init__(self, pos, groups, collision_sprites, frames, data):
		super().__init__(groups)
		self.z = Z_LAYERS['main']
		self.data = data
		 
		self.frames, self.frame_index = frames, 0
		self.state, self.facing_right = 'idle', True
		self.image = self.frames[self.state][self.frame_index]

		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox_rect = self.rect.inflate(-76, -36)
		self.old_rect = self.hitbox_rect.copy()

		# movement 
		self.direction = vector()
		self.speed = 200
		self.gravity = 1300
		self.jump = False
		self.jump_height = 700
		self.attacking = False

		# collision 
		self.collision_sprites = collision_sprites
		self.semi_collision_sprites = semi_collision_sprites
		self.on_surface = {'floor': False, 'left': False, 'right': False}
		self.platform = None

		# timer
		self.timers = {
			'wall jump': Timer(400),
			'wall slide block': Timer(250),
			'platform skip': Timer(100),
			'attack block': Timer(500),
			'hit': Timer(400)
		}

		# audio 
		self.attack_sound = attack_sound
		self.jump_sound = jump_sound


	def input(self):
		keys = pygame.key.get_pressed()
		input_vector = vector(0,0)
		if not self.timers['wall jump'].active:
			
			if keys[pygame.K_d]:
				input_vector.x += 1
				self.facing_right = True
			
			if keys[pygame.K_a]:
				input_vector.x -= 1
				self.facing_right = False
			
			if keys[pygame.K_s]:
				self.timers['platform skip'].activate()

			if keys[pygame.K_SPACE]:
				self.attack()

			self.direction.x = input_vector.normalize().x if input_vector else input_vector.x

		if keys[pygame.K_w]:
			self.jump = True		

	def move(self, dt):
		# horizontal 
		self.hitbox_rect.x += self.direction.x * self.speed * dt
		self.collision('horizontal')
		
		# vertical 
		if not self.on_surface['floor'] and any((self.on_surface['left'], self.on_surface['right'])) and not self.timers['wall slide block'].active:
			self.direction.y = 0
			self.hitbox_rect.y += self.gravity / 10 * dt
		else:
			self.direction.y += self.gravity / 2 * dt
			self.hitbox_rect.y += self.direction.y * dt
			self.direction.y += self.gravity / 2 * dt

		if self.jump:
			if self.on_surface['floor']:
				self.direction.y = -self.jump_height
				self.timers['wall slide block'].activate()
				self.hitbox_rect.bottom -= 1
				self.jump_sound.play()
			elif any((self.on_surface['left'], self.on_surface['right'])) and not self.timers['wall slide block'].active:
				self.timers['wall jump'].activate()
				self.direction.y = -self.jump_height
				self.direction.x = 1 if self.on_surface['left'] else -1
				self.jump_sound.play()
			self.jump = False
		
		self.collision('vertical')
		self.semi_collision()
		self.rect.center = self.hitbox_rect.center

   def attack(self):

   def animate(self, dt):
   def get_damage(self):
   def update(self, dt):
	   self.input()
	   self.move(dt)
	   self.animate(dt)
