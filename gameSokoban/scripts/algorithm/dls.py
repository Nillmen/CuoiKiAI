import time


def run(self, playerX=None, playerY=None, boxes=None, steps=None, visited=None,
        limit=50, original_limit=50, state_count_ref=None, best_path_ref=None, step_count=0, start_time=None):

    is_root_call = playerX is None
    if is_root_call:
        self.add_data()
        playerX, playerY = self.get_player_pos()
        boxes = tuple(self.boxPos)
        steps = [(playerX, playerY)]
        visited = set([(playerX, playerY, boxes)])
        state_count_ref = [0]
        best_path_ref = [steps]
        self.observed_states.clear()
        start_time = time.perf_counter()

    # ✅ Dừng nếu vượt quá giới hạn thời gian / bước
    if self.check_limit_condition(step_count, time.perf_counter() - start_time):
        return None, None

    # ✅ Nếu hoàn thành
    if self.is_complete(boxes):
        return self.save_result(steps, True, state_count_ref[0], step_count)

    # ✅ Nếu đạt giới hạn độ sâu
    if limit <= 0:
        if len(steps) > len(best_path_ref[0]):
            best_path_ref[0] = steps
        return None, None

    result = None

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
            state_count_ref[0] += 1
            step_count += 1

            current_depth = original_limit - limit + 1
            self.observe(newX, newY, new_boxes, depth=current_depth)

            result, details = run(self,
                newX, newY, tuple(new_boxes),
                steps + [(newX, newY)], visited,
                limit - 1, original_limit,
                state_count_ref, best_path_ref, step_count, start_time
            )

            if result:
                return result, details

    if len(steps) > len(best_path_ref[0]):
        best_path_ref[0] = steps

    if is_root_call and result is None:
        best_path = best_path_ref[0]
        return self.save_result(best_path, False, state_count_ref[0], step_count)

    return None, None
