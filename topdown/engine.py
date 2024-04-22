import pygame
import json

from pathlib import Path
from loguru import logger

from .display import Display, Event, MenuDisplay
from .bodies import Character, Enemy, Physics

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

        self.event = Event()
        self.display = MenuDisplay()

    def update(self):
        running = self.event.update()
        self.display.update(self.screen)
        return running


class Scene():
    def __init__(self, screen):
        self.screen = screen
        
        self.event = Event()
        self.input = Input()
        self.physics = Physics()
        self.display = Display()

        self.sprites = pygame.sprite.Group()
        # self.bodies = []
        # self.add_body(Character())
        # self.add_body(Enemy())

    def update(self):
        running = self.event.update()
        self.input.update()
        self.physics.update(self.input, self.sprites)
        self.screen.fill((0, 0, 0))
        # for character in characters:
        #     screen.blit(character.image, character.rect)
        self.sprites.draw(self.screen)
        pygame.display.flip()
        # self.display.update(self.screen, self.bodies)
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


class Input():
    def __init__(self):
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()

    def update(self):
        self.x_axis = self.process_axis(self.joystick.get_axis(0))
        self.y_axis = self.process_axis(self.joystick.get_axis(1))

    def process_axis(self, value: float):
        value = round(value, 1)
        if value <= 0.1 and value >= 0.0:
            value = 0.0
        elif value >= -0.1 and value < 0.0:
            value = 0.0
        else:
            value = value
        return value
    