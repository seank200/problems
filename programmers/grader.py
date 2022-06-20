import solution
from random import randint

def generate_input():
    info = ["java backend junior pizza 150","python frontend senior chicken 210","python frontend senior chicken 150","cpp backend senior pizza 260","java backend junior chicken 80","python backend senior chicken 50"]
    query = ["java and backend and junior and pizza 100","python and frontend and senior and chicken 200","cpp and - and senior and pizza 250","- and backend and senior and - 150","- and - and - and chicken 100","- and - and - and - 150"]
    
    info = info * 8333
    query = query * 16666

    return info, query


# res = solution.solution(["R", "R"])
print("Generating inputs... ", end="", flush=True)
genereted_input = generate_input()
print("Done")
print("Running...", flush=True)
res = solution.solution(*genereted_input)

print(res)