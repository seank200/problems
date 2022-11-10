yoots = []

for _ in range(3):
    yoots.append(input().split(" "))

result = ['D', 'C', 'B', 'A', 'E']

for yoot in yoots:
    yc = 0
    for y in yoot:
        if y == '1':
            yc += 1
    print(result[yc])

