import sys

input = sys.stdin.readline
output = lambda x: sys.stdout.write(f"{x}\n")

trees = dict()

tree = input().rstrip()
while tree:
    if tree in trees:
        trees[tree] += 1
    else:
        trees[tree] = 1
    
    tree = input().rstrip()

tree_names_sorted = sorted(trees.keys())
total = sum(trees.values())
for tree_name in tree_names_sorted:
    percentage = round(trees[tree_name] * 100 / total, 4)
    output(f"{tree_name} {percentage}")
