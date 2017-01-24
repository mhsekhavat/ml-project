def generate_state_three_mins(map_size):
    states = []
    index = 0
    for i in range(0, map_size * map_size):
        for j in range(i + 1, map_size * map_size):
            for k in range(j + 1, map_size * map_size):
                index += 1
                print[(i / map_size, i % map_size), (j / map_size, j % map_size), (k / map_size, k % map_size)]
                states.append(
                    [(i / map_size, i % map_size), (j / map_size, j % map_size), (k / map_size, k % map_size)])
    print(index)
    return states


def generate_state_four_mins(map_size):
    states = []
    for i in range(0, map_size * map_size):
        for j in range(i + 1, map_size * map_size):
            for k in range(j + 1, map_size * map_size):
                for w in range(k + 1, map_size * map_size):
                    states.append(
                        [(i / map_size, i % map_size), (j / map_size, j % map_size), (k / map_size, k % map_size)])
    return states


def exist_uncover_around_tile(board, x, y):
    if y != 0 and x != 0:
        if board[x - 1][y - 1] < 0:
            return True
    if y != 0:
        if board[x][y - 1] < 0:
            return True
    if y != 0 and x != len(board) - 1:
        if board[x + 1][y - 1] < 0:
            return True
    if x != 0:
        if board[x - 1][y] < 0:
            return True
    if x != len(board) - 1:
        if board[x + 1][y] < 0:
            return True
    if x != 0 and y != len(board[0]) - 1:
        if board[x - 1][y + 1] < 0:
            return True
    if y != len(board[0]) - 1:
        if board[x][y + 1] < 0:
            return True
    if x != len(board) - 1 and y != len(board[0]) - 1:
        if board[x + 1][y + 1] < 0:
            return True
    return False


def right_is_frontier(board, pos):
    pass


def left_is_frontier(board, pos):
    pass


def top_is_frontier(board, pos):
    pass


def bo_is_frontier(board, pos):
    pass


def represent_state(board):
    start_pos = (0, 0)
    state_name = ""
    for y in range(0, len(board)):
        for x in range(0, len(board[y])):
            if board[y][x] >= 0:
                if exist_uncover_around_tile(board=board, x=x, y=y):
                    start_pos = (x, y)
    state_name = str(start_pos[0]) + str(start_pos[1])
    currentPos = (start_pos[0], start_pos[1])
    while True:
        if right_is_frontier(board, currentPos):
            pass
