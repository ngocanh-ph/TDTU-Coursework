class SokobanState:
    def __init__(self, grid, player, boxes):
        self.grid = grid
        self.player = player
        self.boxes = tuple(sorted(boxes))

    def __hash__(self):
        return hash((self.player, self.boxes))

    def __eq__(self, other):
        return self.player == other.player and self.boxes == other.boxes

    def is_goal(self, goals):
        return all(box in goals for box in self.boxes)

    def moves(self):
        # 4 hướng: (dx, dy, tên action)
        directions = [(0, 1, "South"), (0, -1, "North"), (1, 0, "East"), (-1, 0, "West")]
        for dx, dy, action_name in directions:
            px, py = self.player
            nx, ny = px + dx, py + dy
            if self.grid[ny][nx] == '%':
                continue
            new_boxes = list(self.boxes)
            if (nx, ny) in self.boxes:
                bx, by = nx + dx, ny + dy
                if self.grid[by][bx] == '%' or (bx, by) in self.boxes:
                    continue
                new_boxes.remove((nx, ny))
                new_boxes.append((bx, by))
                yield action_name, SokobanState(self.grid, (nx, ny), new_boxes)
            else:
                yield action_name, SokobanState(self.grid, (nx, ny), new_boxes)

    @staticmethod
    def get_neighbors(state):
        neighbors = []
        for action, next_state in state.moves():
            neighbors.append((action, next_state, 1))
        return neighbors