n: int = (10006428 + 1) * (10006428 - 1)

def f(n: int) -> int:
    i: int = 2
    while i * i <= n:
        while n % i == 0:
            n //= i
        i += 1
    return n

print(f(n))
