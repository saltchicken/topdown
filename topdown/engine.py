import pygame
from pygame.locals import QUIT

from loguru import logger

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
    
class Character():
    def __init__(self):
        self.WIDTH, self.HEIGHT = 50, 50
        self.image = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect()
        self.move_speed = 5
        self._x = float(self.WIDTH / 2) 
        self._y = float(self.HEIGHT / 2)

    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y
    
    @x.setter
    def x(self, value):
        self._x = value
        self.rect.x = int(self._x - self.WIDTH / 2)
        # max(0, min(player_rect.x, SCREEN_WIDTH - player_rect.width))

    @y.setter
    def y(self, value):
        self._y = value
        self.rect.y = int(self._y - self.HEIGHT / 2)
        # max(0, min(player_rect.y, SCREEN_HEIGHT - player_rect.height))
    
    @staticmethod
    def create_character():
        return Character()

class Physics:
    def __init__(self):
        pass
    def update(self, input, characters):
        for character in characters:
            character.x += input.x_axis * character.move_speed
            character.y += input.y_axis * character.move_speed

class Display:
    def __init__(self):
        pass
    def update(self, screen, characters):
        for character in characters:
            screen.blit(character.image, character.rect)
        pygame.display.flip()

class Event:
    def __init__(self):
        pass
    def update(self):
        for event in pygame.event.get():
                if event.type == QUIT:
                    return False
        return True


