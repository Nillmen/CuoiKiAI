import time
from collections import deque
from itertools import permutations, product

def input_infor(self):
    playerX, playerY = self.get_player_pos()
    self.ac3_infor = {
        "pos_character_row": {"type": int, "value": playerX},
        "pos_character_col": {"type": int, "value": playerY}
    }
    return self.ac3_infor

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
    if not hasattr(self, 'and_or_infor'):
        input_infor(self)
    playerX_new = int(self.ac3_infor["pos_character_row"]["value"])
    playerY_new = int(self.ac3_infor["pos_character_col"]["value"])
    playerX_old, playerY_old = self.get_player_pos()
    if (playerX_new, playerY_new) != (playerX_old, playerY_old):
        self.map_data[playerX_new][playerY_new] = "c"
        if (playerY_old, playerX_old) in self.pos_endpoints:
            self.map_data[playerX_old][playerY_old] = "p"
        else:
            self.map_data[playerX_old][playerY_old] = "g"
    self.window.set_data("map_current", self.map_data)

def ac3_algorithm(self):
    self.add_data()
    boxes = list(self.boxPos)
    goals = list(self.endPointPos)

    domain = {box: list(goals) for box in boxes}

    queue = deque([(xi, xj) for xi in boxes for xj in boxes if xi != xj])

    while queue:
        xi, xj = queue.popleft()
        revised = False
        new_domain = []

        for vi in domain[xi]:
            ok_i, _ = self.can_move_box_to(xi, vi, boxes)
            if not ok_i:
                revised = True
                continue

            found_support = False
            for vj in domain[xj]:
                if vi == vj:
                    continue
                ok_j, _ = self.can_move_box_to(xj, vj, boxes)
                if ok_j:
                    found_support = True
                    break

            if found_support:
                new_domain.append(vi)
            else:
                revised = True

        if revised:
            domain[xi] = new_domain
            if not domain[xi]:
                return False
            for xk in boxes:
                if xk != xi and xk != xj:
                    queue.append((xk, xi))

    return domain


def get_all_valid_solutions_optimized(self, domain):
    self.add_data()
    boxes = list(self.boxPos)
    solutions = []

    lists = [domain[box] for box in boxes]
    for goal_assignment in product(*lists):
        if len(set(goal_assignment)) != len(boxes):
            continue

        for order in permutations(range(len(boxes))):
            cur_boxes = list(boxes)
            ok = True
            for box_idx in order:
                cur_box_pos = cur_boxes[box_idx]
                target_pos = goal_assignment[box_idx]
                if cur_box_pos == target_pos:
                    continue
                other_boxes = [b for i,b in enumerate(cur_boxes) if i != box_idx]
                success, _ = self.can_move_box_to(cur_box_pos, target_pos, other_boxes)
                if success:
                    cur_boxes[box_idx] = target_pos
                else:
                    ok = False
                    break
            if ok:
                solutions.append({
                    'mapping': {boxes[i]: goal_assignment[i] for i in range(len(boxes))},
                    'order': order
                })
    return solutions


def find_path_for_solution_local(self, player_start, solution):
    self.add_data()
    player_pos = tuple(player_start)
    boxes = list(self.boxPos)
    current_boxes = [tuple(b) for b in boxes]
    full_path = []

    for box_idx in solution['order']:
        box_key = boxes[box_idx]
        goal_pos = tuple(solution['mapping'][box_key])
        current_box_pos = current_boxes[box_idx]

        if current_box_pos == goal_pos:
            continue

        queue = deque([(player_pos, current_box_pos, [], list(current_boxes))])
        visited = set()
        visited.add((player_pos, tuple(current_boxes)))
        found = False

        while queue and not found:
            ppos, bpos, path, boxes_state = queue.popleft()
            for dx, dy in self.directions:
                new_px, new_py = ppos[0] + dx, ppos[1] + dy
                new_player = (new_px, new_py)
                new_boxes = list(boxes_state)

                if new_player == bpos:
                    bx, by = bpos
                    push_x, push_y = bx + dx, by + dy
                    if self.is_free(push_x, push_y, new_boxes):
                        new_boxes[box_idx] = (push_x, push_y)
                        new_path = path + [new_player]
                        new_box_pos = (push_x, push_y)

                        if new_box_pos == goal_pos:
                            full_path.extend(new_path)
                            player_pos = new_player
                            current_boxes = [tuple(b) for b in new_boxes]
                            found = True
                            break

                        state_key = (new_player, tuple(sorted(new_boxes)))
                        if state_key not in visited:
                            visited.add(state_key)
                            queue.append((new_player, new_box_pos, new_path, list(new_boxes)))
                else:
                    if self.is_free(new_px, new_py, new_boxes):
                        new_path = path + [new_player]
                        state_key = (new_player, tuple(sorted(new_boxes)))
                        if state_key not in visited:
                            visited.add(state_key)
                            queue.append((new_player, bpos, new_path, list(new_boxes)))

        if not found:
            return False
    return full_path


def run(self):

    state_count = 0
    step_count = 0
    best_path = []

    self.add_data()
    player_start = self.get_player_pos()

    start_time = time.perf_counter()

    domain = ac3_algorithm(self)
    if domain is False:
        return self.save_result(best_path, is_solution=False, state_count=state_count, step_count=step_count)

    if hasattr(self, "check_limit_condition") and self.check_limit_condition(step_count, time.perf_counter() - start_time):
        return self.save_result(best_path, is_solution=False, state_count=state_count, step_count=step_count)

    solutions = get_all_valid_solutions_optimized(self, domain)
    state_count += 1 

    if not solutions:
        return self.save_result(best_path, is_solution=False, state_count=state_count, step_count=step_count)


    for sol in solutions:
        sol['cost'] = self.calculate_solution_cost(sol, player_start)
    solutions.sort(key=lambda s: s['cost'])

    for sol in solutions:
        if hasattr(self, "check_limit_condition") and self.check_limit_condition(step_count, time.perf_counter() - start_time):
            break

        self.observe(player_start[0], player_start[1], tuple(self.boxPos), depth=None, costG=None, costH=None, costF=sol['cost'])
        path = find_path_for_solution_local(self, player_start, sol)
        state_count += 1

        if path is not False:
            steps_positions = [player_start] + path if path and path[0] != player_start else [player_start] + path
            if len(steps_positions) > len(best_path):
                best_path = steps_positions

            return self.save_result(steps_positions, is_solution=True, state_count=state_count, step_count=step_count)

        step_count += 1

    return self.save_result(best_path, is_solution=False, state_count=state_count, step_count=step_count)