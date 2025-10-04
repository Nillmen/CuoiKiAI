# scripts/endpoint.py
import pygame
import os

class Endpoint(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_size):
        super().__init__()
        
        self.image_path = r"assets\images\endpoint.png"
        self.image = pygame.image.load(self.image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect = self.image.get_rect(topleft=(x * tile_size, y * tile_size))