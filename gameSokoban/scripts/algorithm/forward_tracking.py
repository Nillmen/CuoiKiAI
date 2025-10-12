# algorithms/forward_tracking.py
import time
from itertools import permutations
from collections import deque



def run(self):
    """
    Thuật toán CSP với Forward Checking cho Sokoban (Forward Tracking).
    Xét tất cả hoán vị thứ tự đẩy boxes.
    Trả solution đầu tiên tìm thấy (dict {'mapping': {box: goal, ...}, 'order': (idx0, idx1, ...), 'box_order': [box1, box2, ...], 'player_path': [(r0,c0), ...]}).
    Nếu không có, trả None.
    Observe ở backtrack và BFS sub-routines.
    """
    self.state_count = 0
    self.step_count = 0
    best_path = []  # list of positions
    self.best_path_length = 0
    self.start_time = time.perf_counter()
    
    self.add_data()
    player_start = self.get_player_pos()
    boxes = list(self.boxPos)
    goals_list = list(self.endPointPos)
    num_boxes = len(boxes)
    
    if num_boxes != len(goals_list):
        return self.save_result([], False, self.state_count, self.step_count)
    
    initial_domains = [set(goals_list) for _ in range(num_boxes)]
    initial_boxes = tuple(sorted(boxes))
    
    # Observe initial state trước khi bắt đầu
    self.observe(player_start[0], player_start[1], list(initial_boxes), depth=0)
    
    solution_found = False
    # Xét tất cả hoán vị thứ tự đẩy
    for perm_order in permutations(range(num_boxes)):
        if self.check_limit_condition(self.step_count, time.perf_counter() - self.start_time):
            break
        order = [boxes[i] for i in perm_order]  # Thứ tự boxes theo perm
        domains = [initial_domains[i].copy() for i in range(num_boxes)]
        assignment = {}
        
        result = self.backtrack(order, 0, domains, initial_boxes, player_start, assignment, depth=0)
        if result:
            # Chuyển order thành indices gốc (theo boxPos ban đầu)
            idx_order = tuple(boxes.index(b) for b in order)
            result['order'] = idx_order
            result['box_order'] = order  # Giữ order boxes cho extract path
            # Extract player path (sẽ observe thêm trong sub-paths)
            player_path = self.extract_player_path(result, player_start)
            if player_path:
                if len(player_path) > self.best_path_length:
                    best_path = player_path
                    self.best_path_length = len(player_path)
                # Check if this is a complete solution
                final_boxes = [result['mapping'][b] for b in order]
                if self.is_complete(tuple(final_boxes)):
                    solution_found = True
                    return self.save_result(player_path, True, self.state_count, self.step_count)
    
    if solution_found:
        return self.save_result(best_path, True, self.state_count, self.step_count)
    else:
        return self.save_result(best_path, False, self.state_count, self.step_count)