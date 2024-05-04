import os
import pygame
import json

GRID = 64

class Texture():
    def __init__(self, texture_file_path):
        self.texture_file_path = texture_file_path
        texture_name = os.path.splitext(os.path.basename(self.texture_file_path))[0]
        self.texture = pygame.image.load(f'{self.texture_file_path}/{texture_name}.png')
        
        with open(f'{self.texture_file_path}/{texture_name}.json') as info_file:    
            self.info = json.load(info_file)
            
    def draw(self, screen, xy, x_offset = None, y_offset = None):
        screen.blit(self.texture, (xy[0] + x_offset, xy[1] + y_offset))
        

class TextureMaster():
    def __init__(self, profile = ''):
        self.textures = {}
        self.texture_mapping = {0: 'road', 1: 'grass'}
        directory = 'textures/assets/'
        #TODO: Set profile selection for TextureMaster
        for texture in os.listdir(f'{directory}{profile}'):
            self.textures[texture] = Texture(f'{directory}{profile}/{texture}')
            
    def draw_tile(self, screen, texture_name, x, y):
        try:
            texture = self.textures[texture_name]
        except KeyError:
            print("Invalid texture. TODO: Create a default texture. Available textures are:", list(self.textures.keys()))
            # TODO: Probably shouldn't return None. Find better way to handle error like create a default texture
            return None
        texture.draw(screen, (x,y))
        
    def draw_grid(self, screen, texture_map, x, y, x_offset = None, y_offset = None):
        try:
            texture = self.textures[self.texture_mapping[texture_map]]
        except KeyError:
            print("Invalid texture. TODO: Create a default texture. Available textures are:", list(self.textures.keys()))
            # TODO: Probably shouldn't return None. Find better way to handle error like create a default texture
            return None
        
        texture.draw(screen, (x * GRID, y * GRID), x_offset, y_offset)    
        
        
    def fill_screen_tile(self, screen, texture_name):
        info = pygame.display.Info()
        WIDTH, HEIGHT = info.current_w, info.current_h
        # TODO: Remove magic number of 64 (width of texture)
        for y in range(0, HEIGHT, 64):
            for x in range(0, WIDTH, 64):
                self.draw_tile(screen, texture_name, x, y)