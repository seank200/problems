import sys, collections
sys.setrecursionlimit(10 ** 6)
input = sys.stdin.readline

N = int(input())
population = [int(x) for x in input().split(" ")]
adj = collections.defaultdict(list)
for _ in range(N - 1):
    u, v = [int(x) for x in input().split(" ")]
    adj[u - 1].append(v - 1)
    adj[v - 1].append(u - 1)

visited = [False] * N
dp = []
for i in range(N):
    dp.append([0, population[i]])

def dfs(current: int):
    visited[current] = True
    for u in adj[current]:
        if visited[u]:
            continue
        dfs(u)
        dp[current][0] += max(dp[u][0], dp[u][1])
        dp[current][1] += dp[u][0]

dfs(0)
print(max(dp[0]))
