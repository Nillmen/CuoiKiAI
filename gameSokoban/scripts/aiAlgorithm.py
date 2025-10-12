import copy
from scripts.algorithm import bfs,dfs,dls,ids,ucs,greedy,astar,hill_climbing,beam_search,sa,ac3,forward_tracking
import random
from itertools import permutations
from collections import deque
import time

class AIAlgorithm():
    def __init__(self, window):
        self.window = window
        self.algorithm = self.window.get_data("algorithm")
        self.map_data = copy.deepcopy(self.window.get_data("map_current"))
        self.limit_condition_algorithm = self.window.get_data("limit_condition_algorithm")
        self.max_time = self.limit_condition_algorithm["max_time"]
        self.max_step = self.limit_condition_algorithm["max_step"]

        self.boxPos = []
        self.endPointPos = set()

        self.height = len(self.map_data)
        self.width = len(self.map_data[0])

        self.observed_states = []

        self.directions = [(-1,0),(1,0),(0,-1),(0,1)]

        if len(self.algorithm) == 0:
            self.algorithm = "forward_tracking" 

    def get_response(self):
        if self.algorithm == "bfs":
            return bfs.run(self)
        elif self.algorithm == "dfs":
            return dfs.run(self)
        elif self.algorithm == "dls":
            return dls.run(self)
        elif self.algorithm == "ids":
            return ids.run_ids(self)
        elif self.algorithm == "ucs":
            return ucs.run(self)
        elif self.algorithm == "greedy":
            return greedy.run(self)
        elif self.algorithm == "astar":
            return astar.run(self)
        elif self.algorithm == "hill_climbing":
            return hill_climbing.run(self)
        elif self.algorithm == "beam_search":
            return beam_search.run(self)
        elif self.algorithm == "sa":
            return sa.run(self)
        elif self.algorithm == "ac3":
            return ac3.run_ac3(self)
        elif self.algorithm == "forward_tracking":
            return forward_tracking.run(self)
    def add_data(self):
        self.boxPos.clear()
        self.endPointPos.clear()
        for i in range(self.height):
            for j in range(self.width):
                if self.map_data[i][j] == 'b':
                    self.boxPos.append((i, j))
                elif self.map_data[i][j] == 'p':
                    self.endPointPos.add((i, j))
    def get_distance(self,aX,aY,bX,bY):
        return abs(aX - bX) + abs(aY - bY)

    def get_player_pos(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.map_data[i][j] == 'c':
                    return (i, j)
                
    def observe(self, playerX, playerY, boxes, steps=None, depth=None,
            costH=None, costG=None, costF=None, mapNo=None, heat=None):
        """Lưu lại trạng thái hiện tại của thuật toán"""
        state_info = {
            "player": (playerX, playerY),
            "boxes": list(boxes),
            "depth": depth,
            "costH": costH,
            "costG": costG,
            "costF": costF,
            "mapNo": mapNo,
            "heat": heat
        }
        self.observed_states.append(state_info)

    def is_complete(self,boxes):
        return all(box in self.endPointPos for box in boxes)
    
    def save_result(self,steps,is_solution,state_count,step_count):
        path=self.get_path(steps)
        algorithm_details = {
            "total_states_visited": state_count,
            "total_steps_processed": step_count,
            "solution_found": is_solution,
            "solution_length": len(path),
            "trace": self.observed_states
        }
        return path, algorithm_details
    
    def get_path(self,steps):
        path = []
        for i in range(len(steps) - 1):
            dx = steps[i + 1][0] - steps[i][0]
            dy = steps[i + 1][1] - steps[i][1]
            path.append((dy, dx))
        return path

    def player_is_blocked(self,curX, curY, newX, newY, boxes):
        if self.map_data[newX][newY] == "w":
            return True
        elif (newX, newY) in boxes:
            newBoxX, newBoxY = self.pushed_to_point(curX, curY, newX, newY)
            if self.box_is_blocked(newBoxX, newBoxY, boxes):
                return True
            
    def box_is_blocked(self,newX, newY, boxes):
        return (
            self.map_data[newX][newY] == "w"
            or (newX, newY) in boxes
            or self.box_is_dead_lock(newX, newY, boxes)
        )
    
    def pushed_to_point(self,playerX, playerY, boxX, boxY):
        return (boxX + (boxX - playerX), boxY + (boxY - playerY))
    
    def box_is_dead_lock(self,x, y, boxes):
        """Kiểm tra deadlock theo hướng 'unmovable box'"""
        if (x, y) in self.endPointPos:
            return False

        boxes_set = set(boxes)
        unmovables = set()

        for b in boxes_set:
            if b not in self.endPointPos and not self.is_pushable(b, boxes_set):
                unmovables.add(b)


        if (x, y) in unmovables:
            adj_walls = sum(
                1 for dx, dy in self.directions
                if self.map_data[x + dx][y + dy] == 'w'
            )
            if adj_walls >= 2:
                return True
            
        for dx, dy in [(1, 0), (0, 1)]:
            if (x + dx, y + dy) in unmovables:
                return True
            
    def is_pushable(self,box_pos, boxes):
        """Kiểm tra xem hộp có thể bị đẩy theo hướng nào không
        trước trống
        sau trống
        trống = ko hộp,ko tường
        """
        x, y = box_pos
        for dx, dy in self.directions:
            front = (x + dx, y + dy)
            back = (x - dx, y - dy)
            if (front not in boxes and back not in boxes
                and self.map_data[front[0]][front[1]] != 'w'
                and self.map_data[back[0]][back[1]] != 'w'):
                return True
        return False
    def g(self, player_pos, boxes):
        """Tính khoảng cách từ player tới hộp gần nhất"""
        if not boxes:
            return 0
        return min(self.get_distance(player_pos[0], player_pos[1], box[0], box[1]) for box in boxes)
    def h(self, boxes):
        """Trả về trung bình khoảng cách từ mỗi hộp tới đích gần nhất"""
        if not boxes:
            return 0
        if not self.endPointPos:
            return float('inf')  # nếu không có đích, báo vô cực để tránh chọn
        total = 0
        for bx, by in boxes:
            min_dist = min(self.get_distance(bx, by, gx, gy) for (gx, gy) in self.endPointPos)
            total += min_dist
        return total / len(boxes)
    import random

    def random_start_state(self):
        """Sinh ngẫu nhiên vị trí người chơi và hộp (tránh tường, đích, empty và trùng nhau)."""
        occupied = set(self.endPointPos)  # Không spawn lên đích
        new_boxes = []

        # Sinh ngẫu nhiên vị trí hộp
        for _ in range(len(self.boxPos)):
            while True:
                bx = random.randint(1, self.width - 2)
                by = random.randint(1, self.height - 2)
                if self.map_data[by][bx] not in ('w', 'e', 'p') and (bx, by) not in occupied and not self.box_is_dead_lock(bx, by, new_boxes):
                    occupied.add((bx, by))
                    new_boxes.append((bx, by))
                    break

        # Sinh ngẫu nhiên vị trí người chơi
        while True:
            playerX = random.randint(1, self.width - 2)
            playerY = random.randint(1, self.height - 2)
            if self.map_data[playerY][playerX] not in ('w', 'e') and (playerX, playerY) not in occupied:
                break

        return (playerX, playerY, tuple(sorted(new_boxes)))

    def get_neighbors(self, playerX, playerY, boxes):
        """Lấy tất cả trạng thái hàng xóm hợp lệ của player."""
        neighbors = []

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

                # Nếu hộp bị đẩy vào deadlock → bỏ qua
                if self.box_is_dead_lock(newBoxX, newBoxY, new_boxes):
                    continue

            neighbors.append((newX, newY, tuple(sorted(new_boxes))))
        return neighbors


    def box_can_be_pushed_to(self, boxX, boxY, goalX, goalY):
        """Kiểm tra xem hộp tại (boxX, boxY) có thể được đẩy tới (goalX, goalY) không."""
        queue = deque([(self.get_player_pos(), (boxX, boxY))])
        visited = set([(self.get_player_pos(), (boxX, boxY))])

        while queue:
            (playerX, playerY), (bX, bY) = queue.popleft()
            if (bX, bY) == (goalX, goalY):
                return True

            for dx, dy in self.directions:
                newPX, newPY = playerX + dx, playerY + dy
                # Người không được đi xuyên tường hoặc hộp
                if not self.is_free(newPX, newPY, [(bX, bY)]):
                    continue

                # Nếu người đứng sau hộp, có thể đẩy
                if (newPX, newPY) == (bX - dx, bY - dy):
                    newBX, newBY = bX + dx, bY + dy
                    if not self.is_free(newBX, newBY, [(bX, bY)]):
                        continue
                    new_state = ((bX, bY), (newBX, newBY))
                else:
                    new_state = ((newPX, newPY), (bX, bY))

                if new_state not in visited:
                    visited.add(new_state)
                    queue.append(new_state)

        return False


    def get_all_valid_solutions(self):
        """Trả về danh sách tất cả các hoán vị hộp–đích hợp lệ."""
        valid_pairs = {}  # valid_pairs[i] = [các index đích mà hộp i có thể đến]
        for i, (bX, bY) in enumerate(self.boxPos):
            valid_pairs[i] = []
            for j, (gX, gY) in enumerate(self.goalPos):
                if self.box_can_be_pushed_to(bX, bY, gX, gY):
                    valid_pairs[i].append(j)

        all_valid_solutions = []
        # Kiểm tra mọi hoán vị giữa các đích
        for perm in permutations(range(len(self.goalPos))):
            valid = True
            for i, goal_idx in enumerate(perm):
                if goal_idx not in valid_pairs[i]:
                    valid = False
                    break
            if valid:
                all_valid_solutions.append([(self.boxPos[i], self.goalPos[perm[i]]) for i in range(len(self.boxPos))])

        return all_valid_solutions


    def is_free(self,x, y, boxes):
        """Kiểm tra ô (x, y) có trống cho người hoặc hộp không."""
        # Tường thì không đi được
        if self.map_data[x][y] == 'w':
            return False
        # Không được đứng lên hộp
        if (x, y) in boxes:
            return False
        return True
    from collections import deque

    def can_move_box_to(self,box_pos, goal_pos, boxes): 
        start = tuple(box_pos)
        goal = tuple(goal_pos)

        other_boxes = set(boxes)
        if start in other_boxes:
            other_boxes.remove(start)

        q = deque([start])
        visited = {start}

        while q:
            x, y = q.popleft()
            if (x, y) == goal:
                return True, boxes

            for dx, dy in self.directions:
                nx, ny = x + dx, y + dy        # hộp di chuyển tới
                backx, backy = x - dx, y - dy  # ô đằng sau hộp (pusher)

                # Cả front và back đều phải trống (so với other_boxes, không phải boxes)
                if not self.is_free(nx, ny, other_boxes):
                    continue
                if not self.is_free(backx, backy, other_boxes):
                    continue

                new_boxes = list(other_boxes) + [(nx, ny)]
                if self.box_is_dead_lock(nx, ny, new_boxes):
                    continue

                if (nx, ny) not in visited:
                    visited.add((nx, ny))
                    q.append((nx, ny))

        return False, boxes



    def get_all_valid_solutions(self):
        """
        Trả về danh sách các solution khả thi.
        Mỗi solution là dict:
        { 'mapping': [(box_pos, goal_pos), ...],  # theo thứ tự boxPos
            'order': (i0, i1, ...)                   # một thứ tự đẩy (chỉ số hộp) chứng minh khả thi
        }
        - Ghi chú: mapping khác nhau nếu hoán vị của goals khác nhau.
        - Hàm thử mọi ánh xạ (permutation của goals) và cho mỗi ánh xạ thử mọi thứ tự đẩy (permutation của boxes).
        - Trả về những ánh xạ mà tồn tại ít nhất 1 thứ tự đẩy thành công (với mô phỏng cập nhật boxes).
        """
        # đảm bảo dữ liệu mới nhất
        self.add_data()
        boxes = list(self.boxPos)           # danh sách hộp (theo thứ tự cố định)
        goals = list(self.endPointPos)      # làm list để có thứ tự cố định cho permutations

        solutions = []

        # xét mọi ánh xạ box -> goal (mỗi hoán vị của goals)
        for perm_goals in permutations(goals, len(boxes)):
            mapping = list(zip(boxes, perm_goals))  # mapping theo thứ tự boxes
            # thử mọi thứ tự đẩy (nếu có n hộp thì có n! thứ tự)
            found_order = None
            for order in permutations(range(len(boxes))):
                cur_boxes = list(boxes)  # trạng thái cập nhật khi mô phỏng
                ok = True
                for box_idx in order:
                    cur_box_pos = cur_boxes[box_idx]
                    target_pos = perm_goals[box_idx]
                    # kiểm tra khả năng đẩy hộp này sang đích, xét các hộp còn lại tại cur_boxes
                    if self.can_move_box_to(cur_box_pos, target_pos, cur_boxes):
                        # cập nhật vị trí hộp này thành target
                        cur_boxes[box_idx] = target_pos
                    else:
                        ok = False
                        break
                if ok:
                    found_order = order
                    break

            if found_order is not None:
                solutions.append({
                    'mapping': mapping,
                    'order': found_order
                })

        return solutions
    def calculate_solution_cost(self,solution, player_start):
        """
        Tính chi phí của một solution cụ thể.
        - solution: dict gồm 'mapping' và 'order' (do get_all_valid_solutions() trả về)
        - player_start: vị trí ban đầu của người chơi (x, y)
        Công thức:
            cost = sum( dist(player → box_i) + dist(box_i → goal_i) )
            (vị trí player cập nhật theo đích của hộp vừa đẩy)
        """
        total_cost = 0
        player_pos = tuple(player_start)
        mapping = solution['mapping']
        order = solution['order']

        for i in order:
            box_pos = list(mapping.keys())[i]
            goal_pos = mapping[box_pos]

            d1 = self.get_distance(player_pos[0], player_pos[1], box_pos[0], box_pos[1])
            d2 = self.get_distance(box_pos[0], box_pos[1], goal_pos[0], goal_pos[1])

            total_cost += d1 + d2
            player_pos = goal_pos


        return total_cost

    def can_player_push_box_to_goal(self, player_start, target_box, goal, other_boxes, depth=0):
        """
        Kiểm tra player có thể đẩy target_box đến goal không, không push other_boxes.
        Nếu True, trả về (True, updated_boxes, final_player_pos) để chain cho box tiếp theo.
        updated_boxes: tuple(sorted(list(others) + [goal])) để hash ổn định.
        final_player_pos: vị trí player khi box vừa đến goal.
        Nếu False: (False, None, None)
        Thêm observe cho từng state trong BFS (depth tăng dần).
        """
        initial_state = (player_start, target_box, frozenset(other_boxes))
        queue = deque([initial_state])
        visited = {initial_state}
        self.state_count += 1  # Initial state
        
        # Observe initial state
        self.observe(player_start[0], player_start[1], list(other_boxes) + [target_box], depth=depth)
        
        while queue:
            if self.check_limit_condition(self.step_count, time.perf_counter() - self.start_time):
                return False, None, None
            p_pos, b_pos, others = queue.popleft()
            self.state_count += 1
            if b_pos == goal:
                updated_boxes = tuple(sorted(list(others) + [goal]))
                return True, updated_boxes, p_pos
            
            for dr, dc in self.directions:
                new_p = (p_pos[0] + dr, p_pos[1] + dc)
                if not self.is_free(new_p[0], new_p[1], others):
                    continue
                
                if new_p == b_pos:  # Push target
                    push_pos = (b_pos[0] + dr, b_pos[1] + dc)
                    if not self.is_free(push_pos[0], push_pos[1], others):
                        continue
                    new_b = push_pos
                    new_others = others
                else:
                    new_b = b_pos
                    new_others = others
                
                new_state = (new_p, new_b, new_others)
                if new_state not in visited:
                    visited.add(new_state)
                    queue.append(new_state)
                    self.step_count += 1  # Count enqueues
                    # Observe new state (depth +1)
                    new_depth = depth + 1
                    self.observe(new_p[0], new_p[1], list(new_others) + [new_b], depth=new_depth)
        
        return False, None, None

    def forward_check(self,domains, assigned_goal, var_idx, num_vars):
        """
        Forward checking: Loại assigned_goal khỏi domains của các biến sau var_idx.
        Trả True nếu không domain nào rỗng, else False.
        """
        for i in range(var_idx + 1, num_vars):
            domains[i].discard(assigned_goal)
            if not domains[i]:
                return False
        return True

    def backtrack(self, order, level, domains, current_boxes, player_pos, assignment, depth=0):
        """
        Backtracking DFS cho assignment theo order (list boxes).
        - order: list các box_pos theo thứ tự đẩy.
        - level: index box hiện tại đang assign.
        - domains: list of sets (miền cho mỗi box trong order).
        - current_boxes: tuple hiện tại của tất cả boxes (assigned + remaining).
        - player_pos: vị trí player hiện tại (sau push trước).
        - assignment: dict {box: goal} tạm thời.
        - depth: depth của backtrack level.
        Trả solution dict {'mapping': assignment.copy(), 'order': order (boxes)} nếu success, else None.
        Observe ở mỗi level backtrack.
        """
        if self.check_limit_condition(self.step_count, time.perf_counter() - self.start_time):
            return None
        
        if level == len(order):
            return {'mapping': assignment.copy(), 'order': order}
        
        # Observe current backtrack level
        self.observe(player_pos[0], player_pos[1], list(current_boxes), depth=depth)
        self.state_count += 1  # Count backtrack levels as states
        
        box = order[level]
        for goal in list(domains[level]):  # Copy để tránh modify trong loop
            success, new_boxes, new_player = self.can_player_push_box_to_goal(player_pos, box, goal, set(current_boxes) - {box}, depth=depth)
            if not success:
                continue
            
            # Assign tạm
            assignment[box] = goal
            old_domains = [d.copy() for d in domains]  # Backup để restore nếu fail
            
            # Forward check
            if self.forward_check(domains, goal, level, len(order)):
                # Recurse với depth +1
                result = self.backtrack(order, level + 1, domains, new_boxes, new_player, assignment, depth + 1)
                if result:
                    return result
            
            # Restore domains
            domains[:] = old_domains
        
        return None

    def get_player_path_to_push(self, player_start, target_box, goal, other_boxes, depth=0):
        """
        Tìm path player để đẩy target_box đến goal, không push other_boxes.
        Trả list path [(r1,c1), (r2,c2), ...] nếu success, else None.
        Path bắt đầu từ player_start, kết thúc tại vị trí player khi box đến goal.
        other_boxes: set hoặc frozenset các vị trí other boxes (fixed, không di chuyển).
        Observe trong BFS với depth.
        """
        initial_state = (player_start, target_box, frozenset(other_boxes))
        queue = deque([(initial_state, [player_start])])  # State + path
        visited = {initial_state}
        self.state_count += 1
        
        # Observe initial
        self.observe(player_start[0], player_start[1], list(other_boxes) + [target_box], depth=depth)
        
        while queue:
            if self.check_limit_condition(self.step_count, time.perf_counter() - self.start_time):
                return None
            (p_pos, b_pos, others), path = queue.popleft()
            self.state_count += 1
            if b_pos == goal:
                return path
            
            for dr, dc in self.directions:
                new_p = (p_pos[0] + dr, p_pos[1] + dc)
                if not self.is_free(new_p[0], new_p[1], others):
                    continue
                
                if new_p == b_pos:  # Push target
                    push_pos = (b_pos[0] + dr, b_pos[1] + dc)
                    if not self.is_free(push_pos[0], push_pos[1], others):
                        continue
                    new_b = push_pos
                    new_others = others
                else:
                    new_b = b_pos
                    new_others = others
                
                new_state = (new_p, new_b, new_others)
                if new_state not in visited:
                    visited.add(new_state)
                    new_path = path + [new_p]
                    queue.append((new_state, new_path))
                    self.step_count += 1
                    # Observe new state
                    new_depth = depth + len(new_path) - 1  # Depth dựa trên path length
                    self.observe(new_p[0], new_p[1], list(new_others) + [new_b], depth=new_depth)
        
        return None

    def extract_player_path(self, solution, initial_player_pos):
        """
        Extract full player path từ solution CSP.
        - solution: dict {'mapping': {box: goal, ...}, 'box_order': [box1, box2, ...]}
        - initial_player_pos: (r, c) ban đầu
        Trả list full path [(r0,c0), (r1,c1), ...] nếu success, else None.
        Observe trong từng sub-path với depth tăng dần.
        """
        if not solution:
            return None
        
        mapping = solution['mapping']
        order = solution['box_order']  # List boxes theo thứ tự đẩy
        full_path = [initial_player_pos]
        player_pos = initial_player_pos
        current_boxes = list(self.boxPos)  # Ban đầu từ map_data
        overall_depth = 0
        
        for idx, box in enumerate(order):
            goal = mapping[box]
            other_boxes_set = set(current_boxes) - {box}
            
            sub_path = self.get_player_path_to_push(player_pos, box, goal, other_boxes_set, depth=overall_depth)
            if sub_path is None:
                return None  # Không thể push box này
            
            # Append sub_path từ bước thứ 2 (tránh duplicate player_pos hiện tại)
            full_path += sub_path[1:]
            player_pos = sub_path[-1]  # Update player_pos cuối sub_path
            
            # Update current_boxes: Di chuyển box đến goal
            current_box_idx = current_boxes.index(box)
            current_boxes[current_box_idx] = goal
            
            # Update overall depth cho sub tiếp theo
            overall_depth += len(sub_path)
        
        return full_path
    def check_limit_condition(self, step_count, period_time):
        if step_count >= self.max_step or period_time >= self.max_time:
            return True
        return False

    