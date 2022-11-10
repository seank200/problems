import sys
input = sys.stdin.readline
N = int(input())
A = set([int(x) for x in input().split(" ")])
M = int(input())
B = [int(x) for x in input().split(" ")]
for b in B:
    print(1 if b in A else 0)
