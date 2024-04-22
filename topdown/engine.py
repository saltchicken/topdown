import pygame
from pygame.locals import QUIT, JOYBUTTONDOWN
import json

from pathlib import Path
from loguru import logger

from .bodies import Character, Enemy

class Topdown:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 1200, 900
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Topdown")

        # self.scene = Scene(self.screen)
        self.scene = Scene.from_config(Path('topdown/scenes/scene1.json'), self.screen)
        self.menu = Menu(self.screen)
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
        print('Good exit')
        sys.exit()

class Menu():
    def __init__(self, screen):
        self.screen = screen
        self.background = (50, 50, 50)
        self.event = Event()

    def update(self):
        running = self.event.update()
        self.screen.fill(self.background)
        pygame.display.flip()
        return running


class Scene():
    def __init__(self, screen):
        self.screen = screen
        self.background = (0, 0, 0)
        self.event = Event()
        self.sprites = pygame.sprite.Group()

    def update(self):
        running = self.event.update()
        self.screen.fill(self.background)
        self.sprites.update()
        self.sprites.draw(self.screen)
        pygame.display.flip()
        return running
    
    @classmethod
    def from_config(cls, config_file, screen):
        scene = cls(screen)
        with open(config_file, 'r') as f:
            config = json.load(f)
            for character_config in config['character']:
                body = Character(position = character_config['position'])
                scene.sprites.add(body)
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
                        print("A button pressed on the controller!")
                    elif event.button == 7:
                        print('Start button: going to scene')
                        return True, False
        return True, True
    