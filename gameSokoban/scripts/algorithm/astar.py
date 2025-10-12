import time
from heapq import heappush, heappop
def run(self):
    state_count = 0
    step_count = 0
    best_path = []  # lưu đường đi tốt nhất đã tìm được

    self.add_data()
    playerX, playerY = self.get_player_pos()
    steps = [(playerX, playerY)]

    initial_state = (playerX, playerY, tuple(self.boxPos))
    g_cost = self.g((playerX, playerY), self.boxPos)
    h_cost = self.h(self.boxPos)
    f_cost = g_cost + h_cost

    queue = []
    heappush(queue, (f_cost, g_cost, initial_state, steps))
    visited = {initial_state: g_cost}

    start_time = time.perf_counter()  # để kiểm soát max_time nếu muốn

    while queue:
        f_cost, g_cost, (playerX, playerY, boxes), steps = heappop(queue)
        state_count += 1

        # kiểm tra giới hạn max_step và max_time
        if hasattr(self, "check_limit_condition") and self.check_limit_condition(step_count, time.perf_counter() - start_time):
            break

        self.observe(playerX, playerY, boxes, steps, costF=f_cost, costG=g_cost, costH=self.h(boxes))

        if len(steps) > len(best_path):
            best_path = steps

        if self.is_complete(boxes):
            return self.save_result(steps,
                                    is_solution=True,
                                    state_count=state_count,
                                    step_count=step_count)

        for dx, dy in self.directions:
            newX = playerX + dx
            newY = playerY + dy

            if self.player_is_blocked(playerX, playerY, newX, newY, boxes):
                continue

            new_boxes = list(boxes)
            if (newX, newY) in boxes:
                idx = boxes.index((newX, newY))
                newBoxX, newBoxY = self.pushed_to_point(playerX, playerY, newX, newY)
                new_boxes[idx] = (newBoxX, newBoxY)

            new_state = (newX, newY, tuple(sorted(new_boxes)))
            new_g = g_cost + self.g((newX, newY), new_boxes)
            new_h = self.h(new_boxes)
            new_f = new_g + new_h

            if new_state not in visited or new_g < visited[new_state]:
                visited[new_state] = new_g
                heappush(queue, (new_f, new_g, new_state, steps + [(newX, newY)]))
                step_count += 1

    return self.save_result(best_path,
                            is_solution=False,
                            state_count=state_count,
                            step_count=step_count)
