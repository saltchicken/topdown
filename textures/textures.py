import os
import pygame
import json

GRID = 64

INIT_X = 0
INIT_Y = 0

TEMP_LIST_MAP_CENTER = (200, 200)

class Texture(pygame.sprite.Sprite):
    def __init__(self, screen, image, info, position):
        super().__init__()
        self.screen = screen
        self.image = image
        self.info = info
        self.rect = self.image.get_rect()
        position[0] -= INIT_X
        position[1] -= INIT_Y
        self.rect.x += position[0] * 64
        self.rect.y += position[1] * 64
        
    def highlight(self, camera):
        overlay_color = (255, 0, 0)
        alpha = 128
        overlay = pygame.Surface((64, 64), pygame.locals.SRCALPHA)
        overlay.fill((*overlay_color, alpha))
        self.screen.blit(overlay, (self.rect.x + camera.x, self.rect.y + camera.y))

class TextureMaster():
    def __init__(self, screen, camera, profile=''):
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
        
    def create_map_sprite_group(self, map, camera, center):
        col_length = 16
        row_length = 20
        x_slice = slice(int(center[0] - row_length // 2) + TEMP_LIST_MAP_CENTER[0], int(center[0] + row_length // 2) + TEMP_LIST_MAP_CENTER[0])
        y_slice = slice(int(center[1] - col_length // 2) + TEMP_LIST_MAP_CENTER[1], int(center[1] + col_length // 2) + TEMP_LIST_MAP_CENTER[1])
        sprite_map = TextureGroup(camera)
        for col_i, col in enumerate(map[y_slice]):
            for row_i, tile in enumerate(col[x_slice]):
                sprite_map.add(Texture(self.screen, self.texture_images[self.texture_mapping[tile]], self.texture_infos[self.texture_mapping[tile]], [row_i + center[0], col_i + center[1]]))
        return sprite_map
                
class TextureGroup(pygame.sprite.Group):
    def __init__(self, camera):
        super().__init__()
        self.camera = camera
    def draw(self, surface):
        for sprite in self.sprites():
            surface.blit(sprite.image, pygame.Rect(sprite.rect.x + self.camera.x, sprite.rect.y + self.camera.y, sprite.rect.width, sprite.rect.height))