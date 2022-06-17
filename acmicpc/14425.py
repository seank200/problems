import sys


getinput = sys.stdin.readline
output = lambda x: sys.stdout.write(f"{x}\n")

N, M = [int(x) for x in getinput().split(" ")]

strs = set()

for i in range(N):
    strs.add(getinput())

exists = 0
for i in range(M):
    if getinput() in strs:
        exists += 1

output(exists)