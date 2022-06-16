from collections import deque

T = int(input())

for i in range(T):
    p = input().replace('RR', '')
    n = int(input())
    li = [int(x) for x in input()[1:-1].split(",") if x]

    dq = deque(li)

    left = True
    error = False
    for func in p:
        if func == "R":
            left = not left
        elif func == "D":
            if len(dq) == 0:
                error = True
                break

            if left:
                dq.popleft()
            else:
                dq.pop()

    if error:
        print("error")
    else:
        if not left:
            dq.reverse()
        print(str(list(dq)).replace(" ", ""))