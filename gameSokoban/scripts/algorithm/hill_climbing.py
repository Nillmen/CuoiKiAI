import time
def run(self, max_steps=200):
    """Thuật toán Hill Climbing với kiểm soát thời gian và số bước."""
    import time

    state_count = 0
    step_count = 0
    steps = []

    self.add_data()
    playerX, playerY = self.get_player_pos()
    boxes = tuple(sorted(self.boxPos))
    steps.append((playerX, playerY))

    start_time = time.perf_counter()  # bắt đầu tính thời gian

    for _ in range(max_steps):
        # ✅ Kiểm tra giới hạn thời gian và số bước
        if self.check_limit_condition(step_count, time.perf_counter() - start_time):
            break

        state_count += 1
        self.observe(playerX, playerY, boxes, steps, costH=self.h(boxes))

        if self.is_complete(boxes):
            return self.save_result(
                steps,
                is_solution=True,
                state_count=state_count,
                step_count=step_count
            )

        neighbors = self.get_neighbors(playerX, playerY, boxes)
        if not neighbors:
            break

        best_neighbor = min(neighbors, key=lambda n: self.h(n[2]))

        if self.h(best_neighbor[2]) < self.h(boxes):
            playerX, playerY, boxes = best_neighbor
            steps.append((playerX, playerY))
            step_count += 1
        else:
            break  # không cải thiện → dừng

    return self.save_result(
        steps,
        is_solution=False,
        state_count=state_count,
        step_count=step_count
    )
