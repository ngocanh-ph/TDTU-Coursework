from common.search.node import Node
from collections import deque

class Search:
  def __init__(self):
    self.nodes_expanded = 0         # số node đã duyệt để đo hiệu năng
    self.max_frontier_size = 0      # kích thước hàng đợi lớn nhất để đo hiệu năng

  def bfs(self, initial_state, goal_states, get_neighbors):
    frontier = deque()
    frontier_states = set()
    explored = set()

    start_node = Node(state=initial_state)

    frontier.append(start_node)
    frontier_states.add(initial_state)

    while frontier:
      self.max_frontier_size = max(self.max_frontier_size, len(frontier))

      current_node = frontier.popleft()
      frontier_states.remove(current_node.state)
      self.nodes_expanded += 1

      # check goal
      if current_node.state in goal_states:
        return current_node

      explored.add(current_node.state)

      # duyệt neighbor
      for action, next_state, cost in get_neighbors(current_node.state):
        if next_state not in explored and next_state not in frontier_states:
          child = Node(
            state=next_state,
            parent=current_node,
            action=action,
            g=current_node.g + cost,
          )
          frontier.append(child)
          frontier_states.add(next_state)

    return None