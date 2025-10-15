import pygame
from scripts.objects.character import Character
from scripts.objects.box import Box
from scripts.objects.endpoint import Endpoint
from scripts.objects.ground import Ground
from scripts.objects.wall import Wall

class Map():
    def __init__(self, window):
        self.window = window
        self.screen = self.window.screen

        self.mode = self.window.get_data("mode")
        self.level = self.window.get_data("level")
        self.map_ori = self.window.get_data("map_ori_list")[self.level]
        self.pos_history_list = self.window.get_data("pos_history_list").copy()
        print(self.pos_history_list)
        self.map_ori = [list(row) for row in self.map_ori]
        self.map_current = self.window.get_data("map_current").copy()
        if len(self.map_current) == 0:
            self.map_current = self.map_ori.copy()
            self.window.set_data("map_current", self.map_current)
        print("mapcurrent", self.map_current)
        self.state = self.window.get_data("pos_state").copy()
        self.pos_endpoints = self.window.get_data("pos_endpoints").copy()

        self.row_quantity = len(self.map_current)
        self.col_quantity = len(self.map_current[0])

        self.screen_size = self.window.get_data("screen_size")

        self.tile_size = int(2 / 3 * self.screen_size[1] / self.row_quantity)

        self.play_part_sceen_size = (round(self.tile_size * self.col_quantity), round(self.tile_size * self.row_quantity))
        self.menu_part_screen_size = (self.play_part_sceen_size[0], round(1 / 2 * self.play_part_sceen_size[1]))
        self.screen_size = (self.play_part_sceen_size[0], round(self.play_part_sceen_size[1] + self.menu_part_screen_size[1]))
        self.window.set_data("screen_size", self.screen_size)
        self.screen = pygame.display.set_mode(self.screen_size)
        self.objects = []


    def create_map(self):
        self.objects = []
        pos_endpoints = []
        pos_boxes = []
        pos_character = None

        self.map_current = self.window.get_data("map_current")
        print(self.map_current)

        for row_index, row in enumerate(self.map_current):
            for col_index, cell in enumerate(row):
                x = col_index * self.tile_size
                y = row_index * self.tile_size + self.menu_part_screen_size[1]

                if cell == "w":  # tường
                    obj = Wall(x, y, self.tile_size)
                    self.objects.append(obj)

                elif cell == "g":  # mặt đất
                    obj = Ground(x, y, self.tile_size)
                    self.objects.append(obj)

                elif cell == "b":  # thùng
                    g = Ground(x, y, self.tile_size)
                    b = Box(x, y, self.tile_size)
                    pos_boxes.append((col_index, row_index))
                    if self.pos_endpoints and (col_index, row_index) in self.pos_endpoints:
                        p = Endpoint(x, y, self.tile_size)
                        self.objects.extend([g, p, b])
                    else:
                        self.objects.extend([g, b])

                elif cell == "c":  # nhân vật
                    g = Ground(x, y, self.tile_size)
                    c = Character(self.window, x, y, self.tile_size)
                    pos_character = (col_index, row_index)
                    if self.pos_endpoints and (col_index, row_index) in self.pos_endpoints:
                        p = Endpoint(x, y, self.tile_size)
                        self.objects.extend([g, p, c])
                    else:
                        self.objects.extend([g, c])

                elif cell == "e":  # khoảng trống
                    g = Ground(x, y, self.tile_size)
                    self.objects.append(g)

                elif cell == "p":  # điểm đích
                    g = Ground(x, y, self.tile_size)
                    p = Endpoint(x, y, self.tile_size)
                    pos_endpoints.append((col_index, row_index))
                    self.objects.extend([g, p])

        if len(self.pos_endpoints) == 0:
            self.pos_endpoints = pos_endpoints.copy()
            self.window.set_data("pos_endpoints", self.pos_endpoints)

        if len(self.state) == 0:
            self.state = {
                "pos_character" : pos_character,
                "pos_boxes" : pos_boxes.copy()
            }
            self.window.set_data("pos_state", self.state)

    def draw_map(self):
        for obj in self.objects:
            self.screen.blit(obj.image, obj.rect)