import time

def input_infor(self):
    playerX, playerY = self.get_player_pos()
    self.beam_in_infor = {
        "pos_character_row": {"type": int, "value": playerX},
        "pos_character_col": {"type": int, "value": playerY},
        "beam_width": {"type": int, "value": 10} 
    }
    return self.beam_in_infor


def check_input_infor(self, key_value_list):
    try:
        x_new = int(list(key_value_list[0].values())[0])
        y_new = int(list(key_value_list[1].values())[0])
        beam_width = int(list(key_value_list[2].values())[0])
    except:
        return False


    level = self.window.get_data("level")
    map_data = self.window.get_data("map_ori_list")[level]
    if (x_new >= len(map_data)
        or y_new >= len(map_data[0])
        or map_data[x_new][y_new] in "bwe"):
        return False


    if beam_width <= 0:
        return False

    return True


def change_input_infor(self, key_value_list=None):
    playerX_new = int(self.beam_in_infor["pos_character_row"]["value"])
    playerY_new = int(self.beam_in_infor["pos_character_col"]["value"])
    playerX_old, playerY_old = self.get_player_pos()

    if (playerX_new, playerY_new) != (playerX_old, playerY_old):
        self.map_data[playerX_new][playerY_new] = "c"
        if (playerY_old, playerX_old) in self.pos_endpoints:
            self.map_data[playerX_old][playerY_old] = "p"
        else:
            self.map_data[playerX_old][playerY_old] = "g"
    if key_value_list and len(key_value_list) > 0:
        beam_width = int(list(key_value_list[2].values())[0])
        self.window.set_data("beam_width", beam_width)
    self.window.set_data("map_current", self.map_data)


def run(self):
    state_count = 0
    step_count = 0
    best_path = []

    beam_width = self.window.get_data("beam_width")
    if beam_width is None:
        beam_width = 10

    self.add_data()
    playerX, playerY = self.get_player_pos()
    steps = [(playerX, playerY)]
    initial_state = (playerX, playerY, tuple(self.boxPos))

    def manhattan(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def heuristic(state):
        _, _, boxes = state
        total = 0
        for bx, by in boxes:
            if not self.endPointPos:
                continue
            total += min(manhattan((bx, by), g) for g in self.endPointPos)
        return total

    current_beam = [(heuristic(initial_state), 0, initial_state, steps)]
    visited = set([initial_state])
    start_time = time.perf_counter()

    while current_beam:
        current_beam.sort(key=lambda x: (x[0], x[1]))
        current_beam = current_beam[:beam_width]

        next_beam = []
        tie_counter = 0

        for _, _, (playerX, playerY, boxes), steps in current_beam:
            if self.check_limit_condition(step_count, time.perf_counter() - start_time):
                break

            state_count += 1
            self.observe(playerX, playerY, boxes, len(current_beam), steps, costH=heuristic((playerX, playerY, boxes)))

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
                    tie_counter += 1
                    h_value = heuristic(new_state)
                    next_beam.append((h_value, tie_counter, new_state, steps + [(newX, newY)]))
                    step_count += 1

        current_beam = next_beam

    return self.save_result(best_path, is_solution=False,
                            state_count=state_count,
                            step_count=step_count)