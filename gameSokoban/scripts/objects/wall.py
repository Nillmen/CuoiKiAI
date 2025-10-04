# scripts/wall.py
import pygame
import os

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_size):
        super().__init__()
        # LƯU Ý: thư mục assets (có 's') và tên file mình để chữ thường 'wall.png'
        self.image_path = r"assets\images\wall.png"
        self.image = pygame.image.load(self.image_path).convert_alpha()
        # dùng convert_alpha() nếu ảnh có transparent
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect = self.image.get_rect(topleft=(x * tile_size, y * tile_size))
