import pygame
import os

class Character:
    def __init__(self, x, y, tile_size):
        self.rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
        # Tải các sprite theo hướng với đường dẫn tương đối
        
        self.sprites = {
            "right": pygame.transform.scale(pygame.image.load(r"assets\images\characterRight.png") , (tile_size, tile_size)),
            "left": pygame.transform.scale(pygame.image.load(r"assets\images\characterLeft.png"), (tile_size, tile_size)),
            "up": pygame.transform.scale(pygame.image.load(r"assets\images\characterBack.png"), (tile_size, tile_size)),
            "down": pygame.transform.scale(pygame.image.load(r"assets\images\character.png"), (tile_size, tile_size))
        }
        self.current_sprite = "right"  # Hướng mặc định
        self.image = self.sprites[self.current_sprite]

    def move(self, dx, dy, walls, boxes):
        new_rect = self.rect.copy()
        new_rect.x += dx * self.rect.width
        new_rect.y += dy * self.rect.height

        # Cập nhật sprite theo hướng di chuyển
        if dx > 0:
            self.current_sprite = "right"
        elif dx < 0:
            self.current_sprite = "left"
        elif dy < 0:
            self.current_sprite = "up"
        elif dy > 0:
            self.current_sprite = "down"
        self.image = self.sprites[self.current_sprite]

        # Kiểm tra va chạm với tường
        for wall in walls:
            if new_rect.colliderect(wall.rect):
                return False

        # Kiểm tra va chạm với hộp
        for box in boxes:
            if new_rect.colliderect(box.rect):
                if not box.move(dx, dy, walls, boxes):
                    return False
                else:
                    self.rect = new_rect
                    return True

        self.rect = new_rect
        return True