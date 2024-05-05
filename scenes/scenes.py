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

    def update(self):
        self.screen.fill(self.background)
        self.input.update()
        self.collision_look_ahead()
        if self.player:
            self.all_sprites.update(self.input, self.player.move_speed, self.player_collision)
            if not self.player_collision:     
                self.x_offset -= self.input.x_axis * self.player.move_speed
                self.y_offset -= self.input.y_axis * self.player.move_speed
        # TODO: Needs a better way against guarding when scene doesn't have map. Also row_i switching with col_i is a trip.
        if self.map:
            self.draw_map()
        
        # TODO: Implement z_order. Blit images in front of the other in proper order
        # self.z_order_sort_all_sprites()
        
        self.draw_hitboxes()
        
        self.visual_collisions()
                
        pygame.display.flip()
        
        self.player_collision = False
        
    # def z_order_sort_all_sprites(self):
    #     self.all_sprites = sorted(self.all_sprites, key=lambda sprite: sprite.y)
    
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
        if self.player:
            hitbox = self.player.get_lookahead_hitbox(self.input)
            player_collision = False
            for enemy in self.enemies:
                if enemy.hitbox:
                    collision = hitbox.colliderect(enemy.hitbox)
                else:
                    continue
                if collision:
                    player_collision = True
            if player_collision:
                self.player_collision = True
            else:
                self.player_collision = False
            # logger.debug(f"Player collision lookahead: {self.player_collision}")
            
            

    def visual_collisions(self):
        if self.player:
            for enemy in self.enemies:
                collision = self.player.visual_hitbox.colliderect(enemy.visual_hitbox)
                if collision:
                    self.handle_visual_collisions(self.player, enemy)
                    
    def handle_visual_collisions(self, player, enemy):
        if player.y > enemy.y:
            self.all_sprites.change_layer(player, 1)
            self.all_sprites.change_layer(enemy, 0)
        else:
            self.all_sprites.change_layer(player, 0)
            self.all_sprites.change_layer(enemy, 1)
        logger.debug(f"Player {player} collided with Enemy {enemy}")
        
    @classmethod
    def from_config(cls, config_file, screen):
        scene = cls(screen)
        with open(config_file, 'r') as f:
            config = json.load(f)
            for enemy_config in config['enemies']:
                enemy = Enemy(position = enemy_config['position'])
                scene.all_sprites.add(enemy)
                scene.enemies.add(enemy)
            player = Player(position = config['player']['position'])
            scene.all_sprites.add(player)
            scene.player = player
            scene.map = config['map']
        return scene    
    
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
        if value <= 0.55 and value >= 0.0:
            value = 0.0
        elif value >= -0.55 and value < 0.0:
            value = 0.0
        else:
            value = value
        return value