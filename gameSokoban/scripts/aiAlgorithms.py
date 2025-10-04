import collections

class Algorithm:
    def __init__(self, window):
        self.window = window
        self.algorithm = self.window.get_data("algorithm")
        self.level = self.window.get_data("level")
        self.game_map = self.window.get_data("map_ori")[self.level - 1]

        self.rows = len(self.game_map)
        self.cols = len(self.game_map[0]) if self.rows > 0 else 0
        self.player_pos = None
        self.boxes = []
        self.targets = []
        self.walls = set()
        self.set_data_map()

    def get_solution(self):
        if self.algorithm =="BFS":
            return self.bfs()
    def set_data_map(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.game_map[r][c] == 'c':
                    self.player_pos = (r, c)
                elif self.game_map[r][c] == 'b':
                    self.boxes.append((r, c))
                elif self.game_map[r][c] == 'p':
                    self.targets.append((r, c))
                elif self.game_map[r][c] == 'w':
                    self.walls.add((r, c))

    def _is_valid_position(self, pos):
        r, c = pos
        return 0 <= r < self.rows and 0 <= c < self.cols and pos not in self.walls

    def _get_new_state(self, state, direction):
        player_pos, boxes = state
        pr, pc = player_pos
        dr, dc = direction
        new_pr, new_pc = pr + dr, pc + dc
        new_player_pos = (new_pr, new_pc)
        
        if not self._is_valid_position(new_player_pos):
            return None
        
        new_boxes = boxes[:]
        box_pos = (new_pr, new_pc)
        if box_pos in boxes:
            box_new_r, box_new_c = new_pr + dr, new_pc + dc
            new_box_pos = (box_new_r, box_new_c)
            if not self._is_valid_position(new_box_pos) or new_box_pos in boxes:
                return None
            box_idx = boxes.index(box_pos)
            new_boxes[box_idx] = new_box_pos
        
        return (new_player_pos, tuple(new_boxes))

    def _is_goal_state(self, boxes):
        return all(box in self.targets for box in boxes)

    def _is_deadlock(self, box_pos, boxes):
        r, c = box_pos
        if box_pos in self.targets:
            return False
        if (self._is_blocked(r, c, -1, 0, boxes) and self._is_blocked(r, c, 0, -1, boxes)) or \
           (self._is_blocked(r, c, -1, 0, boxes) and self._is_blocked(r, c, 0, 1, boxes)) or \
           (self._is_blocked(r, c, 1, 0, boxes) and self._is_blocked(r, c, 0, -1, boxes)) or \
           (self._is_blocked(r, c, 1, 0, boxes) and self._is_blocked(r, c, 0, 1, boxes)):
            return True
        return False

    def _is_blocked(self, r, c, dr, dc, boxes):
        return (r + dr, c + dc) in self.walls or (r + dr, c + dc) in boxes

    def bfs(self): 
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        initial_state = (self.player_pos, tuple(self.boxes))
        
        # queue chứa: (state, path, moves)
        queue = collections.deque([(initial_state, [self.player_pos], [])])
        visited = {initial_state}
        
        while queue:
            (player_pos, boxes), path, moves = queue.popleft()
            
            if self._is_goal_state(boxes):
                return path, moves   # trả về cả 2 list
            
            for direction in directions:
                new_state = self._get_new_state((player_pos, list(boxes)), direction)
                if new_state and new_state not in visited:
                    new_player_pos, new_boxes = new_state
                    if not any(self._is_deadlock(box, new_boxes) for box in new_boxes):
                        visited.add(new_state)
                        
                        # cập nhật path và moves
                        new_path = path + [new_player_pos]
                        new_moves = moves + [direction]

                        queue.append((new_state, new_path, new_moves))
        
        return [], []
