from settings import * 
from sprites import AnimatedSprite
from random import randint
from os.path import join
from timer import Timer

class UI:
    def __init__(self, font, frames):
        self.display_surface = pygame.display.get_surface()
        self.sprites = pygame.sprite.Group()
        self.font = font
        self.big_font = pygame.font.SysFont('Arial', 60)  
        
        # health / hearts 
        self.heart_frames = frames['heart']
        self.heart_surf_width = self.heart_frames[0].get_width()
        self.heart_padding = 6

        # coins 
        self.coin_amount = 0
        self.coin_timer = Timer(1000)
        self.coin_surf = frames['coin']

        # Game over state
        self.game_over = False
        self.restart_rect = None
        self.quit_rect = None

    def create_hearts(self, amount):
        for sprite in self.sprites:
            sprite.kill()
        for heart in range(amount):
            x = 10 + heart * (self.heart_surf_width + self.heart_padding)
            y = 10
            Heart((x,y), self.heart_frames, self.sprites)
   
    def display_coins(self):
        text_surf = self.font.render(str(self.coin_amount), False, '#ffffff')
        text_rect = text_surf.get_rect(topleft=(16, 34))  
        
        coin_rect = self.coin_surf.get_rect(center=text_rect.bottomleft).move(0, -6)
        
        # Show to game
        self.display_surface.blit(text_surf, text_rect)
        self.display_surface.blit(self.coin_surf, coin_rect)

    def display_game_over(self):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.display_surface.blit(overlay, (0, 0))
        self.big_font = pygame.font.Font(join('..', 'asset', 'ui', 'runescape_uf.ttf'), 60)

        game_over_text = self.big_font.render("Game Over", True, (255, 50, 50))
        game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 100))
        self.display_surface.blit(game_over_text, game_over_rect)

        restart_text = self.font.render("RESTART", True, (255, 255, 255))
        self.restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 50))
        pygame.draw.rect(self.display_surface, (50, 50, 50), self.restart_rect.inflate(20, 20))
        self.display_surface.blit(restart_text, self.restart_rect)

        quit_text = self.font.render("QUIT", True, (255, 255, 255))
        self.quit_rect = quit_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 120))
        pygame.draw.rect(self.display_surface, (50, 50, 50), self.quit_rect.inflate(20, 20))
        self.display_surface.blit(quit_text, self.quit_rect)

    def check_buttons(self, pos):
        if self.game_over:
            if self.restart_rect and self.restart_rect.collidepoint(pos):
                return "restart"
            elif self.quit_rect and self.quit_rect.collidepoint(pos):
                return "quit"
        return None

    def display_text(self):
        if self.coin_timer.active:
            text_surf = self.font.render(str(self.coin_amount), False, '#ffffff')
            text_rect = text_surf.get_rect(topleft = (16,34))
            self.display_surface.blit(text_surf, text_rect)

            coin_rect = self.coin_surf.get_rect(center = text_rect.bottomleft).move(0,-6)
            self.display_surface.blit(self.coin_surf, coin_rect)

    def show_coins(self, amount):
        self.coin_amount = amount
        self.coin_timer.activate()

    def update(self, dt):
        self.display_coins()
        self.sprites.update(dt)
        self.sprites.draw(self.display_surface)
        self.display_text()
        if self.game_over:
            self.display_game_over()

class Heart(AnimatedSprite):
    def __init__(self, pos, frames, groups):
        super().__init__(pos, frames, groups)
        self.active = False

    def animate(self, dt):
        self.frame_index += ANIMATION_SPEED * dt
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:
            self.active = False
            self.frame_index = 0

    def update(self, dt):
        if self.active:
            self.animate(dt)
        else:
            if randint(0,2000) == 1:
                self.active = True
