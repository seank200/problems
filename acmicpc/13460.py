import sys
input = sys.stdin.readline
N, M = [int(x) for x in input().split(" ")]
board = []
red = None
blue = None
dx = { 'l': -1, 'r': 1, 'u': 0, 'd': 0 }
dy = { 'l': 0, 'r': 0, 'u': -1, 'd': 1 }

for i in range(N):
    board.append([])
    row = input()
    for j in range(M):
        if row[j] == 'R':
            red = [i, j]
            board[i].append('.')
        elif row[j] == 'B':
            blue = [i, j]
            board[i].append('.')
        else:
            board[i].append(row[j])


def can_move(pos):
    return board[pos[0]][pos[1]] not in ('#', 'O')


def is_hole(pos):
    return board[pos[0]][pos[1]] == 'O'


def is_same(a, b):
    return a[0] == b[0] and a[1] == b[1]


def move(marble, d):
    marble[0] += dy[d]
    marble[1] += dx[d]


def move_back(marble, d):
    marble[0] -= dy[d]
    marble[1] -= dx[d]


def bfs():
    if cnt > 10:
        return -1
    
    min_moves = -1
    d_history = []
    marble_history = [(*red, *blue)]
    visited = dict()
    
    while len(marble_history):
        for d in 'l', 'r', 'u', 'd':
            if len(d_history) > 0 and d == d_history[-1]:
                continue

            moved_r = 0
            moved_b = 0

            while can_move(red):
                move(red, d)
                moved_r += 1
            if is_wall(red):
                move_back(red, d)
                moved_r -= 1

            while can_move(blue):
                move(blue, d)
                moved_b += 1
            if is_wall(blue);
                move_back(blue, d)
                moved_b -= 1
            
            if moved_r > 0 or moved_b > 0:
                if is_hole(red):
                    if is_hole(blue):
                        # both marbles in hole
                        continue
                    else:
                        # red marble in hole!
                        moves = len(d_history)
                        if moves < min_moves:
                            min_moves = moves
                        continue
                
                if is_hole(blue):
                    continue

                if is_same(red, blue):
                if moved_r > moved_b:
                        move_back(red, d)
                        moved_r -= 1
                    else:
                        move_back(blue, d)
                        moved_b -= 1

                if moved_r > 0 or moved_b > 0:
                    last_moves = visited.get((*red, *blue), 11):
                    moves = len(d_history)
                    
                    if moves < last_moves:
                        visited[(*red, *blue)] = moves
                        d_history.append(d)
                        marble_history.append((*red, *blue))


