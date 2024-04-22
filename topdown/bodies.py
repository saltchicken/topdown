import pygame

class Body():
    def __init__(self, position):
        self.WIDTH, self.HEIGHT = 50, 50
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

class Character(Body):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.image.fill((255,0,0))
        self.move_speed = 5
    
class Enemy(Body):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.image.fill((0,255,0))
        self.move_speed = 2

class Physics:
    def __init__(self):
        pass
    def update(self, input, bodies):
        for body in bodies:
            if isinstance(body, Character):
                body.x += input.x_axis * body.move_speed
                body.y += input.y_axis * body.move_speed
            elif isinstance(body, Enemy):
                body.x += 0.1 * body.move_speed
                body.y += 0.1 * body.move_speed