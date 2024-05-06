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
        
    def update(self, events):
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
        
        self.camera = Camera()
        
        self.load_config(config_file)
        
        # TODO: This is needed to initialize sprites or else it throws attribute errors. Figure out a way so this is unneeded as it may cause unwanted stuff to happen.
        self.all_sprites.update(self.input, self.player.move_speed, self.player_collision)
        
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

    def update(self, events):
        self.screen.fill(self.background)
        self.input.update()
        self.collision_look_ahead()
        self.all_sprites.update(self.input, self.player.move_speed, self.player_collision)
        if not self.player_collision:     
            self.camera.x -= self.input.x_axis * self.player.move_speed
            self.camera.y -= self.input.y_axis * self.player.move_speed

        self.draw_map()
        self.all_sprites.draw(self.screen)
        self.draw_hitboxes()
        self.visual_collisions()
        
        
                
        pygame.display.flip()
    
    def draw_hitboxes(self):
        if self.player:
            self.player.draw_hitbox(self.screen, self.player.visual_hitbox)
        for enemy in self.enemies:
            enemy.draw_hitbox(self.screen, enemy.visual_hitbox)
        
    def draw_map(self):
        # TODO: Cleanup variable names
        for row_i, row in enumerate(self.map[self.camera.y_slice]):
            for col_i, col in enumerate(row[self.camera.x_slice]):
                self.texture.draw_grid(self.screen, col, col_i - 1, row_i - 1, self.camera)

    def collision_look_ahead(self):
        hitbox = self.player.get_lookahead_hitbox(self.input)
        self.player_collision = False
        for enemy in self.enemies:
            if enemy.hitbox:
                if hitbox.colliderect(enemy.hitbox):
                    self.player_collision = True
                    logger.debug(f"Player collision lookahead: {self.player_collision}")
                    
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
        logger.debug(f"Player {player} collided with Enemy {enemy}")
        
    
    
class Menu(Scene):
    def __init__(self, screen):
        super().__init__(screen)
        self.background = (40, 40, 40)
        self.fields = {}
        self.fields['option_dropdown'] = Dropdown(self.screen, 100, 100)
        self.fields['edit_dropdown'] = Dropdown(self.screen, 300, 100)
        
        

    def update(self, events):
        self.screen.fill(self.background)
        
        for event in events:
            # TODO: Make this more efficient. Check all fields rectcollide and pass to the appropriate one
            if event.type == pygame.MOUSEBUTTONDOWN:
                for field in self.fields.values():
                    field.update(event)
        
        for field in self.fields.values():
            field.draw()       
        
        pygame.display.flip()
        
class Field():
    def __init__(self, screen, x, y):
        self.screen = screen
        self.x = x
        self.y = y
         
            
class Dropdown(Field):
    def __init__(self, screen, x, y):
        super().__init__(screen, x, y)
        self.DROPDOWN_WIDTH = 150
        self.DROPDOWN_HEIGHT = 30
        
        self.OPTION_HEIGHT = 30
        
        self.FONT_SIZE = 24
        self.font = pygame.font.SysFont(None, self.FONT_SIZE)
        
        self.show_options = False
        self.selected_option = 0
        
        self.dropdown_rect = pygame.Rect(self.x, self.y, self.DROPDOWN_WIDTH, self.DROPDOWN_HEIGHT)
        self.options = ["Option 1", "Option 2", "Option 3"]
        
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (200, 200, 200)
        
    def update(self, event):
        if self.dropdown_rect.collidepoint(event.pos):
            self.show_options = not self.show_options
        elif self.show_options:
            for i in range(len(self.options)):
                option_rect = pygame.Rect(self.x, self.y + self.DROPDOWN_HEIGHT + i * self.OPTION_HEIGHT, self.DROPDOWN_WIDTH, self.OPTION_HEIGHT)
                if option_rect.collidepoint(event.pos):
                    self.selected_option = i
                    logger.debug(f'Option {self.selected_option} selected')
                    self.show_options = False
    
    def draw(self):
        pygame.draw.rect(self.screen, self.GRAY, (self.x, self.y, self.DROPDOWN_WIDTH, self.DROPDOWN_HEIGHT))
        pygame.draw.rect(self.screen, self.BLACK, (self.x, self.y, self.DROPDOWN_WIDTH, self.DROPDOWN_HEIGHT), 2)
        text = self.font.render(self.options[self.selected_option], True, self.BLACK)
        text_rect = text.get_rect(center=(self.x + self.DROPDOWN_WIDTH // 2, self.y + self.DROPDOWN_HEIGHT // 2))
        self.screen.blit(text, text_rect)
        if self.show_options:
            self.draw_options()
            
    def draw_options(self):
        x = self.x
        y = self.y + self.DROPDOWN_HEIGHT
        for i, option in enumerate(self.options):
            if i == self.selected_option:
                pygame.draw.rect(self.screen, self.GRAY, (x, y + i * self.OPTION_HEIGHT, self.DROPDOWN_WIDTH, self.OPTION_HEIGHT))
            pygame.draw.rect(self.screen, self.BLACK, (x, y + i * self.OPTION_HEIGHT, self.DROPDOWN_WIDTH, self.OPTION_HEIGHT), 2)
            
            text = self.font.render(option, True, self.BLACK)
            text_rect = text.get_rect(center=(x + self.DROPDOWN_WIDTH // 2, y + i * self.OPTION_HEIGHT + self.OPTION_HEIGHT // 2))
            self.screen.blit(text, text_rect)    
    
            
class Camera():
    def __init__(self):
        self.map_center = (11, 9)
        self.row_length = 22
        self.col_length = 18
        self._x = 0.0
        self._y = 0.0
        self.center_offset = [0.0, 0.0]
        
        # map_center = [int(self.map_center[0] - self.center_offset[0]), int(self.map_center[1] - self.center_offset[1])]
        # map_center[0] - self.camera.row_length // 2 : map_center[0] + self.camera.row_length // 2
        self.y_slice = slice(int(self.map_center[1] - self.center_offset[1] - self.col_length // 2), 
                             int(self.map_center[1] - self.center_offset[1] + self.col_length // 2)
                             )
        self.x_slice = slice(int(self.map_center[0] - self.center_offset[0] - self.row_length // 2), 
                             int(self.map_center[0] - self.center_offset[0] + self.row_length // 2)
                             )
        
    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y
    
    @x.setter
    def x(self, value):
        # TODO: Find better way to deal with precision issue
        self._x = round(value, 5)
        self.center_offset[0] = self._x // 64
        self.x_slice = slice(int(self.map_center[0] - self.center_offset[0] - self.row_length // 2), 
                             int(self.map_center[0] - self.center_offset[0] + self.row_length // 2)
                             )

    @y.setter
    def y(self, value):
        # TODO: Find better way to deal with precision issue
        self._y = round(value, 5)
        self.center_offset[1] = self._y // 64
        self.y_slice = slice(int(self.map_center[1] - self.center_offset[1] - self.col_length // 2), 
                             int(self.map_center[1] - self.center_offset[1] + self.col_length // 2)
                             )
        
    
class Input():
    def __init__(self):
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()
        self.x_axis = 0.0
        self.y_axis = 0.0

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