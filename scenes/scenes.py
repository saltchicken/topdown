import json
from loguru import logger
import pygame

from bodies.bodies import Enemy, Player
from textures.textures import TextureMaster
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
        self.map = None

        self.camera = Camera((21, 9))

        self.load_config(config_file)

    def load_config(self, config_file):
        with open(config_file, 'r') as file:
            config = json.load(file)
            for enemy_config in config['enemies']:
                enemy = Enemy(position=enemy_config['position'])
                self.all_sprites.add(enemy)
                self.enemies.add(enemy)
            player = Player(self.camera, self.all_sprites, position=config['player']['position'])
            self.all_sprites.add(player)
            self.player = player
            self.map = config['map']

    def update(self, events):
        self.screen.fill(self.background)
        self.all_sprites.update()

        self.draw_map()
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
