import time
import random

def input_infor(self):
    playerX, playerY = self.get_player_pos()
    self.po_in_infor = {
        "pos_character_row": {"type": int, "value": playerX},
        "pos_character_col": {"type": int, "value": playerY}
    }
    return self.po_in_infor

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
    playerX_new = int(self.po_in_infor["pos_character_row"]["value"])
    playerY_new = int(self.po_in_infor["pos_character_col"]["value"])
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
    best_path = []       

    self.add_data()
    playerX, playerY = self.get_player_pos()
    steps = [(playerX, playerY)]

    initial_state = (playerX, playerY, tuple(self.boxPos))
    initial_priority = calculate_priority(self, playerX, playerY, self.boxPos)
    stack = [(initial_priority, initial_state, steps)]
    visited = set([initial_state])

    start_time = time.perf_counter()

    while stack:

        stack.sort(key=lambda x: x[0], reverse=True)
        priority, (playerX, playerY, boxes), steps = stack.pop() 

        if self.check_limit_condition(step_count, time.perf_counter() - start_time):
            break

        state_count += 1

        self.observe(playerX, playerY, boxes, steps=steps, depth=len(steps)-1, len_queue=len(stack))

        if len(steps) > len(best_path):
            best_path = steps

        if self.is_complete(boxes):
            return self.save_result(steps, is_solution=True,
                                    state_count=state_count,
                                    step_count=step_count)


        directions = self.directions.copy()
        

        if random.random() < 0.2: 
            directions = random.sample(directions, max(2, len(directions) * 3 // 4))  
        
        for dx, dy in directions:
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
                priority = calculate_priority(self, newX, newY, new_boxes)
                stack.append((priority, new_state, steps + [(newX, newY)]))
                step_count += 1

    return self.save_result(best_path, is_solution=False,
                            state_count=state_count,
                            step_count=step_count)

def calculate_priority(self, playerX, playerY, boxes):
    priority = 0
    
    min_player_dist = float('inf')
    for goal in self.endPointPos:
        distance = abs(playerX - goal[0]) + abs(playerY - goal[1])
        if distance < min_player_dist:
            min_player_dist = distance
    priority -= min_player_dist 

    total_box_dist = 0
    for box in boxes:
        if box not in self.endPointPos:
            min_dist_for_box = min([abs(box[0] - goal[0]) + abs(box[1] - goal[1]) for goal in self.endPointPos])
            total_box_dist += min_dist_for_box
    priority -= total_box_dist * 2 
    

    boxes_on_goals = sum(1 for box in boxes if box in self.endPointPos)
    priority += boxes_on_goals * 1000 
    

    priority += random.uniform(-0.1, 0.1) 
    
    return priority