import pygame
from scripts.map import Map
from scripts.controller import Controller

class Gameplay():
    def __init__(self, window):
        self.window = window
        self.screen = self.window.screen
        self.mode = self.window.get_data("mode")
        self.level = self.window.get_data("level")
        self.map = Map(self.window)
        print("mapbe", self.window.get_data("map_current"))
        self.map.create_map()
        print("mapaf", self.window.get_data("map_current"))
        self.controller = Controller(self.window)
        self.clock = pygame.time.Clock()
        self.fps = self.window.get_data("fps")

    def handle_events(self, event):
        if self.mode == "human":
            if event and event.type == pygame.KEYDOWN:
                print("-3", self.window.get_data("map_current"))
                print("đã chạy key down")
                self.controller.handle_human_action(event.key)
                self.map.create_map()
        if self.mode == "AI":
            if not event:
                if self.controller.handle_AI_action():
                    self.map.create_map()
                #pass

        if event and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.window.set_data("status_screen", "menu")
                self.window.set_data("menu_back", True)
        return True
    
    def run(self):
        self.map.draw_map()
        pygame.display.flip()
        self.clock.tick(self.fps)

    def release(self):
        pass