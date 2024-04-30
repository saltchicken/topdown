import json
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
        
        self.hitbox = None

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
        self.hitbox = self.get_hitbox()
        self.physics()
        self.animate()
    
    def get_hitbox(self):
        action_frame = self.state.current_action.animation.frame_i
        # if action_frame >= self.state.current_action.animation.count:
        #     logger.warning('animation.i is greater than count, why is this happening')
        #     return pygame.Rect( self.rect.x + self.state.current_action.hitbox[-1][0],
        #                     self.rect.y + self.state.current_action.hitbox[-1][1],
        #                     self.state.current_action.hitbox[-1][2],
        #                     self.state.current_action.hitbox[-1][3])
        return pygame.Rect( self.rect.x + self.state.current_action.hitbox[action_frame][0],
                            self.rect.y + self.state.current_action.hitbox[action_frame][1],
                            self.state.current_action.hitbox[action_frame][2],
                            self.state.current_action.hitbox[action_frame][3])
        
    def draw_hitbox(self, screen):
        pygame.draw.rect(screen, (255,255,255), self.hitbox, 1)

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
        if self.input.a_button == 1 and self.state.current_action == self.state.actions['idle']:
            self.state.set_action('attack_1')
        try:
            self.image = self.state.current_action.animation.next()
        except StopIteration:
            self.state.set_action('idle')
            # self.image = self.state.current_action.animation.next()
            
    def update(self):
        self.input.update()
        super().update()
        
        

class Enemy(Body):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.state = State('enemy')
        # self.image.fill((0,255,0))
        self.move_speed = 2

    def physics(self):
        self.x += 0.1 * self.move_speed
        self.y += 0.1 * self.move_speed
        
    def animate(self):
        self.image = self.state.current_action.animation.next()
        # self.image = pygame.transform.flip(self.image, True, False)

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
        for action in os.listdir(f'{directory}{profile}'):
            with open(f'{directory}{profile}/{action}/{action}.json') as info_file:    
                action_info = json.load(info_file)
            self.actions[action] = Action(  action_info['width'], 
                                            action_info['height'], 
                                            f'{directory}{profile}/{action}/{action}.png', 
                                            action_info['count'], 
                                            action_info['loop'], 
                                            action_info['frames'],
                                            action_info['hitbox']
                                         )
        # self.offset_rect = action_info['hitbox']

        
        self.set_action('idle')
        
    def set_action(self, action):
        try:
            self.current_action = self.actions[action]
        except KeyError:
            print("Invalid state. State remains the same. Available states are:", list(self.actions.keys()))
        self.current_action.animation.iter() # Reset the action when switched
        
    
@dataclass
class Action():
        # action: str
        width: int
        height: int
        sprite_sheet_filepath: str
        count:int
        loop: bool
        frames: int
        hitbox: list
        
        def __post_init__(self):
            self.animation = self.load_animation()
        
        def load_animation(self):
            # return SpriteStripAnim(self.sprite_sheet_filepath, (0,0,128,128), self.count, (0, 0, 0), self.loop, 8)
            return SpriteStripAnim(self.sprite_sheet_filepath, rect=(0,0,self.width, self.height), count=self.count, loop=self.loop, frames=self.frames)
    