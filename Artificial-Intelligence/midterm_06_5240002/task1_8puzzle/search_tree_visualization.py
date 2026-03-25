from collections import deque
from graphviz import Digraph
from common.search.node import Node
from task1_8puzzle.puzzle_state import get_neighbors


def state_to_label(state):
    return "\n".join(
        [" ".join("_" if x == 0 else str(x) for x in row) for row in state]
    )


def illustrate_search_tree(initial_state, n_limit=15):
    dot = Digraph(format='png')
    dot.attr('node', shape='ellipse')

    start_node = Node(state=initial_state)
    node_id_map = {start_node.state: "N0"}

    dot.node("N0", state_to_label(start_node.state))

    frontier = deque([start_node])
    visited = set([start_node.state])

    count = 1
    node_counter = 1

    # ===== BFS TREE =====
    while frontier and count < n_limit:
        current_node = frontier.popleft()
        current_id = node_id_map[current_node.state]

        for action, next_state, cost in get_neighbors(current_node.state):
            if count >= n_limit:
                break

            if next_state in visited:
                continue

            child_node = Node(
                state=next_state,
                parent=current_node,
                action=action,
                g=current_node.g + cost
            )

            # tạo id ổn định
            child_id = f"N{node_counter}"
            node_id_map[next_state] = child_id

            # vẽ node
            dot.node(child_id, state_to_label(next_state))
 
            dot.edge(current_id, child_id, label=action)

            frontier.append(child_node)
            visited.add(next_state)

            node_counter += 1
            count += 1

   
    dot.render('8puzzle_search_tree', view=True)
    print(f"Đã vẽ cây với {count} nút.")