import solution
from random import randint

def answer():
    digits = ['1', '2', '4']
    num = ''
    for i in range(18):
        num += digits[randint(0, 2)]
    return num


def calc_input(num: str):
    n = 0
    for i, d in enumerate(num):
        exp = len(num) - 1 - i
        dig = int(d) if int(d) < 4 else 3
        n += dig * (3 ** exp)
    return n

print(solution.solution(7))
print(solution.solution(10))

for i in range(1000000):
    ans = answer()
    inp = calc_input(ans)
    out = solution.solution(inp)
    if ans != out:
        print(ans, inp)
        print(out)
        break