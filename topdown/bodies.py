import os
import pygame

from loguru import logger

from dataclasses import dataclass

from .spritesheet import spritesheet, SpriteStripAnim

class Body(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.WIDTH, self.HEIGHT = 128, 128 
        self.image = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.rect = self.image.get_rect()
        self._x = float(self.WIDTH / 2) + float(position[0])
        self._y = float(self.HEIGHT / 2) + float(position[1])

    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y
    
    @x.setter
    def x(self, value):
        self._x = value
        self.rect.x = int(self._x - self.WIDTH / 2)
        # max(0, min(player_rect.x, SCREEN_WIDTH - player_rect.width))

    @y.setter
    def y(self, value):
        self._y = value
        self.rect.y = int(self._y - self.HEIGHT / 2)
        # max(0, min(player_rect.y, SCREEN_HEIGHT - player_rect.height))

    def physics(self):
        pass
    
    def animate(self):
        pass

    def update(self):
        pass

class Player(Body):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.state = State('player')
        self.move_speed = 5
        self.input = Input()

    def physics(self):
        self.x += self.input.x_axis * self.move_speed
        self.y += self.input.y_axis * self.move_speed
          
    def animate(self):
        if self.input.a_button == 1 and self.state.current_action == self.state.actions['idle_loop']:
            self.state.set_action('attack_1')
        try:
            self.image = self.state.current_action.animation.next()
        except StopIteration:
            self.state.set_action('idle_loop')
            
    def update(self):
        self.input.update()
        self.physics()
        self.animate()

class Enemy(Body):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.image.fill((0,255,0))
        self.move_speed = 2

    def physics(self):
        self.x += 0.1 * self.move_speed
        self.y += 0.1 * self.move_speed
        
    def update(self):
        self.physics()
        # self.animate()

class Input():
    def __init__(self):
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()

    def update(self):
        self.x_axis = self.process_axis(self.joystick.get_axis(0))
        self.y_axis = self.process_axis(self.joystick.get_axis(1))
        self.a_button = self.joystick.get_button(0)
        # print(self.a_button)
       

    def process_axis(self, value: float):
        value = round(value, 1)
        if value <= 0.1 and value >= 0.0:
            value = 0.0
        elif value >= -0.1 and value < 0.0:
            value = 0.0
        else:
            value = value
        return value


class State:
    def __init__(self, profile):
        self.actions = {}
        directory = 'topdown/spritesheet/assets/'
        for filename in os.listdir(f'{directory}{profile}'):
            action_name = filename.split('.')[0]
            print(action_name)
            if filename.split('.')[0].split('_')[-1] == 'loop':
                loop = True
            else:
                loop = False
            self.actions[action_name] = Action(f'{directory}{profile}/{filename}', loop)
        # self.actions['attack_1'] = Action('topdown/spritesheet/assets/player/attack_1.png', False)
        # self.actions['idle_loop'] = Action('topdown/spritesheet/assets/player/idle.png', True)
        self.current_action = None
        self.set_action('idle_loop')
        
    def set_action(self, action):
        try:
            self.current_action = self.actions[action]
        except KeyError:
            print("Invalid state. State remains the same. Available states are:", list(self.actions.keys()))
        self.current_action.animation.iter()
        
    
@dataclass
class Action():
        # action: str
        sprite_sheet_filepath: str
        # count:int
        loop:int
        
        def __post_init__(self):
            self.animation = self.load_animation()
        
        def load_animation(self):
            # return SpriteStripAnim(self.sprite_sheet_filepath, (0,0,128,128), self.count, (0, 0, 0), self.loop, 8)
            return SpriteStripAnim(self.sprite_sheet_filepath, loop=self.loop, frames=8)
    