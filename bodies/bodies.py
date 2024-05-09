"""
This module provides functions in relation to the bodies of the engine.
"""

import json
import os
from dataclasses import dataclass
import pygame

from loguru import logger


GRID = 64


class Body(pygame.sprite.Sprite):
    def __init__(self,position):
        super().__init__()
        self.WIDTH, self.HEIGHT = 128, 128
        self.image = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.rect = self.image.get_rect()
        # self.grid_x = int(self._x // GRID)
        # self.grid_y = int((self._y + self.grid_y_offset) // GRID)
        
        # These offset are specific to the 128 x 128 sprites.
        # self.x_grid_offset = 32
        # self.y_grid_offset = 10
        
        # self._x = position[0] * 64 - self.x_grid_offset
        # self._y = position[1] * 64 - self.y_grid_offset
        
        self._x = position[0] * 64
        self._y = position[1] * 64
        # self._x = float(self.WIDTH / 2) + float(position[0])
        # self._y = float(self.HEIGHT / 2) + float(position[1])
        # self.grid_x_offset = 0
        # self.grid_y_offset = 0
        
        self.hitbox = self.get_hitbox()
        self.visual_hitbox = None

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @x.setter
    def x(self, value):
        # TODO: Find better way to deal with precision issue
        self._x = round(value, 5)
        self.rect.x = int(self._x - self.WIDTH / 2)
        # self.grid_x = int(self._x // GRID)
        # max(0, min(player_rect.x, SCREEN_WIDTH - player_rect.width))

    @y.setter
    def y(self, value):
        # TODO: Find better way to deal with precision issue
        self._y = round(value, 5)
        self.rect.y = int(self._y - self.HEIGHT / 2)
        # self.grid_y = int((self._y + self.grid_y_offset) // GRID)
        # max(0, min(player_rect.y, SCREEN_HEIGHT - player_rect.height))

    def physics(self):
        pass

    def animate(self):
        pass

    def update(self):
        self.physics()
        self.animate()
        self.hitbox = self.get_hitbox()
        self.visual_hitbox = self.get_visual_hitbox()

    def get_hitbox(self):
        action_frame = self.state.current_action.animation.frame_i
        # TODO: Remove this check after confirmed that animation doesn't cause this to happen.
        if action_frame >= self.state.current_action.animation.count:
            logger.warning('animation.i is greater than count, why is this happening')
        #     return pygame.Rect( self.rect.x + self.state.current_action.hitbox[-1][0],
        #                     self.rect.y + self.state.current_action.hitbox[-1][1],
        #                     self.state.current_action.hitbox[-1][2],
        #                     self.state.current_action.hitbox[-1][3])
        return pygame.Rect(self.rect.x + self.state.current_action.hitbox[action_frame][0],
                           self.rect.y +
                           self.state.current_action.hitbox[action_frame][1],
                           self.state.current_action.hitbox[action_frame][2],
                           self.state.current_action.hitbox[action_frame][3])

    def get_visual_hitbox(self):
        action_frame = self.state.current_action.animation.frame_i
        return pygame.Rect(self.rect.x + self.state.current_action.visual_hitbox[action_frame][0],
                           self.rect.y +
                           self.state.current_action.visual_hitbox[action_frame][1],
                           self.state.current_action.visual_hitbox[action_frame][2],
                           self.state.current_action.visual_hitbox[action_frame][3])

    def get_lookahead_hitbox(self, input):
        # TODO: Determine why 5 and see if there is a better value.
        return pygame.Rect(self.hitbox[0] + input.x_axis * 5,
                           self.hitbox[1] + input.y_axis * 5,
                           self.hitbox[2],
                           self.hitbox[3])

    def draw_hitbox(self, screen, hitbox):
        pygame.draw.rect(screen, (255, 255, 255), hitbox, 1)


class Player(Body):
    def __init__(self, camera, all_sprites, *args, **kwargs):
        self.state = State('player2')
        self.camera = camera
        self.player_class = kwargs['player_class']
        self.input = Input()
        self.all_sprites = all_sprites
        
        # TODO: Find better way to determine (10, 8) placing player in center.
        # info = pygame.display.Info()
        # width, height = info.current_w, info.current_h
        # super().__init__(self.camera, (width // 2 - 64, height // 2 - 64))
        super().__init__((10, 8))

        self.move_speed = 3
        self.grid_y_offset = 54
        # Set x to _x to call the setter method. Needed or initialization is buggy due to initializing setter method.
        self.x = self._x
        self.y = self._y

        self.layer = 0

    def physics(self):
        pass
        # if abs(self.input.x_axis) > 0:
        #     self.x += self.input.x_axis * self.move_speed
        # if abs(self.input.y_axis) > 0:
        #     self.y += self.input.y_axis * self.move_speed

    def animate(self):
        # if self.input.a_button == 1 and self.state.current_action == self.state.actions['idle']:
        #     self.state.set_action('attack_1')
        try:
            self.image = self.state.current_action.animation.next()
        except StopIteration:
            self.state.set_action('FSS_idle')
            self.image = self.state.current_action.animation.next()
        if self.input.x_axis == 0 and self.input.y_axis == 0 and self.state.current_action != self.state.actions['FSS_idle']:
            if self.state.current_action == self.state.actions['FSS']:
                self.state.set_action('FSS_idle')
            elif self.state.current_action == self.state.actions['BSS']:
                self.state.set_action('BSS_idle')
            elif self.state.current_action == self.state.actions['LSS']:
                self.state.set_action('LSS_idle')
            elif self.state.current_action == self.state.actions['RSS']:
                self.state.set_action('RSS_idle')
        elif self.input.x_axis > 0 and self.state.current_action != self.state.actions['RSS'] and abs(self.input.x_axis) > abs(self.input.y_axis):
            self.state.set_action('RSS')
        elif self.input.x_axis < 0 and self.state.current_action != self.state.actions['LSS'] and abs(self.input.x_axis) > abs(self.input.y_axis):
            self.state.set_action('LSS')
        elif self.input.y_axis < 0 and self.state.current_action != self.state.actions['BSS'] and abs(self.input.y_axis) > abs(self.input.x_axis):
            self.state.set_action('BSS')
        elif self.input.y_axis > 0 and self.state.current_action != self.state.actions['FSS'] and abs(self.input.y_axis) > abs(self.input.x_axis):
            self.state.set_action('FSS')

    def update(self):
        self.input.update()
        super().update()
        player_collision = self.collision_look_ahead()
        if not player_collision:
            x = self.input.x_axis * self.move_speed
            y = self.input.y_axis * self.move_speed
            for body in self.all_sprites:
                if not isinstance(body, Player):
                    if not player_collision:
                        body.camera_move(x, y)
                        self.camera.x -= x
                        self.camera.y -= y
        
        
    def collision_look_ahead(self):
        hitbox = self.get_lookahead_hitbox(self.input)
        for body in self.all_sprites:
            # TODO: This would be better to use a group that doesn't have player in it
            if not isinstance(body, Player):
                if body.hitbox:
                    if hitbox.colliderect(body.hitbox):
                        logger.debug(f"Player collision")
                        return True
        return False


class Enemy(Body):
    def __init__(self, *args, **kwargs):
        self.state = State('enemy')
        super().__init__(**kwargs)

        # self.image.fill((0,255,0))
        self.move_speed = 2

        self.layer = 1
        
    def camera_move(self, x, y):
        self.x -= x
        self.y -= y

    def physics(self):
        pass
            # self.x += 0.1 * self.move_speed
            # self.y += 0.1 * self.move_speed

    def animate(self):
        self.image = self.state.current_action.animation.next()
        # self.image = pygame.transform.flip(self.image, True, False)


class State:
    def __init__(self, profile):
        self.actions = {}
        directory = 'bodies/assets/'
        for action in os.listdir(f'{directory}{profile}'):
            with open(f'{directory}{profile}/{action}/{action}.json') as info_file:
                action_info = json.load(info_file)
            self.actions[action] = Action(action_info['width'],
                                          action_info['height'],
                                          f'{directory}{
                                              profile}/{action}/{action}.png',
                                          action_info['count'],
                                          action_info['loop'],
                                          action_info['frames'],
                                          action_info['hitbox'],
                                          action_info['visual_hitbox']
                                          )
        # self.offset_rect = action_info['hitbox']

        self.set_action('FSS_idle')

    def set_action(self, action):
        try:
            self.current_action = self.actions[action]
        except KeyError:
            print("Invalid state. State remains the same. Available states are:", list(
                self.actions.keys()))
        self.current_action.animation.iter()  # Reset the action when switched


@dataclass
class Action():
    # action: str
    width: int
    height: int
    sprite_sheet_filepath: str
    count: int
    loop: bool
    frames: int
    hitbox: list
    visual_hitbox: list

    def __post_init__(self):
        self.animation = self.load_animation()

    def load_animation(self):
        # return SpriteStripAnim(self.sprite_sheet_filepath, (0,0,128,128), self.count, (0, 0, 0), self.loop, 8)
        return SpriteStripAnim(self.sprite_sheet_filepath, rect=(0, 0, self.width, self.height), count=self.count, loop=self.loop, frames=self.frames)
    
class Input():
    def __init__(self):
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()
        self.x_axis = 0.0
        self.y_axis = 0.0

    def update(self):
        self.x_axis = self.process_axis(self.joystick.get_axis(0))
        self.y_axis = self.process_axis(self.joystick.get_axis(1))
        self.a_button = self.joystick.get_button(0)
        # print(self.a_button)

    def process_axis(self, value: float):
        value = round(value, 1)
        threshold = 0.55
        if value <= threshold and value >= 0.0:
            value = 0.0
        elif value >= -threshold and value < 0.0:
            value = 0.0
        else:
            value = value
        return value


class spritesheet(object):
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert_alpha()
        except pygame.error as message:
            print('Unable to load spritesheet image:', filename)
            raise message
    # Load a specific image from a specific rectangle

    def image_at(self, rectangle, colorkey=None):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    def images_at(self, rects, colorkey=None):
        "Loads multiple images, supply a list of coordinates"
        return [self.image_at(rect, colorkey) for rect in rects]

    def load_strip(self, rect, image_count, colorkey=None):
        # if image_count is None and rect is None:
        #     width, height = self.sheet.get_size()
        #     rect = (0,0, height, height)
        #     image_count = width // height
        # print(f"rect: {rect}, image_count: {image_count}")
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)


class SpriteStripAnim(object):
    """    
    This class provides an iterator (iter() and next() methods), and a
    __add__() method for joining strips which comes in handy when a
    strip wraps to the next row.
    """

    def __init__(self, filename, rect, count, colorkey=(0, 0, 0), loop=False, frames=1):
        self.filename = filename
        ss = spritesheet(filename)
        self.images = ss.load_strip(rect, count, colorkey)
        self.count = count
        self.i = 0
        # TODO: Remove need for frame_i, very ugly. Using just i iterates just above len on StopIteration. Should be a better way to do this.
        self.frame_i = 0
        self.loop = loop
        self.frames = frames
        self.f = frames

    def iter(self):
        self.i = 0
        self.frame_i = 0
        self.f = self.frames
        return self

    def next(self):
        if self.i >= len(self.images):
            if not self.loop:
                raise StopIteration
            else:
                self.i = 0
                self.frame_i = 0
        image = self.images[self.i]
        self.f -= 1
        if self.f == 0:
            self.i += 1
            self.frame_i += 1
            self.f = self.frames
        if self.frame_i >= len(self.images):
            self.frame_i -= 1
        return image

    def __add__(self, ss):
        self.images.extend(ss.images)
        return self
