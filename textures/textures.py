import os
import pygame
import json

GRID = 64


class Texture():
    def __init__(self, texture_file_path):
        self.texture_file_path = texture_file_path
        texture_name = os.path.splitext(
            os.path.basename(self.texture_file_path))[0]
        self.texture = pygame.image.load(
            f'{self.texture_file_path}/{texture_name}.png')

        with open(f'{self.texture_file_path}/{texture_name}.json') as info_file:
            self.info = json.load(info_file)

class TextureMaster():
    def __init__(self, profile=''):
        self.textures = {}
        self.texture_mapping = {0: 'road', 1: 'grass'}
        directory = 'textures/assets/'
        # TODO: Set profile selection for TextureMaster
        for texture in os.listdir(f'{directory}{profile}'):
            self.textures[texture] = Texture(f'{directory}{profile}/{texture}')

    def draw_grid(self, screen, texture_map, x, y, camera=None):
        try:
            texture = self.textures[self.texture_mapping[texture_map]]
        except KeyError:
            print("Invalid texture. TODO: Create a default texture. Available textures are:", list(
                self.textures.keys()))
            # TODO: Probably shouldn't return None. Find better way to handle error like create a default texture
            return None
        if camera:
            x -= camera.x // 64
            y -= camera.y // 64
            screen.blit(texture.texture, (x * GRID + camera.x, y * GRID + camera.y))
        else:
            screen.blit(texture.texture, (x * GRID, y * GRID))
