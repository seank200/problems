UP    = -1,  0
DOWN  =  1,  0
LEFT  =  0, -1
RIGHT =  0,  1
DIRECTION_OPPOSITE = { LEFT: RIGHT, RIGHT: LEFT, UP: DOWN, DOWN: UP, None: None }
DIRECTION_NAME = { LEFT: 'LEFT', RIGHT: 'RIGHT', UP: 'UP', DOWN: 'DOWN' }
# history = set()
history = dict()

def parse_input():
    N, M = [int(x) for x in input().split()]
    board = []
    marbles = { 'R': [-1, -1], 'B': [-1, -1] }
    for r in range(N):
        row = input()
        board.append([])
        for c in range(M):
            if row[c] in ['R', 'B']:
                marbles[row[c]] = [r, c]
                board[r].append('.')
            else:
                board[r].append(row[c])
    return board, marbles

def index_board(board):
    board_index = []
    N = len(board)
    M = len(board[0])

    # Index horizontally
    hori_walls = []
    for r, row in enumerate(board):
        row_walls = []
        board_index.append([])
        for c, val in enumerate(row):
            board_index[r].append([-1, -1])
            if val == '#':
                if c == 0 or row[c-1] != '#':
                    # Start of wall
                    row_walls.append([c, -1])
                if c == M-1 or row[c+1] != '#':
                    # End of wall
                    row_walls[-1][1] = c
            elif val == 'O':
                row_walls.append([c, c])
            else:
                board_index[r][c][0] = len(row_walls)
        hori_walls.append(row_walls)
    
    # Index vertically
    vert_walls = []
    for c in range(M):
        col_walls = []
        for r in range(N):
            if board[r][c] == '#':
                if r == 0 or board[r-1][c] != '#':
                    # Start of wall
                    col_walls.append([r, -1])
                if r == N - 1 or board[r+1][c] != '#':
                    # End of wall
                    col_walls[-1][1] = r
            elif board[r][c] == 'O':
                col_walls.append([r, r])
            else:
                board_index[r][c][1] = len(col_walls)
        vert_walls.append(col_walls)
    return board_index, hori_walls, vert_walls

def already_visited(marbles, cnt):
    position = tuple([*marbles['R'], *marbles['B']])
    if position in history:
        return history[position] <= cnt
    return False

def add_history(marbles, cnt):
    global history
    history[tuple([*marbles['R'], *marbles['B']])] = cnt

def is_at(a, b):
    return a[0] == b[0] and a[1] == b[1]

def move_back_one(m, direction):
    return m[0] - direction[0], m[1] - direction[1]

def is_in_way(marble, direction, marbles):
    other_marble = 'B' if marble == 'R' else 'R'
    if marbles[marble][0] == marbles[other_marble][0]:
        if direction == LEFT and marbles[marble][1] < marbles[other_marble][1]:
            return True
        if direction == RIGHT and marbles[marble][1] > marbles[other_marble][1]:
            return True
    if marbles[marble][1] == marbles[other_marble][1]:
        if direction == UP and marbles[marble][0] < marbles[other_marble][0]:
            return True
        if direction == DOWN and marbles[marble][0] > marbles[other_marble][0]:
            return True
    return False

def is_in_hole(marble, marbles, board):
    r, c = marbles[marble]
    return board[r][c] == 'O'

def move(marble, direction, marbles, board, indexed_board):
    board_index, hori_walls, vert_walls = indexed_board
    mr , mc  = marbles[marble]
    nmr, nmc = marbles[marble]

    if direction == LEFT:
        nmc = hori_walls[nmr][board_index[nmr][nmc][0] - 1][1]
    elif direction == RIGHT:
        nmc = hori_walls[nmr][board_index[nmr][nmc][0]][0]
    elif direction == UP:
        nmr = vert_walls[nmc][board_index[nmr][nmc][1] - 1][1]
    else:
        nmr = vert_walls[nmc][board_index[nmr][nmc][1]][0]
    other_marble = 'B' if marble == 'R' else 'R'
    while (is_at((nmr, nmc), marbles[other_marble]) and board[nmr][nmc] != 'O') or board[nmr][nmc] == '#':
        # print("MOVING BACK", marble, DIRECTION_NAME[direction])
        nmr, nmc = move_back_one((nmr, nmc), direction)
    marbles[marble][0] = nmr
    marbles[marble][1] = nmc
    return not is_at((mr, mc), marbles[marble]) # Moved?

def solve(board, marbles, indexed_board, cnt = 0, last_direction = None):
    original_marbles = {'R': marbles['R'][:], 'B': marbles['B'][:] }

    min_cnt = None
    for direction in UP, DOWN, LEFT, RIGHT:
        if direction != DIRECTION_OPPOSITE[last_direction]:
            marbles['R'][0], marbles['R'][1] = original_marbles['R']
            marbles['B'][0], marbles['B'][1] = original_marbles['B']
            if is_in_way('R', direction, marbles):
                moved_r = move('R', direction, marbles, board, indexed_board)
                moved_b = move('B', direction, marbles, board, indexed_board)
            else:
                moved_b = move('B', direction, marbles, board, indexed_board)
                moved_r = move('R', direction, marbles, board, indexed_board)
            moved = moved_r or moved_b
            if moved:
                if not already_visited(marbles, cnt + 1):
                    add_history(marbles, cnt + 1)
                    if not is_in_hole('B', marbles, board):
                        if is_in_hole('R', marbles, board):
                            if min_cnt == None or cnt + 1 < min_cnt:
                                min_cnt = cnt + 1
                        else:
                            sol = solve(board, marbles, indexed_board, cnt + 1, direction)
                            if sol and (min_cnt == None or sol < min_cnt):
                                min_cnt = sol
    marbles['R'][0], marbles['R'][1] = original_marbles['R']
    marbles['B'][0], marbles['B'][1] = original_marbles['B']
    
    return min_cnt

def debug(board, marbles):
    for r, row in enumerate(board):
        for c, val in enumerate(row):
            if is_at((r, c), marbles['R']):
                print('R', end=" ")
            elif is_at((r, c), marbles['B']):
                print('B', end=" ")
            else:
                print(val, end=" ")
        print()
    print()
            

def main():
    board, marbles = parse_input()
    sol = solve(board, marbles, index_board(board))
    print(-1 if sol == None else sol)

main()