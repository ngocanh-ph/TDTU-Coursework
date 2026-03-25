import sys
import os
import time
import random

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.search.astar import astar
from common.search.bfs import Search
from task1_8puzzle.puzzle_state import is_goal, get_neighbors, goal_states
from task1_8puzzle.puzzle_heuristic import PuzzleHeuristic
from task1_8puzzle.search_tree_visualization import illustrate_search_tree


def flatten_state(state):
    """Chuyển state 2D thành 1D list"""
    return [val for row in state for val in row]


def unflatten_state(flat):
    """Chuyển 1D list thành state 2D tuple"""
    return tuple(tuple(flat[i*3:(i+1)*3]) for i in range(3))


def is_solvable(state):
    """Kiểm tra trạng thái có giải được không (tính số inversion)"""
    flat = flatten_state(state)
    inversions = 0
    for i in range(len(flat)):
        for j in range(i + 1, len(flat)):
            if flat[i] != 0 and flat[j] != 0 and flat[i] > flat[j]:
                inversions += 1
    return inversions % 2 == 0


def generate_random_state():
    """Sinh random trạng thái hợp lệ (solvable)"""
    tiles = list(range(9))
    while True:
        random.shuffle(tiles)
        state = unflatten_state(tiles)
        if is_solvable(state):
            return state


def get_best_goal(initial_state, heuristic):
    best_goal = None
    best_h = float('inf')

    for g in goal_states:
        h = heuristic(flatten_state(initial_state), flatten_state(g))
        if h < best_h:
            best_h = h
            best_goal = g

    return best_goal


def print_solution(result):
    if result is None:
        print("Không tìm thấy lời giải")
        return

    path, cost, expanded_nodes = result

    print("\nKết quả:")
    print(f"Số bước: {len(path) - 1}")
    print(f"Chi phí: {cost}")
    print(f"Số node mở rộng: {expanded_nodes}")

    print("\nĐường đi:")
    for step, (action, state) in enumerate(path):
        print(f"\nBước {step}: {action}")
        for row in state:
            print(row)


def run_astar(initial_state, heuristic_name, verbose=True):
    heuristic_func = PuzzleHeuristic.get_heuristic(heuristic_name)

    goal_state = get_best_goal(initial_state, heuristic_func)

    if verbose:
        print("\nGoal được chọn:")
        for row in goal_state:
            print(row)

    flat_goal = flatten_state(goal_state)
    heuristic = lambda s: heuristic_func(flatten_state(s), flat_goal)

    start_time = time.time()

    result = astar(
        start_state=initial_state,
        goal_test=is_goal,
        get_neighbors=get_neighbors,
        heuristic=heuristic
    )

    end_time = time.time()

    if result:
        path, cost, expanded_nodes = result
        return path, cost, expanded_nodes, end_time - start_time
    else:
        return None


def run_bfs(initial_state):
    """Chạy BFS cho 8-Puzzle"""
    search = Search()

    start_time = time.time()
    result = search.bfs(initial_state, set(goal_states), get_neighbors)
    end_time = time.time()

    if result:
        path = result.get_path()
        cost = result.g
        return path, cost, search.nodes_expanded, search.max_frontier_size, end_time - start_time
    else:
        return None

# YC4: Thí nghiệm random so sánh hiệu quả 2 heuristic
def experiment_random_compare(n_tests=20):
    """
    Sinh random n_tests trạng thái ban đầu, chạy A* với 2 heuristic,
    thu thập và in bảng so sánh average path cost, nodes expanded, time.
    """
    print("\n" + "="*70)
    print("THÍ NGHIỆM: So sánh hiệu quả 2 heuristic trên random states")
    print(f"Số test cases: {n_tests}")
    print("="*70)

    stats = {
        "misplaced": {"cost": [], "nodes": [], "time": []},
        "gaschnig":  {"cost": [], "nodes": [], "time": []},
    }

    for i in range(n_tests):
        state = generate_random_state()
        print(f"\nTest {i+1}: {flatten_state(state)}")

        for name in ["misplaced", "gaschnig"]:
            result = run_astar(state, name, verbose=False)
            if result:
                path, cost, expanded, t = result
                stats[name]["cost"].append(cost)
                stats[name]["nodes"].append(expanded)
                stats[name]["time"].append(t)
            else:
                print(f"  {name}: Không tìm thấy lời giải")

    # In bảng kết quả
    print("\n" + "="*70)
    print(f"{'Metric':<25} {'Misplaced':>15} {'Gaschnig':>15}")
    print("-"*55)

    for metric_name, key in [("Avg Path Cost", "cost"), ("Avg Nodes Expanded", "nodes"), ("Avg Time (s)", "time")]:
        vals_m = stats["misplaced"][key]
        vals_g = stats["gaschnig"][key]
        avg_m = sum(vals_m) / len(vals_m) if vals_m else 0
        avg_g = sum(vals_g) / len(vals_g) if vals_g else 0
        print(f"{metric_name:<25} {avg_m:>15.4f} {avg_g:>15.4f}")

    print("="*70)


# YC8: Thí nghiệm so sánh A* (2 heuristic) vs BFS
def experiment_astar_vs_bfs(n_tests=10):
    """
    So sánh time & space complexity giữa A*(misplaced), A*(gaschnig), BFS.
    """
    print("\n" + "="*70)
    print("THÍ NGHIỆM: So sánh A* (2 heuristic) vs BFS")
    print(f"Số test cases: {n_tests}")
    print("="*70)

    stats = {
        "A*(misplaced)": {"nodes": [], "time": []},
        "A*(gaschnig)":  {"nodes": [], "time": []},
        "BFS":           {"nodes": [], "frontier": [], "time": []},
    }

    for i in range(n_tests):
        state = generate_random_state()
        print(f"\nTest {i+1}: {flatten_state(state)}")

        # A* misplaced
        r1 = run_astar(state, "misplaced", verbose=False)
        if r1:
            stats["A*(misplaced)"]["nodes"].append(r1[2])
            stats["A*(misplaced)"]["time"].append(r1[3])

        # A* gaschnig
        r2 = run_astar(state, "gaschnig", verbose=False)
        if r2:
            stats["A*(gaschnig)"]["nodes"].append(r2[2])
            stats["A*(gaschnig)"]["time"].append(r2[3])

        # BFS
        r3 = run_bfs(state)
        if r3:
            path, cost, nodes_exp, max_frontier, t = r3
            stats["BFS"]["nodes"].append(nodes_exp)
            stats["BFS"]["frontier"].append(max_frontier)
            stats["BFS"]["time"].append(t)

    # In bảng kết quả
    print("\n" + "="*70)
    print(f"{'Algorithm':<20} {'Avg Nodes':>12} {'Avg Frontier':>14} {'Avg Time(s)':>14}")
    print("-"*60)

    for algo in ["A*(misplaced)", "A*(gaschnig)", "BFS"]:
        nodes = stats[algo]["nodes"]
        times = stats[algo]["time"]
        frontiers = stats[algo].get("frontier", [])

        avg_n = sum(nodes) / len(nodes) if nodes else 0
        avg_t = sum(times) / len(times) if times else 0
        avg_f = sum(frontiers) / len(frontiers) if frontiers else float('nan')

        print(f"{algo:<20} {avg_n:>12.1f} {avg_f:>14.1f} {avg_t:>14.6f}")

    print("="*70)


def main():
    initial_state = (
        (1, 8, 2),
        (0, 4, 3),
        (7, 6, 5)
    )

    print("Trạng thái ban đầu:")
    for row in initial_state:
        print(row)

    # Heuristic 1
    print("\nA* - Misplaced Tiles Heuristic")
    result1 = run_astar(initial_state, "misplaced")

    if result1:
        path, cost, expanded, t = result1
        print_solution((path, cost, expanded))
        print(f"Thời gian: {t:.6f}s")

    # Heuristic 2
    print("\nA* - Gaschnig Heuristic")
    result2 = run_astar(initial_state, "gaschnig")

    if result2:
        path, cost, expanded, t = result2
        print_solution((path, cost, expanded))
        print(f"Thời gian: {t:.6f}s")

    # So sánh
    print("\nSo sánh:")
    if result1 and result2:
        print(f"Misplaced -> nodes: {result1[2]}, time: {result1[3]:.6f}")
        print(f"Gaschnig  -> nodes: {result2[2]}, time: {result2[3]:.6f}")

    # Visualization
    print("\nVẽ cây tìm kiếm (15 node):")
    illustrate_search_tree(initial_state, n_limit=15)

    # ===== THÍ NGHIỆM =====
    experiment_random_compare(n_tests=20)
    experiment_astar_vs_bfs(n_tests=10)


if __name__ == "__main__":
    main()