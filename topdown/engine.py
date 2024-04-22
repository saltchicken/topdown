import pygame

from loguru import logger

from .display import Display, Event
from .bodies import Character, Physics

class Topdown:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 1200, 900
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Topdown")

        self.event = Event()

        self.input = Input()
        self.physics = Physics()
        self.display = Display()

        self.clock = pygame.time.Clock()

        self.characters = []
        self.characters.append(Character.create_character())

        self.running = False

    def loop(self):
        self.running = True
        while self.running:
            self.screen.fill((0, 0, 0))
            self.running = self.event.update()
            self.input.update()
            self.physics.update(self.input, self.characters)
            self.display.update(self.screen, self.characters)

            self.clock.tick(90)
        self.exit()

    def exit(self):
        pygame.quit()
        import sys
        sys.exit()

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
    