import pygame

class Controller():
    def __init__(self, window):
        self.window = window
        self.map_current = self.window.get_data("map_current")
        self.pos_history_list = []
        self.state = self.window.get_data("pos_state")
        self.pos_character = self.state["pos_character"]
        self.pos_boxes = self.state["pos_boxes"].copy()


    #hàm undo
    def restore_state(self):
    
        if len(self.pos_history_list) == 0:
            return
        state_before = self.pos_history_list.pop()
        print(state_before)
        self.move(None, state_before)
        self.state = {
            "pos_character" : state_before["pos_character"],
            "pos_boxes" : state_before["pos_boxes"].copy()
        }
        self.window.set_data("pos_state", self.state)
        self.window.set_data("pos_history_list", self.pos_history_list)
        self.window.set_data("map_current", self.map_current)
        
    def handle_AI_action(self, d):
        self.move(d)
    
    def handle_human_action(self, key):
        dx = dy = 0
        if key == pygame.K_UP:
            print("đã chạy")
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

        d = (dx, dy)
        self.move(d)
    
    def save_state(self, pose_character, pos_boxes):
        print(self.state)
        self.pos_history_list.append(self.state)
        print(self.pos_history_list)
        self.state = {
            "pos_character" : pose_character,
            "pos_boxes" : pos_boxes.copy()
        }
        self.window.set_data("pos_state", self.state)
        self.window.set_data("pos_history_list", self.pos_history_list)
        self.window.set_data("map_current", self.map_current)

    def move(self, d=None, state_before=None):
        if state_before is None:
            new_x_c = self.pos_character[0] + d[0]
            new_y_c = self.pos_character[1] + d[1]

            if self.map_current[new_y_c][new_x_c] == "w":
                print("đã chạy")
                return
            elif self.map_current[new_y_c][new_x_c] == "b":
                new_x_b = new_x_c + d[0]
                new_y_b = new_y_c + d[1]
                if self.map_current[new_y_b][new_x_b] == "w" or self.map_current[new_y_b][new_x_b] == "b":
                    return 
                elif self.map_current[new_y_b][new_x_b] == "g":
                    for i in range(len(self.pos_boxes)):
                        if self.pos_boxes[i] == (new_x_c, new_y_c):
                            self.pos_boxes[i] = (new_x_b, new_y_b)
                            self.map_current[new_y_b][new_x_b], self.map_current[new_y_c][new_x_c] = self.map_current[new_y_c][new_x_c], self.map_current[new_y_b][new_x_b]
                            self.map_current[new_y_c][new_x_c], self.map_current[self.pos_character[1]][self.pos_character[0]] = self.map_current[self.pos_character[1]][self.pos_character[0]], self.map_current[new_y_c][new_x_c]
                            self.pos_character = (new_x_c, new_y_c)
                            self.save_state(self.pos_character, self.pos_boxes)
                            break
                elif self.map_current[new_y_b][new_x_b] == "p":
                    self.map_current[new_y_b][new_x_b] = "g"
                    for i in range(len(self.pos_boxes)):
                        if self.pos_boxes[i] == (new_x_c, new_y_c):
                            self.pos_boxes[i] = (new_x_b, new_y_b)
                            self.map_current[new_y_b][new_x_b], self.map_current[new_y_c][new_x_c] = self.map_current[new_y_c][new_x_c], self.map_current[new_y_b][new_x_b]
                            self.map_current[new_y_c][new_x_c], self.map_current[self.pos_character[1]][self.pos_character[0]] = self.map_current[self.pos_character[1]][self.pos_character[0]], self.map_current[new_y_c][new_x_c]
                            self.pos_character = (new_x_c, new_y_c)
                            self.save_state(self.pos_character, self.pos_boxes)
                            break
            elif self.map_current[new_y_c][new_x_c] == "g":
                self.map_current[new_y_c][new_x_c], self.map_current[self.pos_character[1]][self.pos_character[0]] = self.map_current[self.pos_character[1]][self.pos_character[0]], self.map_current[new_y_c][new_x_c]
                self.pos_character = (new_x_c, new_y_c)
                self.save_state(self.pos_character, self.pos_boxes)
            elif self.map_current[new_y_c][new_x_c] == "p":
                self.map_current[new_y_c][new_x_c] = "g"
                self.map_current[new_y_c][new_x_c], self.map_current[self.pos_character[1]][self.pos_character[0]] = self.map_current[self.pos_character[1]][self.pos_character[0]], self.map_current[new_y_c][new_x_c]
                self.pos_character = (new_x_c, new_y_c)
                self.save_state(self.pos_character, self.pos_boxes)
        else:
            pos_character_before = state_before["pos_character"]
            pos_boxes_before = state_before["pos_boxes"].copy()
            if self.map_current[pos_character_before[1]][pos_character_before[0]] == "p":
                self.map_current[pos_character_before[1]][pos_character_before[0]] = "g"
            self.map_current[pos_character_before[1]][pos_character_before[0]], self.map_current[self.pos_character[1]][self.pos_character[0]] = self.map_current[self.pos_character[1]][self.pos_character[0]], self.map_current[pos_character_before[1]][pos_character_before[0]]
            for i, pos_box in enumerate(self.pos_boxes):
                print(pos_box, pos_boxes_before[i])
                if pos_box != pos_boxes_before[i]:
                    if self.map_current[pos_boxes_before[i][1]][pos_boxes_before[i][0]] == "p":
                        self.map_current[pos_boxes_before[i][1]][pos_boxes_before[i][0]] = "g"
                    self.map_current[pos_box[1]][pos_box[0]], self.map_current[pos_boxes_before[i][1]][pos_boxes_before[i][0]] = self.map_current[pos_boxes_before[i][1]][pos_boxes_before[i][0]], self.map_current[pos_box[1]][pos_box[0]]
                    break
                else:
                    print("thất bại")
            self.pos_character = pos_character_before
            self.pos_boxes = pos_boxes_before.copy()

        pos_endpoints = self.window.get_data("pos_endpoints")
        print(pos_endpoints)
        for pos_endpoint in pos_endpoints:
            if self.map_current[pos_endpoint[1]][pos_endpoint[0]] != "c" and self.map_current[pos_endpoint[1]][pos_endpoint[0]] != "b":
                self.map_current[pos_endpoint[1]][pos_endpoint[0]] = "p"
        
        


    




