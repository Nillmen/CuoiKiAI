
import pygame
import os 
class Box(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_size):
        super().__init__()
        self.image_path = r"assets\images\box.png"
        self.image = pygame.image.load(self.image_path)
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect = self.image.get_rect(topleft=(x * tile_size, y * tile_size))
        self.tile_size = tile_size

    def move(self, dx, dy, walls, boxes):
        """Di chuyển box nếu phía trước trống (không tường, không box khác)."""
        new_rect = self.rect.move(dx * self.tile_size, dy * self.tile_size)

        # Kiểm tra va chạm với tường
        for wall in walls:
            if new_rect.colliderect(wall.rect):
                return False  # không di chuyển được

        # Kiểm tra va chạm với box khác
        for box in boxes:
            if box is not self and new_rect.colliderect(box.rect):
                return False

        # Nếu trống -> di chuyển
        self.rect = new_rect
        return True
