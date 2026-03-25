goal_states=[
    ((1,2,3),(4,5,6),(7,8,0)),  
    ((8,7,6),(5,4,3),(2,1,0)),  
    ((0,1,2),(3,4,5),(6,7,8)),  
    ((0,8,7),(6,5,4),(3,2,1)),  
]

def is_goal(state):
    return state in goal_states

def get_neighbors(state):
    neighbors = []
    seen = set()
    r =-1
    c =-1
    
    # Tìm vị trí ô trống
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                r, c = i, j
                break
        if r != -1:
            break

    # Đi lên (UP)
    if r > 0:
        new_state = [list(row) for row in state]
        new_state[r][c], new_state[r-1][c] = new_state[r-1][c], new_state[r][c]
        neighbors.append(('UP', tuple(tuple(row) for row in new_state), 1))
        
    # Đi xuống (DOWN)
    if r < 2:
        new_state = [list(row) for row in state]
        new_state[r][c], new_state[r+1][c] = new_state[r+1][c], new_state[r][c]
        neighbors.append(('DOWN', tuple(tuple(row) for row in new_state), 1))
        
    # Đi trái (LEFT)
    if c > 0:
        new_state = [list(row) for row in state]
        new_state[r][c], new_state[r][c-1] = new_state[r][c-1], new_state[r][c]
        neighbors.append(('LEFT', tuple(tuple(row) for row in new_state), 1))
        
    # Đi phải (RIGHT)
    if c < 2:
        new_state = [list(row) for row in state]
        new_state[r][c], new_state[r][c+1] = new_state[r][c+1], new_state[r][c]
        neighbors.append(('RIGHT', tuple(tuple(row) for row in new_state), 1))

    # Đi chữ L (L-shaped)
    l_moves =[(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
    for dr, dc in l_moves:
        new_r, new_c = r + dr, c + dc
        if 0 <= new_r < 3 and 0 <= new_c < 3:
            new_state = [list(row) for row in state]
            new_state[r][c], new_state[new_r][new_c] = new_state[new_r][new_c], new_state[r][c]
            neighbors.append(('L-shaped', tuple(tuple(row) for row in new_state), 1))

    # Hoán đổi chia hết (Divisible Swap)
    for i in range(3):
        for j in range(3):
            val1 = state[i][j] 
            
            # Xét ô bên phải
            if j < 2:
                val2 = state[i][j+1]
                if val1 != 0 and val2 != 0 and (val1 % val2 == 0 or val2 % val1 == 0):
                    new_state = [list(row) for row in state]
                    new_state[i][j], new_state[i][j+1] = new_state[i][j+1], new_state[i][j]
                    neighbors.append(('Divisible Swap Right', tuple(tuple(row) for row in new_state), 1))

            # Xét ô bên dưới
            if i < 2:
                val3 = state[i+1][j]
                if val1 != 0 and val3 != 0 and (val1 % val3 == 0 or val3 % val1 == 0):
                    new_state = [list(row) for row in state]
                    new_state[i][j], new_state[i+1][j] = new_state[i+1][j], new_state[i][j]
                    neighbors.append(('Divisible Swap Down', tuple(tuple(row) for row in new_state), 1))
    
    # Nhảy qua đầu (Jump Over)
    jump_moves = [(-2, 0), (2, 0), (0, -2), (0, 2)]
    for dr, dc in jump_moves:
        new_r, new_c = r + dr, c + dc
        mid_r, mid_c = r + dr // 2, c + dc // 2
        if 0 <= new_r < 3 and 0 <= new_c < 3 and state[mid_r][mid_c] != 0:
            new_state = [list(row) for row in state]
            new_state[r][c], new_state[new_r][new_c] = new_state[new_r][new_c], new_state[r][c]
            neighbors.append(('Jump Over', tuple(tuple(row) for row in new_state), 1))
    return neighbors