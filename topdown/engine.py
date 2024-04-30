import pygame
from pygame.locals import QUIT, JOYBUTTONDOWN
import json

from pathlib import Path
from loguru import logger

from .bodies import Player, Enemy

class Topdown:
    def __init__(self):
        pygame.init()
        
        # For specific window size
        self.WIDTH, self.HEIGHT = 1200, 900
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        
        # # For fullscreen
        # info = pygame.display.Info()
        # monitor_width = info.current_w
        # monitor_height = info.current_h
        # self.screen = pygame.display.set_mode((monitor_width, monitor_height), pygame.FULLSCREEN)

        pygame.display.set_caption("Topdown")

        # self.scene = Scene(self.screen)
        self.scene = Scene.from_config(Path('topdown/scenes/scene1.json'), self.screen)
        self.menu = Scene(self.screen)
        self.clock = pygame.time.Clock()

    def loop(self):
        # TODO: Fix this message with self.running. Shouldn't be needed.
        self.running = True
        self.switch = True
        while self.running:
            self.switch = True
            while self.switch and self.running:
                self.running, self.switch = self.menu.update()
                self.clock.tick(90)
            self.switch = True
            while self.switch and self.running:
                self.running, self.switch = self.scene.update()
                self.clock.tick(90)
        self.exit()

    def exit(self):
        pygame.quit()
        import sys
        logger.debug('Good exit')
        sys.exit()

class Scene():
    def __init__(self, screen):
        self.screen = screen
        self.background = (40, 40, 40)
        self.event = Event()
        self.all_sprites = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

    def update(self):
        running = self.event.update()
        self.screen.fill(self.background)
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        
        self.collisions()
        
        pygame.display.flip()
        return running
    
    def collisions(self):
        # TODO: Why are two collisions detected at start
        for player in self.players:
            pygame.draw.rect(self.screen, (255,255,255), player.hitbox, 1)
            for enemy in self.enemies:
                collision = player.hitbox.colliderect(enemy.hitbox)
                pygame.draw.rect(self.screen, (255,255,255), enemy.hitbox, 1)
                if collision:
                    logger.debug(collision)
    
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
    
class Event:
    def __init__(self):
        pass
    def update(self):
        for event in pygame.event.get():
                if event.type == QUIT:
                    return False, False
                elif event.type == JOYBUTTONDOWN:
                    # Check if the 'A' button is pressed
                    if event.button == 0:  # Adjust this index if needed, 0 usually represents the 'A' button
                        # logger.debug("A button pressed on the controller!")
                        pass
                    elif event.button == 7:
                        logger.debug('Start button: switching scenes')
                        return True, False
        return True, True
    