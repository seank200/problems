import sys

EMPTY = 0
HOUSE = 1
CHICKEN = 2

input = sys.stdin.readline

N, M = [int(x) for x in input().split(" ")]
city = []
for r in range(N):
    city.append([int(x) for x in input().split(" ")])

houses = []
chickens = set()

for r, row in enumerate(city):
    for c, col in enumerate(row):
        if col == HOUSE:
            houses.append((r, c))
        elif col == CHICKEN:
            chickens.add((r, c))

def get_closest_chicken(house):
    hr, hc = house
    closest_chicken = (-1, -1)
    min_dis = float('inf')
    for chicken in chickens:
        cr, cc = chicken
        dis = abs(hr - cr) + abs(hc - cc)
        if dis < min_dis:
            min_dis = dis
            closest_chicken = chicken
    
    return closest_chicken, min_dis

closest_count = dict()
for chicken in chickens:
    closest_count[chicken] = 0

for house in houses:
    closest_chicken, _ = get_closest_chicken(house)
    closest_count[closest_chicken] += 1

remove_priority_list = list(closest_count.items())
remove_priority_list.sort(key=lambda x: x[1])

remove_count = len(chickens) - M

for i in range(remove_count):
    chickens.remove(remove_priority_list[i][0])

print(chickens)

city_chicken_distance = 0
for house in houses:
    _, min_dis = get_closest_chicken(house)
    city_chicken_distance += min_dis
    print(min_dis)

print(city_chicken_distance)