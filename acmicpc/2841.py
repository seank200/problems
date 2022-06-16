from collections import deque
import sys

np = sys.stdin.readline()
N, P = [int(x) for x in np.split(" ")]

pressed = []
for i in range(N):
    pressed.append(deque())
moves = 0

for n in range(N):
    lp = sys.stdin.readline()
    l, p = [int(x) - 1 for x in lp.split(" ")]

    while len(pressed[l]) and pressed[l][-1] > p:
        pressed[l].pop()
        moves += 1
    
    if not(len(pressed[l]) and pressed[l][-1] == p):
        pressed[l].append(p)
        moves += 1
    
sys.stdout.write(str(moves))
