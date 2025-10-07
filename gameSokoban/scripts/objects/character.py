import pygame
import os

class Character():
    def __init__(self, window, x, y, tile_size):
        # Tải các sprite theo hướng với đường dẫn tương đối
        self.window = window
        self.sprites = {
            "right": pygame.transform.scale(pygame.image.load(r"assets\images\character\characterRight.png") , (tile_size, tile_size)),
            "left": pygame.transform.scale(pygame.image.load(r"assets\images\character\characterLeft.png"), (tile_size, tile_size)),
            "up": pygame.transform.scale(pygame.image.load(r"assets\images\character\characterBack.png"), (tile_size, tile_size)),
            "down": pygame.transform.scale(pygame.image.load(r"assets\images\character\character.png"), (tile_size, tile_size))
        }

        self.pos_history_list = self.window.get_data("pos_history_list")

        self.current_sprite = ""
        if len(self.pos_history_list) > 0:
            pos_character = self.window.get_data("pos_state")["pos_character"]
            pos_character_before = self.pos_history_list[-1]["pos_character"]
            if pos_character[0] - pos_character_before[0] > 0:
                self.current_sprite = "right"
            elif pos_character[0] - pos_character_before[0] < 0:
                self.current_sprite = "left"
            elif pos_character[1] - pos_character_before[1] > 0:
                self.current_sprite = "down"
            elif pos_character[1] - pos_character_before[1] < 0:
                self.current_sprite = "up"
        else:
            self.current_sprite = "right" 
        self.image = self.sprites[self.current_sprite]
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect = self.image.get_rect(topleft=(x, y))

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