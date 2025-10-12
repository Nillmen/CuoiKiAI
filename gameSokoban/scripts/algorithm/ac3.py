# ac3.py
import time
from collections import deque
from itertools import permutations, product

def ac3_algorithm(self):
    """Chạy AC-3, trả về domain dict hoặc False nếu phát hiện domain rỗng."""
    self.add_data()
    boxes = list(self.boxPos)
    goals = list(self.endPointPos)

    # init domain
    domain = {box: list(goals) for box in boxes}

    queue = deque([(xi, xj) for xi in boxes for xj in boxes if xi != xj])

    while queue:
        xi, xj = queue.popleft()
        revised = False
        new_domain = []

        for vi in domain[xi]:
            # kiểm tra hộp xi có thể tới vi (xem self.can_move_box_to)
            ok_i, _ = self.can_move_box_to(xi, vi, boxes)
            if not ok_i:
                # không thể tới vi => loại
                revised = True
                continue

            # tìm support cho vi trong domain[xj]
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
    """
    domain: dict {box_pos: [goal_pos,...]}
    Trả về list các solution dict:
      {
        'mapping': {box_pos: goal_pos, ...},
        'order': tuple(order_of_box_indices)  # thứ tự push chứng minh khả thi
      }
    """
    self.add_data()
    boxes = list(self.boxPos)
    solutions = []

    # product qua mọi lựa chọn goal cho từng hộp theo domain
    lists = [domain[box] for box in boxes]
    for goal_assignment in product(*lists):
        # đảm bảo không trùng goal
        if len(set(goal_assignment)) != len(boxes):
            continue

        # thử mọi thứ tự đẩy (permutation indices)
        for order in permutations(range(len(boxes))):
            cur_boxes = list(boxes)
            ok = True
            for box_idx in order:
                cur_box_pos = cur_boxes[box_idx]
                target_pos = goal_assignment[box_idx]
                if cur_box_pos == target_pos:
                    continue
                # other boxes (cập nhật)
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
    """
    Áp dụng tìm đường (BFS ưu tiên heuristic nhỏ) để kiểm tra feasibility thực tế
    và trả về danh sách vị trí player sẽ đi qua (list of (x,y)) nếu thành công,
    hoặc False nếu không.
    (Phiên bản nhẹ dùng các phương thức của self; tương tự find_path_for_solution bạn có)
    """
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

        # BFS-like with heuristic ordering (deque)
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

                # try push if player steps into box
                if new_player == bpos:
                    bx, by = bpos
                    push_x, push_y = bx + dx, by + dy
                    if self.is_free(push_x, push_y, new_boxes):
                        new_boxes[box_idx] = (push_x, push_y)
                        new_path = path + [new_player]
                        new_box_pos = (push_x, push_y)

                        if new_box_pos == goal_pos:
                            full_path.extend(new_path)
                            # after push player stands on the box's old cell (where he pushed from)
                            player_pos = new_player
                            current_boxes = [tuple(b) for b in new_boxes]
                            found = True
                            break

                        # else tiếp tục
                        state_key = (new_player, tuple(sorted(new_boxes)))
                        if state_key not in visited:
                            visited.add(state_key)
                            queue.append((new_player, new_box_pos, new_path, list(new_boxes)))
                else:
                    # normal walk
                    if self.is_free(new_px, new_py, new_boxes):
                        new_path = path + [new_player]
                        state_key = (new_player, tuple(sorted(new_boxes)))
                        if state_key not in visited:
                            visited.add(state_key)
                            queue.append((new_player, bpos, new_path, list(new_boxes)))

        if not found:
            return False
    return full_path


def run_ac3(self):
    """
    Entry point giống cấu trúc astar.run:
    - chạy AC-3,
    - lấy solutions,
    - sắp xếp theo cost,
    - kiểm tra từng solution với find_path,
    - quản lý step/time limit, observe, state_count, step_count,
    - trả về self.save_result(...)
    """
    state_count = 0
    step_count = 0
    best_path = []

    self.add_data()
    player_start = self.get_player_pos()

    start_time = time.perf_counter()

    # 1) AC-3
    domain = ac3_algorithm(self)
    if domain is False:
        return self.save_result(best_path, is_solution=False, state_count=state_count, step_count=step_count)

    # kiểm limit ngay cả sau AC-3
    if hasattr(self, "check_limit_condition") and self.check_limit_condition(step_count, time.perf_counter() - start_time):
        return self.save_result(best_path, is_solution=False, state_count=state_count, step_count=step_count)

    # 2) Lấy solutions khả thi từ domain
    solutions = get_all_valid_solutions_optimized(self, domain)
    state_count += 1  # AC-3 + sinh solution được coi là 1 trạng thái (tùy bạn adjust)

    if not solutions:
        return self.save_result(best_path, is_solution=False, state_count=state_count, step_count=step_count)

    # 3) Tính cost & sắp xếp
    for sol in solutions:
        sol['cost'] = self.calculate_solution_cost(sol, player_start)
    solutions.sort(key=lambda s: s['cost'])

    # 4) thử từng solution: tìm path thực tế player
    for sol in solutions:
        # kiểm limit trước khi thử mỗi solution
        if hasattr(self, "check_limit_condition") and self.check_limit_condition(step_count, time.perf_counter() - start_time):
            break

        self.observe(player_start[0], player_start[1], tuple(self.boxPos), depth=None, costG=None, costH=None, costF=sol['cost'])
        # tìm đường (hàm nội bộ nếu bạn chưa có)
        path = find_path_for_solution_local(self, player_start, sol)
        state_count += 1

        if path is not False:
            # convert full_path (list of player positions) thành dạng steps (player positions sequence)
            # ensure steps includes starting pos
            steps_positions = [player_start] + path if path and path[0] != player_start else [player_start] + path
            if len(steps_positions) > len(best_path):
                best_path = steps_positions

            # thành công -> trả về
            return self.save_result(steps_positions, is_solution=True, state_count=state_count, step_count=step_count)

        step_count += 1  # vừa thử một solution

    # nếu hết solutions mà chưa tìm được
    return self.save_result(best_path, is_solution=False, state_count=state_count, step_count=step_count)
