"""
SokobanHeuristic — Heuristic cho bài toán Sokoban

Admissibility & Consistency:

1. Box Count Heuristic (h1):
   - Admissible: Đếm số hộp chưa nằm trên goal. Mỗi hộp sai vị trí cần
     ít nhất 1 bước đẩy để đưa vào goal, nên h1 luôn <= chi phí thực tế → admissible.
   - Consistent: Mỗi bước di chuyển chỉ có thể đẩy tối đa 1 hộp vào goal,
     nên h1(n) - h1(n') <= 1 = c(n, n') → consistent.

2. Deadlock Heuristic (h2):
   - Admissible: Trả về 0 (nếu không deadlock) hoặc inf (nếu deadlock).
     Khi deadlock thì thực sự không có lời giải → chi phí = inf → admissible.
     Khi không deadlock, h=0 <= mọi chi phí → admissible.
   - KHÔNG consistent: h có thể nhảy từ 0 lên inf giữa 2 state kề nhau.

3. Improved Heuristic (h3 = h1 + h2):
   - Admissible: Là max(h1, h2) thực chất — nếu deadlock thì inf (đúng),
     nếu không thì trả h1 (admissible) → admissible.
   - Tổ hợp cho kết quả tốt nhất trong thực tế.
"""


class SokobanHeuristic:

    @staticmethod
    def box_count_heuristic(state, goals):
        return sum(1 for box in state.boxes if box not in goals)

    @staticmethod
    def deadlock_heuristic(state, goals):
        for (x, y) in state.boxes:
            if (x, y) not in goals:
                if (state.grid[y-1][x] == '%' and state.grid[y][x-1] == '%') or \
                   (state.grid[y-1][x] == '%' and state.grid[y][x+1] == '%') or \
                   (state.grid[y+1][x] == '%' and state.grid[y][x-1] == '%') or \
                   (state.grid[y+1][x] == '%' and state.grid[y][x+1] == '%'):
                    return float('inf')
        return 0

    @staticmethod
    def improved_heuristic(state, goals):
        count = 0
        for (x, y) in state.boxes:
            if (x, y) not in goals:
                count += 1
                if (state.grid[y-1][x] == '%' and state.grid[y][x-1] == '%') or \
                   (state.grid[y-1][x] == '%' and state.grid[y][x+1] == '%') or \
                   (state.grid[y+1][x] == '%' and state.grid[y][x-1] == '%') or \
                   (state.grid[y+1][x] == '%' and state.grid[y][x+1] == '%'):
                    return float('inf')
        return count

    @staticmethod
    def get_heuristic(name):
        if name == "count":
            return SokobanHeuristic.box_count_heuristic
        elif name == "deadlock":
            return SokobanHeuristic.deadlock_heuristic
        elif name == "improved":
            return SokobanHeuristic.improved_heuristic
        else:
            raise ValueError("Heuristic không hợp lệ!")