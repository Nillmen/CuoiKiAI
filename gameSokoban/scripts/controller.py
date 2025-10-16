import pygame
import time
from scripts.aiAlgorithm import AIAlgorithm

class Controller():
    def __init__(self, window):
        self.window = window
        self.map_current = self.window.get_data("map_current").copy()
        self.map_current = [list(row) for row in self.map_current]
        self.pos_history_list = self.window.get_data("pos_history_list").copy()
        self.state = self.window.get_data("pos_state").copy()
        self.pos_character = self.state["pos_character"]
        self.pos_boxes = self.state["pos_boxes"].copy()
        self.algorithm_time = self.window.get_data("algorithm_time_run_each_step")
        self.ai_algorithm = AIAlgorithm(self.window)
        self.algorithm_step_list, self.algorithm_detail_dict = None, None
        self.index_step_list = 0

    def restore_state(self):
    
        if len(self.pos_history_list) == 0:
            return
        state_before = self.pos_history_list.pop()
        self.move(None, state_before)
        self.state = {
            "pos_character" : state_before["pos_character"],
            "pos_boxes" : state_before["pos_boxes"].copy()
        }
        self.window.set_data("pos_state", self.state)
        self.window.set_data("pos_history_list", self.pos_history_list)
        self.window.set_data("map_current", self.map_current)

    def run_algorithm(self):
        if self.window.get_data("mode") == "AI" and len(self.ai_algorithm.algorithm) > 0:
            self.algorithm_step_list, self.algorithm_detail_dict = self.ai_algorithm.get_response()


    def handle_AI_action(self):
        if self.algorithm_step_list is None or len(self.algorithm_step_list) == 0:
            return False

        if not hasattr(self, "last_ai_time"):
            self.last_ai_time = time.perf_counter()

        if self.index_step_list < len(self.algorithm_step_list):
            current_time = time.perf_counter()

            if current_time - self.last_ai_time >= self.algorithm_time:
                d = self.algorithm_step_list[self.index_step_list]
                self.move(d)
                self.index_step_list += 1
                self.last_ai_time = current_time
                return True
        else:
            return False
    
    def handle_human_action(self, key):
        dx = dy = 0
        if key == pygame.K_UP:
            dy = -1
        elif key == pygame.K_DOWN:
            dy = 1
        elif key == pygame.K_LEFT:
            dx = -1
        elif key == pygame.K_RIGHT:
            dx = 1
        elif key == pygame.K_z: 
            self.restore_state()
            return
        if dx == 0 and dy == 0:
            return

        d = (dx, dy)
        self.move(d)
    
    def save_state(self, pos_character, pos_boxes):
        self.pos_history_list.append(self.state)
        self.state = {
            "pos_character": pos_character,
            "pos_boxes": pos_boxes.copy()
        }
        self.window.set_data("pos_state", self.state)
        self.window.set_data("pos_history_list", self.pos_history_list)
        self.window.set_data("map_current", self.map_current)

    def move(self, d=None, state_before=None):
        if state_before is None:
            new_x_c = self.pos_character[0] + d[0]
            new_y_c = self.pos_character[1] + d[1]

            print(self.map_current[new_y_c][new_x_c])

            if self.map_current[new_y_c][new_x_c] == "w":
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
                if pos_box != pos_boxes_before[i]:
                    if self.map_current[pos_boxes_before[i][1]][pos_boxes_before[i][0]] == "p":
                        self.map_current[pos_boxes_before[i][1]][pos_boxes_before[i][0]] = "g"
                    self.map_current[pos_box[1]][pos_box[0]], self.map_current[pos_boxes_before[i][1]][pos_boxes_before[i][0]] = self.map_current[pos_boxes_before[i][1]][pos_boxes_before[i][0]], self.map_current[pos_box[1]][pos_box[0]]
                    break
            self.pos_character = pos_character_before
            self.pos_boxes = pos_boxes_before.copy()

        pos_endpoints = self.window.get_data("pos_endpoints")
        for pos_endpoint in pos_endpoints:
            if self.map_current[pos_endpoint[1]][pos_endpoint[0]] != "c" and self.map_current[pos_endpoint[1]][pos_endpoint[0]] != "b":
                self.map_current[pos_endpoint[1]][pos_endpoint[0]] = "p"
        
    def check_win(self, mode):
        if mode == "human":
            pose_endpoints = self.window.get_data("pos_endpoints")
            len_true = 0
            for pos_box in self.state["pos_boxes"]:
                if pos_box in pose_endpoints:
                    len_true += 1
            if len_true == len(pose_endpoints):
                return True
            return False
        elif mode == "AI":
            return self.ai_algorithm.check_win()

    def check_can_solve(self, mode):
        if mode == "AI":
            return self.ai_algorithm.check_can_solve()

    def check_algorithm_selecting(self):
        self.ai_algorithm.algorithm = self.window.get_data("algorithm")
        if len(self.ai_algorithm.algorithm) > 0:
            return True
        return False
    
    def check_complete_AI(self):
        return self.algorithm_step_list is None or self.index_step_list == len(self.algorithm_step_list)
    




