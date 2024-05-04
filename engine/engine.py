import pygame
from pygame.locals import QUIT, JOYBUTTONDOWN

from pathlib import Path
from loguru import logger

from scenes.scenes import Scene

class Topdown:
    def __init__(self):
        pygame.init()
        self.set_screen_size(1280, 1024)
        # self.set_screen_size(fullscreen=True)
        pygame.display.set_caption("Topdown")
        self.scenes = {}
        self.scenes['scene'] = Scene.from_config(Path('scenes/assets/scene2.json'), self.screen)
        self.scenes['menu'] = Scene(self.screen)
        self.set_scene('menu')
        self.clock = pygame.time.Clock()
        
    def loop(self):
        self.running = True
        while self.running:
            self.handle_events()
            self.current_scene.update()
            self.clock.tick(90)
        self.exit()
        
    def set_screen_size(self, width=None, height=None, fullscreen=False):
        if fullscreen or width == None or height == None:
            info = pygame.display.Info()
            self.WIDTH, self.HEIGHT = info.current_w, info.current_h
            self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.FULLSCREEN)
        else:
            self.WIDTH, self.HEIGHT = width, height
            self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        
    def set_scene(self, scene):
        try:
            self.current_scene = self.scenes[scene]
        except KeyError:
            print("Invalid state. State remains the same. Available scenes are:", list(self.scenes.keys()))
            
    def handle_events(self):
        for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                elif event.type == JOYBUTTONDOWN:
                    # Check if the 'A' button is pressed
                    if event.button == 0:  # Adjust this index if needed, 0 usually represents the 'A' button
                        # logger.debug("A button pressed on the controller!")
                        pass
                    elif event.button == 7:
                        logger.debug('Start button: switching scenes')
                        if self.current_scene != self.scenes['menu']:
                            self.current_scene = self.scenes['menu']
                        else:
                            self.current_scene = self.scenes['scene']

    def exit(self):
        pygame.quit()
        import sys
        logger.debug('Good exit')
        sys.exit()
