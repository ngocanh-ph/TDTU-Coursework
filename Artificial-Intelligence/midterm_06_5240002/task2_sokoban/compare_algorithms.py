import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
from common.search.astar import astar
from common.search.bfs import Search
from sokoban_state import SokobanState
from sokoban_heuristic import SokobanHeuristic


# ===== MAP TEST =====
level1 = [
    "%%%%%",
    "%A B%",
    "% D %",
    "%%%%%"
]

level2 = [
    "%%%%%%%",
    "%A    %",
    "% BBB %",
    "% DDD %",
    "%%%%%%%"
]

level3 = [
    "%%%%%%%%",
    "%A     %",
    "% BBBB %",
    "% DDDD %",
    "%%%%%%%%"
]

# ===== LOAD MAP =====
def load_map(level):
    grid=[]
    player=None
    boxes=[]
    goals=[]
    for y,row in enumerate(level):
        grid_row=[]
        for x,c in enumerate(row):
            if c=='%':
                grid_row.append('%')
            else:
                grid_row.append(' ')
            if c=='A':
                player=(x,y)
            if c=='B':
                boxes.append((x,y))
            if c=='D':
                goals.append((x,y))
            if c=='C':
                boxes.append((x,y))
                goals.append((x,y))
        grid.append(grid_row)
    return grid,player,boxes,goals

# ===== RUN A* EXPERIMENT =====
def run_astar_experiment(level, heuristic_func, name):
    grid, player, boxes, goals = load_map(level)
    start_state = SokobanState(grid, player, boxes)

    metrics = {}

    start_time = time.time()

    result = astar(
        start_state,
        lambda state: state.is_goal(goals),
        SokobanState.get_neighbors,
        lambda state: heuristic_func(state, goals),
        metrics=metrics
    )

    end_time = time.time()

    runtime = end_time - start_time

    if not result:
        print(f"  {name:<20} | No solution")
        return

    path, cost, nodes = result

    print(f"  {name:<20} | Nodes: {metrics['nodes_expanded']:>6} | Frontier: {metrics['max_frontier']:>6} | Time: {runtime:.4f}s")


# ===== RUN BFS EXPERIMENT =====
def run_bfs_experiment(level):
    grid, player, boxes, goals = load_map(level)
    start_state = SokobanState(grid, player, boxes)

    goal_set = set()
    # Tạo tập goal states cho BFS: state mà tất cả box nằm trên goal
    # BFS cần goal_test khác: dùng goal_test function
    search = Search()

    start_time = time.time()

    # Sử dụng BFS với goal_test tùy chỉnh
    # Vì bfs() nhận goal_states là set, ta cần wrap lại
    class BFSGoalWrapper:
        """Wrapper để bfs() có thể dùng `state in goal_states` check"""
        def __contains__(self, state):
            return state.is_goal(goals)

    result = search.bfs(start_state, BFSGoalWrapper(), SokobanState.get_neighbors)

    end_time = time.time()

    runtime = end_time - start_time

    if not result:
        print(f"  {'BFS':<20} | No solution")
        return

    print(f"  {'BFS':<20} | Nodes: {search.nodes_expanded:>6} | Frontier: {search.max_frontier_size:>6} | Time: {runtime:.4f}s")


# ===== MAIN =====
if __name__ == "__main__":

    levels = [
        ("Level 1", level1),
        ("Level 2", level2),
        ("Level 3", level3)
    ]

    heuristics = [
        ("A*(Count)", SokobanHeuristic.box_count_heuristic),
        ("A*(Deadlock)", SokobanHeuristic.deadlock_heuristic),
        ("A*(Improved)", SokobanHeuristic.improved_heuristic),
    ]

    for level_name, level in levels:
        print(f"\n===== {level_name} =====")

        for h_name, h_func in heuristics:
            run_astar_experiment(level, h_func, f"{h_name}")

        # BFS comparison
        run_bfs_experiment(level)