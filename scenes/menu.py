import pygame

from loguru import logger

class Field():
    def __init__(self, screen, x, y):
        self.screen = screen
        self.x = x
        self.y = y


class Dropdown(Field):
    def __init__(self, screen, x, y):
        super().__init__(screen, x, y)
        self.DROPDOWN_WIDTH = 150
        self.DROPDOWN_HEIGHT = 30

        self.OPTION_HEIGHT = 30

        self.FONT_SIZE = 24
        self.font = pygame.font.SysFont(None, self.FONT_SIZE)

        self.show_options = False
        self.selected_option = 0

        self.dropdown_rect = pygame.Rect(
            self.x, self.y, self.DROPDOWN_WIDTH, self.DROPDOWN_HEIGHT)
        self.options = ["Option 1", "Option 2", "Option 3"]

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (200, 200, 200)

    def update(self, event):
        if self.dropdown_rect.collidepoint(event.pos):
            self.show_options = not self.show_options
        elif self.show_options:
            for i in range(len(self.options)):
                option_rect = pygame.Rect(self.x, self.y + self.DROPDOWN_HEIGHT +
                                          i * self.OPTION_HEIGHT, self.DROPDOWN_WIDTH, self.OPTION_HEIGHT)
                if option_rect.collidepoint(event.pos):
                    self.selected_option = i
                    logger.debug(f'Option {self.selected_option} selected')
                    self.show_options = False

    def draw(self):
        pygame.draw.rect(self.screen, self.GRAY, (self.x, self.y,
                         self.DROPDOWN_WIDTH, self.DROPDOWN_HEIGHT))
        pygame.draw.rect(self.screen, self.BLACK, (self.x,
                         self.y, self.DROPDOWN_WIDTH, self.DROPDOWN_HEIGHT), 2)
        text = self.font.render(
            self.options[self.selected_option], True, self.BLACK)
        text_rect = text.get_rect(
            center=(self.x + self.DROPDOWN_WIDTH // 2, self.y + self.DROPDOWN_HEIGHT // 2))
        self.screen.blit(text, text_rect)
        if self.show_options:
            self.draw_options()

    def draw_options(self):
        x = self.x
        y = self.y + self.DROPDOWN_HEIGHT
        for i, option in enumerate(self.options):
            if i == self.selected_option:
                pygame.draw.rect(self.screen, self.GRAY, (x, y + i *
                                 self.OPTION_HEIGHT, self.DROPDOWN_WIDTH, self.OPTION_HEIGHT))
            pygame.draw.rect(self.screen, self.BLACK, (x, y + i *
                             self.OPTION_HEIGHT, self.DROPDOWN_WIDTH, self.OPTION_HEIGHT), 2)

            text = self.font.render(option, True, self.BLACK)
            text_rect = text.get_rect(center=(
                x + self.DROPDOWN_WIDTH // 2, y + i * self.OPTION_HEIGHT + self.OPTION_HEIGHT // 2))
            self.screen.blit(text, text_rect)