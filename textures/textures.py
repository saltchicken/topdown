import os
import pygame

class TextureMaster():
    def __init__(self, profile = ''):
        self.textures = {}
        directory = 'textures/assets/'
        for texture in os.listdir(f'{directory}{profile}'):
            texture_name = os.path.splitext(os.path.basename(texture))[0]
            self.textures[texture_name] = pygame.image.load(f'{directory}{profile}/{texture}')
            
    def draw_tile(self, screen, texture_name, x, y):
        try:
            texture = self.textures[texture_name]
        except KeyError:
            print("Invalid texture. TODO: Create a default texture. Available textures are:", list(self.textures.keys()))
            # TODO: Probably shouldn't return None. Find better way to handle error like create a default texture
            return None
        screen.blit(self.textures[texture_name], (x,y))
        
    def fill_screen_tile(self, screen, texture_name):
        info = pygame.display.Info()
        WIDTH, HEIGHT = info.current_w, info.current_h
        # TODO: Remove magic number of 64 (width of texture)
        for y in range(0, HEIGHT, 64):
            for x in range(0, WIDTH, 64):
                self.draw_tile(screen, texture_name, x, y)