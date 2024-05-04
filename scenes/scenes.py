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
        self.all_sprites = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.texture = TextureMaster()
        self.map = None
        
        # TODO: Clean this up for dealing with where center of camera is
        self.map_center = (11, 9)
        self.row_length = 20
        self.col_length = 16
        
        self.x_offset = 0.0
        self.y_offset = 0.0

    def update(self):
        self.screen.fill(self.background)
        # self.texture.draw_tiles(self.screen, 'grass', 2, 3)
        # self.texture.fill_screen_tile(self.screen, 'grass')
        
        
        self.all_sprites.update()
        
        # TODO: Need a better way of getting the main character for camera moving
        current_player = None
        for player in self.players:
            current_player = player
            break
        
        if current_player:
            self.x_offset -= current_player.input.x_axis * current_player.move_speed
            self.y_offset -= current_player.input.y_axis * current_player.move_speed
        
        # TODO: Needs a better way against guarding when scene doesn't have map. Also row_i switching with col_i is a trip.
        if self.map:
            for row_i, row in enumerate(self.map):
                for col_i, col in enumerate(row):
                    self.texture.draw_grid(self.screen, col, col_i - 1, row_i - 1, self.x_offset, self.y_offset)
        # if self.map:
        #     for row_i, row in enumerate(self.map[self.map_center[1] - self.col_length // 2 : self.map_center[1] + self.col_length // 2]):
        #         for col_i, col in enumerate(row[self.map_center[0] - self.row_length // 2 : self.map_center[0] + self.row_length // 2]):
        #             self.texture.draw_grid(self.screen, col, col_i, row_i)
                    
        
        # TODO: Implement z_order. Blit images in front of the other in proper order
        self.all_sprites.draw(self.screen)
        
        self.collisions()
        
        # for player in self.players:
        #     print(player.grid_x, player.grid_y)
        
        pygame.display.flip()

    def collisions(self):
        # TODO: Why are two collisions detected at start
        for player in self.players:
            player.draw_hitbox(self.screen)
            for enemy in self.enemies:
                collision = player.hitbox.colliderect(enemy.hitbox)
                enemy.draw_hitbox(self.screen)
                if collision: self.handle_collisions(player, enemy)
                    
    def handle_collisions(self, player, enemy):
        pass
        # logger.debug(f"Player {player} collided with Enemy {enemy}")
        
    @classmethod
    def from_config(cls, config_file, screen):
        scene = cls(screen)
        with open(config_file, 'r') as f:
            config = json.load(f)
            for enemy_config in config['enemies']:
                enemy = Enemy(position = enemy_config['position'])
                scene.all_sprites.add(enemy)
                scene.enemies.add(enemy)
            for player_config in config['player']:
                player = Player(position = player_config['position'])
                scene.all_sprites.add(player)
                scene.players.add(player)
            scene.map = config['map']
        return scene    