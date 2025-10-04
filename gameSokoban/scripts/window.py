import pygame
import os

os.environ['SDL_VIDEO_CENTERED'] = '1' 
pygame.init()

image_icon_path = r"assets\images\icon.png"

class Window():
    def __init__(self):
        info = pygame.display.Info()
        screen_w, screen_h = info.current_w, info.current_h
        self.size = (screen_w, screen_h)
        self.screen = pygame.display.set_mode(self.size)

        self.caption = "Sokoban Game"
        pygame.display.set_caption(self.caption)
    
        self.icon_ori = pygame.image.load(image_icon_path).convert_alpha()
        self.icon = pygame.transform.scale(self.icon_ori, (32, 32))
        pygame.display.set_icon(self.icon)

        self.data = {"status_screen" : "menu"}

    def set_data(self, name, value):
        self.data[name] = value

    def get_data(self, name):
        return self.data.get(name)