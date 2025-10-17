import time
from collections import deque
import random


def input_infor(self):
    playerX, playerY = self.get_player_pos()
    self.ms_bfs_in_infor = {
        "pos_character_row" : { "type" : int, "value" : playerX },
        "pos_character_col" : { "type" : int, "value" : playerY },
        "number_state": { 
            "type": int, 
            "value": 3 # Ví dụ: Tìm tổng cộng 3 vị trí bắt đầu
        }
    }
    return self.ms_bfs_in_infor

def check_input_infor(self, key_value_list):
    try:
        x_new = int(list(key_value_list[0].values())[0])
        y_new = int(list(key_value_list[1].values())[0])
        num_states = int(list(key_value_list[2].values())[0])
    except (ValueError, IndexError):
        return False

    level = self.window.get_data("level")
    map_data = self.window.get_data("map_ori_list")[level]
    if (x_new >= len(map_data) or y_new >= len(map_data[0]) or map_data[x_new][y_new] in "bwe"):
        return False
    
    if num_states <= 0:
        return False
        
    return True

def change_input_infor(self, key_value_list=None):
    playerX_new = int(self.ms_bfs_in_infor["pos_character_row"]["value"])
    playerY_new = int(self.ms_bfs_in_infor["pos_character_col"]["value"])
    num_states = int(self.ms_bfs_in_infor["number_state"]["value"])

    playerX_old, playerY_old = self.get_player_pos()

    if (playerX_new, playerY_new) != (playerX_old, playerY_old):
        self.map_data[playerX_new][playerY_new] = "c"
        if (playerY_old, playerX_old) in self.pos_endpoints:
            self.map_data[playerX_old][playerY_old] = "p"
        else:
            self.map_data[playerX_old][playerY_old] = "g"
            
    self.window.set_data("num_total_states", num_states)
    self.window.set_data("map_current", self.map_data)

def _solve_sokoban_with_bfs_from_start(self, start_player_pos, initial_boxes):
    state_count = 0
    step_count = 0
    start_time = time.perf_counter()
    initial_state = (start_player_pos[0], start_player_pos[1], initial_boxes)
    queue = deque([(initial_state, [start_player_pos])])
    visited = {initial_state}
    while queue:
        if self.check_limit_condition(step_count, time.perf_counter() - start_time):
            return None
        (playerX, playerY, boxes), steps = queue.popleft()
        state_count += 1

        self.observe(playerX, playerY, boxes, len_queue=len(queue), steps=steps, depth=len(steps))
        if self.is_complete(boxes):
            return (steps, state_count, step_count)
        for dx, dy in self.directions:
            newX, newY = playerX + dx, playerY + dy
            if self.player_is_blocked(playerX, playerY, newX, newY, boxes):
                continue
            new_boxes = list(boxes)
            if (newX, newY) in boxes:
                idx = boxes.index((newX, newY))
                newBoxX, newBoxY = self.pushed_to_point(playerX, playerY, newX, newY)
                new_boxes[idx] = (newBoxX, newBoxY)
            new_state = (newX, newY, tuple(sorted(new_boxes)))
            if new_state not in visited:
                visited.add(new_state)
                queue.append((new_state, steps + [(newX, newY)]))
                step_count += 1
    return None

def is_blocked(self, row, col):
    num_rows = len(self.map_data)
    num_cols = len(self.map_data[0])
    if not (0 <= row < num_rows and 0 <= col < num_cols):
        return True
    if self.map_data[row][col] == 'w':
        return True
    return False

def run(self):
    self.add_data()
    
    true_start_pos = self.get_player_pos()
    num_total_states = self.window.get_data("num_total_states")
    if num_total_states is None:
        num_total_states = 1
    initial_boxes = tuple(sorted(self.boxPos))
    
    valid_start_points = []
    checked_points = set()
    radius = 0
    
    while len(valid_start_points) < num_total_states:
        found_in_this_radius = False
        for i in range(-radius, radius + 1):
            for p in [(true_start_pos[0] - radius, true_start_pos[1] + i), (true_start_pos[0] + radius, true_start_pos[1] + i)]:
                if p not in checked_points:
                    checked_points.add(p)
                    if not is_blocked(self, p[0], p[1]) and p not in initial_boxes:
                        valid_start_points.append(p)
                        found_in_this_radius = True
                        if len(valid_start_points) == num_total_states: break
            if len(valid_start_points) == num_total_states: break
            
            for p in [(true_start_pos[0] + i, true_start_pos[1] - radius), (true_start_pos[0] + i, true_start_pos[1] + radius)]:
                if p not in checked_points:
                    checked_points.add(p)
                    if not is_blocked(self, p[0], p[1]) and p not in initial_boxes:
                        valid_start_points.append(p)
                        found_in_this_radius = True
                        if len(valid_start_points) == num_total_states: break
            if len(valid_start_points) == num_total_states: break

        if not found_in_this_radius and radius > 0:
            break
            
        radius += 1

    if not valid_start_points:
         return self.save_result([], is_solution=False, state_count=0, step_count=0)

    all_solution_packages = []
    
    for i, start_pos in enumerate(valid_start_points):
        result_package = _solve_sokoban_with_bfs_from_start(self, start_pos, initial_boxes)
        if result_package:
            all_solution_packages.append( (start_pos, result_package) )

    if not all_solution_packages:
        return self.save_result([], is_solution=False, state_count=0, step_count=0)

    
    random_choice = random.choice(all_solution_packages)
    origin_pos, result_data = random_choice
    final_path, final_state_count, final_step_count = result_data
    
    is_true_solution = (origin_pos == true_start_pos)

    return self.save_result(final_path, is_solution=is_true_solution,
                            state_count=final_state_count,
                            step_count=final_step_count)