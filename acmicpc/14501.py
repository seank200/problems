def solve(N, T, P):
    for i, t in enumerate(T):
        if i + t > N:
            T[i] = -1
    choices = []
    if T[0] > 0:
        choices.append([True] + [False] * (T[0] - 1))
    choices.append([False])
    not_finished = True

    while not_finished:
        changed = False
        new_choices = []
        for choice in choices:
            if len(choice) < len(T):
                changed = True
                if choice[-1]:
                    false_cnt = T[len(choice) - 1] - 1
                    if false_cnt:
                        choice.extend([False] * false_cnt)
                    else:
                        if T[len(choice)] > 0:
                            new_choices.append(choice + [True])
                        choice.extend([False])
                else:
                    if T[len(choice)] > 0:
                        new_choices.append(choice + [True])
                    choice.extend([False])
        choices.extend(new_choices)
        if not changed:
            not_finished = False

    max_profit = 0
    for choice in choices:
        profit = sum([p for p, c in zip(P, choice) if c])
        if profit > max_profit:
            max_profit = profit

    return max_profit
        

def main():
    N = int(input())
    T = []
    P = []
    for i in range(N):
        t, p = [int(x) for x in input().split(" ")]
        T.append(t)
        P.append(p)
    ans = solve(N, T, P)
    print(ans)


main()
