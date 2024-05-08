import os
import pygame
import json

GRID = 64


class Texture():
    def __init__(self, texture_file_path):
        self.texture_file_path = texture_file_path
        texture_name = os.path.splitext(
            os.path.basename(self.texture_file_path))[0]
        self.image = pygame.image.load(
            f'{self.texture_file_path}/{texture_name}.png')

        with open(f'{self.texture_file_path}/{texture_name}.json') as info_file:
            self.info = json.load(info_file)

class TextureMaster():
    def __init__(self, screen, profile=''):
        self.screen = screen
        self.textures = {}
        self.texture_mapping = {0: 'road', 1: 'grass'}
        directory = 'textures/assets/'
        # TODO: Set profile selection for TextureMaster. Create json for texture mapping.
        for texture in os.listdir(f'{directory}{profile}'):
            self.textures[texture] = Texture(f'{directory}{profile}/{texture}')

    def draw_grid(self, texture_map, x, y, camera=None):
        texture = self.textures[self.texture_mapping[texture_map]]
        if camera:
            x -= camera.x // GRID
            y -= camera.y // GRID
            self.screen.blit(texture.image, (x * GRID + camera.x, y * GRID + camera.y))
        else:
            self.screen.blit(texture.image, (x * GRID, y * GRID))
            

class Texture2(pygame.sprite.Sprite):
    def __init__(self, image, info, position):
        super().__init__()
        self.image = image
        self.info = info
        self.rect = self.image.get_rect()

class TextureMaster2():
    def __init__(self, screen, profile=''):
        self.screen = screen
        self.texture_images = {}
        self.texture_infos = {}
        self.texture_mapping = {0: 'road', 1: 'grass'}
        directory = 'textures/assets/'
        # TODO: Set profile selection for TextureMaster. Create json for texture mapping.
        for texture in os.listdir(f'{directory}{profile}'):
            texture_name = os.path.splitext(os.path.basename(f'{directory}{profile}/{texture}'))[0]
            self.texture_images[texture] = pygame.image.load(f'{directory}{profile}/{texture}/{texture_name}.png')
            with open(f'{directory}{profile}/{texture}/{texture_name}.json') as info_file:
                self.texture_infos[texture] = json.load(info_file)
            
        self.active_sprite_map = pygame.sprite.Group()

    # def draw_grid(self, texture_map, x, y, camera=None):
    #     texture = self.textures[self.texture_mapping[texture_map]]
    #     if camera:
    #         x -= camera.x // GRID
    #         y -= camera.y // GRID
    #         self.screen.blit(texture.image, (x * GRID + camera.x, y * GRID + camera.y))
    #     else:
    #         self.screen.blit(texture.image, (x * GRID, y * GRID))
    def create_map_sprite_group(self, map, camera):
        for row_i, row in enumerate(map[camera.y_slice]):
            for col_i, col in enumerate(row[camera.x_slice]):
                self.active_sprite_map.add(Texture2(self.texture_images[self.texture_mapping[col]], self.texture_infos[self.texture_mapping[col]], (row_i, col_i)))
                # print(self.texture_images[self.texture_mapping[col]])
                # self.texture.draw_grid(col, col_i - 1, row_i - 1, camera)