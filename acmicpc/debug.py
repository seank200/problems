def move(marbles):
    marbles['R'][0] += 1
    marbles['R'][1] += 1
    marbles['B'][0] += 1
    marbles['B'][1] += 1

def main():
    a = {'R': [0,0], 'B': [0, 0]}
    print(a)
    move(a)
    print(a)

main()