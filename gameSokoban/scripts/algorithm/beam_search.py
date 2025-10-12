import heapq
from heapq import heappush, heappop
import time

def run(self, beam_width=10, max_depth=500):
    state_count = 0
    step_count = 0
    best_path = []

    self.add_data()
    playerX, playerY = self.get_player_pos()
    steps = [(playerX, playerY)]

    initial_state = (playerX, playerY, tuple(sorted(self.boxPos)))
    initial_cost = self.h(self.boxPos)

    queue = [(initial_cost, initial_state, steps)]
    visited = {initial_state: initial_cost}
    depth = 0
    start_time = time.perf_counter()  # bắt đầu đo thời gian

    while queue and depth < max_depth:
        depth += 1
        new_queue = []

        for cost, (playerX, playerY, boxes), steps in queue:
            # ✅ Dừng nếu vượt quá thời gian hoặc số bước
            if self.check_limit_condition(step_count, time.perf_counter() - start_time):
                return self.save_result(best_path,
                                        is_solution=False,
                                        state_count=state_count,
                                        step_count=step_count)

            state_count += 1
            self.observe(playerX, playerY, boxes, steps, depth=depth, costH=cost)

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
                new_cost = self.h(new_boxes)

                if new_state not in visited or new_cost < visited[new_state]:
                    visited[new_state] = new_cost
                    heappush(new_queue, (new_cost, new_state, steps + [(newX, newY)]))
                    step_count += 1

        queue = []
        for _ in range(min(beam_width, len(new_queue))):
            queue.append(heappop(new_queue))

    return self.save_result(best_path,
                            is_solution=False,
                            state_count=state_count,
                            step_count=step_count)
