import pygame
from pygame.locals import QUIT, JOYBUTTONDOWN

class Display:
    def __init__(self):
        pass
    # def update(self, screen, characters):
    #     screen.fill((0, 0, 0))
    #     for character in characters:
    #         screen.blit(character.image, character.rect)
    #     pygame.display.flip()

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
    
class MenuDisplay:
    def __init__(self):
        pass
    def update(self, screen):
        screen.fill((50, 50, 50))
        pygame.display.flip()

# class MenuEvent:
#     def __init__(self):
#         pass
#     def update(self):
#         for event in pygame.event.get():
#                 if event.type == QUIT:
#                     return False
#                 elif event.type == JOYBUTTONDOWN:
#                     if event.button == 0:  # Adjust this index if needed, 0 usually represents the 'A' button
#                         print("A button pressed on the controller in the menu!")
#                     elif event.button == 7:
#                         print('Start button: going to scene')
#                         return False
#         return True