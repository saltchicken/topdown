import pygame
import sys

from loguru import logger

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BG = (75, 85, 65)

GRID = 64

class Menu():
    def __init__(self, screen):
        info = pygame.display.Info()
        self.WIDTH, self.HEIGHT = info.current_w, info.current_h
        self.screen = screen
        self.background = (40, 40, 40)
        
        self.DROPDOWN_WIDTH = 150
        self.DROPDOWN_HEIGHT = 30
        
        self.OPTION_HEIGHT = 30
        
        self.FONT_SIZE = 24
        self.font = pygame.font.SysFont(None, self.FONT_SIZE)
        
        self.show_options = False
        self.selected_option = 0
        

    def update(self, event):
        self.screen.fill(self.background)
        # running = True
        dropdown_rect = pygame.Rect(100, 100, self.DROPDOWN_WIDTH, self.DROPDOWN_HEIGHT)
        options = ["Option 1", "Option 2", "Option 3"]
        
        
        # while running:
        self.screen.fill(BG)
            
        if event:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if dropdown_rect.collidepoint(event.pos):
                    self.show_options = not self.show_options
                elif self.show_options:
                    for i in range(len(options)):
                        option_rect = pygame.Rect(100, 100 + self.DROPDOWN_HEIGHT + i * self.OPTION_HEIGHT, self.DROPDOWN_WIDTH, self.OPTION_HEIGHT)
                        if option_rect.collidepoint(event.pos):
                            self.selected_option = i
                            logger.debug(f'Option {self.selected_option} selected')
                            self.show_options = False
            
        self.draw_dropdown(100, 100, options, self.selected_option)
        if self.show_options:
            self.draw_options(100, 100 + self.DROPDOWN_HEIGHT, options, self.selected_option)
                  
        pygame.display.flip()
        
    def draw_dropdown(self, x, y, options, selected_option):
        pygame.draw.rect(self.screen, GRAY, (x, y, self.DROPDOWN_WIDTH, self.DROPDOWN_HEIGHT))
        pygame.draw.rect(self.screen, BLACK, (x, y, self.DROPDOWN_WIDTH, self.DROPDOWN_HEIGHT), 2)
        
        text = self.font.render(options[selected_option], True, BLACK)
        text_rect = text.get_rect(center=(x + self.DROPDOWN_WIDTH // 2, y + self.DROPDOWN_HEIGHT // 2))
        self.screen.blit(text, text_rect)

    def draw_options(self, x, y, options, selected_option):
        for i, option in enumerate(options):
            if i == selected_option:
                pygame.draw.rect(self.screen, GRAY, (x, y + i * self.OPTION_HEIGHT, self.DROPDOWN_WIDTH, self.OPTION_HEIGHT))
            pygame.draw.rect(self.screen, BLACK, (x, y + i * self.OPTION_HEIGHT, self.DROPDOWN_WIDTH, self.OPTION_HEIGHT), 2)
            
            text = self.font.render(option, True, BLACK)
            text_rect = text.get_rect(center=(x + self.DROPDOWN_WIDTH // 2, y + i * self.OPTION_HEIGHT + self.OPTION_HEIGHT // 2))
            self.screen.blit(text, text_rect)
            