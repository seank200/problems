from itertools import permutations

def is_prime(n):
    for i in range(2, n):
        if n % i == 0:
            return False
    
    return True

def solution(numbers):
    numbers = [ch for ch in numbers]
    primes = []
    
    for i in range(1, len(numbers + 1)):
        perms = permutations(numbers, i)
        print(list(perms))
        primes += [int("".join(p)) for p in perms]
    
    primes = [p for p in primes if is_prime(p)]
    
    return primes