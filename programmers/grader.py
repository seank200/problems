import solution
from random import randint

def generate_input():
    sc = []
    for i in range(1000000):
        sc.append(randint(555555, 1000000))
    return sc

res = solution.solution("17")
# res = solution.solution(generate_input(), 1000000000)

print(res)