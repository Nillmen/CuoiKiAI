import time
from collections import deque

def input_infor(self):
    playerX, playerY = self.get_player_pos()
    self.ids_in_infor = {
        "pos_character_row" : {
            "type" : int,
            "value" : playerX
        },
        "pos_character_col" : {
            "type" : int,
            "value" : playerY
        } 
    }
    return self.ids_in_infor

def check_input_infor(self, key_value_list):
    """Kiểm tra tính hợp lệ của thông tin đầu vào (tương tự BFS/DFS)."""
    for key_value in key_value_list:
        for key, value in key_value.items():
            try:
                v = int(value)
            except:
                return False
    x_old = self.ids_in_infor["pos_character_row"]["value"]
    y_old = self.ids_in_infor["pos_character_col"]["value"]
    x_new = None
    y_new = None
    for key, value in key_value_list[0].items():
        x_new = int(value)
    for key, value in key_value_list[1].items():
        y_new = int(value)
    if (x_old, y_old) != (x_new, y_new):
        level = self.window.get_data("level")
        map_data = self.window.get_data("map_ori_list")[level]
        if x_new >= len(map_data) or y_new >= len(map_data[0]) or map_data[x_new][y_new] in "bwe":
            return False
    return True

def change_input_infor(self, key_value_list=None):
    playerX_new = int(self.ids_in_infor["pos_character_row"]["value"])
    playerY_new = int(self.ids_in_infor["pos_character_col"]["value"])
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
    start_time = time.perf_counter()

    self.add_data()
    playerX, playerY = self.get_player_pos()
    initial_steps = [(playerX, playerY)]
    initial_state = (playerX, playerY, tuple(self.boxPos))

    depth_limit = 0

    while not self.check_limit_condition(step_count, time.perf_counter() - start_time):

        stack = deque([(initial_state, initial_steps)])
        visited_this_iteration = {initial_state: 0}

        while stack:
            (current_playerX, current_playerY, boxes), steps = stack.pop()

            if self.check_limit_condition(step_count, time.perf_counter() - start_time):
                break

            state_count += 1
            current_depth = len(steps) - 1
            self.observe(current_playerX, current_playerY, boxes, steps, depth=current_depth, depth_limit=depth_limit)

            if len(steps) > len(best_path):
                best_path = steps.copy()

            if self.is_complete(boxes):
                return self.save_result(steps, is_solution=True,
                                        state_count=state_count,
                                        step_count=step_count)

            if current_depth >= depth_limit:
                continue

            for dx, dy in self.directions:
                newX, newY = current_playerX + dx, current_playerY + dy

                if self.player_is_blocked(current_playerX, current_playerY, newX, newY, boxes):
                    continue

                new_boxes = list(boxes)
                if (newX, newY) in boxes:
                    idx = boxes.index((newX, newY))
                    newBoxX, newBoxY = self.pushed_to_point(current_playerX, current_playerY, newX, newY)
                    new_boxes[idx] = (newBoxX, newBoxY)

                new_state = (newX, newY, tuple(sorted(new_boxes)))

                if new_state not in visited_this_iteration or visited_this_iteration[new_state] > current_depth + 1:
                    visited_this_iteration[new_state] = current_depth + 1
                    stack.append((new_state, steps + [(newX, newY)]))
                    step_count += 1

        depth_limit += 1

    return self.save_result(best_path, is_solution=False,
                            state_count=state_count,
                            step_count=step_count)