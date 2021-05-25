def f(n: int) -> int:
    if n == 0:
        return 0
    if n == 1:
        return 1
    else:
        return f(n - 1) + f(n - 2)

for i in range(35):
    print(i, f(i))
