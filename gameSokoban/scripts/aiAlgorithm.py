import time
import copy
from collections import deque

class AIAlgorithm():
    def __init__(self, window):
        self.window = window
        self.algorithm = self.window.get_data("algorithm")
        self.map_current = copy.deepcopy(self.window.get_data("map_current"))
        self.limit_condition_algorithm = self.window.get_data("limit_condition_algorithm")
        self.max_time = self.limit_condition_algorithm["max_time"]
        self.max_step = self.limit_condition_algorithm["max_step"]
        if len(self.algorithm) == 0:
            self.algorithm = "bfs" 

    def get_response(self):
        if self.algorithm == "bfs":
            return self.bfs()

    def bfs(self):
        rows = len(self.map_current)
        cols = len(self.map_current[0])

        player = None
        boxes = []
        goals = []

        for y in range(rows):
            for x in range(cols):
                cell = self.map_current[y][x]
                if cell == "c":
                    player = (x, y)
                    self.map_current[y][x] = "g"
                elif cell == "b":
                    boxes.append((x, y))
                    self.map_current[y][x] = "g"
                elif cell == "p":
                    goals.append((x, y))

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        start_state = (player, tuple(sorted(boxes)))

        queue = deque([start_state])
        predecessors = {start_state: (None, None)}
        algorithm_trace = []
        step_counter = 0
        final_state = None
        start_time = time.perf_counter()

        while queue:
            current_state = queue.popleft()
            current_pos_player, current_pos_boxes = current_state

            step_counter += 1
            end_time = time.perf_counter()

            algorithm_trace.append({
                "step": step_counter,
                "processing_state": current_state,
                "queue_size_before_pop": len(queue) + 1,
                "visited_states_count": len(predecessors)
            })

            if (step_counter >= self.max_step) or ((end_time - start_time) >= self.max_time):
                break

            if set(goals) == set(current_pos_boxes):
                final_state = current_state
                break

            for dx, dy in directions:
                next_player_pos = (current_pos_player[0] + dx, current_pos_player[1] + dy)
                px, py = next_player_pos

                if not (0 <= px < cols and 0 <= py < rows and self.map_current[py][px] != "w"):
                    continue

                boxes_list = list(current_pos_boxes)
                
                if next_player_pos not in boxes_list:
                    new_state = (next_player_pos, current_pos_boxes) # Boxes don't move
                    if new_state not in predecessors:
                        predecessors[new_state] = (current_state, (dx, dy))
                        queue.append(new_state)
                else:
                    next_box_pos = (px + dx, py + dy)
                    bx, by = next_box_pos
                    if not (0 <= bx < cols and 0 <= by < rows and self.map_current[by][bx] != 'w' and next_box_pos not in boxes_list):
                        continue
                    
                    boxes_list[boxes_list.index(next_player_pos)] = next_box_pos
                    
                    new_pos_boxes = tuple(sorted(boxes_list))
                    new_state = (next_player_pos, new_pos_boxes)

                    if new_state not in predecessors:
                        predecessors[new_state] = (current_state, (dx, dy))
                        queue.append(new_state)
        
        path = []
        if final_state:
            current = final_state
            while current != start_state:
                parent_state, move = predecessors[current]
                path.append(move)
                current = parent_state
            path.reverse()

        algorithm_details = {
            "total_states_visited": len(predecessors),
            "total_steps_processed": step_counter,
            "solution_found": final_state is not None,
            "solution_length": len(path), 
            "trace": algorithm_trace
        }
        return path, algorithm_details