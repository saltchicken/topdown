import os
import pygame
import json

GRID = 64

INIT_X = 0
INIT_Y = 0
ROW_LENGTH = 20
COLUMN_LENGTH = 16

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
                
        self.active_map = {}
        
    def create_texture_group(self, map, camera, center):
        x_slice = slice(int(center[0] - ROW_LENGTH // 2) + TEMP_LIST_MAP_CENTER[0], int(center[0] + ROW_LENGTH // 2) + TEMP_LIST_MAP_CENTER[0])
        y_slice = slice(int(center[1] - COLUMN_LENGTH // 2) + TEMP_LIST_MAP_CENTER[1], int(center[1] + COLUMN_LENGTH // 2) + TEMP_LIST_MAP_CENTER[1])
        texture_group = TextureGroup(camera)
        for col_i, col in enumerate(map[y_slice]):
            for row_i, tile in enumerate(col[x_slice]):
                texture_group.add(Texture(self.screen, self.texture_images[self.texture_mapping[tile]], self.texture_infos[self.texture_mapping[tile]], [row_i + center[0], col_i + center[1]]))
        return texture_group
    
    def create_active_map(self, map, camera, center):
        grid = [center[0] - ROW_LENGTH, center[1] - COLUMN_LENGTH]
        grid_name = [grid[0] // ROW_LENGTH, grid[1] // COLUMN_LENGTH]
        self.active_map[str(grid_name)] = (self.create_texture_group(map, camera, grid)) # North West
        grid = [center[0], center[1] - COLUMN_LENGTH]
        grid_name = [grid[0] // ROW_LENGTH, grid[1] // COLUMN_LENGTH]
        self.active_map[str(grid_name)] = (self.create_texture_group(map, camera, grid)) # North
        grid = [center[0] + ROW_LENGTH, center[1] - COLUMN_LENGTH]
        grid_name = [grid[0] // ROW_LENGTH, grid[1] // COLUMN_LENGTH]
        self.active_map[str(grid_name)] = (self.create_texture_group(map, camera, grid)) # North East
        grid = [center[0] - ROW_LENGTH, center[1]]
        grid_name = [grid[0] // ROW_LENGTH, grid[1] // COLUMN_LENGTH]
        self.active_map[str(grid_name)] = (self.create_texture_group(map, camera, grid)) # West
        grid = center
        grid_name = [grid[0] // ROW_LENGTH, grid[1] // COLUMN_LENGTH]
        self.active_map[str(grid_name)] = (self.create_texture_group(map, camera, grid)) # Center
        grid = [center[0] + ROW_LENGTH, center[1]]
        grid_name = [grid[0] // ROW_LENGTH, grid[1] // COLUMN_LENGTH]
        self.active_map[str(grid_name)] = (self.create_texture_group(map, camera, grid)) # East
        grid = [center[0] - ROW_LENGTH, center[1] + COLUMN_LENGTH]
        grid_name = [grid[0] // ROW_LENGTH, grid[1] // COLUMN_LENGTH]
        self.active_map[str(grid_name)] = (self.create_texture_group(map, camera, grid)) # South West
        grid = [center[0], center[1] + COLUMN_LENGTH]
        grid_name = [grid[0] // ROW_LENGTH, grid[1] // COLUMN_LENGTH]
        self.active_map[str(grid_name)] = (self.create_texture_group(map, camera, grid)) # South
        grid = [center[0] + ROW_LENGTH, center[1] + COLUMN_LENGTH]
        grid_name = [grid[0] // ROW_LENGTH, grid[1] // COLUMN_LENGTH]
        self.active_map[str(grid_name)] = (self.create_texture_group(map, camera, grid)) # South East
        
    def active_map_replace_right(self, map, camera):
        delete_keys = []
        for grid in self.active_map.keys():
            if eval(grid)[0] == camera.current_grid[0] - 2:
                delete_keys.append(grid)
        for key in delete_keys:
            del self.active_map[key]
        center = [camera.current_grid[0] + 1, camera.current_grid[1]]
        grid = [center[0] * ROW_LENGTH, center[1] * COLUMN_LENGTH]
        texture_group = self.create_texture_group(map, camera, grid)
        self.active_map[str(center)] = texture_group
        center = [camera.current_grid[0] + 1, camera.current_grid[1] + 1]
        grid = [center[0] * ROW_LENGTH, center[1] * COLUMN_LENGTH]
        texture_group = self.create_texture_group(map, camera, grid)
        self.active_map[str(center)] = texture_group
        center = [camera.current_grid[0] + 1, camera.current_grid[1] - 1]
        grid = [center[0] * ROW_LENGTH, center[1] * COLUMN_LENGTH]
        texture_group = self.create_texture_group(map, camera, grid)
        self.active_map[str(center)] = texture_group
        print(len(self.active_map.keys()))
                

            
        
        
        # self.sprite_map_east = self.texture2.create_texture_group(self.map, self.camera, [INIT_X + ROW_LENGTH, INIT_Y])
        # self.sprite_map_west = self.texture2.create_texture_group(self.map, self.camera, [INIT_X - ROW_LENGTH, INIT_Y])
        # self.sprite_map_north = self.texture2.create_texture_group(self.map, self.camera, [INIT_X, INIT_Y - COLUMN_LENGTH])
        
                
class TextureGroup(pygame.sprite.Group):
    def __init__(self, camera):
        super().__init__()
        self.camera = camera
    def draw(self, surface):
        for sprite in self.sprites():
            surface.blit(sprite.image, pygame.Rect(sprite.rect.x + self.camera.x, sprite.rect.y + self.camera.y, sprite.rect.width, sprite.rect.height))