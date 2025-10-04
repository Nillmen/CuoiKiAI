import pygame
import os
from scripts import window
from scripts.objects import box,character,wall,endpoint,ground

class Map():
    def __init__(self, window):
        self.window = window
        self.screen = self.window.screen
        self.level=self.window.get_data("level")
        self.mode=self.window.get_data("mode")
        self.boxes = []
        self.character=None
        self.grounds=[]
        self.endpoints=[]
        self.walls = []

        self.map_objects=[]
        self.mapList = [[  # Level 1
        "ewwwww",
        "wwcppw",
        "wgbbww",
        "wgggwe",
        "wgggwe",
        "wwwwwe"
        ],
    
        [  # Level 2
        "wwwwwww",
        "wppbppw",
        "wppwppw",
        "wgbbbgw",
        "wggbggw",
        "wgbbbcw",
        "wgggggw",
        "wwwwwww"
        ],
    
        [  # Level 3
        "eeeewwwwweeeeeeeeew",
        "eeeewgggweeeeeeeeee",
        "eeeewbggweeeeeeeeee",
        "eewwwggbwweeeeeeeee",
        "eewggbgbgweeeeeeeee",
        "wwwgwgwwgweeewwwwww",
        "wgggwgwwgwwwwwggppw",
        "wgbggbggggggggggppw",
        "wwwwwgwwwgwcwwggppw",
        "eeeewgggggwwwwwwwww",
        "eeeewwwwwwweeeeeeee"

        ]]
        self.window.set_data("map_ori", self.mapList)
    def set_data(self):
        self.window.set_data("map_current", self.mapList[self.level-1])

        
    def createMap(self):
        tile_size = 50
        map_data = self.maps[self.level-1]
        objects = []   # list chứa tất cả object cần vẽ

        for row_index, row in enumerate(map_data):
            for col_index, cell in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size

                if cell == "w":  # tường
                    obj = wall.Wall(x, y, tile_size)
                    self.walls.append(obj)
                    objects.append(obj)

                elif cell == "g":  # mặt đất
                    obj = ground.Ground(x, y, tile_size)
                    self.grounds.append(obj)
                    objects.append(obj)

                elif cell == "b":  # thùng
                    g = ground.Ground(x, y, tile_size)
                    b = box.Box(x, y, tile_size)
                    self.grounds.append(g)
                    self.boxes.append(b)
                    objects.extend([g, b])

                elif cell == "c":  # nhân vật
                    g = ground.Ground(x, y, tile_size)
                    c = character.Character(x, y, tile_size)
                    self.grounds.append(g)
                    self.character = c
                    objects.extend([g, c])

                elif cell == "e":  # khoảng trống
                    g = ground.Ground(x, y, tile_size)
                    self.grounds.append(g)
                    objects.append(g)

                elif cell == "p":  # điểm đích
                    g = ground.Ground(x, y, tile_size)
                    p = endpoint.Endpoint(x, y, tile_size)
                    self.grounds.append(g)
                    self.endpoints.append(p)
                    objects.extend([g, p])

        self.map_objects = objects
        self.set_data()   # lưu lại list object để drawMap xài

    def drawMap(self):
        for obj in self.map_objects:
            self.screen.blit(obj.image, obj.rect)





