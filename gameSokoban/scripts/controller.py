import pygame
import os
#File quản lý di chuyển cho người chơi tự chơi, bao gồm di chuyển hộp và character
class Controller():
    def __init__(self,character,boxes):
        self.character=character
        self.boxes=boxes
        self.history=[]

    def save_state(self):
    
        state = {
            "player": (self.character.rect.x, self.character.rect.y),
            "boxes": [(b.rect.x, b.rect.y) for b in self.boxes]
        }
        self.history.append(state)
    #hàm undo
    def restore_state(self):
    
        if not self.history:
            return
        state = self.history.pop()
        self.character.rect.topleft = state["player"]
        for b, pos in zip(self.boxes, state["boxes"]):
            b.rect.topleft = pos
    def handle_keydown(self,key):
        if not self.character:
            return
        dx = dy = 0
        if key == pygame.K_UP:
            dy = -1
        elif key == pygame.K_DOWN:
            dy = 1
        elif key == pygame.K_LEFT:
            dx = -1
        elif key == pygame.K_RIGHT:
            dx = 1
        elif key == pygame.K_z:  # Phím Undo
            self.restore_state()
            return

        if dx == 0 and dy == 0:
            return

        self.save_state()
        self.character.move(dx, dy, self.walls, self.boxes)

    def move(self, dx, dy, walls, boxes):
        pass


    




