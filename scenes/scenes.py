import json
from loguru import logger
import pygame

from bodies.bodies import Enemy, Player
from textures.textures import TextureMaster


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

    def update(self):
        # self.screen.fill(self.background)
        # self.texture.draw_tiles(self.screen, 'grass', 2, 3)
        self.texture.fill_screen_tile(self.screen, 'grass')
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        
        self.collisions()
        
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
            for player_config in config['player']:
                player = Player(position = player_config['position'])
                scene.all_sprites.add(player)
                scene.players.add(player)
        return scene    