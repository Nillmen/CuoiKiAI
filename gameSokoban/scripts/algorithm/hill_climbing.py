import time
import math
import numpy as np

def input_infor(self):
    playerX, playerY = self.get_player_pos()
    self.hc_in_infor = {
        "pos_character_row": {"type": int, "value": playerX},
        "pos_character_col": {"type": int, "value": playerY}
    }
    return self.hc_in_infor

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

    playerX_new = int(self.hc_in_infor["pos_character_row"]["value"])
    playerY_new = int(self.hc_in_infor["pos_character_col"]["value"])
    playerX_old, playerY_old = self.get_player_pos()
    if (playerX_new, playerY_new) != (playerX_old, playerY_old):
        self.map_data[playerX_new][playerY_new] = "c"
        if (playerY_old, playerX_old) in self.pos_endpoints:
            self.map_data[playerX_old][playerY_old] = "p"
        else:
            self.map_data[playerX_old][playerY_old] = "g"
    self.window.set_data("map_current", self.map_data)

def run(self):
    state_count = 0
    step_count = 0
    self.add_data()
    playerX, playerY = self.get_player_pos()
    current_state = (playerX, playerY, tuple(self.boxPos))
    current_path = [(playerX, playerY)]
    current_heuristic = calculate_heuristic(self, current_state[0], current_state[1], current_state[2]) 
    visited = {current_state}
    start_time = time.perf_counter()

    while True:
        state_count += 1
        self.observe(current_state[0], current_state[1], current_state[2], steps=current_path, costH=current_heuristic, depth=len(current_path)-1)
        if self.is_complete(current_state[2]):
            return self.save_result(current_path, is_solution=True, state_count=state_count, step_count=step_count)
        if self.check_limit_condition(step_count, time.perf_counter() - start_time):
            break
            
        best_neighbor_state = None
        best_neighbor_heuristic = float('inf') 
        best_neighbor_path = None
        
        (current_playerX, current_playerY, current_boxes) = current_state

        for dx, dy in self.directions:
            newX, newY = current_playerX + dx, current_playerY + dy
            if not self.player_is_blocked(current_playerX, current_playerY, newX, newY, current_boxes):
                new_boxes = list(current_boxes)
                if (newX, newY) in current_boxes:
                    idx = current_boxes.index((newX, newY))
                    newBoxX, newBoxY = self.pushed_to_point(current_playerX, current_playerY, newX, newY)
                    new_boxes[idx] = (newBoxX, newBoxY)
                
                neighbor_state = (newX, newY, tuple(sorted(new_boxes)))
                if neighbor_state in visited:
                    continue
                    
                neighbor_heuristic = calculate_heuristic(self, neighbor_state[0], neighbor_state[1], neighbor_state[2])
                
                if neighbor_heuristic < best_neighbor_heuristic:
                    best_neighbor_heuristic = neighbor_heuristic
                    best_neighbor_state = neighbor_state
                    best_neighbor_path = current_path + [(newX, newY)]

        if best_neighbor_state is not None and best_neighbor_heuristic <= current_heuristic:
            current_state = best_neighbor_state
            current_path = best_neighbor_path
            current_heuristic = best_neighbor_heuristic
            visited.add(current_state)
            step_count += 1
        else:
            break
            
    return self.save_result(current_path, is_solution=False, state_count=state_count, step_count=step_count)

def calculate_heuristic(self, playerX, playerY, boxes):
    unassigned_boxes = list(boxes)
    unassigned_goals = list(self.endPointPos)
    box_goal_assignment = {}
    total_box_distance = 0

    while unassigned_boxes:
        best_dist = float('inf')
        best_box = None
        best_goal = None
        for box in unassigned_boxes:
            for goal in unassigned_goals:
                dist = abs(box[0] - goal[0]) + abs(box[1] - goal[1])
                if dist < best_dist:
                    best_dist = dist
                    best_box = box
                    best_goal = goal
        if best_box is not None:
            total_box_distance += best_dist
            box_goal_assignment[best_box] = best_goal
            unassigned_boxes.remove(best_box)
            unassigned_goals.remove(best_goal)
        else:
            break

    total_alignment_cost = 0
    player_pos = np.array([playerX, playerY])

    for box, assigned_goal in box_goal_assignment.items():
        direction_vector = np.array([assigned_goal[0] - box[0], assigned_goal[1] - box[1]])
        if np.any(direction_vector):
            if abs(direction_vector[0]) > abs(direction_vector[1]):
                push_dir = np.array([np.sign(direction_vector[0]), 0])
            else:
                push_dir = np.array([0, np.sign(direction_vector[1])])
            
            ideal_push_spot_coords = np.array(box) - push_dir
            
            spot_y, spot_x = int(ideal_push_spot_coords[0]), int(ideal_push_spot_coords[1])
            if not (0 <= spot_y < self.height and 0 <= spot_x < self.width) or self.map_data[spot_y][spot_x] == 'w':
                total_alignment_cost += 50 
            else:
                alignment_cost = np.sum(np.abs(player_pos - ideal_push_spot_coords))
                total_alignment_cost += alignment_cost

    distance_weight = 1.0
    alignment_weight = 0.3
    
    final_heuristic = (distance_weight * total_box_distance) + (alignment_weight * total_alignment_cost)
    return final_heuristic