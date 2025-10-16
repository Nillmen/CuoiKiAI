import time
from heapq import heappush, heappop

def input_infor(self):

    playerX, playerY = self.get_player_pos()

    self.ucs_in_infor = {
        "pos_character_row": {"type": int, "value": playerX},
        "pos_character_col": {"type": int, "value": playerY}
    }
    return self.ucs_in_infor

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

    playerX_new = int(self.ucs_in_infor["pos_character_row"]["value"])
    playerY_new = int(self.ucs_in_infor["pos_character_col"]["value"])
    playerX_old, playerY_old = self.get_player_pos()

    if (playerX_new, playerY_new) != (playerX_old, playerY_old):
        self.map_data[playerX_new][playerY_new] = "c" 
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

    initial_cost = 1

    queue = []
    heappush(queue, (initial_cost, initial_state, steps))  
    visited = {initial_state: initial_cost}

    start_time = time.perf_counter()

    while queue:
        if self.check_limit_condition(step_count, time.perf_counter() - start_time):
            break

        total_cost, (playerX, playerY, boxes), steps = heappop(queue)
        state_count += 1
        self.observe(playerX, playerY, boxes, steps=steps, costG=total_cost, len_queue=len(queue))

        if len(steps) > len(best_path):
            best_path = steps

        if self.is_complete(boxes):
            return self.save_result(steps,
                                    is_solution=True,
                                    state_count=state_count,
                                    step_count=step_count)

        for dx, dy in self.directions:
            newX, newY = playerX + dx, playerY + dy
            if self.player_is_blocked(playerX, playerY, newX, newY, boxes):
                continue

            cost_of_step = 1
            new_boxes = list(boxes)
            if (newX, newY) in boxes:
                idx = boxes.index((newX, newY))
                newBoxX, newBoxY = self.pushed_to_point(playerX, playerY, newX, newY)
                new_boxes[idx] = (newBoxX, newBoxY)
                cost_of_step = 2 

            new_state = (newX, newY, tuple(sorted(new_boxes)))
            new_cost = total_cost + cost_of_step

            if new_state not in visited or new_cost < visited[new_state]:
                visited[new_state] = new_cost
                new_path = steps + [(newX, newY)]
                heappush(queue, (new_cost, new_state, new_path))
                step_count += 1

    return self.save_result(best_path,
                            is_solution=False,
                            state_count=state_count,
                            step_count=step_count)