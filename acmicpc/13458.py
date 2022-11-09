import math

def solve(N, A, B, C):
    num = len(A)

    A = [x - B for x in A]

    for n in A:
        if n > 0:
            num += math.ceil(n / C)

    return num

def main():
    N = int(input())
    A = [int(x) for x in input().split(" ")]
    B, C = [int(x) for x in input().split(" ")]
    ans = solve(N, A, B, C)
    print(ans)

main()
