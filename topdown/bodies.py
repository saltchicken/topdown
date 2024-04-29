import pygame

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
        
        # ss = spritesheet('topdown/spritesheet/resources/Attack_1.png')
        # self.image = ss.image_at((0, 0, 128, 128))
        # FPS = 90
        self.attack_animation = SpriteStripAnim('topdown/spritesheet/resources/Attack_1.png', (0,0,128,128), 4, (0, 0, 0), True, 8)
        self.idle_animation = SpriteStripAnim('topdown/spritesheet/resources/Idle.png', (0,0,128,128), 7, (0, 0, 0), True, 64)
        # sprite_sheet_image = pygame.image.load('topdown/spritesheet/resources/Attack_1.png').convert_alpha()
        # sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)
        
        # self.image = sprite_sheet.get_image(0, 128, 128, 1, (100,0,0))
        # self.image.fill((255,0,0))
        self.move_speed = 5

        self.input = Input()

    def physics(self):
        self.x += self.input.x_axis * self.move_speed
        self.y += self.input.y_axis * self.move_speed
        
    def animate(self):
        self.image = self.idle_animation.next()
        
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
        print(self.a_button)
       

    def process_axis(self, value: float):
        value = round(value, 1)
        if value <= 0.1 and value >= 0.0:
            value = 0.0
        elif value >= -0.1 and value < 0.0:
            value = 0.0
        else:
            value = value
        return value
    