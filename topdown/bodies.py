import pygame

class Character():
    def __init__(self):
        self.WIDTH, self.HEIGHT = 50, 50
        self.image = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect()
        self.move_speed = 5
        self._x = float(self.WIDTH / 2) 
        self._y = float(self.HEIGHT / 2)

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
    
    @staticmethod
    def create_character():
        return Character()

class Physics:
    def __init__(self):
        pass
    def update(self, input, characters):
        for character in characters:
            character.x += input.x_axis * character.move_speed
            character.y += input.y_axis * character.move_speed