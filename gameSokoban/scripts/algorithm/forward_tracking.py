import time
from itertools import permutations
from collections import deque

def input_infor(self):

    playerX, playerY = self.get_player_pos()
    self.fb_in_infor = {
        "pos_character_row": {"type": int, "value": playerX},
        "pos_character_col": {"type": int, "value": playerY}
    }
    return self.fb_in_infor

def check_input_infor(self, key_value_list):

    try:
        x_new = int(list(key_value_list[0].values())[0])
        y_new = int(list(key_value_list[1].values())[0])
    except (ValueError, IndexError):
        return False

    level = self.window.get_data("level")
    map_data = self.window.get_data("map_ori_list")[level]
    
    if not (0 <= x_new < len(map_data) and 0 <= y_new < len(map_data[0])):
        return False
    if map_data[x_new][y_new] in "bwe": 
        return False
        
    return True

def change_input_infor(self, key_value_list=None):
    playerX_new = int(self.fb_in_infor["pos_character_row"]["value"])
    playerY_new = int(self.fb_in_infor["pos_character_col"]["value"])
    playerX_old, playerY_old = self.get_player_pos()

    if (playerX_new, playerY_new) != (playerX_old, playerY_old):
        self.map_data[playerX_new][playerY_new] = "c" 
        if (playerY_old, playerX_old) in self.pos_endpoints:
            self.map_data[playerX_old][playerY_old] = "p"
        else:
            self.map_data[playerX_old][playerY_old] = "g"
    self.window.set_data("map_current", self.map_data)

def run(self):
    self.state_count = 0
    self.step_count = 0
    best_path = []  
    self.best_path_length = 0
    self.start_time = time.perf_counter()
    
    self.add_data()
    player_start = self.get_player_pos()
    boxes = list(self.boxPos)
    goals_list = list(self.endPointPos)
    num_boxes = len(boxes)
    
    if num_boxes != len(goals_list):
        return self.save_result([], False, self.state_count, self.step_count)
    
    initial_domains = [set(goals_list) for _ in range(num_boxes)]
    initial_boxes = tuple(sorted(boxes))
    
    self.observe(player_start[0], player_start[1], list(initial_boxes), depth=0)
    
    solution_found = False

    for perm_order in permutations(range(num_boxes)):
        if self.check_limit_condition(self.step_count, time.perf_counter() - self.start_time):
            break
        order = [boxes[i] for i in perm_order]  
        domains = [initial_domains[i].copy() for i in range(num_boxes)]
        assignment = {}
        
        result = self.backtrack(order, 0, domains, initial_boxes, player_start, assignment, depth=0)
        
        if result:

            idx_order = tuple(boxes.index(b) for b in order)
            result['order'] = idx_order
            result['box_order'] = order
            
            player_path = self.extract_player_path(result, player_start)
            if player_path:
                if len(player_path) > self.best_path_length:
                    best_path = player_path
                    self.best_path_length = len(player_path)
                
                final_boxes = tuple(result['mapping'][b] for b in order)
                if self.is_complete(final_boxes):
                    solution_found = True
                    return self.save_result(player_path, True, self.state_count, self.step_count)
    
    return self.save_result(best_path, solution_found, self.state_count, self.step_count)