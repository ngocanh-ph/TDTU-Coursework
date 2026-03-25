"""
PuzzleHeuristic — Heuristic cho bài toán 8-Puzzle

Admissibility & Consistency:

1. Misplaced Tiles (h1):
   - Admissible: Mỗi ô sai vị trí cần ÍT NHẤT 1 bước để đưa về đúng chỗ,
     do đó h1 luôn <= chi phí thực tế → admissible.
   - Consistent: Di chuyển 1 bước chỉ có thể sửa tối đa 1 ô sai vị trí,
     nên |h1(n) - h1(n')| <= 1 = c(n, n') → consistent.

2. Gaschnig Heuristic (h2):
   - Admissible: Gaschnig đếm số lần swap tối thiểu với ô trống để đạt goal.
     Vì mỗi swap tương ứng 1 bước di chuyển hợp lệ, và Gaschnig cho phép
     swap với BẤT KỲ ô nào (không bị ràng buộc kề cạnh), nên số swap
     luôn <= số bước di chuyển thực tế → admissible.
   - Consistent: Mỗi bước di chuyển thực tế thay đổi tối đa 1 swap cần thiết,
     nên h2(n) - h2(n') <= c(n, n') → consistent.
"""


class PuzzleHeuristic:
    @staticmethod
    def misplaced_tiles(current_state, goal_state):
        """
        Heuristic 1: Misplaced Tiles
        Đếm số ô sai vị trí (không tính ô trống)
        """
        count = 0
        for i in range(len(current_state)):
            if current_state[i] != 0 and current_state[i] != goal_state[i]:
                count += 1
        return count

    @staticmethod
    def gaschnig_heuristic(current_state, goal_state):
        """
        Heuristic 2: Gaschnig
        - Cho phép swap ô trống với bất kỳ tile nào
        - Đếm số bước cần để đưa về trạng thái đích
        """
        current = list(current_state)  
        goal = list(goal_state)

        steps = 0

        while current != goal:
            blank_index = current.index(0)

            # Nếu vị trí của blank chưa đúng
            if goal[blank_index] != 0:
                target_value = goal[blank_index]
                target_index = current.index(target_value)

                # swap blank với tile đúng
                current[blank_index], current[target_index] = (
                    current[target_index],
                    current[blank_index],
                )
            else:
                # blank đúng chỗ nhưng puzzle chưa hoàn thành
                for i in range(len(current)):
                    if current[i] != goal[i]:
                        current[blank_index], current[i] = current[i], current[blank_index]
                        break

            steps += 1

        return steps

    @staticmethod
    def get_heuristic(name):
    
        if name == "misplaced":
            return PuzzleHeuristic.misplaced_tiles
        elif name == "gaschnig":
            return PuzzleHeuristic.gaschnig_heuristic
        else:
            raise ValueError("Heuristic không hợp lệ! Chọn 'misplaced' hoặc 'gaschnig'")