class Node:
    def __init__(self, state, parent=None, action=None, g=0, h=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.g = g
        self.h = h
        self.f = g + h

    def __lt__(self, other):
        return self.f < other.f

    def __eq__(self, other):
        return self.state == other.state

    def __hash__(self):
        return hash(self.state)

    def get_path(self):
        path = []
        current = self
        while current:
            path.append(current.state)
            current = current.parent
        return path[::-1]

    def get_actions(self):
        actions = []
        current = self
        while current and current.action:
            actions.append(current.action)
            current = current.parent
        return actions[::-1]