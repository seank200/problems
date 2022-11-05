def solution(n):
    number = []
    
    zero = False
    while n > 3:
        r = n % 3
        if r == 0:
            number.append('2' if zero else '4')
            zero = True
        elif r == 1 and zero:
            number.append('4')
        else:
            number.append(str(r-1 if zero else r))
            zero = False
        n //= 3
    
    if zero:
        n -= 1
    if n > 0:
        number.append(str(n if n < 3 else 4))
    
    number.reverse()
    return "".join(number)
