import time
from collections import deque

def input_infor(self):
    playerX, playerY = self.get_player_pos()
    self.bfs_in_infor = {
        "pos_character_row" : {
            "type" : int,
            "value" : playerX
        },
        "pos_character_col" : {
            "type" : int,
            "value" : playerY
        } 
    }
    return self.bfs_in_infor

def check_input_infor(self, key_value_list):
    for key_value in key_value_list:
        for key, value in key_value.items():
            try:
                v = int(value)
            except:
                return False
    x_old = self.bfs_in_infor["pos_character_row"]["value"]
    y_old = self.bfs_in_infor["pos_character_col"]["value"]
    x_new = None
    y_new = None
    for key, value in key_value_list[0].items():
        x_new = int(value)
    for key, value in key_value_list[1].items():
        y_new = int(value)
    if (x_old, y_old) != (x_new, y_new):
        level = self.window.get_data("level")
        map_data = self.window.get_data("map_ori_list")[level]
        if x_new >= len(map_data) or y_new >= len(map_data[0]) or map_data[x_new][y_new] == "b" or map_data[x_new][y_new] == "w":
            return False
    return True

def change_input_infor(self):
    playerX_new = int(self.bfs_in_infor["pos_character_row"]["value"])
    playerY_new = int(self.bfs_in_infor["pos_character_col"]["value"])

    print("new", type(self.bfs_in_infor["pos_character_row"]["value"]), type(self.bfs_in_infor["pos_character_col"]["value"]), playerX_new, playerY_new)

    playerX_old, playerY_old = self.get_player_pos()

    print("old", playerX_old, playerY_old)
    if (playerX_new, playerY_new) != (playerX_old, playerY_old):
        self.map_data[playerX_new][playerY_new] = "c"
        self.map_data[playerX_old][playerY_old] = "g"
    print("change", self.map_data)
    self.window.set_data("map_current", self.map_data)

def run(self):
    state_count = 0
    step_count = 0
    best_path = [] 

    self.add_data()
    print("chạy bfs", self.map_data)
    playerX, playerY = self.get_player_pos()
    steps = [(playerX, playerY)]

    initial_state = (playerX, playerY, tuple(self.boxPos))
    queue = deque([(initial_state, steps)])
    visited = set([initial_state])

    start_time = time.perf_counter()

    while queue:
        (playerX, playerY, boxes), steps = queue.popleft()

        if self.check_limit_condition(step_count, time.perf_counter() - start_time):
            break

        state_count += 1  

        self.observe(playerX, playerY, boxes, steps)

        if len(steps) > len(best_path):
            best_path = steps

        if self.is_complete(boxes):
            return self.save_result(steps, is_solution=True,
                                    state_count=state_count,
                                    step_count=step_count)

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

    return self.save_result(best_path, is_solution=False,
                            state_count=state_count,
                            step_count=step_count)