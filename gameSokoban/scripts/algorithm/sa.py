import time

def run(self, max_steps=1000):
    """Thuật toán Simulated Annealing (có kiểm soát thời gian)."""
    import math, random, time

    initial_temp = 100.0
    cooling_rate = 0.99
    min_temp = 0.1

    state_count = 0
    step_count = 0
    steps = []

    self.add_data()
    cur_heat = initial_temp
    start_time = time.perf_counter()  # bắt đầu tính thời gian

    playerX, playerY = self.get_player_pos()
    boxes = tuple(sorted(self.boxPos))
    steps.append((playerX, playerY))

    while cur_heat > min_temp and step_count < max_steps:
        # ✅ Kiểm tra giới hạn thời gian
        if self.check_limit_condition(step_count, time.perf_counter() - start_time):
            break

        state_count += 1
        self.observe(playerX, playerY, boxes, steps, costH=self.h(boxes), heat=cur_heat)

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

        neighbor = random.choice(neighbors)
        new_cost = self.h(neighbor[2])
        cur_cost = self.h(boxes)

        if new_cost < cur_cost:
            playerX, playerY, boxes = neighbor
            steps.append((playerX, playerY))
            step_count += 1
        else:
            deltaE = new_cost - cur_cost
            p = math.exp(-deltaE / cur_heat)
            if random.random() < p:
                playerX, playerY, boxes = neighbor
                steps.append((playerX, playerY))
                step_count += 1

        cur_heat *= cooling_rate  # làm nguội

    # Không tìm thấy lời giải → trả về best path hiện tại
    return self.save_result(
        steps,
        is_solution=False,
        state_count=state_count,
        step_count=step_count
    )
