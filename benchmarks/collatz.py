def c(n: int) -> int:
    i: int = 0
    while n > 1:
        if n % 2 == 0:
            n //= 2
        else:
            n *= 3
            n += 1
        i += 1
    return i

l: int = 1
m: int = 0
n: int = 1000000
for i in range(1, n):
    a: int = c(i)
    if a > m:
        m = a
        l = i

print(l)
