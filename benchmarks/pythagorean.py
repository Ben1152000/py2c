def t(c: int, p: bool) -> int:
    n: int = 0
    for a in range(c):
        for b in range(c):
            if a * a + b * b == c * c:
                if p:
                    print(a, b, c)
                n += 1
    return n

n: int = 500
l: int = 0
m: int = 0
for i in range(n + 1):
    a = t(i, False)
    if a > m:
        l = i
        m = a

t(l, True)
