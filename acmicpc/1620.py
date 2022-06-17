import sys

_input = lambda: sys.stdin.readline().strip().replace("\n", "")
_print = lambda x: sys.stdout.write(f"{x}\n")

N, M = [int(x) for x in _input().split(" ")]

book_by_name = dict()
book_by_idx = list()
for i in range(N):
    pokemon_name = _input()
    book_by_name[pokemon_name] = i + 1
    book_by_idx.append(pokemon_name)

for i in range(M):
    question = _input()

    if '0' <= question[0] <= '9':
        _print(book_by_idx[int(question) - 1])
    else:
        _print(book_by_name[question])