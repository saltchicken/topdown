import json
from loguru import logger
import pygame

from bodies.bodies import Enemy, Player
from textures.textures import TextureMaster, TextureMaster2
from .menu import Dropdown
from .camera import Camera


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
        self.texture = TextureMaster(screen)
        self.texture2 = TextureMaster2(screen)
        self.map = None

        self.camera = Camera((12, 10))

        self.load_config(config_file)
        
        self.active_sprite_map = self.create_map_sprites()

    def load_config(self, config_file):
        with open(config_file, 'r') as file:
            config = json.load(file)
            for enemy_config in config['enemies']:
                # TODO: Find cleaner way to put in enemy position. Why is 10 and 8 needed.
                position = enemy_config['position']
                enemy_position_x = position[0] - self.camera.init_pos[0] + 10
                enemy_position_y = position[1] - self.camera.init_pos[1] + 8
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

        # Comment this out when testing TextreMaster2
        # self.draw_map()
        # active_sprite_map = self.create_map_sprites()
        self.active_sprite_map.draw(self.screen)
        
        self.all_sprites.draw(self.screen)
        self.draw_hitboxes()
        self.visual_collisions()

        pygame.display.flip()

    def draw_hitboxes(self):
        if self.player:
            self.player.draw_hitbox(self.screen, self.player.visual_hitbox)
        for enemy in self.enemies:
            enemy.draw_hitbox(self.screen, enemy.visual_hitbox)

    def draw_map(self):
        for row_i, row in enumerate(self.map[self.camera.y_slice]):
            for col_i, col in enumerate(row[self.camera.x_slice]):
                self.texture.draw_grid(col, col_i - 1, row_i - 1, self.camera)
                
    def create_map_sprites(self):
        self.texture2.create_map_sprite_group(self.map, self.camera)
        return self.texture2.active_sprite_map


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
