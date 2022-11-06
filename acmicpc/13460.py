N = 0
M = 0
DR_ROW = { 'u': -1, 'r': 0, 'd': 1, 'l': 0 }
DR_COL = { 'u': 0, 'r': 1, 'd': 0, 'l': -1 }
DR_OPP = { 'u': 'd', 'd': 'u', 'r': 'l', 'l': 'r', '': '' }
history = set()
board = []
hole = []

# Index the board
indexed_board = []
row_edges_left = []
row_edges_right = []
col_edges_top = []
col_edges_bottom = []

def find(symbol, row):
    if symbol in row:
        return row.index(symbol)
    return -1

def index_board(board):
    global indexed_board, row_edges_left, row_edges_right, col_edges_top, col_edges_bottom

    # Prepare index
    for r in range(N):
        rr = []
        for c in range(M):
            rr.append([-1, -1])
        indexed_board.append(rr)
    
    # Row index board
    for r, row in enumerate(board):
        row_edges_left.append([])
        row_edges_right.append([])
        idx = 0
        for c, value in enumerate(row):
            if value in ['.', 'R', 'B']:
                if board[r][c-1] not in ['.', 'R', 'B']:
                    row_edges_left[r].append(c-1 if board[r][c-1] == 'O' else c)
                indexed_board[r][c][0] = idx
            elif value in ['#', 'O']:
                if board[r][max(c-1, 0)] not in ['#', 'O']:
                    row_edges_right[r].append(c if board[r][c] == 'O' else c-1)
                    idx += 1
    # Column index board
    for c in range(M):
        col_edges_top.append([])
        col_edges_bottom.append([])
        idx = 0
        for r in range(N):
            if board[r][c] in ['.', 'R', 'B']:
                if board[r-1][c] not in ['.', 'R', 'B']:
                    col_edges_top[c].append(r-1 if board[r-1][c] == 'O' else r)
                indexed_board[r][c][1] = idx
            elif board[r][c] in ['#', 'O']:
                if board[max(r-1, 0)][c] not in ['#', 'O']:
                    col_edges_bottom[c].append(r if board[r][c] == 'O' else r-1)
                    idx += 1

    # for ri, r in enumerate(indexed_board):
    #     for c in r:
    #         print(f"{c[0] if c[0] >= 0 else '-':>2}", end=" ")
    #     print(row_edges_left[ri], row_edges_right[ri])
    # for r in indexed_board:
    #     for c in r:
    #         print(f"{c[1] if c[1] >= 0 else '-':>2}", end=" ")
    #     print()
    # print(col_edges_top)
    # print(col_edges_bottom)

def move(marble, dr, other_marble):
    r, c = marble
    nr, nc = r, c
    if dr == 'l':
        nr = r
        idx = indexed_board[r][c][0]
        nc = row_edges_left[r][idx]
    elif dr == 'r':
        nr = r
        idx = indexed_board[r][c][0]
        nc = row_edges_right[r][idx]
    elif dr == 'u':
        nc = c
        idx = indexed_board[r][c][1]
        nr = col_edges_top[c][idx]
    elif dr == 'd':
        nc = c
        idx = indexed_board[r][c][1]
        nr = col_edges_bottom[c][idx]
    else:
        raise ValueError
    
    new_marble = [nr, nc]
    if is_at(new_marble, other_marble):
        new_marble = move_back_one(new_marble, dr)
    return new_marble

def move_back_one(marble, dr):
    return [marble[0] - DR_ROW[dr], marble[1] - DR_COL[dr]]

def is_at(a, b):
    return a[0] == b[0] and a[1] == b[1]

def is_in_hole(marble):
    return marble[0] == hole[0] and marble[1] == hole[1]

def is_in_way(marble, other_marble, dr):
    if marble[0] == other_marble[0]:
        if dr == 'l' and marble[1] < other_marble[1]:
            return True
        if dr == 'r' and marble[1] > other_marble[1]:
            return True
    if marble[1] == other_marble[1]:
        if dr == 'u' and marble[0] < other_marble[0]:
            return True
        if dr == 'd' and marble[0] > other_marble[0]:
            return True
    return False


def tilt(blue, red, dr):
    new_blue = blue
    new_red = red

    if is_in_way(blue, red, dr):
        new_blue = move(blue, dr, red)
        new_red = move(red, dr, new_blue)
    else:
        new_red = move(red, dr, blue)
        new_blue = move(blue, dr, new_red)
    
    moved = not(is_at(blue, new_blue) and is_at(red, new_red))

    return moved, new_blue, new_red

def solve(blue, red, cnt, last_dr = ''):
    index_board(board)

    cnts = []
    for dr in ['u', 'r', 'd', 'l']:
        if dr != DR_OPP[last_dr]:
            moved, new_blue, new_red = tilt(blue, red, dr)
            if moved:
                # debug(new_blue, new_red)
                position = tuple([*new_blue, *new_red])
                if position not in history:
                    if not is_in_hole(new_blue):
                        if is_in_hole(new_red):
                            cnts.append(cnt + 1)
                        else:
                            history.add(position)
                            res = solve(new_blue, new_red, cnt + 1, dr)
                            if res > 0:
                                cnts.append(res)
    
    return min(cnts) if len(cnts) > 0 else -1

def debug(blue, red):
    for ri, row in enumerate(board):
        for ci, val in enumerate(row):
            if is_at(blue, (ri, ci)):
                print('b', end=" ")
            elif is_at(red, (ri, ci)):
                print('r', end=" ")
            else:
                print(val if val in ['.', '#'] else '.', end=" ")
        print()
    print(blue, red)
    print()


def main():
    global N, M, board, hole
    N, M = [int(x) for x in input().split()]
    blue = []
    red = []

    for r in range(N):
        row = input()
        bc = find('B', row)
        rc = find('R', row)
        hc = find('O', row)
        if bc >= 0:
            blue = [r, bc]
        if rc >= 0:
            red = [r, rc]
        if hc >= 0:
            hole = [r, hc]
        board.append(row)
    
    # debug(blue, red)
    history.add(tuple([*blue,*red]))
    cnt = solve(blue, red, 0)
    print(cnt)

main()