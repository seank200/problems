import sys

N = int(sys.stdin.readline())
S = []
for i in range(N):
    S.append([int(x) for x in sys.stdin.readline().split(" ")])

min_diff = 99999999
selected = [False] * N
start_members = []

for i in range(N):
    for j in range(i+1, N):
        S[i][j] += S[j][i]

def dfs(idx, depth):
    global min_diff
    if depth == N // 2:
        start = 0
        link  = 0

        for i in range(N):
            for j in range(i + 1, N):
                if selected[i] and selected[j]:
                    start += S[i][j]
                elif not selected[i] and not selected[j]:
                    link += S[i][j]

        diff = abs(start - link)

        if diff < min_diff:
            min_diff = diff
        return
    for i in range(idx, N):
        if not selected[i]:
            if len(start_members) and start_members[-1] > i:
                continue
            start_members.append(i)
            selected[i] = True
            dfs(idx + 1, depth + 1)
            selected[i] = False
            start_members.pop()

dfs(0, 0)
print(min_diff)

