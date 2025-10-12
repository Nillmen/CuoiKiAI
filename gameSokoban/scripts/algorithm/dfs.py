import time

def run(self):
    state_count = 0
    step_count = 0
    best_path = []

    self.add_data()
    playerX, playerY = self.get_player_pos()
    steps = [(playerX, playerY)]

    initial_state = (playerX, playerY, tuple(self.boxPos))
    stack = [(initial_state, steps)]
    visited = set([initial_state])

    start_time = time.perf_counter()

    while stack:
        (playerX, playerY, boxes), steps = stack.pop()

        if self.check_limit_condition(step_count, time.perf_counter() - start_time):
            break

        state_count += 1
        self.observe(playerX, playerY, boxes, steps)

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

            new_boxes = list(boxes)
            if (newX, newY) in boxes:
                idx = boxes.index((newX, newY))
                newBoxX, newBoxY = self.pushed_to_point(playerX, playerY, newX, newY)
                new_boxes[idx] = (newBoxX, newBoxY)

            new_state = (newX, newY, tuple(sorted(new_boxes)))
            if new_state not in visited:
                visited.add(new_state)
                stack.append((new_state, steps + [(newX, newY)]))
                step_count += 1

    return self.save_result(best_path,
                            is_solution=False,
                            state_count=state_count,
                            step_count=step_count)
