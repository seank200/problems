import sys
input = sys.stdin.readline

N, M = [int(x) for x in input().split(" ")]
numbers = []
for r in range(N):
    row = [int(x) for x in input().split(" ")]
    numbers.append(row)

tetrominos = [
    # I
    [(0, 0), (0, 1), (0, 2), (0, 3)],
    [(0, 0), (1, 0), (2, 0), (3, 0)],
    
    # Square
    [(0, 0), (0, 1), (1, 0), (1, 1)],
    
    # L
    [(0, 0), (1, 0), (2, 0), (2, 1)],
    [(1, 0), (0, 0), (0, 1), (0, 2)],
    [(0, 0), (0, 1), (1, 1), (2, 1)],
    [(1, 0), (1, 1), (1, 2), (0, 2)],
    [(2, 0), (0, 1), (1, 1), (2, 1)],
    [(0, 0), (1, 0), (1, 1), (1, 2)],
    [(0, 0), (1, 0), (2, 0), (0, 1)],
    [(0, 0), (0, 1), (0, 2), (1, 2)],
    
    # N
    [(0, 0), (1, 0), (1, 1), (2, 1)],
    [(1, 0), (1, 1), (0, 1), (0, 2)],
    [(0, 1), (1, 1), (1, 0), (2, 0)],
    [(0, 0), (0, 1), (1, 1), (1, 2)],

    # T
    [(0, 0), (0, 1), (0, 2), (1, 1)],
    [(0, 0), (1, 0), (2, 0), (1, 1)],
    [(0, 1), (1, 0), (1, 1), (1, 2)],
    [(1, 0), (0, 1), (1, 1), (2, 1)]
]


max_sum = 0
for trmn in tetrominos:
    for i in range(N):
        for j in range(M):
            try:
                sum = 0
                for r, c in trmn:
                    sum += numbers[i + r][j + c]
                if sum > max_sum:
                    max_sum = sum
            except IndexError:
                pass

print(max_sum)
