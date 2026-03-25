import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import threading
import pygame
from common.search.astar import astar
from sokoban_state import SokobanState
from sokoban_heuristic import SokobanHeuristic
from sokoban_gui import draw_grid

TILE_SIZE = 64


# ĐỌC MAP TỪ FILE 
def load_map_from_file(filepath):
    with open(filepath, 'r') as f:
        return [line.rstrip('\n') for line in f.readlines()]


# PARSE MAP 
def load_map(level):
    grid = []
    player = None
    boxes = []
    goals = []
    for y, row in enumerate(level):
        grid_row = []
        for x, c in enumerate(row):
            if c == '%':
                grid_row.append('%')
            else:
                grid_row.append(' ')
            if c == 'A':
                player = (x, y)
            if c == 'B':
                boxes.append((x, y))
            if c == 'D':
                goals.append((x, y))
            if c == 'C':
                boxes.append((x, y))
                goals.append((x, y))
        grid.append(grid_row)
    return grid, player, boxes, goals


# DI CHUYỂN THỦ CÔNG 
def move_player(grid, player, boxes, dx, dy):
    px, py = player
    nx, ny = px + dx, py + dy
    if grid[ny][nx] == '%':
        return player, boxes
    if (nx, ny) in boxes:
        bx, by = nx + dx, ny + dy
        if grid[by][bx] == '%' or (bx, by) in boxes:
            return player, boxes
        boxes = [(bx, by) if (x, y) == (nx, ny) else (x, y) for x, y in boxes]
        return (nx, ny), boxes
    return (nx, ny), boxes


# MENU 
def menu(screen):
    clock = pygame.time.Clock()
    options = ["PLAY", "AUTO"]
    selected = 0
    font = pygame.font.SysFont(None, 60)
    small_font = pygame.font.SysFont(None, 30)
    running = True

    while running:
        screen.fill((30, 30, 30))

        title = pygame.font.SysFont(None, 80).render("SOKOBAN", True, (255, 215, 0))
        screen.blit(title, title.get_rect(center=(screen.get_width() // 2, 100)))

        hint = small_font.render("Use arrow keys to select, Enter to confirm", True, (180, 180, 180))
        screen.blit(hint, hint.get_rect(center=(screen.get_width() // 2, 160)))

        for i, opt in enumerate(options):
            color = (255, 255, 0) if i == selected else (255, 255, 255)
            text = font.render(opt, True, color)
            rect = text.get_rect(center=(screen.get_width() // 2, 240 + i * 80))
            if i == selected:
                pygame.draw.rect(screen, (60, 60, 60),
                                 rect.inflate(20, 10), border_radius=8)
            screen.blit(text, rect)

        pygame.display.flip()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_LEFT]:
                    selected = (selected - 1) % len(options)
                elif event.key in [pygame.K_DOWN, pygame.K_RIGHT]:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    return options[selected].lower()


# LOADING SCREEN (hiển thị khi A* đang chạy)
def show_loading(screen, message="Solving with A*..."):
    font = pygame.font.SysFont(None, 48)
    small = pygame.font.SysFont(None, 30)
    screen.fill((30, 30, 30))
    text = font.render(message, True, (255, 255, 255))
    screen.blit(text, text.get_rect(center=(screen.get_width() // 2,
                                            screen.get_height() // 2 - 20)))
    hint = small.render("Vui lòng chờ...", True, (180, 180, 180))
    screen.blit(hint, hint.get_rect(center=(screen.get_width() // 2,
                                            screen.get_height() // 2 + 30)))
    pygame.display.flip()


# MAIN 
def main():
    # Set working directory về folder chứa file này
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Đọc map từ file
    level = load_map_from_file("example_map.txt")

    pygame.init()

    # Tính kích thước màn hình theo map
    level_w = max(len(row) for row in level)
    level_h = len(level)
    width = max(level_w * TILE_SIZE, 400)
    height = max(level_h * TILE_SIZE, 400)

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Sokoban")

    # Hiển thị menu
    mode = menu(screen)

    # Parse map
    grid, player, boxes, goals = load_map(level)
    goal_set = set(goals)

    solution = None

    #CHẾ ĐỘ AUTO 
    if mode == "auto":
        show_loading(screen, "Đang tìm lời giải A*...")

        start_state = SokobanState(grid, player, boxes)
        heuristic_func = SokobanHeuristic.get_heuristic("improved")

        # Chạy A* trên thread riêng để không đóng băng pygame
        result_container = [None]
        def run_astar():
            result_container[0] = astar(
                start_state,
                lambda state: state.is_goal(goals),
                SokobanState.get_neighbors,
                lambda state: heuristic_func(state, goals)
            )

        t = threading.Thread(target=run_astar, daemon=True)
        t.start()

        # Vẽ loading animation trong khi chờ
        dot_count = 0
        clock_loading = pygame.time.Clock()
        while t.is_alive():
            dots = "." * (dot_count % 4)
            show_loading(screen, f"Solving with A*{dots}")
            dot_count += 1
            clock_loading.tick(2)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

        t.join()
        result = result_container[0]

        if not result:
            # Hiển thị thông báo không tìm được khi thay đổi expample_map phức tạp
            font_err = pygame.font.SysFont(None, 48)
            screen.fill((30, 30, 30))
            msg = font_err.render("No solution found!", True, (255, 80, 80))
            screen.blit(msg, msg.get_rect(center=(width // 2, height // 2)))
            pygame.display.flip()
            pygame.time.wait(3000)
            pygame.quit()
            return

        path, cost, nodes = result

        # In ra console 
        actions = [action for action, state in path if action is not None]
        print(f"\n{'='*50}")
        print(f"Lời giải tìm được: {len(actions)} bước")
        print(f"Tổng chi phí: {cost}")
        print(f"Số node mở rộng: {nodes}")
        print(f"Actions: {actions}")
        print(f"{'='*50}\n")

        solution = [state for action, state in path]

    # GAME LOOP
    clock = pygame.time.Clock()
    running = True
    index = 0
    font_ui = pygame.font.SysFont(None, 42)
    game_won = False

    while running:
        screen.fill((0, 0, 0))

        # Render
        if mode == "auto" and solution:
            if index < len(solution):
                current_state = solution[index]
                index += 1
            else:
                current_state = solution[-1]
            draw_grid(screen, current_state.grid, current_state.player,
                      current_state.boxes, goals)

            # Kiểm tra thắng
            if all(b in goal_set for b in current_state.boxes):
                game_won = True
        else:
            draw_grid(screen, grid, player, boxes, goals)

            # Kiểm tra thắng (manual)
            if all(b in goal_set for b in boxes):
                game_won = True

        # Hiển thị "You Win!"
        if game_won:
            overlay = pygame.Surface((width, 60), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            screen.blit(overlay, (0, 0))
            win_text = font_ui.render("You Win!", True, (0, 220, 100))
            screen.blit(win_text, win_text.get_rect(center=(width // 2, 30)))

        pygame.display.flip()

        # Tốc độ: PLAY=30fps, AUTO=3fps 
        if mode == "play":
            clock.tick(30)
        else:
            clock.tick(3)

        # Xử lý input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # Nhấn R để chơi lại
                if event.key == pygame.K_r:
                    main()
                    return
                # Di chuyển thủ công
                if mode == "play" and not game_won:
                    if event.key == pygame.K_LEFT:
                        player, boxes = move_player(grid, player, boxes, -1, 0)
                    elif event.key == pygame.K_RIGHT:
                        player, boxes = move_player(grid, player, boxes, 1, 0)
                    elif event.key == pygame.K_UP:
                        player, boxes = move_player(grid, player, boxes, 0, -1)
                    elif event.key == pygame.K_DOWN:
                        player, boxes = move_player(grid, player, boxes, 0, 1)

    pygame.quit()


if __name__ == "__main__":
    main()