# https://programmers.co.kr/learn/courses/30/lessons/86052

move = ((1, 0), (0, -1), (-1, 0), (0, 1))
turn = {'L': 1, 'R': -1, 'S': 0}

def solution(grid):
    cycle_lengths = []
    visited = [[[False, False, False, False] for _ in row] for row in grid]    
    for y, row in enumerate(grid):
        for x, _ in enumerate(row):
            for d in range(4):
                if not visited[y][x][d]:
                    cycle_length = 0
                    i, j = x, y
                    while not visited[j][i][d]:
                        visited[j][i][d] = True
                        d = (d + turn[grid[j][i]]) % 4
                        i = (i + move[d][0]) % len(grid[0])
                        j = (j + move[d][1]) % len(grid)
                        cycle_length += 1
                    cycle_lengths.append(cycle_length)
    return sorted([x for x in cycle_lengths if x > 0])