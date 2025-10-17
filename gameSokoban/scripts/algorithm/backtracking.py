import time

def input_infor(self):
    playerX, playerY = self.get_player_pos()
    self.backtrack_in_infor = {
        "pos_character_row": {"type": int, "value": playerX},
        "pos_character_col": {"type": int, "value": playerY}
    }
    return self.backtrack_in_infor

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
    playerX_new = int(self.backtrack_in_infor["pos_character_row"]["value"])
    playerY_new = int(self.backtrack_in_infor["pos_character_col"]["value"])
    playerX_old, playerY_old = self.get_player_pos()

    if (playerX_new, playerY_new) != (playerX_old, playerY_old):
        self.map_data[playerX_new][playerY_new] = "c"
        if (playerY_old, playerX_old) in self.pos_endpoints:
            self.map_data[playerX_old][playerY_old] = "p"
        else:
            self.map_data[playerX_old][playerY_old] = "g"
    self.window.set_data("map_current", self.map_data)

max_limit = 0

def run(self):
    self.add_data()
    playerX, playerY = self.get_player_pos()
    
    initial_state = (playerX, playerY, tuple(self.boxPos))
    initial_path = [(playerX, playerY)]
    visited = {initial_state}
    best_path = [] 
    start_time = time.perf_counter()

    result_path, final_state_count = backtrack_search(
        self, initial_state, initial_path, visited, 0, start_time, best_path
    )

    if result_path:
        final_step_count = len(result_path) - 1
        return self.save_result(result_path, is_solution=True,
                                state_count=final_state_count,
                                step_count=final_step_count)
    else:
        final_step_count = len(best_path) - 1 if best_path else 0
        return self.save_result(best_path, is_solution=False,
                                state_count=final_state_count,
                                step_count=final_step_count)

def backtrack_search(self, current_state, current_path, visited, state_count, start_time, best_path):

    playerX, playerY, boxes = current_state
    state_count += 1

    self.observe(playerX, playerY, boxes,steps=current_path, depth=len(current_path) - 1)

    if len(current_path) > len(best_path):
        best_path[:] = current_path

    if self.is_complete(boxes):
        return current_path, state_count

    step_count = len(current_path) - 1
    if self.check_limit_condition(step_count, time.perf_counter() - start_time):
        return None, state_count

    for dx, dy in self.directions:
        newX, newY = playerX + dx, playerY + dy

        if not self.player_is_blocked(playerX, playerY, newX, newY, boxes):
            new_boxes = list(boxes)
            if (newX, newY) in boxes:
                idx = boxes.index((newX, newY))
                newBoxX, newBoxY = self.pushed_to_point(playerX, playerY, newX, newY)
                new_boxes[idx] = (newBoxX, newBoxY)

            new_state = (newX, newY, tuple(sorted(new_boxes)))

            if new_state not in visited:
                visited.add(new_state)
                
                result_path, updated_state_count = backtrack_search(
                    self, new_state, current_path + [(newX, newY)], visited, state_count, start_time, best_path
                )
                
                state_count = updated_state_count
                
                if result_path:
                    return result_path, state_count
    return None, state_count