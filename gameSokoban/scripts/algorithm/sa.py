import time
import random
import math
import numpy as np

def input_infor(self):
    """Lấy thông tin đầu vào, bao gồm các tham số cho Simulated Annealing."""
    playerX, playerY = self.get_player_pos()
    self.sa_in_infor = {
        "pos_character_row": {"type": int, "value": playerX},
        "pos_character_col": {"type": int, "value": playerY},
        "initial_temperature": {"type": float, "value": 1000.0},
        "cooling_rate": {"type": float, "value": 0.995}
    }
    return self.sa_in_infor

def check_input_infor(self, key_value_list):
    """Kiểm tra tính hợp lệ của thông tin đầu vào."""
    try:
        x_new = int(list(key_value_list[0].values())[0])
        y_new = int(list(key_value_list[1].values())[0])
        temp = float(list(key_value_list[2].values())[0])
        rate = float(list(key_value_list[3].values())[0])
    except (ValueError, IndexError):
        return False
        
    if temp <= 0 or not (0 < rate < 1):
        return False
        
    level = self.window.get_data("level")
    map_data = self.window.get_data("map_ori_list")[level]
    if not (0 <= x_new < len(map_data) and 0 <= y_new < len(map_data[0])):
        return False
    if map_data[x_new][y_new] in "bwe":
        return False
    return True

def change_input_infor(self, key_value_list=None):
    """Cập nhật bản đồ và các tham số của thuật toán."""
    if not hasattr(self, 'sa_in_infor'):
        input_infor(self)
        
    playerX_new = int(self.sa_in_infor["pos_character_row"]["value"])
    playerY_new = int(self.sa_in_infor["pos_character_col"]["value"])
    playerX_old, playerY_old = self.get_player_pos()
    if (playerX_new, playerY_new) != (playerX_old, playerY_old):
        self.map_data[playerX_new][playerY_new] = "c"
        self.map_data[playerX_old][playerY_old] = "g"
    self.window.set_data("map_current", self.map_data)
        
    if key_value_list and len(key_value_list) > 3:
        initial_temperature = float(list(key_value_list[2].values())[0])
        cooling_rate = float(list(key_value_list[3].values())[0])
        self.window.set_data("initial_temperature", initial_temperature)
        self.window.set_data("cooling_rate", cooling_rate)

def is_deadlock(self, box):
    x, y = box
    if (self.map_data[x][y] == 'w') or (box in self.endPointPos):
        return False
    up_wall = (x > 0 and self.map_data[x-1][y] == 'w')
    down_wall = (x < self.height-1 and self.map_data[x+1][y] == 'w')
    left_wall = (y > 0 and self.map_data[x][y-1] == 'w')
    right_wall = (y < self.width-1 and self.map_data[x][y+1] == 'w')
    if (up_wall and left_wall) or (up_wall and right_wall) or (down_wall and left_wall) or (down_wall and right_wall):
        return True
    return False

def run(self):

    state_count = 0
    step_count = 0
    self.add_data()
    
    temperature = self.window.get_data("initial_temperature")
    if temperature is None:
        temperature = 1000.0
    cooling_rate = self.window.get_data("cooling_rate")
    if cooling_rate is None:
        cooling_rate = 0.995
    
    playerX, playerY = self.get_player_pos()
    current_state = (playerX, playerY, tuple(self.boxPos))
    current_path = [(playerX, playerY)]
    current_cost = calculate_heuristic(self, current_state[0], current_state[1], current_state[2])
    
    best_state = current_state
    best_path = current_path
    best_cost = current_cost
    
    start_time = time.perf_counter()

    while temperature > 0.1:
        state_count += 1
        self.observe(current_state[0], current_state[1], current_state[2], steps=current_path, costH=current_cost, depth=len(current_path)-1, heat=temperature)
        
        if self.is_complete(current_state[2]):
            return self.save_result(current_path, is_solution=True, state_count=state_count, step_count=step_count)

        if self.check_limit_condition(step_count, time.perf_counter() - start_time):
            break


        (c_playerX, c_playerY, c_boxes) = current_state
        
        valid_neighbors = []
        for dx, dy in self.directions:
            newX, newY = c_playerX + dx, c_playerY + dy
            if not self.player_is_blocked(c_playerX, c_playerY, newX, newY, c_boxes):
                new_boxes = list(c_boxes)
                if (newX, newY) in c_boxes:
                    idx = c_boxes.index((newX, newY))
                    newBoxX, newBoxY = self.pushed_to_point(c_playerX, c_playerY, newX, newY)
                    new_boxes[idx] = (newBoxX, newBoxY)
                
                neighbor_state = (newX, newY, tuple(sorted(new_boxes)))
                neighbor_path = current_path + [(newX, newY)]
                valid_neighbors.append((neighbor_state, neighbor_path))
        
        if not valid_neighbors:
            temperature *= cooling_rate
            continue

        neighbor_state, neighbor_path = random.choice(valid_neighbors)
        neighbor_cost = calculate_heuristic(self, neighbor_state[0], neighbor_state[1], neighbor_state[2])

        cost_diff = neighbor_cost - current_cost

        if cost_diff < 0:
            current_state = neighbor_state
            current_path = neighbor_path
            current_cost = neighbor_cost
        else:
            acceptance_probability = math.exp(-cost_diff / temperature)
            if random.random() < acceptance_probability:
                current_state = neighbor_state
                current_path = neighbor_path
                current_cost = neighbor_cost
        
        if current_cost < best_cost:
            best_state = current_state
            best_path = current_path
            best_cost = current_cost
        
        step_count += 1
        temperature *= cooling_rate
            
    return self.save_result(best_path, is_solution=is_goal_state(self, best_state), state_count=state_count, step_count=step_count)

def calculate_heuristic(self, playerX, playerY, boxes):
    unassigned_boxes = list(boxes)
    unassigned_goals = list(self.endPointPos)
    box_goal_assignment = {}
    total_box_distance = 0

    while unassigned_boxes:
        best_dist = float('inf')
        best_box, best_goal = None, None
        for box in unassigned_boxes:
            for goal in unassigned_goals:
                dist = abs(box[0] - goal[0]) + abs(box[1] - goal[1])
                if dist < best_dist:
                    best_dist, best_box, best_goal = dist, box, goal
        
        if best_box is not None:
            total_box_distance += best_dist
            box_goal_assignment[best_box] = best_goal
            unassigned_boxes.remove(best_box)
            unassigned_goals.remove(best_goal)
        else: break

    total_alignment_cost = 0
    player_pos = np.array([playerX, playerY])

    for box, assigned_goal in box_goal_assignment.items():
        direction_vector = np.array([assigned_goal[0] - box[0], assigned_goal[1] - box[1]])
        if np.any(direction_vector):
            push_dir = np.array([np.sign(direction_vector[0]), 0]) if abs(direction_vector[0]) > abs(direction_vector[1]) else np.array([0, np.sign(direction_vector[1])])
            ideal_push_spot_coords = np.array(box) - push_dir
            spot_y, spot_x = int(ideal_push_spot_coords[0]), int(ideal_push_spot_coords[1])
            if is_deadlock(self, box):
                total_box_distance += 1000 
            if not (0 <= spot_y < self.height and 0 <= spot_x < self.width) or self.map_data[spot_y][spot_x] == 'w':
                total_alignment_cost += 50
            else:
                total_alignment_cost += np.sum(np.abs(player_pos - ideal_push_spot_coords))
    boxes_on_goal = sum(1 for b in boxes if b in self.endPointPos)
    reward = -10 * boxes_on_goal
    return (1.0 * total_box_distance) + (0.7 * total_alignment_cost) + reward

def is_goal_state(self, state):
    return all(box in self.endPointPos for box in state[2])