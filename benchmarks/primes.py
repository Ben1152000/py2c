def p(n: int) -> bool:
    if n < 4:
        return n > 1
    if not ((n % 2) and (n % 3)):
        return False
    i: int = 5
    while i * i <= n:
        if not (n % i):
            return False
        i += 2
        if not (n % i):
            return False
        i += 4
    return True

s: int = 0
for i in range(1000000):
    s += p(i)
print(s)
