# Nguon: Tham khao tu AI

import time
import heapq

def run(self):
    state_count = 0     # Dem tong trang thai da duyet
    step_count = 0      # # Dem tong so buoc da duyet
    best_path = []      # Luu duong di tot nhat

    self.add_data()
    playerX, playerY = self.get_player_pos()
    steps = [(playerX, playerY)]

    initial_state = (playerX, playerY, tuple(self.boxPos))

    # # Dung Manhattan (L₁ distance) giua hai diem (x₁, y₁) và (x₂, y₂), cong thuc: d=∣x1​−x2​∣+∣y1​−y2​∣
    def manhattan(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])      

    # Heuristic: Tong khoang cach nho nhat tu hop den dich
    def heuristic(state):
        _, _, boxes = state
        total = 0
        for bx, by in boxes:
            best = min(manhattan((bx, by), g) for g in self.endPointPos) if self.endPointPos else 0
            total += best
        return total

    open_list = []  # (h, tie, state, steps)
    tie_counter = 0
    heapq.heappush(open_list, (heuristic(initial_state), tie_counter, initial_state, steps))
    visited = set([initial_state])

    start_time = time.perf_counter()

    while open_list:
        _, _, (playerX, playerY, boxes), steps = heapq.heappop(open_list)

        if self.check_limit_condition(step_count, time.perf_counter() - start_time):
            break

        state_count += 1

        self.observe(playerX, playerY, boxes, steps, costH=heuristic((playerX, playerY, boxes)))

        if len(steps) > len(best_path):
            best_path = steps

        # Neu hop da duoc day vao dung vi tri -> luu ket qua va ket thuc
        if self.is_complete(boxes):
            return self.save_result(steps, is_solution=True,
                                    state_count=state_count,
                                    step_count=step_count)

        # Neu nguoi choi bi chan -> bo qua
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
                heapq.heappush(open_list, (heuristic(new_state), tie_counter, new_state, steps + [(newX, newY)]))
                step_count += 1

    return self.save_result(best_path, is_solution=False,
                            state_count=state_count,
                            step_count=step_count)


