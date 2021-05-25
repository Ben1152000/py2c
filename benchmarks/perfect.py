def p(n: int) -> bool:
    s: int = 0
    for i in range(1, n):
        if not (n % i):
            s += i
    return s == n

for i in range(10000):
    if p(i):
        print(i)
