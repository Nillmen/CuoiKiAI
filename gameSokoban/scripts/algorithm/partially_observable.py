# Nguon: Tham khao tu AI

import time
import random

def run(self):
    state_count = 0     # Dem tong trang thai da duyet
    step_count = 0      # Dem tong so buoc da duyet
    best_path = []      # Luu duong di tot nhat

    self.add_data()
    playerX, playerY = self.get_player_pos()
    steps = [(playerX, playerY)]

    initial_state = (playerX, playerY, tuple(self.boxPos))
    initial_priority = calculate_priority(self, playerX, playerY, self.boxPos)
    stack = [(initial_priority, initial_state, steps)]
    visited = set([initial_state])

    start_time = time.perf_counter()

    while stack:
        # Sap xep stack theo priority truoc khi pop
        stack.sort(key=lambda x: x[0], reverse=True)
        priority, (playerX, playerY, boxes), steps = stack.pop() # Lay phan tu cuoi cung co priority cao nhat

        if self.check_limit_condition(step_count, time.perf_counter() - start_time):
            break

        state_count += 1

        self.observe(playerX, playerY, boxes, steps)

        if len(steps) > len(best_path):
            best_path = steps

        if self.is_complete(boxes):
            return self.save_result(steps, is_solution=True,
                                    state_count=state_count,
                                    step_count=step_count)

        # Su dung DFS voi partial observability - chi quan sat mot so huong
        directions = self.directions.copy()
        
        # Mo phong kha nang chi quan sat mot phan
        if random.random() < 0.2:  # 20% kha nang bi han che tam nhin ==> # Xem xet 3/4 huong, thay vi ca 4 huong
            directions = random.sample(directions, max(2, len(directions) * 3 // 4))  
        
        for dx, dy in directions:
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
                # Uu tien cac state gan goal hon
                priority = calculate_priority(self, newX, newY, new_boxes)
                stack.append((priority, new_state, steps + [(newX, newY)]))
                step_count += 1

    return self.save_result(best_path, is_solution=False,
                            state_count=state_count,
                            step_count=step_count)

def calculate_priority(self, playerX, playerY, boxes):
    # Tinh priority cho state - cao hon = tot hon
    priority = 0
    
    # Priority cho viec gan goal
    for goal in self.endPointPos:
        distance = abs(playerX - goal[0]) + abs(playerY - goal[1])
        priority += 100 / (1 + distance)
    
    # Priority cho viec hop gan goal
    for box in boxes:
        for goal in self.endPointPos:
            box_distance = abs(box[0] - goal[0]) + abs(box[1] - goal[1])
            priority += 200 / (1 + box_distance)  # Hop gan goal = priority cao
    
    # Priority cho so hop da o dung vi tri
    boxes_on_goals = sum(1 for box in boxes if box in self.endPointPos)
    priority += boxes_on_goals * 1000  # Hop da o vi tri goal = priority rat cao
    
    # Them yeu to ngau nhien de mo phong su khong chac chan trong danh gia
    priority += random.uniform(-10, 10)
    
    return priority