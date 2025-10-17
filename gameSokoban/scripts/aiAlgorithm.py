import copy
import time
from collections import deque
from scripts.algorithm import forward_tracking
from scripts.algorithm import bfs, dfs, ids, greedy, beam, backtracking, partially_observable, ucs, astar, hill_climbing, sa, ac3, blind_search
dict_algorithm = {
    "bfs" : bfs,
    "dfs" : dfs,
    "ids" : ids,
    "greedy" : greedy,
    "beam" : beam,
    "backtracking" : backtracking,
    "partially_observable" : partially_observable,
    "ucs" : ucs,
    "astar" : astar,
    "forward_tracking" : forward_tracking,
    "hill_climbing" : hill_climbing,
    "sa" : sa,
    "ac3" : ac3,
    "blind_search" : blind_search
}

class AIAlgorithm():
    def __init__(self, window):
        self.window = window
        self.algorithm = self.window.get_data("algorithm")
        self.map_data = copy.deepcopy(self.window.get_data("map_current"))
        self.map_data = [list(row) for row in self.map_data]
        self.limit_condition_algorithm = self.window.get_data("limit_condition_algorithm")
        self.max_time = self.limit_condition_algorithm["max_time"]
        self.max_step = self.limit_condition_algorithm["max_step"]
        self.pos_endpoints = self.window.get_data("pos_endpoints")

        self.height = len(self.map_data)
        self.width = len(self.map_data[0])

        self.boxPos = []
        self.endPointPos = set()

        self.observed_states = []

        self.directions = [(-1,0),(1,0),(0,-1),(0,1)]

        self.solution_found = False
        self.len_last_queue = 0

    def get_response(self):
        return dict_algorithm[self.algorithm].run(self)

    def get_full_path(self, path_steps, pos_start):
        full_path = []
        for i, step in enumerate(path_steps):
            pos_x = None
            pos_x = None
            if i == 0:
                pos_x = step[0] + pos_start[0]
                pos_y = step[1] + pos_start[1]
            else:
                pos_x = step[0] + full_path[i - 1][0]
                pos_y = step[1] + full_path[i - 1][1]
            full_path.append((pos_x, pos_y))
        return full_path

    def calculate_solution_cost(self,solution, player_start):

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

    def add_data(self):
        self.boxPos.clear()
        self.endPointPos.clear()
        for i in range(self.height):
            for j in range(self.width):
                if self.map_data[i][j] == 'b':
                    self.boxPos.append((i, j))
                elif self.map_data[i][j] == 'p':
                    self.endPointPos.add((i, j))
                elif self.map_data[i][j] == 'c':
                    if (j, i) in self.pos_endpoints:
                        self.endPointPos.add((i, j))

    def get_player_pos(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.map_data[i][j] == 'c':
                    return (i, j)

    def get_player_path_to_push(self, player_start, target_box, goal, other_boxes, depth=0):

        initial_state = (player_start, target_box, frozenset(other_boxes))
        queue = deque([(initial_state, [player_start])]) 
        visited = {initial_state}
        self.state_count += 1
        
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
                
                if new_p == b_pos:
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
                    new_depth = depth + len(new_path) - 1 
                    self.observe(new_p[0], new_p[1], list(new_others) + [new_b], depth=new_depth)
        
        return None

    def is_free(self,x, y, boxes):
        if self.map_data[x][y] == 'w':
            return False
        if (x, y) in boxes:
            return False
        return True
    from collections import deque

    def get_distance(self,aX,aY,bX,bY):
        return abs(aX - bX) + abs(aY - bY)

    def g(self, player_pos, boxes):
        if not boxes:
            return 0
        return min(self.get_distance(player_pos[0], player_pos[1], box[0], box[1]) for box in boxes)
    def h(self, boxes):
        if not boxes:
            return 0
        if not self.endPointPos:
            return float('inf')
        total = 0
        for bx, by in boxes:
            min_dist = min(self.get_distance(bx, by, gx, gy) for (gx, gy) in self.endPointPos)
            total += min_dist
        return total / len(boxes)
    
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
                nx, ny = x + dx, y + dy        
                backx, backy = x - dx, y - dy  

                if not self.is_free(nx, ny, other_boxes):
                    continue
                if not self.is_free(backx, backy, other_boxes):
                    continue

                new_boxes = list(other_boxes) + [(nx, ny)]
                if self.box_is_dead_lock(nx, ny, new_boxes, new_boxes.index((nx, ny))):
                    continue

                if (nx, ny) not in visited:
                    visited.add((nx, ny))
                    q.append((nx, ny))

        return False, boxes

    def observe(self, playerX, playerY, boxes, len_queue=None, steps=None, depth=None, depth_limit=None,
            costH=None, costG=None, costF=None, mapNo=None, heat=None):
        state_info = {
            "player": (playerX, playerY),
            "boxes": list(boxes),
            "len_queue" : len_queue,
            "steps" : steps,
            "depth": depth,
            "limit_depth" : depth_limit,
            "costH": costH,
            "costG": costG,
            "costF": costF,
            "mapNo": mapNo,
            "heat": heat
        }
        self.observed_states.append(state_info)

    def is_complete(self,boxes):
        return all(box in self.endPointPos for box in boxes)

    def can_player_push_box_to_goal(self, player_start, target_box, goal, other_boxes, depth=0):
        initial_state = (player_start, target_box, frozenset(other_boxes))
        queue = deque([initial_state])
        visited = {initial_state}
        self.state_count += 1
        
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
                
                if new_p == b_pos:
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
                    self.step_count += 1 
                    new_depth = depth + 1
                    self.observe(new_p[0], new_p[1], list(new_others) + [new_b], len_queue=len(queue), depth=new_depth)
        
        return False, None, None

    def forward_check(self,domains, assigned_goal, var_idx, num_vars):
        for i in range(var_idx + 1, num_vars):
            domains[i].discard(assigned_goal)
            if not domains[i]:
                return False
        return True

    def backtrack(self, order, level, domains, current_boxes, player_pos, assignment, depth=0):

        if self.check_limit_condition(self.step_count, time.perf_counter() - self.start_time):
            return None
        
        if level == len(order):
            return {'mapping': assignment.copy(), 'order': order}
        
        self.observe(player_pos[0], player_pos[1], list(current_boxes), depth=depth)
        self.state_count += 1 
        
        box = order[level]
        for goal in list(domains[level]):
            success, new_boxes, new_player = self.can_player_push_box_to_goal(player_pos, box, goal, set(current_boxes) - {box}, depth=depth)
            if not success:
                continue
            
            assignment[box] = goal
            old_domains = [d.copy() for d in domains]
            
            if self.forward_check(domains, goal, level, len(order)):
                result = self.backtrack(order, level + 1, domains, new_boxes, new_player, assignment, depth + 1)
                if result:
                    return result

            domains[:] = old_domains
        
        return None

    def save_result(self,steps,is_solution,state_count,step_count):
        path=self.get_path(steps)
        self.solution_found = is_solution
        algorithm_details = {
            "total_states_visited": state_count,
            "total_steps_processed": step_count,
            "solution_found": is_solution,
            "solution_length": len(path),
            "trace": self.observed_states
        }
        return path, algorithm_details
    
    def get_path(self, steps):
        path = []
        for i in range(len(steps) - 1):
            dx = steps[i + 1][0] - steps[i][0]
            dy = steps[i + 1][1] - steps[i][1]
            path.append((dy, dx))
        return path
    
    def get_last_len_queue(self):
        if len(self.observed_states) > 0 and self.observed_states[-1]["len_queue"]:
            return self.observed_states[-1]["len_queue"]
        else:
            return 0

    def player_is_blocked(self,curX, curY, newX, newY, boxes):
        if self.map_data[newX][newY] == "w":
            return True
        elif (newX, newY) in boxes:
            newBoxX, newBoxY = self.pushed_to_point(curX, curY, newX, newY)
            index = boxes.index((newX, newY))
            if self.box_is_blocked(newBoxX, newBoxY, boxes, index):
                return True
            
    def box_is_blocked(self,newX, newY, boxes, index):
        return (
            self.map_data[newX][newY] == "w"
            or (newX, newY) in boxes
            or self.box_is_dead_lock(newX, newY, boxes, index)
        )
    
    def pushed_to_point(self,playerX, playerY, boxX, boxY):
        return (boxX + (boxX - playerX), boxY + (boxY - playerY))
            
    def box_is_dead_lock(self, x, y, boxes, index):
        if (x, y) in self.endPointPos:
            return False

        new_boxes = list(boxes)

        new_boxes[index] = (x,y)

        boxes_set = set(new_boxes)

        deadlock_boxes = []

        for b in boxes_set:
            temporary_deadlock = False

            depend_boxes = set()

            adjacent_directions = [
                ((-1, 0), (0, 1)),
                ((0, 1), (1, 0)),
                ((1, 0), (0, -1)),
                ((0, -1), (-1, 0))
            ]

            for dir1, dir2 in adjacent_directions:
                pos1 = (b[0] + dir1[0], b[1] + dir1[1])
                pos2 = (b[0] + dir2[0], b[1] + dir2[1])
                
                is_blocked1 = (self.map_data[pos1[0]][pos1[1]] == 'w' or pos1 in boxes_set)
                
                is_blocked2 = (self.map_data[pos2[0]][pos2[1]] == 'w' or pos2 in boxes_set)

                if is_blocked1 and is_blocked2:

                    temporary_deadlock = True
                    
                    if pos1 in boxes_set:
                        depend_boxes.add(pos1)
                    if pos2 in boxes_set:
                        depend_boxes.add(pos2)
                
            deadlock_boxes.append({
                "pos" : b,
                "temporary_deadlock" : temporary_deadlock,
                "depend_boxes" : depend_boxes
            })
        
        for d in deadlock_boxes:
            if d["temporary_deadlock"] and len(d["depend_boxes"]) == 0:
                return True
            elif d["temporary_deadlock"]:
                for db in d["depend_boxes"]:
                    len_true = 0
                    for b in deadlock_boxes:
                        if b["pos"] == db and b["temporary_deadlock"]:
                            len_true += 1
                    if len_true == len(d["depend_boxes"]):
                        return True
        
        return False
    
    def extract_player_path(self, solution, initial_player_pos):
        if not solution:
            return None
        
        mapping = solution['mapping']
        order = solution['box_order'] 
        full_path = [initial_player_pos]
        player_pos = initial_player_pos
        current_boxes = list(self.boxPos)  
        overall_depth = 0
        
        for idx, box in enumerate(order):
            goal = mapping[box]
            other_boxes_set = set(current_boxes) - {box}
            
            sub_path = self.get_player_path_to_push(player_pos, box, goal, other_boxes_set, depth=overall_depth)
            if sub_path is None:
                return None 
            
           
            full_path += sub_path[1:]
            player_pos = sub_path[-1] 
            

            current_box_idx = current_boxes.index(box)
            current_boxes[current_box_idx] = goal
            
            overall_depth += len(sub_path)
        
        return full_path

    def check_win(self):
        return self.solution_found
    
    def check_can_solve(self):
        if self.get_last_len_queue() > 1:
            return True
        return False

    def check_limit_condition(self, step_count, period_time):
        if step_count >= self.max_step or period_time >= self.max_time:
            return True
        return False

    