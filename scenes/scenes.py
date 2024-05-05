import json
from loguru import logger
import pygame

from bodies.bodies import Enemy, Player
from textures.textures import TextureMaster

GRID = 64

class Scene():
    def __init__(self, screen):
        info = pygame.display.Info()
        self.WIDTH, self.HEIGHT = info.current_w, info.current_h
        self.screen = screen
        
    def update():
        pass
    

class Level(Scene):
    def __init__(self, screen, config_file):
        super().__init__(screen)
        self.background = (40, 40, 40)
        self.input = Input()
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.player = None
        self.enemies = pygame.sprite.Group()
        self.texture = TextureMaster()
        self.map = None
        
        self.player_collision = False
        
        # TODO: Clean this up for dealing with where center of camera is
        self.map_center = (11, 9)
        self.row_length = 22
        self.col_length = 18
        
        self.x_offset = 0.0
        self.y_offset = 0.0
        
        self.load_config(config_file)
        
    def load_config(self, config_file):
        with open(config_file, 'r') as file:
            config = json.load(file)
            for enemy_config in config['enemies']:
                enemy = Enemy(position = enemy_config['position'])
                self.all_sprites.add(enemy)
                self.enemies.add(enemy)
            player = Player(position = config['player']['position'])
            self.all_sprites.add(player)
            self.player = player
            self.map = config['map']

    def update(self, event):
        self.screen.fill(self.background)
        self.input.update()
        self.collision_look_ahead()
        self.all_sprites.update(self.input, self.player.move_speed, self.player_collision)
        if not self.player_collision:     
            self.x_offset -= self.input.x_axis * self.player.move_speed
            self.y_offset -= self.input.y_axis * self.player.move_speed

        self.draw_map()
        self.draw_hitboxes()
        self.visual_collisions()
                
        pygame.display.flip()
    
    def draw_hitboxes(self):
        self.all_sprites.draw(self.screen)
        if self.player:
            self.player.draw_hitbox(self.screen)
        for enemy in self.enemies:
            enemy.draw_hitbox(self.screen)
        
    def draw_map(self):
        # for row_i, row in enumerate(self.map):
        #     for col_i, col in enumerate(row):
        #         self.texture.draw_grid(self.screen, col, col_i - 1, row_i - 1, self.x_offset, self.y_offset)
        for row_i, row in enumerate(self.map[self.map_center[1] - self.col_length // 2 : self.map_center[1] + self.col_length // 2]):
            for col_i, col in enumerate(row[self.map_center[0] - self.row_length // 2 : self.map_center[0] + self.row_length // 2]):
                self.texture.draw_grid(self.screen, col, col_i - 1, row_i - 1, self.x_offset, self.y_offset)

    def collision_look_ahead(self):
        hitbox = self.player.get_lookahead_hitbox(self.input)
        self.player_collision = False
        for enemy in self.enemies:
            if enemy.hitbox:
                if hitbox.colliderect(enemy.hitbox):
                    self.player_collision = True
                    # logger.debug(f"Player collision lookahead: {self.player_collision}")
                    
    def visual_collisions(self):
        if self.player:
            for enemy in self.enemies:
                collision = self.player.visual_hitbox.colliderect(enemy.visual_hitbox)
                if collision:
                    self.handle_visual_collisions(self.player, enemy)
                    
    def handle_visual_collisions(self, player, enemy):
        # TODO: Layers 0 and 1 were used for learning. Probably need a better settings when environment factored in
        if player.y > enemy.y:
            self.all_sprites.change_layer(player, 1)
            self.all_sprites.change_layer(enemy, 0)
        else:
            self.all_sprites.change_layer(player, 0)
            self.all_sprites.change_layer(enemy, 1)
        # logger.debug(f"Player {player} collided with Enemy {enemy}")
        
    
    
class Menu(Scene):
    def __init__(self, screen):
        super().__init__(screen)
        self.background = (40, 40, 40)
        
        self.DROPDOWN_WIDTH = 150
        self.DROPDOWN_HEIGHT = 30
        
        self.OPTION_HEIGHT = 30
        
        self.FONT_SIZE = 24
        self.font = pygame.font.SysFont(None, self.FONT_SIZE)
        
        self.show_options = False
        self.selected_option = 0
        
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (200, 200, 200)
        self.BG = (75, 85, 65)
        

    def update(self, event):
        self.screen.fill(self.background)
        # running = True
        dropdown_rect = pygame.Rect(100, 100, self.DROPDOWN_WIDTH, self.DROPDOWN_HEIGHT)
        options = ["Option 1", "Option 2", "Option 3"]
        
        
        # while running:
        self.screen.fill(self.BG)
            
        if event:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if dropdown_rect.collidepoint(event.pos):
                    self.show_options = not self.show_options
                elif self.show_options:
                    for i in range(len(options)):
                        option_rect = pygame.Rect(100, 100 + self.DROPDOWN_HEIGHT + i * self.OPTION_HEIGHT, self.DROPDOWN_WIDTH, self.OPTION_HEIGHT)
                        if option_rect.collidepoint(event.pos):
                            self.selected_option = i
                            logger.debug(f'Option {self.selected_option} selected')
                            self.show_options = False
            
        self.draw_dropdown(100, 100, options, self.selected_option)
        if self.show_options:
            self.draw_options(100, 100 + self.DROPDOWN_HEIGHT, options, self.selected_option)
                  
        pygame.display.flip()
        
    def draw_dropdown(self, x, y, options, selected_option):
        pygame.draw.rect(self.screen, self.GRAY, (x, y, self.DROPDOWN_WIDTH, self.DROPDOWN_HEIGHT))
        pygame.draw.rect(self.screen, self.BLACK, (x, y, self.DROPDOWN_WIDTH, self.DROPDOWN_HEIGHT), 2)
        
        text = self.font.render(options[selected_option], True, self.BLACK)
        text_rect = text.get_rect(center=(x + self.DROPDOWN_WIDTH // 2, y + self.DROPDOWN_HEIGHT // 2))
        self.screen.blit(text, text_rect)

    def draw_options(self, x, y, options, selected_option):
        for i, option in enumerate(options):
            if i == selected_option:
                pygame.draw.rect(self.screen, self.GRAY, (x, y + i * self.OPTION_HEIGHT, self.DROPDOWN_WIDTH, self.OPTION_HEIGHT))
            pygame.draw.rect(self.screen, self.BLACK, (x, y + i * self.OPTION_HEIGHT, self.DROPDOWN_WIDTH, self.OPTION_HEIGHT), 2)
            
            text = self.font.render(option, True, self.BLACK)
            text_rect = text.get_rect(center=(x + self.DROPDOWN_WIDTH // 2, y + i * self.OPTION_HEIGHT + self.OPTION_HEIGHT // 2))
            self.screen.blit(text, text_rect)    
    
class Input():
    def __init__(self):
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()

    def update(self):
        self.x_axis = self.process_axis(self.joystick.get_axis(0))
        self.y_axis = self.process_axis(self.joystick.get_axis(1))
        self.a_button = self.joystick.get_button(0)
        # print(self.a_button)
       

    def process_axis(self, value: float):
        value = round(value, 1)
        threshold = 0.55
        if value <= threshold and value >= 0.0:
            value = 0.0
        elif value >= -threshold and value < 0.0:
            value = 0.0
        else:
            value = value
        return value