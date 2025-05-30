from settings import * 
from random import choice
from timer import Timer

class Zombies(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, collision_sprites):
        super().__init__(groups)
        # Animation setup
        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.z = Z_LAYERS['main']
        self.hit_cooldown = Timer(200)  # For damage cooldown
        self.health = 1
        self.is_alive = True
        
        self.direction = choice((-1, 1))
        self.speed = 100
        self.collision_rects = [sprite.rect for sprite in collision_sprites]
        
        self.health = 1
        self.is_alive = True
        
        self.hit_timer = Timer(250)  # For direction reversal cooldown
        self.hit_cooldown = Timer(200)  # For damage cooldown
        self.death_timer = Timer(300)  # Optional: for death animation

    def get_damage(self):
        if not self.hit_cooldown.active and self.is_alive:
            self.health -= 1
            self.hit_cooldown.activate()
            
            if self.health <= 0:
                self.reverse()

    def die(self):
        self.is_alive = False
        self.death_timer.activate()
        self.kill()
        

    def reverse(self):
        if not self.hit_timer.active:
            self.direction *= -1
            self.hit_timer.activate()

    def check_collisions(self):
        floor_rect_right = pygame.Rect(self.rect.bottomright, (1, 1))
        floor_rect_left = pygame.Rect(self.rect.bottomleft, (-1, 1))
        wall_rect = pygame.Rect(self.rect.topleft + vector(-1, 0), 
                              (self.rect.width + 2, 1))


        if (floor_rect_right.collidelist(self.collision_rects) < 0 and self.direction > 0) or \
           (floor_rect_left.collidelist(self.collision_rects) < 0 and self.direction < 0) or \
           (wall_rect.collidelist(self.collision_rects) != -1):
            self.reverse()

    def animate(self, dt):
        self.frame_index += ANIMATION_SPEED * dt
        self.image = self.frames[int(self.frame_index % len(self.frames))]
        if self.direction < 0:
            self.image = pygame.transform.flip(self.image, True, False)

    def update(self, dt):
        if not self.is_alive:
            return

        self.hit_timer.update()
        self.hit_cooldown.update()
        self.death_timer.update()

        self.animate(dt)
        self.check_collisions()
        self.rect.x += self.direction * self.speed * dt

class Wizard(pygame.sprite.Sprite):
	def __init__(self, pos, frames, groups, reverse, player, create_pearl):
		super().__init__(groups)

		if reverse:
			self.frames = {}
			for key, surfs in frames.items():
				self.frames[key] = [pygame.transform.flip(surf, True, False) for surf in surfs]
			self.bullet_direction = -1
		else:
			self.frames = frames 
			self.bullet_direction = 1

		self.frame_index = 0
		self.state = 'idle'
		self.image = self.frames[self.state][self.frame_index]
		self.rect = self.image.get_rect(topleft = pos)
		self.old_rect = self.rect.copy()
		self.z = Z_LAYERS['main']
		self.player = player
		self.shoot_timer = Timer(1000)
		self.has_fired = False
		self.create_pearl = create_pearl

	def state_management(self):
		player_pos, shell_pos = vector(self.player.hitbox_rect.center), vector(self.rect.center)
		player_near = shell_pos.distance_to(player_pos) < 700
		player_front = shell_pos.x < player_pos.x if self.bullet_direction > 0 else shell_pos.x > player_pos.x
		player_level = abs(shell_pos.y - player_pos.y) < 30

		if player_near and player_front and player_level and not self.shoot_timer.active:
			self.state = 'fire'
			self.frame_index = 0
			self.shoot_timer.activate()

	def update(self, dt):
		self.shoot_timer.update()
		self.state_management()

		self.frame_index += ANIMATION_SPEED * dt
		if self.frame_index < len(self.frames[self.state]):
			self.image = self.frames[self.state][int(self.frame_index)]


			if self.state == 'fire' and int(self.frame_index) == 3 and not self.has_fired:
				self.create_pearl(self.rect.center, self.bullet_direction)
				self.has_fired = True 

		else:
			self.frame_index = 0
			if self.state == 'fire':
				self.state = 'idle'
				self.has_fired = False

class Pearl(pygame.sprite.Sprite):
    def __init__(self, pos, groups, surf, direction, speed):
        super().__init__(groups)
        self.pearl = True  
        self.image = surf
        self.rect = self.image.get_rect(center = pos + vector(50 * direction, 0))
        self.direction = direction  
        self.speed = speed
        self.z = Z_LAYERS['main']  

        self.timers = {
            'lifetime': Timer(5000),    
            'reverse': Timer(100)       
        }
        self.timers['lifetime'].activate()

    def reverse(self):
        if not self.timers['reverse'].active:
            self.direction *= -1
            self.timers['reverse'].activate()

    def die(self):
        self.kill()

    def update(self, dt):
        for timer in self.timers.values():
            timer.update()

        self.rect.x += self.direction * self.speed * dt

        if not self.timers['lifetime'].active:
            self.die()
