import pygame
from pygame.locals import QUIT, JOYBUTTONDOWN
import json

from pathlib import Path
from loguru import logger

from .bodies import Player, Enemy

class Topdown:
    def __init__(self):
        pygame.init()
        self.set_screen_size(1200, 900)
        # self.set_screen_size(fullscreen=True)
        pygame.display.set_caption("Topdown")
        self.scenes = {}
        self.scenes['scene'] = Scene.from_config(Path('topdown/scenes/scene2.json'), self.screen)
        self.scenes['menu'] = Scene(self.screen)
        self.set_scene('menu')
        self.clock = pygame.time.Clock()
        
    def loop(self):
        self.running = True
        while self.running:
            self.handle_events()
            self.current_scene.update()
            self.clock.tick(90)
        self.exit()
        
    def set_screen_size(self, width=None, height=None, fullscreen=False):
        if fullscreen or width == None or height == None:
            info = pygame.display.Info()
            self.WIDTH, self.HEIGHT = info.current_w, info.current_h
            self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.FULLSCREEN)
        else:
            self.WIDTH, self.HEIGHT = width, height
            self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        
    def set_scene(self, scene):
        try:
            self.current_scene = self.scenes[scene]
        except KeyError:
            print("Invalid state. State remains the same. Available scenes are:", list(self.scenes.keys()))
            
    def handle_events(self):
        for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                elif event.type == JOYBUTTONDOWN:
                    # Check if the 'A' button is pressed
                    if event.button == 0:  # Adjust this index if needed, 0 usually represents the 'A' button
                        # logger.debug("A button pressed on the controller!")
                        pass
                    elif event.button == 7:
                        logger.debug('Start button: switching scenes')
                        if self.current_scene != self.scenes['menu']:
                            self.current_scene = self.scenes['menu']
                        else:
                            self.current_scene = self.scenes['scene']

    def exit(self):
        pygame.quit()
        import sys
        logger.debug('Good exit')
        sys.exit()

class Scene():
    def __init__(self, screen):
        self.screen = screen
        self.background = (40, 40, 40)
        self.all_sprites = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

    def update(self):
        self.screen.fill(self.background)
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