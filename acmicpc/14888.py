import sys

def dfs(order):
    global min_ans, max_ans

    if len(order) == N - 1:
        ans = A[0]
        for i, op in enumerate(order):
            if   op == 0: # +
                ans += A[i + 1]
            elif op == 1:
                ans -= A[i + 1]
            elif op == 2:
                ans *= A[i + 1]
            elif op == 3:
                is_negative = ans < 0
                ans = abs(ans) // A[i + 1]
                if is_negative:
                    ans *= -1
        if ans < min_ans:
            min_ans = ans
        if ans > max_ans:
            max_ans = ans
        return

    for i, op in enumerate(ops):
        if op > 0:
            order.append(i)
            ops[i] -= 1
            dfs(order)
            ops[i] += 1
            order.pop()

N = int(sys.stdin.readline())    
A = [int(x) for x in sys.stdin.readline().split(" ")]
ops = [int(x) for x in sys.stdin.readline().split(" ")]

min_ans = float('inf')
max_ans = float('-inf')
order = []

dfs(order)

print(max_ans)
print(min_ans)
