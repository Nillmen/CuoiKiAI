# Nguon: Tham khao tu AI

import time

def run(self):
    state_count = 0
    step_count = 0
    best_path = []

    self.add_data()
    playerX, playerY = self.get_player_pos()
    steps = [(playerX, playerY)]

    initial_state = (playerX, playerY, tuple(self.boxPos))
    visited = set([initial_state])
    
    start_time = time.perf_counter()

    result = backtrack_search(self, initial_state, steps, visited, 
                             state_count, step_count, best_path, start_time)
    
    if result:
        final_state_count, final_step_count, solution_path = result
        return self.save_result(solution_path, is_solution=True,
                               state_count=final_state_count,
                               step_count=final_step_count)
    else:
        return self.save_result(best_path, is_solution=False,
                               state_count=state_count,
                               step_count=step_count)

def backtrack_search(self, current_state, current_path, visited, 
                    state_count, step_count, best_path, start_time):
    # Kiem tra dieu kien gioi han
    if self.check_limit_condition(step_count, time.perf_counter() - start_time):
        return None
    
    playerX, playerY, boxes = current_state
    state_count += 1
    
    # Ghi nhan trang thai hien tai
    self.observe(playerX, playerY, boxes, current_path)
    
    # Cap nhat best_path neu can
    if len(current_path) > len(best_path):
        best_path[:] = current_path[:]
    
    # Kiem tra dieu kien thang
    if self.is_complete(boxes):
        return state_count, step_count, current_path
    
    # Thu cac huong di chuyen co the
    for dx, dy in self.directions:
        newX, newY = playerX + dx, playerY + dy
        
        # Kiem tra huong di chuyen co hop le khong
        if not is_valid_move(self, playerX, playerY, newX, newY, boxes):
            continue
        
        # Tinh toan trang thai moi
        new_boxes = list(boxes)
        if (newX, newY) in boxes:
            # Day hop
            idx = boxes.index((newX, newY))
            newBoxX, newBoxY = self.pushed_to_point(playerX, playerY, newX, newY)
            new_boxes[idx] = (newBoxX, newBoxY)
        
        new_state = (newX, newY, tuple(sorted(new_boxes)))
        
        # Kiem tra trang thai moi da duoc tham chua
        if new_state not in visited:
            # Danh dau trang thai da tham
            visited.add(new_state)
            
            # Them buoc di chuyen vao duong di
            new_path = current_path + [(newX, newY)]
            step_count += 1
            
            # Goi de quy de tiep tuc tim kiem
            result = backtrack_search(self, new_state, new_path, visited,
                                    state_count, step_count, best_path, start_time)
            
            # Neu tim thay giai phap, tra ve ket qua
            if result:
                return result
            
            # Backtrack: bo danh dau trang thai da tham
            visited.remove(new_state)
    
    return None

def is_valid_move(self, playerX, playerY, newX, newY, boxes):
    # Kiem tra ranh gioi
    if not (0 <= newX < self.height and 0 <= newY < self.width):
        return False
    
    # Kiem tra tuong
    if self.map_data[newX][newY] == 'w':
        return False
    
    # Kiem tra co day hop khong
    if (newX, newY) in boxes:
        newBoxX, newBoxY = self.pushed_to_point(playerX, playerY, newX, newY)
        
        # Kiem tra vi tri moi cua hop co hop le khong
        if not (0 <= newBoxX < self.height and 0 <= newBoxY < self.width):
            return False
        
        if self.map_data[newBoxX][newBoxY] == 'w':
            return False
        
        if (newBoxX, newBoxY) in boxes:
            return False
        
        # Kiem tra deadlock
        if self.box_is_dead_lock(newBoxX, newBoxY, boxes):
            return False
    
    return True