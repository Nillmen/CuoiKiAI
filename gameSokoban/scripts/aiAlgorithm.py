import copy
from scripts.algorithm import bfs

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
            self.algorithm = "bfs" 

    def get_response(self):
        if self.algorithm == "bfs":
            return bfs.run(self)
        
    def add_data(self):
        self.boxPos.clear()
        self.endPointPos.clear()
        for i in range(self.height):
            for j in range(self.width):
                if self.map_data[i][j] == 'b':
                    self.boxPos.append((i, j))
                elif self.map_data[i][j] == 'p':
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
    
    def check_limit_condition(self, step_count, period_time):
        if step_count >= self.max_step or period_time >= self.max_time:
            return True
        return False

    