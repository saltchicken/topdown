import pygame
from pygame.locals import QUIT, JOYBUTTONDOWN

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
                elif event.type == JOYBUTTONDOWN:
                    # Check if the 'A' button is pressed
                    if event.button == 0:  # Adjust this index if needed, 0 usually represents the 'A' button
                        print("A button pressed on the controller!")
        return True