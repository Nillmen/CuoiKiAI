import copy
from scripts.algorithm import bfs, dfs

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
        self.bfs_in_infor = bfs.input_infor(self)
        self.dfs_in_infor = dfs.input_infor(self)

        self.boxPos = []
        self.endPointPos = set()

        self.observed_states = []

        self.directions = [(-1,0),(1,0),(0,-1),(0,1)]

        self.solution_found = False

    def get_response(self):
        if self.algorithm == "bfs":
            return bfs.run(self)
        if self.algorithm == "dfs":
            return dfs.run(self)
        
    def get_input(self):
        if self.algorithm == "bfs":
            return bfs.input_infor(self)
        elif self.algorithm == "dfs":
            return dfs.input_infor(self)

    def add_data(self):
        self.boxPos.clear()
        self.endPointPos.clear()
        print("debug", self.map_data)
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
        self.solution_found = is_solution
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
    
    def check_win(self):
        return self.solution_found

    def check_limit_condition(self, step_count, period_time):
        if step_count >= self.max_step or period_time >= self.max_time:
            return True
        return False

    