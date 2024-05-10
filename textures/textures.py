import os
import pygame
import json

GRID = 64

INIT_X = 0
INIT_Y = 0

TEMP_LIST_MAP_CENTER = (200, 200)

# class Texture():
#     def __init__(self, texture_file_path):
#         self.texture_file_path = texture_file_path
#         texture_name = os.path.splitext(
#             os.path.basename(self.texture_file_path))[0]
#         self.image = pygame.image.load(
#             f'{self.texture_file_path}/{texture_name}.png')

#         with open(f'{self.texture_file_path}/{texture_name}.json') as info_file:
#             self.info = json.load(info_file)

# class TextureMaster():
#     def __init__(self, screen, profile=''):
#         self.screen = screen
#         self.textures = {}
#         self.texture_mapping = {0: 'road', 1: 'grass'}
#         directory = 'textures/assets/'
#         # TODO: Set profile selection for TextureMaster. Create json for texture mapping.
#         for texture in os.listdir(f'{directory}{profile}'):
#             self.textures[texture] = Texture(f'{directory}{profile}/{texture}')

#     def draw_grid(self, texture_map, x, y, camera=None):
#         texture = self.textures[self.texture_mapping[texture_map]]
#         if camera:
#             x -= camera.x // GRID
#             y -= camera.y // GRID
#             self.screen.blit(texture.image, (x * GRID + camera.x, y * GRID + camera.y))
#         else:
#             self.screen.blit(texture.image, (x * GRID, y * GRID))
            

class Texture2(pygame.sprite.Sprite):
    def __init__(self, screen, image, info, position):
        super().__init__()
        self.screen = screen
        self.image = image
        self.info = info
        self.rect = self.image.get_rect()
        # These offset are specific to the 128 x 128 sprites.
        # self.x_grid_offset = 32
        # self.y_grid_offset = 10
        # self.rect.x += position[0] * 64 + self.x_grid_offset
        # self.rect.y += position[1] * 64 + self.y_grid_offset
        # TODO: Figure out why these magic numbers are needed. 10 and 8
        position[0] -= INIT_X
        position[1] -= INIT_Y
        self.rect.x += position[0] * 64
        self.rect.y += position[1] * 64
        
    def highlight(self, camera):
        overlay_color = (255, 0, 0)
        alpha = 128
        overlay = pygame.Surface((64, 64), pygame.locals.SRCALPHA)
        overlay.fill((*overlay_color, alpha))
        # self.screen.blit(overlay, (grid_x * 64 + self.camera.x, grid_y * 64 + self.camera.y))
        self.screen.blit(overlay, (self.rect.x + camera.x, self.rect.y + camera.y))

class TextureMaster2():
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
            
        # self.active_sprite_map = TextureGroup(camera)
        # self.all_grids = pygame.sprite.Group()
        # self.grids = {}

    # def draw_grid(self, texture_map, x, y, camera=None):
    #     texture = self.textures[self.texture_mapping[texture_map]]
    #     if camera:
    #         x -= camera.x // GRID
    #         y -= camera.y // GRID
    #         self.screen.blit(texture.image, (x * GRID + camera.x, y * GRID + camera.y))
    #     else:
    #         self.screen.blit(texture.image, (x * GRID, y * GRID))
    
    # def create_map_sprites(self):
    #     self.texture2.create_map_sprite_group()
    #     return self.texture2.active_sprite_map
    
    # def add_grid(self, map, camera, center):
    #     self.grids[str(center)] = self.create_map_sprite_group(map, camera, center)
        
    
    def create_map_sprite_group(self, map, camera, center):
        col_length = 16
        row_length = 20
        x_slice = slice(int(center[0] - row_length // 2) + TEMP_LIST_MAP_CENTER[0], int(center[0] + row_length // 2) + TEMP_LIST_MAP_CENTER[0])
        
        y_slice = slice(int(center[1] - col_length // 2) + TEMP_LIST_MAP_CENTER[1], int(center[1] + col_length // 2) + TEMP_LIST_MAP_CENTER[1])
        print(y_slice)
        # for col_i, col in enumerate(map[camera.y_slice]):
        #     for row_i, tile in enumerate(col[camera.x_slice]):
        sprite_map = TextureGroup(camera)
        for col_i, col in enumerate(map[y_slice]):
            for row_i, tile in enumerate(col[x_slice]):
                # self.active_sprite_map.add(Texture2(self.texture_images[self.texture_mapping[tile]], self.texture_infos[self.texture_mapping[tile]], (row_i, col_i)))
                sprite_map.add(Texture2(self.screen, self.texture_images[self.texture_mapping[tile]], self.texture_infos[self.texture_mapping[tile]], [row_i + center[0], col_i + center[1]]))

                # print(self.texture_images[self.texture_mapping[col]])
                # self.texture.draw_grid(col, col_i - 1, row_i - 1, camera)
        return sprite_map
        # self.all_grids.add(sprite_map)
                
class TextureGroup(pygame.sprite.Group):
    def __init__(self, camera):
        super().__init__()
        self.camera = camera
    def draw(self, surface):
        for sprite in self.sprites():
            surface.blit(sprite.image, pygame.Rect(sprite.rect.x + self.camera.x, sprite.rect.y + self.camera.y, sprite.rect.width, sprite.rect.height))