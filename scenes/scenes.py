import json
from loguru import logger
import pygame

from bodies.bodies import Enemy, Player
from textures.textures import TextureMaster
from .menu import Dropdown
from .camera import Camera

INIT_X = 0
INIT_Y = 0
ROW_LENGTH = 20
COLUMN_LENGTH = 16

TEMP_LIST_MAP_CENTER = (200, 200)


class Scene():
    def __init__(self, screen):
        info = pygame.display.Info()
        self.WIDTH, self.HEIGHT = info.current_w, info.current_h
        self.screen = screen

    def update(self, events):
        pass


class Level(Scene):
    def __init__(self, screen, config_file):
        super().__init__(screen)
        self.background = (40, 40, 40)
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.player = None
        self.enemies = pygame.sprite.Group()
        # self.texture = TextureMaster(screen)
        
        self.map = None

        self.camera = Camera((INIT_X, INIT_Y))
        self.texture = TextureMaster(screen, self.camera)

        self.load_config(config_file)
        
        self.texture.create_active_map(self.map, self.camera, [INIT_X, INIT_Y])
        
        self.current_grid = self.texture.active_map[str(self.camera.current_grid)]
        
        self.previous_grid_x = self.camera.current_grid[0]
        self.previous_grid_y = self.camera.current_grid[1]
        
        # self.sprite_map_center = self.texture2.create_texture_group(self.map, self.camera, [INIT_X, INIT_Y])
        # self.sprite_map_east = self.texture2.create_texture_group(self.map, self.camera, [INIT_X + ROW_LENGTH, INIT_Y])
        # self.sprite_map_west = self.texture2.create_texture_group(self.map, self.camera, [INIT_X - ROW_LENGTH, INIT_Y])
        # self.sprite_map_north = self.texture2.create_texture_group(self.map, self.camera, [INIT_X, INIT_Y - COLUMN_LENGTH])
        
        # Needed for update debug. Can be deleted when no longer needed.
        self.count = 0

    def load_config(self, config_file):
        with open(config_file, 'r') as file:
            config = json.load(file)
            for enemy_config in config['enemies']:
                # TODO: Find cleaner way to put in enemy position. Why is 10 and 8 needed.
                position = enemy_config['position']
                enemy_position_x = position[0] - self.camera.init_pos[0] + INIT_X
                enemy_position_y = position[1] - self.camera.init_pos[1] + INIT_Y
                enemy = Enemy(position=(enemy_position_x, enemy_position_y))
                self.all_sprites.add(enemy)
                self.enemies.add(enemy)
            # TODO: Player class is just for show. Remove.
            player = Player(self.camera, self.all_sprites, player_class=config['player']['class'])
            self.all_sprites.add(player)
            self.player = player
            self.map = config['map']

    def update(self, events):
        self.screen.fill(self.background)
        self.all_sprites.update()
        self.current_grid = self.texture.active_map[str(self.camera.current_grid)]
        self.check_grid_change()
        
        for map in self.texture.active_map.values():
            map.draw(self.screen)
            
        self.all_sprites.draw(self.screen)
        self.draw_hitboxes()
        self.draw_player_center_point()
        self.visual_collisions()
        self.map_grid_collisions()
        
        self.update_debug()
        # self.highlight_grid(1, 2)

        pygame.display.flip()
        
    def check_grid_change(self):
        if self.previous_grid_x != self.camera.current_grid[0]:
            if self.previous_grid_x > self.camera.current_grid[0]:
                print('x grid change left. New grid ' + str(self.camera.current_grid))
                self.texture.active_map_replace_left(self.map, self.camera)
            else:
                print('x grid change right. New grid ' + str(self.camera.current_grid))
                self.texture.active_map_replace_right(self.map, self.camera)
            self.previous_grid_x = self.camera.current_grid[0]
        if self.previous_grid_y != self.camera.current_grid[1]:
            if self.previous_grid_y > self.camera.current_grid[1]:
                print('y grid change up. New grid ' + str(self.camera.current_grid))
                self.texture.active_map_replace_up(self.map, self.camera)
            else:
                print('y grid change down. New grid ' + str(self.camera.current_grid))
                self.texture.active_map_replace_down(self.map, self.camera)
            self.previous_grid_y = self.camera.current_grid[1]
        
        
        
    def draw_player_center_point(self):
        point = (self.player.hitbox.x + self.player.hitbox.width // 2, self.player.hitbox.y + self.player.hitbox.height // 2)
        pygame.draw.circle(self.screen, (255, 255, 255), (point[0], point[1]), 1)
        
    def highlight_grid(self, grid_x, grid_y):
        grid_x -= INIT_X
        grid_y -= INIT_Y
        # TODO: Figure out these magic numbers based on centering
        grid_x += 10
        grid_y += 8
        overlay_color = (255, 0, 0)
        alpha = 128
        overlay = pygame.Surface((64, 64), pygame.locals.SRCALPHA)
        overlay.fill((*overlay_color, alpha))
        self.screen.blit(overlay, (grid_x * 64 + self.camera.x, grid_y * 64 + self.camera.y))

    def draw_hitboxes(self):
        if self.player:
            self.player.draw_hitbox(self.screen, self.player.visual_hitbox)
        for enemy in self.enemies:
            enemy.draw_hitbox(self.screen, enemy.visual_hitbox)

    # def draw_map(self):
    #     for row_i, row in enumerate(self.map[self.camera.y_slice]):
    #         for col_i, col in enumerate(row[self.camera.x_slice]):
    #             self.texture.draw_grid(col, col_i - 1, row_i - 1, self.camera)
                
    
    def map_grid_collisions(self):
        # for texture_group in self.texture.active_map.values():
        for texture in self.current_grid:
            if texture.rect.collidepoint(self.player.standing_point):
                texture.highlight(self.camera)

    def visual_collisions(self):
        if self.player:
            for enemy in self.enemies:
                collision = self.player.visual_hitbox.colliderect(
                    enemy.visual_hitbox)
                if collision:
                    self.handle_visual_collisions(self.player, enemy)

    def handle_visual_collisions(self, player, enemy):
        # TODO: Layers 0 and 1 were used for learning. Probably need a better settings when environment factored in
        if player.y > enemy.y:
            self.all_sprites.change_layer(player, 1)
            self.all_sprites.change_layer(enemy, 0)
        else:
            self.all_sprites.change_layer(player, 0)
            self.all_sprites.change_layer(enemy, 1)
        logger.debug(f"Player {player} collided with Enemy {enemy}")
        
    def update_debug(self):
        self.count += 1
        if self.count >= 50:
            # Print stuff
            logger.debug(f'Map center: {self.camera.map_center}, Current grid: {self.camera.current_grid}, Active grid: {self.current_grid}, Grids: {len(self.texture.active_map.keys())}')
            self.count = 0


class Menu(Scene):
    def __init__(self, screen):
        super().__init__(screen)
        self.background = (40, 40, 40)
        self.fields = {}
        self.fields['option_dropdown'] = Dropdown(self.screen, 100, 100)
        self.fields['edit_dropdown'] = Dropdown(self.screen, 300, 100)

    def update(self, events):
        self.screen.fill(self.background)

        for event in events:
            # TODO: Make this more efficient. Check all fields rectcollide and pass to the appropriate one
            if event.type == pygame.MOUSEBUTTONDOWN:
                for field in self.fields.values():
                    field.update(event)

        for field in self.fields.values():
            field.draw()

        pygame.display.flip()
