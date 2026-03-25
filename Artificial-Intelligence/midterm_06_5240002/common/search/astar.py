from heapq import heappush, heappop
from common.search.node import Node


def reconstruct_path(node):
    path = []
    while node:
        path.append((node.action, node.state))
        node = node.parent
    path.reverse()
    return path


def astar(start_state, goal_test, get_neighbors, heuristic, metrics=None):
    max_frontier = 0        # kích thước frontier lớn nhất
    nodes_expanded = 0      # số node đã duyệt

    open_list = []               # priority queue
    closed_set = set()          # các state đã duyệt
    g_score = {}                 # g_score[state] = chi phí nhỏ nhất để đến state đó từ start    

    start_node = Node(
        state=start_state,
        g=0,
        h=heuristic(start_state)
    )

    heappush(open_list, start_node)
    g_score[start_state] = 0

    while open_list:
        max_frontier = max(max_frontier, len(open_list))

        current = heappop(open_list)
        if current.g > g_score.get(current.state, float('inf')):
            continue

        nodes_expanded += 1

        if goal_test(current.state):

            if metrics is not None:
                metrics['max_frontier'] = max_frontier
                metrics['nodes_expanded'] = nodes_expanded
            
             # truy vết đường đi
            path = reconstruct_path(current)
            return path, current.g, nodes_expanded

        closed_set.add(current.state)


        for action, next_state, cost in get_neighbors(current.state):

            # nếu đã duyệt -> bỏ qua
            if next_state in closed_set:
                continue

             # tính chi phí mới
            tentative_g = current.g + cost

            # nếu tìm được đường tốt hơn
            if next_state not in g_score or tentative_g < g_score[next_state]:

                # cập nhật chi phí tốt nhất
                g_score[next_state] = tentative_g

                h_value = heuristic(next_state)

                child = Node(
                    state=next_state,
                    parent=current,
                    action=action,
                    g=tentative_g,
                    h=h_value
                )

                heappush(open_list, child)

    return None