N = 0
M = 0
DR_ROW = { 'u': -1, 'r': 0, 'd': 1, 'l': 0 }
DR_COL = { 'u': 0, 'r': 1, 'd': 0, 'l': -1 }
DR_OPP = { 'u': 'd', 'd': 'u', 'r': 'l', 'l': 'r', '': '' }
history = set()

def find(symbol, row):
    if symbol in row:
        return row.index(symbol)
    return -1

def is_same(m1, m2):
    return m1[0] == m2[0] and m1[1] == m2[1]

def move_one(marble, dr, hole = None):
    if hole and is_same(marble, hole):
        return marble[:]
    return [marble[0] + DR_ROW[dr], marble[1] + DR_COL[dr]]

def can_move(board, marble, other_marble, dr):
    new_marble = move_one(marble, dr)
    if board[new_marble[0]][new_marble[1]] == '#':
        return False
    
    if is_same(new_marble, other_marble):
        new_other_marble = move_one(other_marble, dr)
        if board[new_other_marble[0]][new_other_marble[1]] == '#':
            return False
    
    return True

def move(board, marble, other_marble, hole, dr):
    can_marble_move = can_move(board, marble, other_marble, dr)
    can_other_marble_move = can_move(board, other_marble, marble, dr)
    while can_marble_move or can_other_marble_move:
        if can_marble_move:
            marble = move_one(marble, dr, hole)
        if can_other_marble_move:
            other_marble = move_one(other_marble, dr, hole)
        if is_same(marble, hole) and is_same(other_marble, hole):
            break
        can_marble_move = can_move(board, marble, other_marble, dr)
        can_other_marble_move = can_move(board, other_marble, marble, dr)
    return marble, other_marble

def tilt(dr, board, blue, red, hole):
    can_blue_move = can_move(board, blue, red, dr)
    can_red_move = can_move(board, red, blue, dr)

    if not can_blue_move and not can_red_move:
        return False, None, None
    
    moved = True
    new_blue, new_red = move(board, blue, red, hole, dr)

    return moved, new_blue, new_red

def solve(board, blue, red, hole, cnt, last_dr = ''):
    global history
    cnts = []

    for dr in ['u', 'r', 'd', 'l']:
        if dr != DR_OPP[last_dr]:
            moved, new_blue, new_red = tilt(dr, board, blue, red, hole)
            if moved:
                position = tuple([*new_blue, *new_red])
                if position not in history:
                    if not is_same(new_blue, hole):
                        if is_same(new_red, hole):
                            cnts.append(cnt + 1)
                        else:
                            history.add(position)
                            ans = solve(board, new_blue, new_red, hole, cnt + 1, dr)
                            if ans > 0:
                                cnts.append(ans)

    return min(cnts) if len(cnts) > 0 else -1

def debug(board, blue, red):
    global N, M
    b = []
    for r in range(N):
        rr = []
        for c in range(M):
            if board[r][c] in ['#', '.', 'O']:
                rr.append(board[r][c])
            else:
                rr.append('.')
        b.append(rr)
    
    b[blue[0]][blue[1]] = 'B'
    b[red[0]][red[1]] = 'R'

    for r in b:
        print(r)

def main():
    global N, M
    N, M = [int(x) for x in input().split()]

    board = []
    blue = []
    red = []
    hole = []

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
    
    cnt = solve(board, blue, red, hole, 0)
    print(cnt)

main()