import pygame
from pygame.locals import QUIT

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